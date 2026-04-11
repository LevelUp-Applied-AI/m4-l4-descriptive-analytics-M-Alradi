import pandas as pd
from eda_report import EDAReport

df = pd.read_csv("data/student_performance.csv")

report = EDAReport(
    df,
    output_dir="output/challenges/",
    columns=None,           # ← analyze all numeric columnsor
    style="darkgrid"        # configurable
)

report.run()