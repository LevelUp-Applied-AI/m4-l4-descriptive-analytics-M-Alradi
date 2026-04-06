## 1. Dataset Description

* **Shape:** 2000 rows × 10 columns
* **Columns:**
  `student_id, department, semester, course_load, study_hours_weekly, gpa, attendance_pct, has_internship, commute_minutes, scholarship`
* **Notable Data Quality Issues:**

  * Some missing values in `commute_minutes` (~10%) and `study_hours_weekly` (~5%)
  * `has_internship` stored as `"Yes"/"No"` strings (converted to numeric for analysis)
  * Minor variations in scholarship types, requiring standardization

**See:** `output/data_profile.txt` for full data profile including missing values, descriptive statistics, and data types.

---

## 2. Key Distribution Findings

### Numeric Variables (Histograms + KDE)

* `gpa` distribution is roughly **symmetric** with a slight tail toward lower GPAs, indicating most students have mid-to-high GPAs with few low outliers.
* `study_hours_weekly` is roughly **symmetric** with a slight **right skew**, indicating most students study around 10–20 hours per week, with a few outliers studying much longer.
* `attendance_pct` distribution is negatively skewed (left-skewed), indicating that most entries show high attendance—concentrated between 70% and 90% — with a noticeable spike at 100% and a long tail of infrequent lower outliers.
* `commute_minutes`  is right-skewed (positively skewed), showing that most commutes are relatively short—peaking around 25 minutes—with a long tail extending toward 80 minutes, indicating a few users have significantly longer travel times.

**See:** 
* `output/gpa_distribution.png`
* `output/attendance_pct_distribution.png`
* `output/commute_minutes_distribution.png`
* `output/study_hours_weekly_distribution.png`

### Boxplot: GPA Across Departments

* Medians are remarkably consistent, with `Engineering` and `Biology` showing a tiny lead over `Business` and `Mathematics`.

* The middle 50% of students in every department fall almost exactly within the same 2.5 to 3.1 range.

* Most departments show low outliers (students with GPAs below 1.5), while only `Biology` and `Mathematics` have students hitting a perfect 4.0.

**See:** `output/gpa_by_department_boxplot.png`

### Categorical Variables (Bar Charts)

* Scholarship distribution is remarkably even, but `Merit` scholarships are actually the most common (above 400), while `Department` scholarships are the least frequent by a small margin.

* Most students do not have internships, with the "Yes" count being significantly lower than the "No" count.

**See:** `output/scholarship_distribution.png`

---

## 3. Notable Correlations

* **Top correlated pairs:**

  1. `study_hours_weekly` & `gpa` (strong positive correlation)

     * Students who study more tend to achieve higher GPA.
  2. `attendance_pct` & `gpa` (moderate positive correlation)

     * Students with higher attendance generally have better academic performance.

* **Caveats:**

  * Correlation does **not imply causation**.
  * Other factors (motivation, prior preparation, course difficulty) may influence both variables.

**See:** `output/correlation_heatmap.png`
**See:** `output/scatter_study_hours_weekly_vs_gpa.png`
**See:** `output/scatter_gpa_vs_attendance_pct.png`

---

## 4. Hypothesis Test Results

### Hypothesis 1: GPA difference (Internship vs. No Internship)

* **Test Used:** Independent samples t-test

* **Results:**
    * **t-statistic:** 14.2288
    * **p-value:** 0.0000
    * **Cohen’s d:** 0.7061

* **Interpretation:**
    * **Statistically significant difference:** Students with internships have a significantly different GPA compared to those without. 
    * **Practical Significance:** The Cohen's d of **0.71** indicates a **medium-to-large effect size**, meaning the GPA gap isn't just statistically real, but also quite meaningful in practice.

---

### Hypothesis 2: Scholarship status vs. Department

* **Test Used:** Chi-square test of independence

* **Results:**
    * **Chi-square statistic:** 13.9486
    * **Degrees of freedom:** 12
    * **p-value:** 0.3040
    
* **Interpretation:**
    * **No significant association:** With a p-value well above 0.05, there is no evidence that certain departments are linked to specific scholarship types. Scholarships appear to be distributed independently of a student's department.

---

## 5. Actionable Recommendations

1. **Encourage study habits that improve GPA**

   * Finding: `study_hours_weekly` strongly correlates with GPA.
   * Recommendation: Offer structured study programs, workshops, or peer tutoring to increase study hours among students with lower GPAs.

2. **Promote class attendance**

   * Finding: `attendance_pct` positively correlates with GPA.
   * Recommendation: Consider attendance incentives or awareness campaigns to improve academic performance.

3. **Internship opportunities for skill-building**

   * Finding: Limited students have internships, and initial analysis suggests possible GPA benefits.
   * Recommendation: Expand internship programs and career counseling to increase student participation, potentially enhancing practical learning and performance.

---

**References to Saved Charts:**

* Histograms: * `output/gpa_distribution.png`, `output/attendance_pct_distribution.png`, `output/commute_minutes_distribution.png`, `output/study_hours_weekly_distribution.png`
* Boxplot: `output/gpa_by_department_boxplot.png`
* Bar chart: `output/scholarship_distribution.png`
* Correlation: `output/correlation_heatmap.png`
* Scatter plots: `output/scatter_study_hours_weekly_vs_gpa.png`, `output/scatter_gpa_vs_attendance_pct.png`
---