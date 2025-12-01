import os
import pandas as pd

# ---------------------------
# SETUP: File and folder paths
# ---------------------------

# Project root folder (one level above /scripts)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Input dataset
DATA_PATH = os.path.join(BASE_DIR, "dataset", "HR_comma_sep.csv")

# Output folder
OUTPUT_DIR = os.path.join(BASE_DIR, "output", "xlsx_output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Output Excel file path
XLSX_OUT = os.path.join(OUTPUT_DIR, "q1_data_exploration.xlsx")


def main():
    # -----------------------------------
    # 1. Load the dataset into a DataFrame
    # -----------------------------------
    df = pd.read_csv(DATA_PATH)

    # --------------------------------------------------
    # 2. Prepare different parts of the data exploration
    #    Each section will become a separate Excel sheet
    # --------------------------------------------------

    # Dataset row & column count
    dataset_shape = pd.DataFrame({"shape": [df.shape]})

    # Data types of each column
    column_dtypes = df.dtypes.reset_index()
    column_dtypes.columns = ["column", "dtype"]

    # Missing values per column
    missing_values = df.isna().sum().reset_index()
    missing_values.columns = ["column", "missing_count"]

    # Number of duplicate rows
    duplicate_rows = pd.DataFrame({"duplicate_rows": [df.duplicated().sum()]})

    # Basic statistics for numeric columns
    describe_numeric = df.describe().reset_index()
    describe_numeric.rename(columns={"index": "stat"}, inplace=True)

    # Target variable analysis (if available)
    if "left" in df.columns:
        left_distribution = df["left"].value_counts().reset_index()
        left_distribution.columns = ["left_value", "count"]

        left_proportion = df["left"].value_counts(normalize=True).reset_index()
        left_proportion.columns = ["left_value", "proportion"]
    else:
        left_distribution = pd.DataFrame()
        left_proportion = pd.DataFrame()

    # --------------------------------------------------
    # 3. Write all results into a single Excel file
    # --------------------------------------------------
    with pd.ExcelWriter(XLSX_OUT, engine="openpyxl") as writer:
        dataset_shape.to_excel(writer, sheet_name="dataset_shape", index=False)
        column_dtypes.to_excel(writer, sheet_name="column_dtypes", index=False)
        missing_values.to_excel(writer, sheet_name="missing_values", index=False)
        duplicate_rows.to_excel(writer, sheet_name="duplicate_rows", index=False)
        describe_numeric.to_excel(writer, sheet_name="describe_numeric", index=False)
        left_distribution.to_excel(writer, sheet_name="left_distribution", index=False)
        left_proportion.to_excel(writer, sheet_name="left_proportion", index=False)

    print(f"[Q1] Excel file created successfully at:\n{XLSX_OUT}")


if __name__ == "__main__":
    main()
