from __future__ import annotations

import numpy as np
import pytest

from pymatviz.correlation import marchenko_pastur
from tests.conftest import np_rng


@pytest.mark.parametrize("filter_high_evals", [True, False])
def test_marchenko_pastur(filter_high_evals: bool) -> None:
    n_rows, n_cols = 50, 100
    rand_mat = np_rng.normal(0, 1, size=(n_rows, n_cols))
    corr_mat = np.corrcoef(rand_mat)

    marchenko_pastur(
        corr_mat, gamma=n_cols / n_rows, filter_high_evals=filter_high_evals
    )
