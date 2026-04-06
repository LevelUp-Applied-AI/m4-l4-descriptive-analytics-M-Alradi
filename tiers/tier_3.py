import pandas as pd
from utils.stats_utils import (
    bootstrap_mean_ci,
    parametric_ttest_ci,
    power_analysis
)
from utils.simulation_utils import false_positive_simulation


def main():
    print("===== Tier 3 — Statistical Simulation & Power Analysis =====")

    df = pd.read_csv("data/student_performance.csv")

    group_yes = df[df["has_internship"] == "Yes"]["gpa"].dropna().values
    group_no = df[df["has_internship"] == "No"]["gpa"].dropna().values

    # -------------------------------------------------
    # Bootstrap CIs
    # -------------------------------------------------
    print("\nBootstrap 95% Confidence Intervals:")
    print("Internship YES:", bootstrap_mean_ci(group_yes))
    print("Internship NO :", bootstrap_mean_ci(group_no))

    # -------------------------------------------------
    # Parametric t-test
    # -------------------------------------------------
    ttest_results = parametric_ttest_ci(group_yes, group_no)
    print("\nParametric t-test Results:")
    print(ttest_results)

    # -------------------------------------------------
    # Power Analysis
    # -------------------------------------------------
    power_results = power_analysis(group_yes, group_no)
    print("\nPower Analysis:")
    print(power_results)

    # -------------------------------------------------
    # False Positive Simulation
    # -------------------------------------------------
    fp_rate = false_positive_simulation()
    print("\nFalse Positive Simulation:")
    print("Observed rate:", fp_rate)


if __name__ == "__main__":
    main()