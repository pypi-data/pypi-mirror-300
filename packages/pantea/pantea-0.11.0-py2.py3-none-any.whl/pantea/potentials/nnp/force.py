from typing import Dict

import jax
from frozendict import frozendict
from jax import grad, jit

from pantea.atoms.structure import StructureAsKernelArgs
from pantea.descriptors.scaler import ScalerParams
from pantea.potentials.nnp.energy import (
    AtomicPotentialInterface,
    ModelParams,
    _compute_energy,
)
from pantea.types import Array, Element

_grad_compute_energy = grad(_compute_energy, argnums=1)

_jitted_grad_compute_energy = jit(
    _grad_compute_energy,
    static_argnums=0,
)


def negative(array: Array) -> Array:
    return -1.0 * array


def _compute_forces(
    atomic_potentials: frozendict[Element, AtomicPotentialInterface],
    positions: Dict[Element, Array],
    models_params: Dict[Element, ModelParams],
    scalers_params: Dict[Element, ScalerParams],
    structure: StructureAsKernelArgs,
) -> Dict[Element, Array]:
    """Compute force components using the gradient of the total energy."""
    gradients = _jitted_grad_compute_energy(
        atomic_potentials,
        positions,
        models_params,
        scalers_params,
        structure,
    )
    return jax.tree.map(negative, gradients)
