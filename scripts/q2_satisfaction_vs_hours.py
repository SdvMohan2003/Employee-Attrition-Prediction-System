"""
scripts/q2_satisfaction_vs_hours.py

- Reads dataset/d HR_comma_sep.csv
- Computes correlation between satisfaction and average hours
- Saves a short summary to an XLSX file in output/xlsx_output/
- Saves two image files (scatter + distribution) to output/image_output/
"""

import os
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------
# Paths (easy to update later)
# ---------------------------
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_PATH = os.path.join(BASE_DIR, "dataset", "HR_comma_sep.csv")

XLSX_DIR = os.path.join(BASE_DIR, "output", "xlsx_output")
IMG_DIR = os.path.join(BASE_DIR, "output", "image_output")
os.makedirs(XLSX_DIR, exist_ok=True)
os.makedirs(IMG_DIR, exist_ok=True)

XLSX_OUT = os.path.join(XLSX_DIR, "q2_satisfaction_summary.xlsx")
SCATTER_OUT = os.path.join(IMG_DIR, "q2_scatter_satisfaction_vs_hours.png")
DIST_OUT = os.path.join(IMG_DIR, "q2_distribution_satisfaction_left_vs_stayed.png")

# ---------------------------
# Simple helper to pick column
# ---------------------------
def pick_column(df, candidates):
    """Return first name from candidates that exists in df.columns, or None."""
    for c in candidates:
        if c in df.columns:
            return c
    return None

# ---------------------------
# Main function
# ---------------------------
def main():
    # 1) Load data
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Data file not found: {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)

    # 2) Find columns (tolerant to small name differences)
    sat_col = pick_column(df, ["satisfaction_level", "satisfaction"])
    hours_col = pick_column(df, ["average_monthly_hours", "average_montly_hours", "avg_monthly_hours"])
    left_col = pick_column(df, ["left", "attrition"])

    # Informative error if columns missing
    missing = []
    if sat_col is None:
        missing.append("satisfaction")
    if hours_col is None:
        missing.append("average_monthly_hours")
    if left_col is None:
        missing.append("left")
    if missing:
        raise KeyError(f"Missing columns: {', '.join(missing)}. Available: {list(df.columns)}")

    # 3) Rename columns to simple fixed names used below
    df = df.rename(columns={sat_col: "satisfaction_level",
                            hours_col: "average_monthly_hours",
                            left_col: "left"})

    # 4) Compute simple numbers for summary
    total_rows = len(df)
    corr_all = df["satisfaction_level"].corr(df["average_monthly_hours"])
    left_df = df[df["left"] == 1]
    corr_left = left_df["satisfaction_level"].corr(left_df["average_monthly_hours"]) if len(left_df) > 0 else None

    # Compute quartile means for employees who left (if any)
    quartile_means = None
    if len(left_df) > 0:
        # use qcut; if it fails because of duplicates, pandas will raise — keep simple for beginners
        left_df = left_df.copy()
        left_df["satisfaction_bin"] = pd.qcut(left_df["satisfaction_level"], 4, labels=False, duplicates="drop")
        quartile_means = left_df.groupby("satisfaction_bin")["average_monthly_hours"].mean()

    # 5) Prepare summary DataFrame(s) to write to XLSX
    summary_rows = [
        ["data_file", DATA_PATH],
        ["total_rows", total_rows],
        ["used_columns", "satisfaction_level, average_monthly_hours, left"],
        ["correlation_all", f"{corr_all:.4f}" if pd.notna(corr_all) else "nan"],
        ["correlation_left", f"{corr_left:.4f}" if corr_left is not None and pd.notna(corr_left) else "n/a"]
    ]
    summary_df = pd.DataFrame(summary_rows, columns=["metric", "value"])

    # quartile means as DataFrame (optional)
    if quartile_means is not None:
        quartile_df = quartile_means.reset_index().rename(columns={"satisfaction_bin": "quartile", "average_monthly_hours": "avg_monthly_hours"})
    else:
        quartile_df = pd.DataFrame(columns=["quartile", "avg_monthly_hours"])

    # Also include columns list and dtypes for debugging
    dtypes_df = df.dtypes.reset_index().rename(columns={"index": "column", 0: "dtype"})

    # 6) Write results to one XLSX file with multiple sheets
    with pd.ExcelWriter(XLSX_OUT, engine="openpyxl") as writer:
        summary_df.to_excel(writer, sheet_name="summary", index=False)
        dtypes_df.to_excel(writer, sheet_name="column_dtypes", index=False)
        quartile_df.to_excel(writer, sheet_name="quartile_means", index=False)

    print(f"[Q2] Summary XLSX saved to: {XLSX_OUT}")

    # 7) Create and save scatter plot (satisfaction vs avg hours) colored by left
    plt.figure(figsize=(6, 4))
    for val, label in [(0, "Stayed"), (1, "Left")]:
        subset = df[df["left"] == val]
        if subset.empty:
            continue
        plt.scatter(subset["satisfaction_level"], subset["average_monthly_hours"], s=10, alpha=0.5, label=label)
    plt.xlabel("Satisfaction Level")
    plt.ylabel("Average Monthly Hours")
    plt.title("Satisfaction vs Average Monthly Hours")
    plt.legend()
    plt.tight_layout()
    plt.savefig(SCATTER_OUT, dpi=300)
    plt.close()
    print(f"[Q2] Scatter image saved to: {SCATTER_OUT}")

    # 8) Distribution plot of satisfaction for stayed vs left
    stayed = df[df["left"] == 0]["satisfaction_level"]
    left = df[df["left"] == 1]["satisfaction_level"]

    plt.figure(figsize=(6, 4))
    plt.hist(stayed, bins=20, alpha=0.6, density=True, label="Stayed")
    plt.hist(left, bins=20, alpha=0.6, density=True, label="Left")
    plt.xlabel("Satisfaction Level")
    plt.ylabel("Density")
    plt.title("Satisfaction Level: Left vs Stayed")
    plt.legend()
    plt.tight_layout()
    plt.savefig(DIST_OUT, dpi=300)
    plt.close()
    print(f"[Q2] Distribution image saved to: {DIST_OUT}")


if __name__ == "__main__":
    main()
