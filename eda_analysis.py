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
from scipy import stats


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
    df = pd.read_csv('data/student_performance.csv')
    #x= df.shape
    #y= df.dtypes
    ##z= df.describe
    with open('output/data_profile.txt','w') as f :
        f.write(f'Shape:\n{df.shape}\n')
        f.write("=============\n")
        f.write(f'data types: \n{df.dtypes}\n')
        f.write("=============\n")
        f.write(f'Missing Count:\n{df.isnull().sum()}\n')
        f.write("=============\n")
        f.write(f'Missing Percent:\n{df.isnull().sum()/ len(df)*100}\n')
        f.write("=============\n\n")

        f.write("=== Handling Decisions ===\n\n")
        x = df['commute_minutes'].median()
        f.write(f'Median For commute_minute:\n{x}\n\n')
        f.write("=============\n\n")
        f.write(f'BEFORE commute_minutes:\n{df['commute_minutes'][0:9]}\n\n')
        f.write("=============\n\n")
        df["commute_minutes"] = df['commute_minutes'].fillna(x)
        f.write("=============\n\n")
        f.write(f'AFTER commute_minutes:\n{df['commute_minutes'][0:9]}\n\n')
        f.write(f'Missing Count:\n{df.isnull().sum()}\n\n')

        
        drop_value = df.dropna(subset=['scholarship'], inplace=True)
        f.write(f'AFTER Drop scholarship NaN:\n{df.isnull().sum()}\n')
        return df



    pass


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
    fig,axes = plt.subplots(figsize = (10,6))
    sns.histplot(df["gpa"], kde=True)
    axes.set_title("GPA Distribution")
    axes.set_xlabel("GPA")
    axes.set_ylabel("Count")
    plt.tight_layout()
    plt.savefig("output/dist_gpa.png")
    plt.close()

    fig,axes = plt.subplots(figsize = (10,6))
    sns.histplot(df["study_hours_weekly"], kde=True)
    axes.set_title("study_hours Distribution")
    axes.set_xlabel("study_hours")
    axes.set_ylabel("Count")
    plt.tight_layout()
    plt.savefig("output/dist_study_hours.png")
    plt.close()

    fig,axes = plt.subplots(figsize = (10,6))
    sns.histplot(df["attendance_pct"], kde=True)
    axes.set_title("attendance Distribution")
    axes.set_xlabel("attendance")
    axes.set_ylabel("Count")
    plt.tight_layout()
    plt.savefig("output/dist_attendance.png")
    plt.close()

    fig,axes = plt.subplots(figsize = (10,6))
    sns.histplot(df["commute_minutes"], kde=True)
    axes.set_title("commute_minutes Distribution")
    axes.set_xlabel("commute_minutes")
    axes.set_ylabel("Count")
    plt.tight_layout()
    plt.savefig("output/dist_commute_minutes.png")
    plt.close()

    sns.boxplot(x='department', y='gpa',data= df)
    plt.title("GPA by Department")
    plt.savefig("output/gpa_boxplot.png")
    plt.close()


    df["scholarship"].value_counts().plot(kind="bar")
    plt.title("Scholarship Distribution")
    plt.savefig("output/scholarship.png")
    plt.close()
    
    return df
    
    
    pass


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
    corr_matrix = df.corr(numeric_only=True)
    plt.figure(figsize=(10,6))
    sns.heatmap(corr_matrix,annot=True,cmap='coolwarm')
    plt.title("Correlation Matrix")
    plt.savefig("output/correlation_heatmap.png")
    plt.close()

    corr_pairs = corr_matrix.unstack()
    corr_pairs = corr_pairs[corr_pairs < 1]  # حذف self-correlation
    top_pairs = corr_pairs.abs().sort_values(ascending=False).drop_duplicates().head(2)

    print(top_pairs)

    sns.scatterplot(x="study_hours_weekly", y="gpa", data=df)
    plt.title("Study Hours vs GPA")
    plt.savefig("output/scatter_study_gpa.png")
    plt.close()

    sns.scatterplot(x="attendance_pct", y="gpa", data=df)
    plt.title("attendance vs GPA")
    plt.savefig("output/scatter_attendance_gpa.png")
    plt.close()

    pass


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
    alpha = 0.05

    print("\n=== Hypothesis Testing Results ===\n")

    # --------------------------------------------------
    # Hypothesis 1: Internship vs GPA (Independent t-test)
    # --------------------------------------------------
    print("Hypothesis 1: Students with internships have higher GPA\n")

    # Handle 0/1 or True/False values
    group_yes = df[df["has_internship"] == 1]["gpa"]
    group_no = df[df["has_internship"] == 0]["gpa"]

    # T-test
    t_stat, p_val = stats.ttest_ind(group_yes, group_no, nan_policy='omit')

    # Cohen's d
    mean1, mean2 = group_yes.mean(), group_no.mean()
    std1, std2 = group_yes.std(), group_no.std()
    n1, n2 = len(group_yes), len(group_no)

    pooled_std = np.sqrt(((n1 - 1)*std1**2 + (n2 - 1)*std2**2) / (n1 + n2 - 2))
    cohens_d = (mean1 - mean2) / pooled_std

    # Interpretation
    if p_val < alpha:
        interpretation = "There is a statistically significant difference in GPA."
    else:
        interpretation = "There is NO statistically significant difference in GPA."

    print(f"T-statistic: {t_stat:.4f}")
    print(f"P-value: {p_val:.4f}")
    print(f"Cohen's d: {cohens_d:.4f}")
    print(f"Interpretation: {interpretation}\n")

    results["internship_ttest"] = {
        "t_stat": t_stat,
        "p_value": p_val,
        "cohens_d": cohens_d
    }

    # --------------------------------------------------
    # Hypothesis 2: Scholarship vs Department (Chi-square)
    # --------------------------------------------------
    print("Hypothesis 2: Scholarship status is associated with department\n")

    # Contingency table
    contingency_table = pd.crosstab(df["department"], df["scholarship"])

    # Chi-square test
    chi2, p, dof, expected = stats.chi2_contingency(contingency_table)

    # Interpretation
    if p < alpha:
        interpretation2 = "There IS a significant association between scholarship and department."
    else:
        interpretation2 = "There is NO significant association between scholarship and department."

    print(f"Chi-square statistic: {chi2:.4f}")
    print(f"P-value: {p:.4f}")
    print(f"Degrees of freedom: {dof}")
    print(f"Interpretation: {interpretation2}\n")

    results["scholarship_chi2"] = {
        "chi2": chi2,
        "p_value": p,
        "dof": dof
    }

    return results
    pass


def main():
    """Orchestrate the full EDA pipeline."""
    os.makedirs("output", exist_ok=True)

    # TODO: Load and profile the dataset
    df = load_and_profile('data/student_performance.csv')
    # TODO: Generate distribution plots
    plot_distributions(df)
    # TODO: Analyze correlations
    # TODO: Run hypothesis tests
    plot_correlations(df)
    results = run_hypothesis_tests(df)
    # TODO: Write a FINDINGS.md summarizing your analysis
     


if __name__ == "__main__":
    main()
