## Data Storage and Maintenance - Canadian Job Market Trends Analysis Project

This folder documents the schema design, storage structure, and maintenance strategy for managing job market datasets in the job_market_trends MongoDB database.

### Objectives

- Centralize and normalize raw and enriched job market data using a flexible document-based database.
- Enable efficient querying and aggregation using MongoDB's aggregation pipeline.
- Support continuous updates and integration of real-time data feeds (job scraping).

### Database: `job_market_trends`

The job_market_trends MongoDB database stores all curated job market data in collections designed for flexible querying, easy updates, and seamless integration with real-time scrapers and dashboards.

### 🗂️ Core Collections

Database _job_market_trends_ 

1. _labour_force_stats_ – Monthly Canadian labour force metrics including employment, unemployment, and participation rates by province, age, and gender.

2. _industry_employment_ – Employment trends by NAICS industry and province, supporting sector-level and regional analysis.

3. _employment_forecast_ – Projected job openings and workforce demand across occupations in Canada for 2025–2033.

4. _market_condition_ – Assessment of recent labour market conditions (2021–2023), indicating occupational shortages, surpluses, or balance.

5. _job_postings_ – Real-time Job Bank postings with details on job title, location, employer, wages, and employment type.

### ⚙️ Maintenance Practices

#### ✅ Ingestion Strategy
- Use `Data_Loading_Script.py` for batch loading.
- Column normalization and null checks handled before insert.
- Timestamp columns converted appropriately.

#### 🔄 Update Schedule
- Monthly: Labour Force & Industry Jobs (from StatsCan, Open Canada).
- Daily/Weekly:Job postings via automated scraper.
- Monthly archiving of API data.
- Automated backups.

#### 🧹 Data Hygiene
- De-duplication using IDs.
- Missing values filled with defaults or flagged for review.
- Normalization ensures analytical consistency.

#### 🛡️ Backups
- Weekly dump using mongodump to backups.
- Retain minimum 3 historical snapshots.

### 📤 Integration Points

- Data is used by:
  - Dashboards (Tableau ) for trends and forecasting.
  - APIs for interactive job search and labor market insights.
