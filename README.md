# SENG8081-S25-Team1
## Contibutors
* Anuroopa Balachandran
* Bin Hu
* Ce Chen
* Xiaoman Yang

## Project
### Canadian Job Market Trends Analaysis 

#### Abstract
In today's dynamic economic landscape, understanding job market trends is critical for policymakers, businesses, and job seekers. This project outlines solution for analyzing Canadian job market trends by integrating real-time data from government APIs with curated historical datasets. The system tracks key metrics such as employment rates, industry growth, regional demand, and skill requirements to analyze and visualize employment trends, job posting dynamics, sectoral shifts, and unemployment patterns across Canadian provinces, with the goal of identifying economic signals, emerging industries, and potential indicators of recession or recovery.

#### Introduction
This project conducts a comprehensive analysis of Canada’s job market, focusing on employment trends, regional disparities, industry growth, and emerging skill demands. Objectives include:
* Identifying high-growth sectors and declining industries.
* Analyzing regional employment hotspots.
* Predicting future skill requirements using historical data.
* Building an interactive dashboard for policymakers and job seekers.

#### System Components
* Python Backend: Data ingestion, cleaning, and analysis.
* Real-Time API: Statistics Canada Labour Force Survey API.
* Historical Dataset: Government of Canada Open Data Portal.
* Custom Web Scraper: Collects live job postings from Canada Job Bank.
* Database: NoSQL storage using MongoDB.
* Dashboard: Tableau (connected via MongoDB BI Connector).
  
#### Data Research and Integration

##### Sources

* https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1410028703
* https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1410002301
* https://open.canada.ca/data/en/dataset/e80851b8-de68-43bd-a85c-c72e1b3a3890/resource/da1135c5-a1df-4a07-a81e-de308ae6cce6
* https://open.canada.ca/data/en/dataset/e80851b8-de68-43bd-a85c-c72e1b3a3890/resource/ff795791-0728-4dcf-8fdd-d7ba9e1210b8
* https://www.jobbank.gc.ca/jobsearch/

#### Data Collection

##### Purpose

- Cleaning datasets by fixing missing, null or error values.
- Standardize raw data formats for loading into the job_market_trends database.
- Maintain reproducibility and versioning of collected data files.
- Scrape live job postings using a custom Python scraper.

##### Approaches

1. Historical Data
    1. Download official CSV datasets from Government of Canada open data sources.
    2. Save them locally for ingestion into downstream systems.
    3. Real-Time Data

2. Real-Time Data
    1. Use Selenium and Selenium Wire to scrape dynamically loaded job postings from Job Bank Canada.
    2. Parse HTML content using BeautifulSoup to extract job-level details.
    3. Store raw data into MongoDB (job_postings collection), using upsert to avoid duplicates.
    4. Raw fields such as date and salary are stored as-is; no data cleaning, parsing, or normalization is performed in this stage.

#### Data Storage

Data Storage: _MongoDB_

##### Schema: 

Database: _job_market_trends_ 

Collections: 

1. _labour_force_stats_ – Monthly Canadian labour force metrics including employment, unemployment, and participation rates by province, age, and gender.

2. _industry_employment_ – Employment trends by NAICS industry and province, supporting sector-level and regional analysis.

3. _employment_forecast_ – Projected job openings and workforce demand across occupations in Canada for 2025–2033.

4. _market_condition_ – Assessment of recent labour market conditions (2021–2023), indicating occupational shortages, surpluses, or balance.

5. _job_postings_ – Real-time Job Bank postings with details on job title, location, employer, wages, and employment type.

#### Data Quality

##### Overview

This module performs automated quality validation on all `.csv` files in the project’s dataset directories. It ensures that each dataset meets basic quality standards before further processing or analysis.

##### Checks Performed

- **Empty File Check**: Skips files that are completely empty.
- **Missing Values**: Detects nulls, NaNs, or empty string fields.
- **Duplicate Rows**: Flags rows that are exact duplicates.
- **Blank Columns**: Identifies columns with only missing/blank values.
- **Whitespace Trimming**: Ensures no extra spaces in string fields.
- **Invalid Encodings**: Ensures data is in UTF-8 and contains valid characters.
- **Column Type Consistency**: Validates if columns have consistent types.

##### Output

A report is generated for each file scanned:
- **Location**: Saved as `data_quality_report.html` in the root or script directory.
- **Content Includes**:
  - Total Records Count
  - Number of Records Passed and Failed
  - Summary Table with Row-wise Error Info (if any)
  - ✅ `ALL PASS` indicator if no failures
  - ❌ `X FAILED` indicator if errors are found
  
#### Data Analysis and Visualization
This section examines Canada's labor market dynamics through visualizations created with Tableau. 

##### Purpose of Visualization

The goal of the visualization phase is to:  
- Present **historical trends** in employment and labour force participation.  
- Highlight **regional and sector-based job demand** using vacancies and wages.  
- Show **real-time hiring trends** from Job Bank postings.  
- Provide **forward-looking projections (2025–2033)** to identify emerging skill gaps.  

##### Visualization Tool

- **Tableau**
  - Interactive KPIs and charts for employment trends, job vacancies, and real-time postings.  
  - Connected via **MongoDB BI Connector** to allow for dynamic data refresh.
  - Cretaed two dashboards - one with generalized labour statistics trend and another with occupation/industry specific trend.

The analysis reveals critical insights that are valuable for policymakers, educators, and business stakeholders, supporting evidence-based planning and strategic decisions.

#### DevOps

- DevOps approach focused on automation, integration.
- Local pipeline to automate data ingestion and transformation.
- GitHub for Version control, pull request management, and branching workflows.
- Apscheduler for job scheduling orchestrates scraping and download tasks at scheduled using cron job.
- Code Versioning & Collaboration









