from abc import ABCMeta, abstractmethod
from dataclasses import dataclass

import jax
import jax.numpy as jnp

from pantea.descriptors.acsf.cutoff import CutoffFunction
from pantea.descriptors.acsf.symmetry import BaseSymmetryFunction
from pantea.pytree import register_jax_pytree_node
from pantea.types import Array


class RadialSymmetryFunction(BaseSymmetryFunction, metaclass=ABCMeta):
    """A base class for `two body` (radial) symmetry functions."""

    def __hash__(self) -> int:
        """Enforce to use the parent class's hash method (JIT)."""
        return super().__hash__()

    @abstractmethod
    def __call__(self, rij: Array) -> Array: ...


@dataclass
class G1(RadialSymmetryFunction):
    """Plain cutoff function as symmetry function."""

    cfn: CutoffFunction

    def __post_init__(self) -> None:
        self._assert_jit_dynamic_attributes()
        self._assert_jit_static_attributes(expected=("cfn",))

    def __hash__(self) -> int:
        """Enforce to use the parent class's hash method (JIT)."""
        return super().__hash__()

    @jax.jit
    def __call__(self, rij: Array) -> Array:
        return self.cfn(rij)


@dataclass
class G2(RadialSymmetryFunction):
    """Radial exponential symmetry function."""

    cfn: CutoffFunction
    r_shift: float
    eta: float

    def __post_init__(self) -> None:
        self._assert_jit_dynamic_attributes()
        self._assert_jit_static_attributes(expected=("cfn", "r_shift", "eta"))

    def __hash__(self) -> int:
        """Enforce to use the parent class's hash method (JIT)."""
        return super().__hash__()

    @jax.jit
    def __call__(self, rij: Array) -> Array:
        return jnp.exp(-self.eta * (rij - self.r_shift) ** 2) * self.cfn(rij)


register_jax_pytree_node(G1)
register_jax_pytree_node(G2)
