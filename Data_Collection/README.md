## Data Collection - Canadian Job Market Trends Analysis Project

This folder contains the scripts and automation tools used to fetch datasets for the Canadian Job Market Trends analysis.

### Purpose

- Cleaning datasets by fixing missing, null or error values.
- Standardize raw data formats for loading into the job_market_trends database.
- Maintain reproducibility and versioning of collected data files.

### 🗂️ Contents

Below are the datasets downloaded/fetched using *Data_Collection_Script.py*:

- StatCan Labourforce.csv
- StatCan_bylndustry.csv
- employment_projections_2024_2033.csv
- labour market conditions 2021 2023.csv
- job_postings.zip


### Approaches

**Historical Data**
1. Download CSV datasets.
2. Clean data using pandas.
3. Load into SQL Server via pyodbc.

**Real-Time Data**
1. Fetch data using API calls - Python’s requests.
2. Parse responses into structured tables.
3. Merge with historical data using pandas/SQL.
