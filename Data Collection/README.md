## Data Collection - Canadian Job Market Trends Analysis Project

This folder contains the scripts and automation tools used to fetch datasets for the Canadian Job Market Trends analysis.

### Purpose

- Scrape real-time job postings from Job Bank Canada across all provinces and territories.
- Extract structured job attributes such as title, employer, location, salary, and posting date.
- Tag each job with the full province name for downstream analysis.
- Store raw, unmodified data into the job_market_trends MongoDB database with deduplication support.

### 🗂️ Contents

Below are the datasets downloaded/fetched using *Data_Collection_Script.py*:

- StatCan Labourforce.csv
- StatCan_bylndustry.csv
- employment_projections_2024_2033.csv
- labour market conditions 2021 2023.csv
- job_postings.zip


### Approaches

**Historical Data**
1. Download official CSV datasets from Government of Canada open data sources.
2. Save them locally for ingestion into downstream systems.

**Real-Time Data**
1. Use Selenium and Selenium Wire to scrape dynamically loaded job postings from Job Bank Canada.
2. Parse HTML content using BeautifulSoup to extract job-level details.
3. Store raw data into MongoDB (job_postings collection), using upsert to avoid duplicates.
4. Raw fields such as date and salary are stored as-is; no data cleaning, parsing, or normalization is performed in this stage.