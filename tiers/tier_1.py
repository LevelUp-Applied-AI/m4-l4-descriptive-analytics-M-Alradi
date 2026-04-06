import os
import itertools
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import f_oneway, ttest_ind
from eda_analysis import handle_missing_values

CHALLENGES_OUTPUT_DIR = "output/challenges"
os.makedirs(CHALLENGES_OUTPUT_DIR, exist_ok=True)


def department_gpa_anova(df):
    """
    Test whether average GPA differs across departments using ANOVA.
    If significant, run post-hoc pairwise t-tests with Bonferroni correction.
    Also generate violin plot visualization.
    """

    print("\n========== ANOVA: GPA Across Departments ==========\n")

    if not {"department", "gpa"}.issubset(df.columns):
        print("Required columns not found.")
        return

    # -----------------------------
    # 1️⃣ Prepare Groups
    # -----------------------------
    departments = df["department"].unique()
    groups = [
        df[df["department"] == dept]["gpa"].dropna()
        for dept in departments
    ]

    # Remove departments with <2 observations
    valid_groups = []
    valid_departments = []
    for dept, group in zip(departments, groups):
        if len(group) >= 2:
            valid_groups.append(group)
            valid_departments.append(dept)

    if len(valid_groups) < 2:
        print("Not enough data to perform ANOVA.")
        return

    # -----------------------------
    # 2️⃣ One-Way ANOVA
    # -----------------------------
    F_stat, p_value = f_oneway(*valid_groups)

    print(f"F-statistic: {F_stat:.4f}")
    print(f"p-value: {p_value:.4f}")

    if p_value < 0.05:
        print("Result: Statistically significant differences in GPA across departments.\n")
        significant = True
    else:
        print("Result: No statistically significant GPA differences across departments.\n")
        significant = False

    # -----------------------------
    # 3️⃣ Post-hoc Tests (if significant)
    # -----------------------------
    if significant:
        print("Post-hoc Pairwise Comparisons (Bonferroni corrected):\n")

        comparisons = list(itertools.combinations(valid_departments, 2))
        m = len(comparisons)  # number of comparisons

        for dept1, dept2 in comparisons:
            group1 = df[df["department"] == dept1]["gpa"].dropna()
            group2 = df[df["department"] == dept2]["gpa"].dropna()

            t_stat, raw_p = ttest_ind(group1, group2, equal_var=False)

            # Bonferroni correction
            corrected_p = min(raw_p * m, 1.0)

            print(f"{dept1} vs {dept2}")
            print(f"  t = {t_stat:.4f}, raw p = {raw_p:.4f}, Bonferroni p = {corrected_p:.4f}")

            if corrected_p < 0.05:
                print("  → Significant difference\n")
            else:
                print("  → Not significant\n")

    # -----------------------------
    # 4️⃣ Violin Plot
    # -----------------------------
    plt.figure(figsize=(10, 6))
    sns.violinplot(x="department", y="gpa", data=df, inner="box")
    plt.title("GPA Distribution by Department (Violin Plot)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"{CHALLENGES_OUTPUT_DIR}/gpa_by_department_violin.png")
    plt.close()

    print(f"Violin plot saved to {CHALLENGES_OUTPUT_DIR}/gpa_by_department_violin.png\n")


def main():
    # Load and clean data
    df = pd.read_csv("data/student_performance.csv")
    cleaned_df = handle_missing_values(df)
    department_gpa_anova(cleaned_df)


if __name__ == "__main__":
    main()
