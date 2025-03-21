# Exploratory Data Analysis

This project uses ydata-profiling to generate comprehensive exploratory data analysis reports.

## Generated Reports

The EDA process generates three HTML reports in the `reports/profiling/` directory:

1. `train_profile.html`: Detailed analysis of the training dataset
2. `test_profile.html`: Detailed analysis of the test dataset
3. `comparison_profile.html`: Comparison between training and test datasets

## Running the Analysis

To generate the reports, run:

```bash
make eda
```

## Report Contents

The profiling reports include:
- Dataset overview (number of variables, observations, etc.)
- Variable analysis (type, missing values, distribution, etc.)
- Correlation analysis
- Missing values analysis
- Statistical description of variables
- Data quality warnings

## Using the Reports

1. Open the generated HTML files in your web browser
2. Use the navigation menu to explore different aspects of the data
3. Pay special attention to:
   - Missing values
   - Correlations between features
   - Distribution of target variable
   - Data quality warnings