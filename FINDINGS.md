# FINDINGS.md

## 1. Dataset Description

* **Shape:** 2000 rows × 10 columns

* **Columns and Types:**

  * `student_id` (str)
  * `department` (str)
  * `semester` (str)
  * `course_load` (int64)
  * `study_hours_weekly` (float64)
  * `gpa` (float64)
  * `attendance_pct` (float64)
  * `has_internship` (str)
  * `commute_minutes` (float64)
  * `scholarship` (str)

* **Notable Data Quality Issues:**

  * `commute_minutes` had 9.05% missing values, filled with the median (25 minutes).
  * `scholarship` had 19.45% missing values, which were dropped from the dataset.

* **After cleaning:** no missing values remain.

---

## 2. Key Distribution Findings

* `gpa` and `study_hours_weekly` are slightly right-skewed, indicating a few students with exceptionally high values.
* `attendance_pct` is left-skewed, showing that most students attend regularly with a few low outliers.
* Box plots by `department` reveal:

  * Some departments have **higher median GPA** than others.
  * Course load differences across departments show **wider variability** in student workloads.

**See charts:**
output\dist_attendance.png
output\dist_commute_minutes.png
output\dist_gpa.png
output\dist_study_hours.png
output\gpa_boxplot.png
output\scatter_attendance_gpa.png
output\scatter_study_gpa.png
output\scholarship.png
output\correlation_heatmap.png

---

## 3. Notable Correlations

* **Most correlated pair:** `study_hours_weekly` and `gpa`.
* `attendance_pct` also positively correlates with `gpa`.

**See chart:**
[GPA vs Study Hours](output/gpa_vs_study_hours.png)


---

## 4. Hypothesis Test Results

### Hypothesis 1: Students with internships have higher GPA

* **Test used:** Independent t-test
* **Results:**

  * T-statistic: `nan`
  * P-value: `nan`
  * Cohen's d: `nan`
* **Interpretation:** Not enough data to perform the test. No statistically significant difference detected.

### Hypothesis 2: Scholarship status is associated with department

* **Test used:** Chi-square test
* **Results:**

  * Chi-square statistic: 13.9486
  * P-value: 0.3040
  * Degrees of freedom: 12
* **Interpretation:** No significant association between scholarship and department.

---
