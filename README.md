📘 Employee Attrition Prediction System

A complete end-to-end mini data science project that analyzes why employees leave, explores key factors, and builds ML models to predict attrition.

This project includes:

Data exploration

Relationship analysis

Factor analysis

Machine learning modeling

Automated outputs saved as clear Excel reports + plotted images

📂 Project Structure

```
Employee Attrition Prediction System/
│
├── dataset/
│   └── HR_comma_sep.csv
│
├── output/
│   ├── image_output/
│   │   ├── q2_scatter_satisfaction_vs_hours.png
│   │   ├── q2_distribution_satisfaction_left_vs_stayed.png
│   │   ├── q3_dept_attrition_bar.png
│   │   ├── q3_salary_attrition_bar.png
│   │   ├── q4_confusion_logistic.png
│   │   └── q4_confusion_random_forest.png
│   │
│   └── xlsx_output/
│       ├── q1_data_exploration.xlsx
│       ├── q2_satisfaction_summary.xlsx
│       ├── q3_factor_analysis.xlsx
│       └── q4_model_results.xlsx
│
├── scripts/
│   ├── q1_explore_data.py
│   ├── q2_satisfaction_vs_hours.py
│   ├── q3_factor_analysis.py
│   └── q4_modeling.py
│
├── README.md
└── requirements.txt
```

🚀 Project Overview
📊 Objective

To analyze HR data, understand what drives employee attrition, visualize trends, and build predictive machine learning models.

📁 Dataset Used

HR_comma_sep.csv contains:

satisfaction_level

average_montly_hours

number_project

time_spend_company

Work_accident

promotion_last_5years

salary

Department

left (target variable – 1 = left, 0 = stayed)

⚙️ Setup Instructions
1. Create virtual environment
python -m venv .venv

2. Activate venv

PowerShell

.\.venv\Scripts\activate

3. Install libraries
pip install -r requirements.txt

4. Run scripts from project root
python scripts/q1_explore_data.py
python scripts/q2_satisfaction_vs_hours.py
python scripts/q3_factor_analysis.py
python scripts/q4_modeling.py

🧪 Analysis & Outputs

Below is a clear explanation of what each script generates.

✅ Q1 – Data Exploration

Script: q1_explore_data.py
Output: output/xlsx_output/q1_data_exploration.xlsx

Includes:

Dataset shape

Column dtypes

Missing values

Duplicate rows

Summary statistics

Target distribution (left vs stayed)

✅ Q2 – Satisfaction vs Working Hours

Script: q2_satisfaction_vs_hours.py
Outputs:

q2_satisfaction_summary.xlsx

Scatter plot

Satisfaction distribution plot

Key insights:

Relationship between satisfaction level & working hours

Correlation for all employees + only employees who left

✅ Q3 – Factor Analysis

Script: q3_factor_analysis.py
Outputs:

q3_factor_analysis.xlsx

Department attrition bar chart

Salary attrition bar chart

Findings include:

Which departments have the highest attrition

Impact of salary levels

Impact of promotions

Combined effect of department + salary

✅ Q4 – Machine Learning Models

Script: q4_modeling.py
Outputs:

q4_model_results.xlsx

Confusion matrix for Logistic Regression

Confusion matrix for Random Forest

Models used:

Logistic Regression

Random Forest Classifier

Metrics saved:

Accuracy

Classification report

Confusion matrix

Top features (from Random Forest)

📈 Sample Results
🔥 Best Model (Expected)

Random Forest usually performs better because:

Handles nonlinear relationships

Captures complex patterns

Works well with mixed data types

✔️ Requirements

The requirements.txt includes:

pandas
numpy
matplotlib
scikit-learn
openpyxl

🎯 Summary

This project covers the complete workflow of an Employee Attrition Analysis System:

Module	Task	Output
Q1	Data Exploration	XLSX
Q2	Satisfaction vs Hours	XLSX + Images
Q3	Factor Analysis	XLSX + Images
Q4	Machine Learning Models	XLSX + Images

Everything is automated and stored cleanly inside output/.
