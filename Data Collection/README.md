## Data Collection - Canadian Job Market Trends Analysis Project

This folder contains the scripts and automation tools used to prepare datasets for the Canadian Job Market Trends analysis.

### Purpose

- Cleaning datasets by fixing missing, null or error values.
- Standardize raw data formats for loading into the job_market_trends database.
- Maintain reproducibility and versioning of collected data files.

### 🗂️ Contents

Below are the datasets cleaned using *Data_Cleaning_Script.py*:

- CLEANED_industry_jobs.zip
- CLEANED_job_postings.csv
- CLEANED_labour_force_stats.csv

### Approaches

**Historical Data**
1. Download CSV datasets.
2. Clean data using pandas.
3. Load into SQL Server via pyodbc.

**Real-Time Data**
1. Fetch data using API calls - Python’s requests.
2. Parse responses into structured tables.
3. Merge with historical data using pandas/SQL.
