import numpy as np
from scipy import stats


def false_positive_simulation(
    n_simulations=5000,
    n_per_group=50,
    alpha=0.05,
    mean=3.0,
    std=0.4,
    random_state=None
):
    """
    Simulate t-tests under the null hypothesis
    and compute observed false positive rate.
    """
    rng = np.random.default_rng(random_state)
    false_positives = 0

    for _ in range(n_simulations):
        group1 = rng.normal(mean, std, n_per_group)
        group2 = rng.normal(mean, std, n_per_group)

        _, p_value = stats.ttest_ind(group1, group2)

        if p_value < alpha:
            false_positives += 1

    return false_positives / n_simulations