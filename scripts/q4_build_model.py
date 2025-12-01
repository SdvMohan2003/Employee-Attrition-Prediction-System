"""
scripts/q4_modeling.py

- Train Logistic Regression and Random Forest to predict 'left'
- Save results into an XLSX file under output/xlsx_output/
- Save confusion matrix images under output/image_output/

Run:
  python scripts\q4_modeling.py
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

# ---------------------------
# Paths
# ---------------------------
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Accept either "data" or "dataset" folder
if os.path.exists(os.path.join(BASE_DIR, "data", "HR_comma_sep.csv")):
    DATA_PATH = os.path.join(BASE_DIR, "data", "HR_comma_sep.csv")
else:
    DATA_PATH = os.path.join(BASE_DIR, "dataset", "HR_comma_sep.csv")

XLSX_DIR = os.path.join(BASE_DIR, "output", "xlsx_output")
IMG_DIR = os.path.join(BASE_DIR, "output", "image_output")
os.makedirs(XLSX_DIR, exist_ok=True)
os.makedirs(IMG_DIR, exist_ok=True)

XLSX_OUT = os.path.join(XLSX_DIR, "q4_model_results.xlsx")
CM_IMG_LR = os.path.join(IMG_DIR, "q4_confusion_logistic.png")
CM_IMG_RF = os.path.join(IMG_DIR, "q4_confusion_random_forest.png")

# ---------------------------
# Configuration
# ---------------------------
RANDOM_STATE = 42
TEST_SIZE = 0.20

# ---------------------------
# Small helper: plot + save confusion matrix
# ---------------------------
def save_confusion_matrix_image(cm, labels, filepath, title="Confusion Matrix"):
    """
    cm: 2x2 numpy array
    labels: list of label names (e.g. ['Stayed', 'Left'])
    filepath: where to save PNG
    """
    plt.figure(figsize=(4, 3))
    plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    plt.title(title)
    plt.colorbar()
    tick_marks = range(len(labels))
    plt.xticks(tick_marks, labels)
    plt.yticks(tick_marks, labels)

    # Annotate numbers
    thresh = cm.max() / 2.0
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            plt.text(j, i, format(int(cm[i, j]), 'd'),
                     horizontalalignment="center",
                     color="white" if cm[i, j] > thresh else "black")

    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.tight_layout()
    plt.savefig(filepath, dpi=200)
    plt.close()

# ---------------------------
# Main
# ---------------------------
def main():
    # 1) Load data
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Data file not found at: {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)

    # 2) Check target column
    if "left" not in df.columns:
        raise KeyError("Target column 'left' not found in dataset.")

    # 3) Prepare features (X) and target (y)
    y = df["left"]
    X = df.drop(columns=["left"])

    # 4) Encode categorical variables (one-hot)
    # drop_first=True removes one dummy to avoid perfect multicollinearity
    X = pd.get_dummies(X, drop_first=True)

    # 5) Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
    )

    # Containers to collect results for XLSX
    summary_rows = []
    lr_report_df = None
    rf_report_df = None
    feature_importances_df = pd.DataFrame()

    # ---------- Logistic Regression ----------
    lr = LogisticRegression(max_iter=1000, n_jobs=-1, random_state=RANDOM_STATE)
    lr.fit(X_train, y_train)
    y_pred_lr = lr.predict(X_test)

    acc_lr = accuracy_score(y_test, y_pred_lr)
    cm_lr = confusion_matrix(y_test, y_pred_lr)
    cr_lr = classification_report(y_test, y_pred_lr, output_dict=True)

    # Put classification report into a DataFrame for Excel
    lr_report_df = pd.DataFrame(cr_lr).transpose().reset_index().rename(columns={"index": "class_or_metric"})

    summary_rows.append(["Logistic Regression", "accuracy", acc_lr])

    # Save confusion matrix image
    save_confusion_matrix_image(cm_lr, labels=["Stayed (0)", "Left (1)"], filepath=CM_IMG_LR, title="Logistic Regression CM")

    # ---------- Random Forest ----------
    rf = RandomForestClassifier(n_estimators=200, random_state=RANDOM_STATE, n_jobs=-1)
    rf.fit(X_train, y_train)
    y_pred_rf = rf.predict(X_test)

    acc_rf = accuracy_score(y_test, y_pred_rf)
    cm_rf = confusion_matrix(y_test, y_pred_rf)
    cr_rf = classification_report(y_test, y_pred_rf, output_dict=True)

    rf_report_df = pd.DataFrame(cr_rf).transpose().reset_index().rename(columns={"index": "class_or_metric"})
    summary_rows.append(["Random Forest", "accuracy", acc_rf])

    # Feature importances (from Random Forest) — show top 20 for readability
    if hasattr(rf, "feature_importances_"):
        fi = rf.feature_importances_
        fi_df = pd.DataFrame({
            "feature": X.columns,
            "importance": fi
        }).sort_values("importance", ascending=False).reset_index(drop=True)
        feature_importances_df = fi_df.head(20)

    # Save Random Forest confusion matrix image
    save_confusion_matrix_image(cm_rf, labels=["Stayed (0)", "Left (1)"], filepath=CM_IMG_RF, title="Random Forest CM")

    # ---------- Save results to XLSX ----------
    summary_df = pd.DataFrame(summary_rows, columns=["model", "metric", "value"])

    # Write multiple sheets: summary, lr_report, rf_report, feature_importances
    with pd.ExcelWriter(XLSX_OUT, engine="openpyxl") as writer:
        summary_df.to_excel(writer, sheet_name="summary", index=False)
        lr_report_df.to_excel(writer, sheet_name="logistic_report", index=False)
        rf_report_df.to_excel(writer, sheet_name="rf_report", index=False)
        feature_importances_df.to_excel(writer, sheet_name="feature_importances", index=False)
        # also save a small sample of X columns and dtypes for debugging
        pd.DataFrame({"column": X.columns, "dtype": X.dtypes.astype(str)}).to_excel(writer, sheet_name="features", index=False)

    print(f"[Q4] XLSX results saved to: {XLSX_OUT}")
    print(f"[Q4] Confusion images saved to: {CM_IMG_LR} and {CM_IMG_RF}")
    print(f"[Q4] Accuracy - Logistic: {acc_lr:.4f}, Random Forest: {acc_rf:.4f}")

if __name__ == "__main__":
    main()
