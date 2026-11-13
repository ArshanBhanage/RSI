"""Pure mathematical contracts; these inputs are not experiment outcomes."""

import math

import pytest

from queryforge.metrics import gap_closed


def test_improvement_and_regression_signs():
    assert gap_closed(0.5, 0.75) == 0.5
    assert gap_closed(0.5, 0.25) == -0.5
    assert gap_closed(10, 5, 0) == 0.5
    assert gap_closed(1, 1) is None


def test_nonfinite_is_not_a_score():
    with pytest.raises(ValueError):
        gap_closed(0.5, math.nan)
