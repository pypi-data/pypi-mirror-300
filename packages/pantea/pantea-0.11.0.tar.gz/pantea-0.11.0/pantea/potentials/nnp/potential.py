from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Optional, Tuple

import jax.numpy as jnp
from frozendict import frozendict
from jax import random

from pantea.atoms.element import ElementMap
from pantea.atoms.structure import Structure
from pantea.descriptors.acsf.acsf import ACSF
from pantea.descriptors.acsf.angular import G3, G9
from pantea.descriptors.acsf.cutoff import CutoffFunction
from pantea.descriptors.acsf.radial import G1, G2
from pantea.descriptors.acsf.symmetry import NeighborElements
from pantea.descriptors.scaler import DescriptorScaler, ScalerParams
from pantea.logger import logger
from pantea.models.nn.initializer import UniformInitializer
from pantea.models.nn.model import ModelParams, NeuralNetworkModel
from pantea.potentials.nnp.atomic_potential import AtomicPotential
from pantea.potentials.nnp.energy import _jitted_compute_energy
from pantea.potentials.nnp.force import _compute_forces
from pantea.potentials.nnp.settings import NeuralNetworkPotentialSettings
from pantea.types import Array, Element


@dataclass
class NeuralNetworkPotential:
    """
    High-dimensional neural network potential (HDNNP) - second generation.

    It contains all the required descriptors, scalers, and neural networks for each element,
    and an updater to fit the potential model using the reference structure data.
    """

    directory: Path
    elements: Tuple[Element, ...]
    scaler_save_format: str = field(repr=False)
    model_save_format: str = field(repr=False)
    atomic_potentials: frozendict[Element, AtomicPotential]
    models_params: Dict[Element, ModelParams] = field(repr=False)
    scalers_params: Dict[Element, Optional[ScalerParams]] = field(repr=False)

    @classmethod
    def from_runner(
        cls,
        filename: Path,
    ) -> NeuralNetworkPotential:
        potfile = Path(filename)
        settings = NeuralNetworkPotentialSettings.from_file(potfile)
        atomic_potentials = cls._build_atomic_potentials(settings)
        models_params = cls._initialize_models_params(settings, atomic_potentials)
        scalers_params = cls._initialize_scalers_params(settings)
        return NeuralNetworkPotential(
            directory=potfile.parent,
            elements=tuple(element for element in settings.elements),
            scaler_save_format=settings.scaler_save_format,
            model_save_format=settings.model_save_format,
            atomic_potentials=atomic_potentials,
            models_params=models_params,
            scalers_params=scalers_params,
        )

    def __call__(self, structure: Structure) -> Array:
        """
        Compute the total energy.

        :param structure: Structure
        :return: total energy
        """
        self._check_scaler_params_exist()
        return _jitted_compute_energy(
            self.atomic_potentials,
            structure.get_positions_per_element(),
            self.models_params,
            self.scalers_params,
            structure.as_kernel_args(),
        )  # type: ignore

    def compute_forces(self, structure: Structure) -> Array:
        """
        Compute force components.

        :param structure: input structure
        :return: predicted force components for all atoms
        """
        self._check_scaler_params_exist()
        forces_dict = _compute_forces(
            self.atomic_potentials,
            structure.get_positions_per_element(),
            self.models_params,
            self.scalers_params,
            structure.as_kernel_args(),
        )
        forces = jnp.empty_like(structure.forces)
        for element in structure.get_unique_elements():
            atom_index = structure.select(element)
            forces = forces.at[atom_index].set(forces_dict[element])
        return forces

    def load_scaler(self) -> None:
        """Loads scaler parameters for all elements."""
        # Load scaler parameters for each element separately
        for element in self.elements:
            atomic_number = ElementMap.get_atomic_number_from_element(element)
            scaler_file = Path(
                self.directory,
                self.scaler_save_format.format(atomic_number),
            )
            logger.info(
                f"Loading scaler parameters for element ({element}): "
                f"{scaler_file.name}"
            )
            scaler = self.atomic_potentials[element].scaler
            self.scalers_params[element] = scaler.load(scaler_file)

    def load_model(self) -> None:
        """Load model parameters for all elements."""
        for element in self.elements:
            atomic_number = ElementMap.get_atomic_number_from_element(element)
            model_file = Path(
                self.directory,
                self.model_save_format.format(atomic_number),
            )
            logger.info(
                f"Loading model weights for element ({element}): {model_file.name}"
            )
            model = self.atomic_potentials[element].model
            self.models_params[element] = model.load(model_file)

    def load(self) -> None:
        """Load scaler and model."""
        self.load_scaler()
        self.load_model()

    @classmethod
    def _build_atomic_potentials(
        cls,
        settings: NeuralNetworkPotentialSettings,
    ) -> frozendict[Element, AtomicPotential]:
        """
        Initialize atomic potential for each element.
        This method can be override in case that different atomic potential is used.
        """
        logger.info("Initializing atomic potentials")
        atomic_potentials: Dict[Element, AtomicPotential] = dict()
        descriptors = cls._build_descriptors(settings)
        scalers = cls._build_scalers(settings)
        models = cls._build_models(settings)
        for element in settings.elements:
            atomic_potentials[element] = AtomicPotential(
                descriptor=descriptors[element],
                scaler=scalers[element],
                model=models[element],
            )
        return frozendict(atomic_potentials)

    @classmethod
    def _initialize_models_params(
        cls,
        settings: NeuralNetworkPotentialSettings,
        atomic_potentials: frozendict[Element, AtomicPotential],
    ) -> Dict[Element, ModelParams]:
        """
        Initialize neural network model parameters for each element
        (e.g. neural network kernel and bias values).

        This method be used to initialize model params of the potential with a different random seed.
        """
        logger.info("Initializing model params")
        models_params: Dict[Element, ModelParams] = dict()
        random_keys = random.split(
            random.PRNGKey(settings.random_seed),
            settings.number_of_elements,
        )
        for i, element in enumerate(settings.elements):
            models_params[element] = atomic_potentials[element].model.init(  # type: ignore
                random_keys[i],
                jnp.ones((1, atomic_potentials[element].model_input_size)),
            )[
                "params"
            ]
        return models_params

    @classmethod
    def _initialize_scalers_params(
        cls,
        settings: NeuralNetworkPotentialSettings,
    ) -> Dict[Element, Optional[ScalerParams]]:
        return {element: None for element in settings.elements}

    @classmethod
    def _build_descriptors(
        cls,
        settings: NeuralNetworkPotentialSettings,
    ) -> Dict[Element, ACSF]:
        """Initialize descriptor for each element."""
        logger.info("Initializing descriptors")
        descriptors: Dict[Element, ACSF] = dict()
        radials = defaultdict(list)
        angulars = defaultdict(list)

        for args in settings.symfunction_short:

            cfn = CutoffFunction.from_type(
                cutoff_type=settings.cutoff_type,
                r_cutoff=args.r_cutoff,
            )

            if args.acsf_type == 1:
                symmetry_function = G1(cfn)
                neighbor_elements = NeighborElements(args.neighbor_element_j)
                radials[args.central_element].append(
                    (symmetry_function, neighbor_elements)
                )
            elif args.acsf_type == 2:
                symmetry_function = G2(cfn, eta=args.eta, r_shift=args.r_shift)
                neighbor_elements = NeighborElements(args.neighbor_element_j)
                radials[args.central_element].append(
                    (symmetry_function, neighbor_elements)
                )
            elif args.acsf_type == 3:
                symmetry_function = G3(
                    cfn,
                    eta=args.eta,
                    zeta=args.zeta,  # type: ignore
                    lambda0=args.lambda0,  # type: ignore
                    r_shift=args.r_cutoff,
                )
                neighbor_elements = NeighborElements(
                    args.neighbor_element_j, args.neighbor_element_k
                )
                angulars[args.central_element].append(
                    (symmetry_function, neighbor_elements)
                )
            elif args.acsf_type == 9:
                symmetry_function = G9(
                    cfn,
                    eta=args.eta,
                    zeta=args.zeta,  # type: ignore
                    lambda0=args.lambda0,  # type: ignore
                    r_shift=args.r_cutoff,
                )
                neighbor_elements = NeighborElements(
                    args.neighbor_element_j, args.neighbor_element_k
                )
                angulars[args.central_element].append(
                    (symmetry_function, neighbor_elements)
                )
        # Instantiate ACSF for each element
        for element in settings.elements:
            descriptors[element] = ACSF(
                central_element=element,
                radial_symmetry_functions=tuple(radials[element]),
                angular_symmetry_functions=tuple(angulars[element]),
            )
        return descriptors

    @classmethod
    def _build_scalers(
        cls,
        settings: NeuralNetworkPotentialSettings,
    ) -> Dict[Element, DescriptorScaler]:
        """Initialize descriptor scaler for each element."""
        logger.info("Initializing descriptor scalers")
        scalers: Dict[Element, DescriptorScaler] = dict()
        # Prepare scaler input argument if exist in settings
        scaler_kwargs = {
            first: settings[second]
            for first, second in {
                "scale_type": "scale_type",
                "scale_min": "scale_min_short",
                "scale_max": "scale_max_short",
            }.items()
            if second in settings.keywords()
        }
        logger.debug(f"Scaler kwargs={scaler_kwargs}")
        # Assign an ACSF scaler to each element
        for element in settings.elements:
            scalers[element] = DescriptorScaler.from_type(**scaler_kwargs)
        return scalers

    @classmethod
    def _build_models(
        cls,
        settings: NeuralNetworkPotentialSettings,
    ) -> Dict[Element, NeuralNetworkModel]:
        """Initialize neural network model for each element."""
        logger.info("Initializing neural network models")
        models: Dict[Element, NeuralNetworkModel] = dict()

        for element in settings.elements:
            logger.debug(f"Element: {element}")

            hidden_layers = zip(
                settings.global_nodes_short,
                settings.global_activation_short[:-1],
            )
            output_layer: Tuple[int, str] = (
                1,
                settings.global_activation_short[-1],
            )
            kernel_initializer: UniformInitializer = UniformInitializer(
                weights_range=(
                    settings.weights_min,
                    settings.weights_max,
                )
            )
            models[element] = NeuralNetworkModel(
                hidden_layers=tuple([(n, t) for n, t in hidden_layers]),
                output_layer=output_layer,
                kernel_initializer=kernel_initializer,
            )
        return models

    def _check_scaler_params_exist(self) -> None:
        if None in self.scalers_params.values():
            logger.error(
                (
                    f"Scaler parameters are not set yet for all the elements ({self.scalers_params})."
                    "Try loading or fitting the scaler first."
                ),
                exception=ValueError,
            )

    # def set_extrapolation_warnings(self, threshold: Optional[int] = None) -> None:
    #     """
    #     shows warning whenever a descriptor value is out of bounds defined by
    #     minimum/maximum values in the scaler.

    #     set_extrapolation_warnings(None) will disable it.

    #     :param threshold: maximum number of warnings
    #     :type threshold: int
    #     """
    #     logger.info(f"Setting extrapolation warning: {threshold}")
    #     for pot in self.atomic_potentials.values():
    #         pot.scaler.set_max_number_of_warnings(threshold)

    # @property
    # def extrapolation_warnings(self) -> Dict[Element, int]:
    #     return {
    #         element: pot.scaler.number_of_warnings
    #         for element, pot in self.atomic_potentials.items()
    #     }

    @property
    def descriptors(self) -> Dict[Element, ACSF]:
        """Return descriptor for each element."""
        return {
            element: potential.descriptor
            for element, potential in self.atomic_potentials.items()
        }

    @property
    def scalers(self) -> Dict[Element, DescriptorScaler]:
        """Return scaler for each element."""
        return {
            element: potential.scaler
            for element, potential in self.atomic_potentials.items()
        }

    @property
    def models(self) -> Dict[Element, NeuralNetworkModel]:
        """Return model for each element."""
        return {
            element: potential.model
            for element, potential in self.atomic_potentials.items()
        }

    @property
    def r_cutoff(self) -> float:
        """Return the maximum cutoff radius found between all descriptors."""
        return max(
            [
                potential.descriptor.r_cutoff
                for potential in self.atomic_potentials.values()
            ]
        )

    @property
    def num_elements(self) -> int:
        return len(self.elements)


NNP = NeuralNetworkPotential
