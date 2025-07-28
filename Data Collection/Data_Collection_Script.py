import os
import time
import pandas as pd
import requests
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Setup Base Folder
base_dir = os.path.join(os.getcwd(), "Data Collection")
os.makedirs(base_dir, exist_ok=True)

# Labour Force Stats
def run_time_series_download():
    ref_periods = [
        {"month": "12", "year": "2021"},
        {"month": "12", "year": "2022"},
        {"month": "12", "year": "2023"},
        {"month": "12", "year": "2024"},
        {"month": (datetime.today().replace(day=1) - timedelta(days=1)).strftime("%m"), "year": "2025"}
    ]
    temp_dir = os.path.join(base_dir, "temp_time")
    os.makedirs(temp_dir, exist_ok=True)

    options = Options()
    options.add_argument('--headless')
    options.add_experimental_option('prefs', {'download.default_directory': temp_dir})

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 15)

    for period in ref_periods:
        month, year = period['month'], period['year']
        url = f"https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1410028703&pickMembers%5B0%5D=3.1&pickMembers%5B1%5D=4.1&cubeTimeFrame.startMonth={month}&cubeTimeFrame.startYear={year}&referencePeriods={year}{month}01%2C{year}{month}01"
        driver.get(url)
        try:
            wait.until(EC.element_to_be_clickable((By.ID, "downloadOverlayLink"))).click()
            wait.until(EC.element_to_be_clickable((By.ID, "downloadDbLoading"))).click()
            print(f"Time-series download for {year}-{month}")
            time.sleep(10)
        except Exception as e:
            print(f"Failed for {year}-{month}: {e}")

    driver.quit()

    # Merge and save directly under base_dir
    files = [f for f in os.listdir(temp_dir) if f.endswith('.csv')]
    dfs = [pd.read_csv(os.path.join(temp_dir, f)) if i == 0 else pd.read_csv(os.path.join(temp_dir, f)).iloc[1:] for i, f in enumerate(files)]
    final_df = pd.concat(dfs, ignore_index=True)
    final_path = os.path.join(base_dir, "StatCan_Labourforce.csv")
    final_df.to_csv(final_path, index=False)
    print(f"Merged CSV: {final_path}")
    for f in files:
        os.remove(os.path.join(temp_dir, f))
    os.rmdir(temp_dir)

# Labour force characteristics by industry
def run_geography_download():
    geographies = [{"id": f"1.{i}", "name": name} for i, name in enumerate([
        "Canada", "Newfoundland and Labrador", "Prince Edward Island", "Nova Scotia",
        "New Brunswick", "Quebec", "Ontario", "Manitoba", "Saskatchewan",
        "Alberta", "British Columbia"
    ], start=1)]

    temp_dir = os.path.join(base_dir, "temp_geo")
    os.makedirs(temp_dir, exist_ok=True)

    options = Options()
    options.add_argument('--headless')
    options.add_experimental_option('prefs', {'download.default_directory': temp_dir})

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 15)

    for geo in geographies:
        geo_num = geo['id'].split('.')[1]
        url = f"https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1410002301&pickMembers%5B0%5D=1.{geo_num}"
        driver.get(url)
        try:
            wait.until(EC.element_to_be_clickable((By.ID, "downloadOverlayLink"))).click()
            wait.until(EC.element_to_be_clickable((By.ID, "downloadDbLoading"))).click()
            print(f"Geography download for {geo['name']}")
            time.sleep(10)
        except Exception as e:
            print(f"Failed for {geo['name']}: {e}")

    driver.quit()

    # Merge and save directly under base_dir
    files = [f for f in os.listdir(temp_dir) if f.endswith('.csv')]
    dfs = [pd.read_csv(os.path.join(temp_dir, f)) if i == 0 else pd.read_csv(os.path.join(temp_dir, f)).iloc[1:] for i, f in enumerate(files)]
    final_df = pd.concat(dfs, ignore_index=True)
    final_path = os.path.join(base_dir, "StatCan_byIndustry.csv")
    final_df.to_csv(final_path, index=False)
    print(f"Merged geography CSV: {final_path}")
    for f in files:
        os.remove(os.path.join(temp_dir, f))
    os.rmdir(temp_dir)

# Direct API Downloads
def run_api_downloads():
    resources = [
        {
            "name": "employment_projections_2024_2033.csv",
            "url": "https://open.canada.ca/data/dataset/e80851b8-de68-43bd-a85c-c72e1b3a3890/resource/da1135c5-a1df-4a07-a81e-de308ae6cce6/download/employment_emploi_2024_2033_noc2021.csv"
        },
        {
            "name": "labour_market_conditions_2021_2023.csv",
            "url": "https://open.canada.ca/data/dataset/e80851b8-de68-43bd-a85c-c72e1b3a3890/resource/ff795791-0728-4dcf-8fdd-d7ba9e1210b8/download/rlmc_crmt_2021_2023_noc2021.csv"
        }
    ]

    for res in resources:
        path = os.path.join(base_dir, res["name"])
        try:
            resp = requests.get(res["url"])
            resp.raise_for_status()
            with open(path, "wb") as f:
                f.write(resp.content)
            print(f"API download complete: {res['name']}")
        except Exception as e:
            print(f"Failed to download {res['name']}: {e}")

# Run All 
if __name__ == "__main__":
    print("Starting full data collection...")
    run_time_series_download()
    run_geography_download()
    run_api_downloads()
    print("All tasks completed. CSVs are located in:", base_dir)