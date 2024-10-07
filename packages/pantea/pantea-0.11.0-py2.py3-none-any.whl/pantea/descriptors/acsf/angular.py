from abc import ABCMeta, abstractmethod
from dataclasses import dataclass

import jax
import jax.numpy as jnp

from pantea.descriptors.acsf.cutoff import CutoffFunction
from pantea.descriptors.acsf.symmetry import BaseSymmetryFunction
from pantea.pytree import register_jax_pytree_node
from pantea.types import Array


class AngularSymmetryFunction(BaseSymmetryFunction, metaclass=ABCMeta):
    """A base class for `three body` (angular) symmetry functions."""

    def __hash__(self) -> int:
        """Enforce to use the parent class's hash method (JIT)."""
        return super().__hash__()

    @abstractmethod
    def __call__(
        self,
        rij: Array,
        rik: Array,
        rjk: Array,
        cost: Array,
    ) -> Array: ...


@dataclass
class G3(AngularSymmetryFunction):
    """Angular symmetry function."""

    cfn: CutoffFunction
    eta: float
    zeta: float
    lambda0: float
    r_shift: float

    def __post_init__(self) -> None:
        self._assert_jit_dynamic_attributes()
        self._assert_jit_static_attributes(
            expected=("cfn", "eta", "zeta", "lambda0", "r_shift")
        )

    def __hash__(self) -> int:
        """Enforce to use the parent class's hash method (JIT)."""
        return super().__hash__()

    @jax.jit
    def __call__(
        self,
        rij: Array,
        rik: Array,
        rjk: Array,
        cost: Array,
    ) -> Array:
        return (
            2.0 ** (1.0 - self.zeta)
            * jnp.power(1 + self.lambda0 * cost, self.zeta)
            * jnp.exp(-self.eta * (rij**2 + rik**2 + rjk**2))
            * self.cfn(rij)
            * self.cfn(rik)
            * self.cfn(rjk)
        )


@dataclass
class G9(AngularSymmetryFunction):
    """
    Modified angular symmetry function.

    J. Behler, J. Chem. Phys. 134, 074106 (2011).
    """

    cfn: CutoffFunction
    eta: float
    zeta: float
    lambda0: float
    r_shift: float

    def __post_init__(self) -> None:
        self._assert_jit_dynamic_attributes()
        self._assert_jit_static_attributes(
            expected=("cfn", "eta", "zeta", "lambda0", "r_shift")
        )

    def __hash__(self) -> int:
        """Enforce to use the parent class's hash method (JIT)."""
        return super().__hash__()

    @jax.jit
    def __call__(
        self,
        rij: Array,
        rik: Array,
        rjk: Array,
        cost: Array,
    ) -> Array:
        # TODO: r_shift, define params argument instead
        return (
            2.0 ** (1.0 - self.zeta)
            * jnp.power(1 + self.lambda0 * cost, self.zeta)
            * jnp.exp(-self.eta * (rij**2 + rik**2))
            * self.cfn(rij)
            * self.cfn(rik)
        )


register_jax_pytree_node(G3)
register_jax_pytree_node(G9)
