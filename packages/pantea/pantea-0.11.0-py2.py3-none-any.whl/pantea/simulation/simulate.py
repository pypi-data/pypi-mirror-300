from pathlib import Path
from typing import Optional, Protocol

import ase
import ase.io

from pantea.atoms.structure import Structure
from pantea.logger import logger
from pantea.types import Array


class PotentialInterface(Protocol):
    def __call__(self, structure: Structure) -> Array: ...

    def compute_forces(self, structure: Structure) -> Array: ...


class MDSystemInterface(Protocol):
    potential: PotentialInterface
    structure: Structure


class SimulatorInterface(Protocol):
    step: int

    def repr_physical_params(self, system: MDSystemInterface) -> None: ...

    def simulate_one_step(self, system: MDSystemInterface) -> None: ...


def simulate(
    system: MDSystemInterface,
    simulator: SimulatorInterface,
    num_steps: int = 1,
    output_freq: Optional[int] = None,
    filename: Optional[Path] = None,
    append: bool = False,
) -> None:
    """
    Simulate system for a given number of steps.

    :param system: a system of particles and the interacting potential.
    :type system: MDSystemInterface
    :param simulator: either a molecular dynamics (MD) or monte carlo (MC) simulator
    :type simulator: SimulatorInterface
    :param num_steps: number of steps, defaults to 1
    :type num_steps: int, optional
    :param output_freq: print outputs and/or dump configuration file after this number of steps, defaults to None
    :type output_freq: Optional[int], optional
    :param filename: output configuration file (e.g., `*.xyz`) as supported in the ASE, defaults to None
    :type filename: Optional[Path], optional
    :param append: whether append to the exiting configuration file or not, defaults to False
    :type append: bool, optional
    """

    cls_name = simulator.__class__.__name__
    logger.info(f"Running {cls_name} for {num_steps} steps")

    if output_freq is None:
        output_freq = 1 if num_steps < 100 else int(0.01 * num_steps)
    is_output: bool = output_freq > 0

    if filename is not None:
        filename = Path(filename)
        if is_output:
            logger.info(
                f"Writing atomic configuration into '{filename.name}' "
                f"file every {output_freq} steps"
            )
        if not append:
            with open(str(filename), "w"):
                pass

    # system.structure.forces = system.potential.compute_forces(system.structure)
    init_step: int = simulator.step
    try:
        for _ in range(num_steps):
            if is_output and ((simulator.step - init_step) % output_freq == 0):
                print(simulator.repr_physical_params(system))
                if filename is not None:
                    atoms = system.structure.to_ase()
                    ase.io.write(str(filename), atoms, append=True)
            simulator.simulate_one_step(system)

    except KeyboardInterrupt:
        print("KeyboardInterrupt")
    if is_output:
        print(simulator.repr_physical_params(system))
