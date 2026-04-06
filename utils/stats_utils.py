import numpy as np
from scipy import stats
from statsmodels.stats.power import TTestIndPower


# -------------------------------------------------
# Bootstrap Confidence Interval
# -------------------------------------------------
def bootstrap_mean_ci(data, n_bootstrap=10000, ci=95, random_state=None):
    """
    Compute bootstrap confidence interval for the mean.
    """
    rng = np.random.default_rng(random_state)
    data = np.asarray(data)
    n = len(data)

    means = [
        np.mean(rng.choice(data, size=n, replace=True))
        for _ in range(n_bootstrap)
    ]

    lower = np.percentile(means, (100 - ci) / 2)
    upper = np.percentile(means, 100 - (100 - ci) / 2)

    return lower, upper


# -------------------------------------------------
# Parametric Independent t-test + CI
# -------------------------------------------------
def parametric_ttest_ci(group1, group2, alpha=0.05):
    """
    Independent t-test (Welch) with CI for mean difference.
    """
    group1 = np.asarray(group1)
    group2 = np.asarray(group2)

    t_stat, p_value = stats.ttest_ind(group1, group2, equal_var=False)

    diff = np.mean(group1) - np.mean(group2)

    se = np.sqrt(
        np.var(group1, ddof=1) / len(group1)
        + np.var(group2, ddof=1) / len(group2)
    )

    df = len(group1) + len(group2) - 2
    t_crit = stats.t.ppf(1 - alpha / 2, df)

    margin = t_crit * se
    ci = (diff - margin, diff + margin)

    return {
        "t_stat": t_stat,
        "p_value": p_value,
        "mean_diff": diff,
        "ci": ci,
    }


# -------------------------------------------------
# Cohen's d
# -------------------------------------------------
def compute_effect_size(group1, group2):
    """
    Compute Cohen's d.
    """
    group1 = np.asarray(group1)
    group2 = np.asarray(group2)

    mean_diff = np.mean(group1) - np.mean(group2)

    pooled_std = np.sqrt(
        ((len(group1) - 1) * np.var(group1, ddof=1)
         + (len(group2) - 1) * np.var(group2, ddof=1))
        / (len(group1) + len(group2) - 2)
    )

    return mean_diff / pooled_std


# -------------------------------------------------
# Power Analysis
# -------------------------------------------------
def power_analysis(group1, group2, alpha=0.05, power=0.8):
    """
    Compute required sample size per group for given power.
    """
    effect_size = abs(compute_effect_size(group1, group2))

    analysis = TTestIndPower()

    sample_size = analysis.solve_power(
        effect_size=effect_size,
        power=power,
        alpha=alpha,
        ratio=1.0
    )

    return {
        "effect_size": effect_size,
        "required_sample_per_group": int(np.ceil(sample_size))
    }