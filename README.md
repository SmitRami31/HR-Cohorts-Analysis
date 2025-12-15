# HR Strategic Workforce Analytics Dashboard

A data-driven Streamlit application that provides strategic insights into workforce dynamics through year-over-year cohort analysis. This dashboard helps HR leaders and executives identify critical talent risks, stagnation patterns, and intervention opportunities.

##  Project Overview

This analytics dashboard analyzes employee data across two consecutive years (2024-2025) to uncover hidden patterns in workforce dynamics, retention challenges, and manager effectiveness. It transforms raw HR data into actionable strategic insights using advanced cohort analysis and visualization techniques.

##  Key Insights Provided

### 1. **Intervention Effectiveness Failure**
- **What it shows:** Success/failure rate of retention efforts for high-risk talent
- **Business Value:** Identifies whether your retention programs are working
- **Visualization:** Pie chart showing three outcomes for employees flagged as "High Risk":
  - Left the organization
  - Still at risk (intervention failed)
  - Risk mitigated (intervention succeeded)
- **Actionable Metric:** Overall failure rate percentage

### 2. **Manager Capability Crisis**
- **What it shows:** Which managers have the most stagnant employees on their teams
- **Business Value:** Pinpoints coaching and development gaps at the leadership level
- **Visualization:** Horizontal bar chart ranking managers by number of stagnant team members
- **Actionable Metric:** Top 5 managers requiring immediate capability development

### 3. **Cross-Functional Success Pattern**
- **What it shows:** Impact of manager/team changes on breaking stagnation cycles
- **Business Value:** Proves that lateral moves and team changes drive employee growth
- **Visualization:** Grouped bar chart comparing improvement rates between employees who:
  - Changed managers vs. stayed with same manager
  - Improved vs. stayed stagnant
- **Actionable Metric:** Success rate correlation with manager changes

### 4. **Department Concentration Alert**
- **What it shows:** Year-over-year growth of stagnant employees by department
- **Business Value:** Identifies departments accumulating talent risks faster than others
- **Visualization:** Grouped bar chart showing 2024 vs 2025 stagnation counts per department
- **Actionable Metric:** Top 5 departments with highest concentration of stagnant talent

### 5. **Dual-Risk Hidden Gems**
- **What it shows:** High-potential employees who are currently stagnating
- **Business Value:** Identifies highest-ROI retention targets (high value + high flight risk)
- **Visualization:** Interactive data table with employee details and replacement costs
- **Actionable Metric:** 
  - Total financial liability if these employees leave
  - Count of critical employees requiring immediate intervention
  - Recommended action: Schedule stay interviews within 7 days

##  How It Works

### Data Processing
The dashboard applies sophisticated cohort logic to categorize employees:

**Stagnant Employees** - Identified by combination of:
- **Long tenure in role:** >3 years in current position
- **Low competence level:** Starter/Confirmed/Experienced bands

**High-Risk Talent** - Identified by combination of:
- **High potential:** KEY, HIGHPO, RISING, CONSIST, STAR designations
- **High attrition risk:** Medium, High, or Very High flight risk scores

**Dual-Risk Candidates** - Employees who are BOTH stagnant AND high-risk (highest priority)

### Year-Over-Year Analysis
The dashboard merges 2024 and 2025 datasets to track:
- Employee retention status (Left vs. Retained)
- Changes in risk profiles over time
- Manager and department changes
- Improvement or regression in stagnation/risk status

##  Use Cases

This dashboard is ideal for:
- **HR Leaders:** Strategic workforce planning and risk mitigation
- **Talent Development Teams:** Identifying coaching and development needs
- **Executive Leadership:** Understanding retention ROI and talent pipeline health
- **Department Heads:** Benchmarking team health across the organization

## 👤 Author

- GitHub: [@smitrami31](https://github.com/smitrami31)
