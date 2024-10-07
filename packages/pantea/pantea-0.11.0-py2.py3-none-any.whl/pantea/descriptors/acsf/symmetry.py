from abc import ABCMeta, abstractmethod
from typing import NamedTuple, Optional

from pantea.descriptors.acsf.cutoff import CutoffFunction
from pantea.logger import logger
from pantea.pytree import BaseJaxPytreeDataClass
from pantea.types import Array, Element


class BaseSymmetryFunction(BaseJaxPytreeDataClass, metaclass=ABCMeta):
    """
    A base class for symmetry functions.
    All symmetry functions (i.e. radial and angular) must derive from this base class.
    """

    def __init__(self, cfn: CutoffFunction) -> None:
        self.cfn: CutoffFunction = cfn
        logger.debug(repr(self))

    @abstractmethod
    def __call__(self, *args, **kwargs) -> Array: ...

    @property
    def r_cutoff(self) -> float:
        return self.cfn.r_cutoff


class NeighborElements(NamedTuple):
    """
    Represent the chemical environment including neighbor elements.
    """

    # central: Element
    neighbor_j: Element
    neighbor_k: Optional[Element] = None
