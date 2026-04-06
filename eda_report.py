import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


class EDAReport:
    def __init__(
        self,
        df: pd.DataFrame,
        output_dir: str = "output/challenges/",
        columns: list | None = None,
        style: str = "whitegrid",
    ):
        self.df = df.copy()
        self.output_dir = output_dir
        self.columns = columns
        self.style = style

        os.makedirs(self.output_dir, exist_ok=True)

        sns.set_style(self.style)

    # -------------------------------------------------
    # 1️⃣ Data Profile
    # -------------------------------------------------
    def data_profile(self) -> pd.DataFrame:
        profile = pd.DataFrame({
            "dtype": self.df.dtypes,
            "missing_values": self.df.isnull().sum(),
            "missing_percent": self.df.isnull().mean() * 100,
            "n_unique": self.df.nunique()
        })

        profile.to_csv(f"{self.output_dir}/data_profile.csv")
        return profile

    # -------------------------------------------------
    # 2️⃣ Distribution Plots
    # -------------------------------------------------
    def distribution_plots(self):
        numeric_cols = self._get_numeric_columns()

        for col in numeric_cols:
            plt.figure(figsize=(6, 4))
            sns.histplot(self.df[col].dropna(), kde=True)
            plt.title(f"Distribution of {col}")
            plt.tight_layout()
            plt.savefig(f"{self.output_dir}/dist_{col}.png")
            plt.close()

    # -------------------------------------------------
    # 3️⃣ Correlation Heatmap
    # -------------------------------------------------
    def correlation_heatmap(self):
        numeric_df = self.df[self._get_numeric_columns()]

        if numeric_df.shape[1] < 2:
            return

        corr = numeric_df.corr()

        plt.figure(figsize=(10, 8))
        sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
        plt.title("Correlation Heatmap")
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/correlation_heatmap.png")
        plt.close()

    # -------------------------------------------------
    # 4️⃣ Missing Data Visualization
    # -------------------------------------------------
    def missing_visualization(self):
        plt.figure(figsize=(8, 4))
        sns.heatmap(self.df.isnull(), cbar=False)
        plt.title("Missing Data Heatmap")
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/missing_data.png")
        plt.close()

    # -------------------------------------------------
    # 5️⃣ Outlier Summary (IQR)
    # -------------------------------------------------
    def outlier_summary(self) -> pd.DataFrame:
        numeric_cols = self._get_numeric_columns()
        summary = {}

        for col in numeric_cols:
            q1 = self.df[col].quantile(0.25)
            q3 = self.df[col].quantile(0.75)
            iqr = q3 - q1

            lower = q1 - 1.5 * iqr
            upper = q3 + 1.5 * iqr

            outliers = self.df[(self.df[col] < lower) | (self.df[col] > upper)]

            summary[col] = {
                "outlier_count": len(outliers),
                "lower_bound": lower,
                "upper_bound": upper,
            }

        summary_df = pd.DataFrame(summary).T
        summary_df.to_csv(f"{self.output_dir}/outlier_summary.csv")

        return summary_df

    # -------------------------------------------------
    # Utility
    # -------------------------------------------------
    def _get_numeric_columns(self):
        if self.columns:
            return [c for c in self.columns if pd.api.types.is_numeric_dtype(self.df[c])]
        return self.df.select_dtypes(include=np.number).columns.tolist()

    # -------------------------------------------------
    # Run Full Report
    # -------------------------------------------------
    def run(self):
        self.data_profile()
        self.distribution_plots()
        self.correlation_heatmap()
        self.missing_visualization()
        self.outlier_summary()