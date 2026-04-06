"""Lab 4 — Descriptive Analytics: Student Performance EDA

Conduct exploratory data analysis on the student performance dataset.
Produce distribution plots, correlation analysis, hypothesis tests,
and a written findings report.

Usage:
    python eda_analysis.py
"""
import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind, chi2_contingency

OUTPUT_DIR = "output"

def load_and_profile(filepath):
    """Load the dataset and generate a data profile report.

    Args:
        filepath: path to the CSV file (e.g., 'data/student_performance.csv')

    Returns:
        DataFrame: the loaded dataset

    Side effects:
        Saves a text profile to output/data_profile.txt containing:
        - Shape (rows, columns)
        - Data types for each column
        - Missing value counts per column
        - Descriptive statistics for numeric columns
    """
    # TODO: Load the dataset and report its shape, data types, missing values,
    #       and descriptive statistics to output/data_profile.txt

    
    # Load dataset
    df = pd.read_csv(filepath)

    # Generate profile content
    with open(f"{OUTPUT_DIR}/data_profile.txt", "w", encoding="utf-8") as f:
        f.write("=== DATA PROFILE REPORT ===\n\n")
        
        # Shape
        f.write("1. Dataset Shape\n")
        f.write(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}\n\n")
        
        # Data types
        f.write("2. Data Types\n")
        f.write(df.dtypes.to_string())
        f.write("\n\n")
        
        # Missing values
        f.write("3. Missing Values (per column)\n")
        f.write(df.isnull().sum().to_string())
        f.write("\n\n")
        
        # Descriptive statistics (numeric only)
        f.write("4. Descriptive Statistics (Numeric Columns)\n")
        f.write(df.describe().to_string())
        f.write("\n")
    
    return df


def handle_missing_values(df):
    """
    Handle missing values with documented reasoning.

    Strategy:
    - commute_minutes:
        If ~10% missing and assumed MCAR (Missing Completely At Random),
        impute with the median (robust to skew/outliers).
    - study_hours_weekly:
        If ~5% missing and assumed MCAR,
        drop those rows since impact on dataset size is small.
    - All other columns:
        Leave unchanged unless explicitly handled.

    Args:
        df (pd.DataFrame): Input dataset

    Returns:
        pd.DataFrame: Cleaned dataset
    """

    df_clean = df.copy()

    # --- 1. commute_minutes ---
    if "commute_minutes" in df_clean.columns:
        missing_pct = df_clean["commute_minutes"].isna().mean() * 100
        
        if missing_pct > 0:
            median_value = df_clean["commute_minutes"].median()

        df_clean = df_clean.assign(
            commute_minutes=df_clean["commute_minutes"].fillna(
            df_clean["commute_minutes"].median()
        )
    )

    # --- 2. study_hours_weekly ---
    if "study_hours_weekly" in df_clean.columns:
        missing_pct = df_clean["study_hours_weekly"].isna().mean() * 100
        
        if missing_pct > 0:
            df_clean = df_clean.dropna(subset=["study_hours_weekly"])

    return df_clean


def plot_distributions(df):
    """Create distribution plots for key numeric variables.

    Args:
        df: pandas DataFrame with the student performance data

    Returns:
        None

    Side effects:
        Saves at least 3 distribution plots (histograms with KDE or box plots)
        as PNG files in the output/ directory. Each plot should have a
        descriptive title that states what the distribution reveals.
    """
    # TODO: Create distribution plots for numeric columns like GPA,
    #       study hours, attendance, and commute minutes
    # TODO: Use histograms with KDE overlay (sns.histplot) or box plots
    # TODO: Save each plot to the output/ directory
    
    # -----------------------------
    # 1️⃣ Histograms with KDE
    # -----------------------------
    numeric_cols = ["gpa", "study_hours_weekly", "attendance_pct", "commute_minutes"]

    for col in numeric_cols:
        if col in df.columns:
            plt.figure()
            sns.histplot(df[col], kde=True)
            plt.title(f"Distribution of {col}")
            plt.xlabel(col)
            plt.ylabel("Frequency")
            plt.tight_layout()
            plt.savefig(f"output/{col}_distribution.png")
            plt.close()

    # -----------------------------
    # 2️⃣ Boxplot: GPA by Department
    # -----------------------------
    if "gpa" in df.columns and "department" in df.columns:
        plt.figure()
        sns.boxplot(x="department", y="gpa", data=df)
        plt.title("GPA Distribution Across Departments")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig("output/gpa_by_department_boxplot.png")
        plt.close()

    # -----------------------------
    # 3️⃣ Bar Chart: Scholarship Distribution
    # -----------------------------
    if "scholarship" in df.columns:
        plt.figure()
        df["scholarship"].value_counts().plot(kind="bar")
        plt.title("Scholarship Distribution")
        plt.xlabel("Scholarship Status")
        plt.ylabel("Count")
        plt.tight_layout()
        plt.savefig("output/scholarship_distribution.png")
        plt.close()

    print("Distribution plots saved to output/ directory.")


