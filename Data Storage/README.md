## Data Storage and Maintenance - Canadian Job Market Trends Analysis Project

This folder documents the schema design, storage structure, and maintenance strategy for managing job market datasets in the job_market_trends MongoDB database.

### Objectives

- Centralize and normalize raw and enriched job market data using a flexible document-based database.
- Enable efficient querying and aggregation using MongoDB's aggregation pipeline.
- Support continuous updates and integration of real-time data feeds (job scraping).

### Database: `job_market_trends`

The job_market_trends MongoDB database stores all curated job market data in collections designed for flexible querying, easy updates, and seamless integration with real-time scrapers and dashboards.

### 🗂️ Core Collections

_Schema file_ defines the schema for database job_market_trends and below tables:

1. `labour_force_stats`
- Labour force characteristics by region, gender, age group
- Source: Statistics Canada Table 14-10-0287-01

2. `industry_jobs`
- NAICS industry job counts across years and sectors
- Source: Open Canada Job Bank

3. `job_postings`
- Detailed job postings scraped from LinkedIn or Google Jobs
- Integrates with real time jib search results
- Source: Kaggle

### ⚙️ Maintenance Practices

#### ✅ Ingestion Strategy
- Use `load_data.py` for batch loading.
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
  - _load_data.py_ for ingest.
  - Dashboards (Tableau or MongoDB Charts) for trends and forecasting.
  - APIs for interactive job search and labor market insights.
