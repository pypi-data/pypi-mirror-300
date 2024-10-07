import pickle
from dataclasses import field
from pathlib import Path
from typing import Callable, List, Tuple

from flax import linen as nn
from frozendict import frozendict

from pantea.logger import logger
from pantea.models.nn.activation import _activation_function_map
from pantea.types import Array, Dtype, default_dtype

ModelParams = frozendict[str, Array]


class NeuralNetworkModel(nn.Module):
    """Neural network model that outputs energy."""

    hidden_layers: Tuple[Tuple[int, str], ...]
    output_layer: Tuple[int, str] = (1, "identity")
    params_dtype: Dtype = field(default_factory=lambda: default_dtype.FLOATX)
    kernel_initializer: Callable = nn.initializers.lecun_normal()

    def setup(self) -> None:
        """Initialize neural network model."""
        self.layers = self.create_network()

    def create_layer(self, features: int) -> nn.Dense:
        """
        Create a dense layer and initialize the weights and biases
        (see `here <https://aiqm.github.io/torchani/examples/nnp_training.html#training-example>`_).
        """
        return nn.Dense(
            features,
            param_dtype=self.params_dtype,
            kernel_init=self.kernel_initializer,
            bias_init=nn.initializers.zeros,
        )

    def create_network(self) -> List:
        """Create a neural network as stack of dense layers and activation functions."""

        layers: List = list()
        # Hidden layers
        for out_size, af_type in self.hidden_layers:
            layers.append(self.create_layer(out_size))
            layers.append(_activation_function_map[af_type])
        # Output layer
        layers.append(self.create_layer(self.output_layer[0]))
        layers.append(_activation_function_map[self.output_layer[1]])
        return layers

    def __call__(self, inputs: Array) -> Array:
        """Compute energy."""
        x = inputs
        for layer in self.layers:
            x = layer(x)
        return x

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(hidden_layers={self.hidden_layers}"
            # f", output_layer={self.output_layer}"
            f", dtype={self.params_dtype.dtype}"  # type: ignore
            ")"
        )

    def save(self, filename: Path, params: ModelParams) -> None:
        """Save model weights."""
        file = str(Path(filename))
        logger.debug(f"Saving model weights into '{file}'")
        with open(file, "wb") as handle:
            pickle.dump(params, handle)

    def load(self, filename: Path) -> ModelParams:
        """Load model weights."""
        file = str(Path(filename))
        logger.debug(f"Loading model weights from '{file}'")
        with open(file, "rb") as handle:
            params = pickle.load(handle)
        return params
