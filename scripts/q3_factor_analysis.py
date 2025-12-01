"""
scripts/q3_factor_analysis.py

Simple, beginner-friendly script that:
 - reads the HR CSV
 - computes simple factor analyses (satisfaction, department, salary, promotion)
 - saves results into one XLSX file in output/xlsx_output/
 - saves a couple of helpful charts into output/image_output/

Run from project root when venv active:
  python scripts\q3_factor_analysis.py
"""

import os
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------
# Paths (easy to update)
# ---------------------------
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Accept either "dataset" or "data" folder (some of your scripts used both)
if os.path.exists(os.path.join(BASE_DIR, "dataset", "HR_comma_sep.csv")):
    DATA_PATH = os.path.join(BASE_DIR, "dataset", "HR_comma_sep.csv")
else:
    DATA_PATH = os.path.join(BASE_DIR, "data", "HR_comma_sep.csv")

XLSX_DIR = os.path.join(BASE_DIR, "output", "xlsx_output")
IMG_DIR = os.path.join(BASE_DIR, "output", "image_output")
os.makedirs(XLSX_DIR, exist_ok=True)
os.makedirs(IMG_DIR, exist_ok=True)

XLSX_OUT = os.path.join(XLSX_DIR, "q3_factor_analysis.xlsx")
DEPT_IMG = os.path.join(IMG_DIR, "q3_dept_attrition_bar.png")
SAL_IMG = os.path.join(IMG_DIR, "q3_salary_attrition_bar.png")

# ---------------------------
# Small helper
# ---------------------------
def attrition_rate(series):
    """Return mean of 'left' for a grouped series or DataFrame column."""
    return series.mean()

# ---------------------------
# Main
# ---------------------------
def main():
    # 1) Load dataset (clear message if not found)
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Data file not found at: {DATA_PATH}\n"
                                f"Please place HR_comma_sep.csv in dataset/ or data/ folder.")
    df = pd.read_csv(DATA_PATH)

    # 2) Ensure 'left' column exists (we need it to compute attrition)
    if "left" not in df.columns:
        raise KeyError("Column 'left' not found in dataset. This script needs 'left' (0/1).")

    # 3) Simple analyses
    # 3a. Satisfaction level: average for stayed vs left
    sat_by_left = df.groupby("left")["satisfaction_level"].mean().reset_index()
    sat_by_left.columns = ["left", "avg_satisfaction"]

    # 3b. Department-wise attrition rate
    if "Department" in df.columns:
        dept_attrition = df.groupby("Department")["left"].mean().reset_index()
        dept_attrition.columns = ["Department", "attrition_rate"]
        dept_attrition = dept_attrition.sort_values("attrition_rate", ascending=False)
    else:
        dept_attrition = pd.DataFrame(columns=["Department", "attrition_rate"])

    # 3c. Salary-wise attrition rate (if salary exists)
    if "salary" in df.columns:
        sal_attrition = df.groupby("salary")["left"].mean().reset_index()
        sal_attrition.columns = ["salary", "attrition_rate"]
        sal_attrition = sal_attrition.sort_values("attrition_rate", ascending=False)
    else:
        sal_attrition = pd.DataFrame(columns=["salary", "attrition_rate"])

    # 3d. Promotion last 5 years vs attrition (if column exists)
    if "promotion_last_5years" in df.columns:
        promo_attrition = df.groupby("promotion_last_5years")["left"].mean().reset_index()
        promo_attrition.columns = ["promotion_last_5years", "attrition_rate"]
    else:
        promo_attrition = pd.DataFrame(columns=["promotion_last_5years", "attrition_rate"])

    # 3e. Combined: attrition by Department & Salary (if salary exists)
    if "salary" in df.columns and "Department" in df.columns:
        dept_sal_attrition = (
            df.groupby(["Department", "salary"])["left"]
            .mean()
            .reset_index()
            .rename(columns={"left": "attrition_rate"})
            .sort_values("attrition_rate", ascending=False)
        )
    else:
        dept_sal_attrition = pd.DataFrame(columns=["Department", "salary", "attrition_rate"])

    # 4) Save results to XLSX, each result is one sheet
    with pd.ExcelWriter(XLSX_OUT, engine="openpyxl") as writer:
        sat_by_left.to_excel(writer, sheet_name="satisfaction_by_left", index=False)
        dept_attrition.to_excel(writer, sheet_name="department_attrition", index=False)
        sal_attrition.to_excel(writer, sheet_name="salary_attrition", index=False)
        promo_attrition.to_excel(writer, sheet_name="promo_attrition", index=False)
        dept_sal_attrition.to_excel(writer, sheet_name="dept_salary_attrition", index=False)

    print(f"[Q3] Excel results saved to: {XLSX_OUT}")

    # 5) Create simple charts and save to images (only if data available)
    # 5a Department attrition bar chart
    if not dept_attrition.empty:
        plt.figure(figsize=(8, 4))
        plt.bar(dept_attrition["Department"], dept_attrition["attrition_rate"])
        plt.xticks(rotation=45, ha="right")
        plt.ylabel("Attrition rate")
        plt.title("Department-wise Attrition Rate")
        plt.tight_layout()
        plt.savefig(DEPT_IMG, dpi=200)
        plt.close()
        print(f"[Q3] Department chart saved to: {DEPT_IMG}")
    else:
        print("[Q3] Department column not found — skipping department chart.")

    # 5b Salary attrition bar chart
    if not sal_attrition.empty:
        plt.figure(figsize=(6, 4))
        plt.bar(sal_attrition["salary"].astype(str), sal_attrition["attrition_rate"])
        plt.ylabel("Attrition rate")
        plt.title("Salary-wise Attrition Rate")
        plt.tight_layout()
        plt.savefig(SAL_IMG, dpi=200)
        plt.close()
        print(f"[Q3] Salary chart saved to: {SAL_IMG}")
    else:
        print("[Q3] Salary column not found — skipping salary chart.")

if __name__ == "__main__":
    main()
