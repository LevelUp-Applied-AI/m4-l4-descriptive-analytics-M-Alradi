import numpy as np
from utils.stats_utils import bootstrap_mean_ci, compute_effect_size


def test_bootstrap_ci_returns_tuple():
    data = np.random.normal(0, 1, 100)
    ci = bootstrap_mean_ci(data, n_bootstrap=1000)
    assert isinstance(ci, tuple)
    assert len(ci) == 2


def test_effect_size_nonzero():
    g1 = np.random.normal(0, 1, 50)
    g2 = np.random.normal(1, 1, 50)
    d = compute_effect_size(g1, g2)
    assert d != 0