def plot_correlations(df):
    """Analyze and visualize relationships between numeric variables.

    Args:
        df: pandas DataFrame with the student performance data

    Returns:
        None

    Side effects:
        Saves at least one correlation visualization to the output/ directory
        (e.g., a heatmap, scatter plot, or pair plot).
    """
    # TODO: Compute the correlation matrix for numeric columns
    # TODO: Create a heatmap or scatter plots showing key relationships
    # TODO: Save the visualization(s) to the output/ directory
    
    # -----------------------------
    # 1️⃣ Compute Correlation Matrix
    # -----------------------------
    numeric_df = df.select_dtypes(include=["number"])
    corr_matrix = numeric_df.corr(method="pearson")

    # -----------------------------
    # 2️⃣ Save Heatmap
    # -----------------------------
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Correlation Matrix (Pearson)")
    plt.tight_layout()
    plt.savefig("output/correlation_heatmap.png")
    plt.close()

    # -----------------------------
    # 3️⃣ Find Top 2 Correlated Pairs
    # -----------------------------
    
    # Remove self-correlations
    corr_matrix_no_diag = corr_matrix - np.eye(len(corr_matrix))

    # Get absolute correlations
    corr_unstacked = corr_matrix_no_diag.abs().unstack()

    # Remove duplicate pairs
    corr_unstacked = corr_unstacked.sort_values(ascending=False)
    corr_unstacked = corr_unstacked[corr_unstacked > 0]

    seen = set()
    top_pairs = []

    for (var1, var2), corr_value in corr_unstacked.items():
        if (var2, var1) not in seen:
            top_pairs.append((var1, var2))
            seen.add((var1, var2))
        if len(top_pairs) == 2:
            break

    # -----------------------------
    # 4️⃣ Scatter Plots for Top 2
    # -----------------------------

    for var1, var2 in top_pairs:
        plt.figure()
        sns.scatterplot(x=df[var1], y=df[var2])
        plt.title(f"{var1} vs {var2}")
        plt.xlabel(var1)
        plt.ylabel(var2)
        plt.tight_layout()
        plt.savefig(f"output/scatter_{var1}_vs_{var2}.png")
        plt.close()

    print("Correlation analysis completed. Plots saved to output/ directory.")


def run_hypothesis_tests(df):
    """Run statistical tests to validate observed patterns.

    Args:
        df: pandas DataFrame with the student performance data

    Returns:
        dict: test results with keys like 'internship_ttest', 'dept_anova',
              each containing the test statistic and p-value

    Side effects:
        Prints test results to stdout with interpretation.

    Tests to consider:
        - t-test: Does GPA differ between students with and without internships?
        - ANOVA: Does GPA differ across departments?
        - Correlation test: Is the correlation between study hours and GPA significant?
    """
    # TODO: Run at least two hypothesis tests on patterns you observe in the data
    # TODO: Report the test statistic, p-value, and your interpretation
    
    results = {}

    print("\n========== HYPOTHESIS TESTING ==========\n")

    # -------------------------------------------------
    # Hypothesis 1: Internship vs GPA (t-test)
    # -------------------------------------------------
    if {"gpa", "has_internship"}.issubset(df.columns):

        df["internship_binary"] = df["has_internship"].map({"Yes": 1, "No": 0})

        group_yes = df[df["internship_binary"] == 1]["gpa"]
        group_no = df[df["internship_binary"] == 0]["gpa"]

        t_stat, p_value = ttest_ind(group_yes, group_no, equal_var=False)

        # Cohen's d
        mean_diff = group_yes.mean() - group_no.mean()
        pooled_std = np.sqrt(
            ((group_yes.std() ** 2) + (group_no.std() ** 2)) / 2
        )
        cohens_d = mean_diff / pooled_std

        print("Hypothesis 1: GPA difference (Internship vs No Internship)")
        print(f"t-statistic: {t_stat:.4f}")
        print(f"p-value: {p_value:.4f}")
        print(f"Cohen's d: {cohens_d:.4f}")

        if p_value < 0.05:
            print("Interpretation: Statistically significant difference in GPA between groups.\n")
        else:
            print("Interpretation: No statistically significant difference in GPA between groups.\n")

        results["hypothesis_1"] = {
            "t_statistic": t_stat,
            "p_value": p_value,
            "cohens_d": cohens_d
        }

    # -------------------------------------------------
    # Hypothesis 2: Scholarship vs Department (Chi-square)
    # -------------------------------------------------
    if {"scholarship", "department"}.issubset(df.columns):

        contingency_table = pd.crosstab(df["department"], df["scholarship"])

        chi2_stat, p_value, dof, expected = chi2_contingency(contingency_table)

        print("Hypothesis 2: Scholarship status vs Department")
        print(f"Chi-square statistic: {chi2_stat:.4f}")
        print(f"Degrees of freedom: {dof}")
        print(f"p-value: {p_value:.4f}")

        if p_value < 0.05:
            print("Interpretation: Scholarship status is significantly associated with department.\n")
        else:
            print("Interpretation: No significant association between scholarship status and department.\n")

        results["hypothesis_2"] = {
            "chi2_statistic": chi2_stat,
            "degrees_of_freedom": dof,
            "p_value": p_value
        }

    return results


def main():
    """Orchestrate the full EDA pipeline."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Load and profile the dataset
    df = load_and_profile("data/student_performance.csv")

    # Clean the data by handling missing values
    cleaned_df = handle_missing_values(df)
    print("Missing values handled. Cleaned dataset ready for analysis.")
    print(f"Cleaned dataset shape: {cleaned_df.shape}")

    # Generate distribution plots
    plot_distributions(cleaned_df)

    # Analyze correlations
    plot_correlations(cleaned_df)

    # Run hypothesis tests
    run_hypothesis_tests(cleaned_df)


if __name__ == "__main__":
    main()
