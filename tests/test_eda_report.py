import pandas as pd
from eda_report import EDAReport

def test_handles_missing_values(tmp_path):
    df = pd.DataFrame({
        "A": [1, 2, None, 4],
        "B": [5, None, 7, 8],
        "C": ["x", "y", "z", None]
    })

    report = EDAReport(df, output_dir=tmp_path)
    profile = report.data_profile()

    assert "missing_values" in profile.columns
    assert profile.loc["A", "missing_values"] == 1


def test_outlier_detection(tmp_path):
    df = pd.DataFrame({
        "A": [1, 2, 3, 4, 100]
    })

    report = EDAReport(df, output_dir=tmp_path)
    summary = report.outlier_summary()

    assert summary.loc["A", "outlier_count"] == 1


def test_small_dataframe(tmp_path):
    df = pd.DataFrame({
        "A": [1],
        "B": ["x"]
    })

    report = EDAReport(df, output_dir=tmp_path)
    report.run()

    assert True  # Should not crash