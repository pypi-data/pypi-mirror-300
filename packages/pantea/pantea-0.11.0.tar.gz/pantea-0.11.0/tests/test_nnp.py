import os

os.environ["JAX_PLATFORM_NAME"] = "cpu"

from pathlib import Path
from typing import Tuple

import jax.numpy as jnp
import pytest

from pantea.datasets import Dataset
from pantea.potentials import NeuralNetworkPotential
from pantea.types import default_dtype

dataset_file = Path("tests", "h2o.data")
potential_file = Path("tests", "h2o.json")
default_dtype.FLOATX = jnp.float32


class TestNeuralNetworkPotential:
    dataset = Dataset.from_runner(dataset_file)
    nnp = NeuralNetworkPotential.from_runner(potential_file)

    @pytest.mark.parametrize(
        "nnp, expected",
        [
            (
                nnp,
                (
                    2,
                    ("H", "O"),
                ),
            ),
        ],
    )
    def test_settings(
        self,
        nnp: NeuralNetworkPotential,
        expected: Tuple,
    ) -> None:
        assert nnp.num_elements == expected[0]
        assert nnp.elements == expected[1]

    @pytest.mark.parametrize(
        "nnp, dataset, expected",
        [
            (
                nnp,
                dataset,
                (
                    jnp.array(-0.00721363),
                    jnp.array(
                        [
                            [-0.00343415, 0.00153666, -0.0203776],
                            [-0.11087799, -0.04327171, 0.10297609],
                            [-0.01472104, 0.0449558, 0.04925348],
                            [-0.02519826, 0.00152729, -0.01613272],
                            [0.06494806, -0.02886784, -0.01245033],
                            [-0.04200673, -0.00515676, -0.07121348],
                            [0.03067259, 0.01101292, -0.04297253],
                            [0.09775139, 0.06042628, -0.10140687],
                            [-0.02604892, 0.04006792, -0.13405925],
                            [0.01066793, -0.00437668, 0.03239093],
                            [0.05837363, 0.07088667, -0.09498966],
                            [0.04761543, -0.03721519, -0.02089787],
                        ]
                    ),
                ),
            ),
        ],
    )
    def test_outputs(
        self,
        nnp: NeuralNetworkPotential,
        dataset: Dataset,
        expected: Tuple,
    ) -> None:
        nnp.load_scaler()
        nnp.load_model()
        assert jnp.allclose(nnp(dataset[0]), expected[0])
        assert jnp.allclose(nnp.compute_forces(dataset[0]), expected[1])
