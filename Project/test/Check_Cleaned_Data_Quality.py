import pandas as pd
from pathlib import Path
from datetime import datetime

def test_employment_projections(csv_path):
    print("Test data quality of Employment Projections dataset")
    try:
        df = pd.read_csv(csv_path)
        print(f"✅ Successfully loaded data from {csv_path}")
    except Exception as e:
        print(f"❌ Failed to load CSV: {e}")
        return

    # 1. Check for missing values
    print("\n=== Missing Values Check ===")
    missing_values = df.isnull().sum()
    if missing_values.sum() == 0:
        print("✅ No missing values found")
    else:
        print("❌ Missing values found:")
        print(missing_values[missing_values > 0])

    # 2. Check for duplicate records
    print("\n=== Duplicate Records Check ===")
    duplicates = df.duplicated()
    if duplicates.sum() == 0:
        print("✅ No duplicate records found")
    else:
        print(f"❌ Found {duplicates.sum()} duplicate records")
        print(df[duplicates].head())

    # 3. Validate year columns are numeric
    print("\n=== Year Columns Validation ===")
    year_columns = [str(year) for year in range(2023, 2034)]
    invalid_years = []
    
    for year in year_columns:
        if year not in df.columns:
            invalid_years.append(year)
            continue
            
        if not pd.api.types.is_numeric_dtype(df[year]):
            invalid_years.append(year)
    
    if not invalid_years:
        print("✅ All year columns contain numeric values")
    else:
        print(f"❌ Issues found in these year columns: {invalid_years}")

    # 4. Basic statistics
    print("\n=== Data Summary ===")
    print(f"Total records: {len(df)}")


def test_labour_market_conditions(csv_path):
    print("\n\nTest data quality of Labour Market Conditions dataset")
    try:
        df = pd.read_csv(csv_path)
        print(f"✅ Successfully loaded data from {csv_path}")
    except Exception as e:
        print(f"❌ Failed to load CSV: {e}")
        return

    # 1. Check for missing values
    print("\n=== Missing Values Check ===")
    missing_values = df.isnull().sum()
    if missing_values.sum() == 0:
        print("✅ No missing values found")
    else:
        print("❌ Missing values found:")
        print(missing_values[missing_values > 0])

    # 2. Check for duplicate records
    print("\n=== Duplicate Records Check ===")
    duplicates = df.duplicated()
    if duplicates.sum() == 0:
        print("✅ No duplicate records found")
    else:
        print(f"❌ Found {duplicates.sum()} duplicate records")
        print(df[duplicates].head())

def test_statcan_by_industry(csv_path):
    print("\n\nTest data quality of StatCan by Industry dataset")
    try:
        df = pd.read_csv(csv_path)
        print(f"✅ Successfully loaded data from {csv_path}")
    except Exception as e:
        print(f"❌ Failed to load CSV: {e}")
        return

    # 1. Missing values check
    print("\n=== Missing Values Check ===")
    missing = df.isnull().sum()
    if missing.sum() == 0:
        print("✅ No missing values found")
    else:
        print("❌ Missing values found:")
        print(missing[missing > 0])

    # 2. Duplicate check
    print("\n=== Duplicate Records Check ===")
    dup = df.duplicated()
    if dup.sum() == 0:
        print("✅ No duplicate records found")
    else:
        print(f"❌ Found {dup.sum()} duplicate records")
        print(df[dup].head())

    # 3. ref_date year range check
    print("\n=== Year Range Check (ref_date) ===")
    invalid_years = df[~df["ref_date"].between(1900, 2025)]
    if invalid_years.empty:
        print("✅ All ref_date values are between 1900 and 2025")
    else:
        print(f"❌ Invalid ref_date values found:\n{invalid_years[['ref_date']].drop_duplicates()}")

    # 4. geo value check
    print("\n=== Geographic Region Check (geo) ===")
    valid_provinces = {
        "Canada", "Newfoundland and Labrador", "Prince Edward Island", "Nova Scotia", "New Brunswick",
        "Quebec", "Ontario", "Manitoba", "Saskatchewan", "Alberta", "British Columbia",
        "Yukon", "Northwest Territories", "Nunavut"
    }
    invalid_geo = df[~df["geo"].isin(valid_provinces)]
    if invalid_geo.empty:
        print("✅ All geo values are valid Canadian regions")
    else:
        print("❌ Invalid geo values found:")
        print(invalid_geo["geo"].drop_duplicates())

    # 5. uom_id and scalar_id numeric check
    print("\n=== Numeric Columns Check (uom_id, scalar_id) ===")
    non_numeric_cols = []
    for col in ["uom_id", "scalar_id"]:
        if not pd.api.types.is_numeric_dtype(df[col]):
            non_numeric_cols.append(col)
    if not non_numeric_cols:
        print("✅ uom_id and scalar_id are numeric")
    else:
        print(f"❌ These columns should be numeric but are not: {non_numeric_cols}")

def test_statcan_labourforce(csv_path):
    print("\n\nTest data quality of StatCan Labourforce dataset")
    try:
        df = pd.read_csv(csv_path)
        print(f"✅ Successfully loaded data from {csv_path}")
    except Exception as e:
        print(f"❌ Failed to load CSV: {e}")
        return

    # 1. Missing values
    print("\n=== Missing Values Check ===")
    missing = df.isnull().sum()
    if missing.sum() == 0:
        print("✅ No missing values found")
    else:
        print("❌ Missing values found:")
        print(missing[missing > 0])

    # 2. Duplicate records
    print("\n=== Duplicate Records Check ===")
    dup = df.duplicated()
    if dup.sum() == 0:
        print("✅ No duplicate records found")
    else:
        print(f"❌ Found {dup.sum()} duplicate records")
        print(df[dup].head())

    # 3. ref_date format check
    print("\n=== ref_date Format Check ===")
    def is_valid_date_format(val):
        try:
            datetime.strptime(val, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    invalid_dates = df[~df["ref_date"].astype(str).apply(is_valid_date_format)]
    if invalid_dates.empty:
        print("✅ All ref_date values follow 'YYYY-MM-DD' format")
    else:
        print("❌ Invalid ref_date format found:")
        print(invalid_dates["ref_date"].drop_duplicates())

    # 4. geo value check
    print("\n=== Geographic Region Check (geo) ===")
    valid_provinces = {
        "Canada", "Newfoundland and Labrador", "Prince Edward Island", "Nova Scotia", "New Brunswick",
        "Quebec", "Ontario", "Manitoba", "Saskatchewan", "Alberta", "British Columbia",
        "Yukon", "Northwest Territories", "Nunavut"
    }
    invalid_geo = df[~df["geo"].isin(valid_provinces)]
    if invalid_geo.empty:
        print("✅ All geo values are valid Canadian regions")
    else:
        print("❌ Invalid geo values found:")
        print(invalid_geo["geo"].drop_duplicates())

    # 5. uom_id and scalar_id numeric check
    print("\n=== Numeric Columns Check (uom_id, scalar_id) ===")
    non_numeric = [col for col in ["uom_id", "scalar_id"] if not pd.api.types.is_numeric_dtype(df[col])]
    if not non_numeric:
        print("✅ uom_id and scalar_id are numeric")
    else:
        print(f"❌ These columns should be numeric but are not: {non_numeric}")

if __name__ == "__main__":
    base_path = Path(__file__).resolve().parents[2] / "Data Collection"

    # First file: Employment Projections
    ep_path = base_path / "CLEANED_employment_projections_2024_2033.csv"
    if not ep_path.exists():
        print(f"❌ Error: File not found at {ep_path}")
    else:
        test_employment_projections(ep_path)

    # Second file: Labour Market Conditions
    lmc_path = base_path / "CLEANED_labour_market_conditions_2021_2023.csv"
    if not lmc_path.exists():
        print(f"\n❌ Error: File not found at {lmc_path}")
    else:
        test_labour_market_conditions(lmc_path)
        
    # Third file: StatCan by Industry
    sci_path = base_path / "CLEANED_StatCan_byIndustry.csv"
    if not sci_path.exists():
        print(f"\n❌ Error: File not found at {sci_path}")
    else:
        test_statcan_by_industry(sci_path)
        
    # Fourth file: StatCan Labourforce
    lf_path = base_path / "CLEANED_StatCan_Labourforce.csv"
    if not lf_path.exists():
        print(f"\n❌ Error: File not found at {lf_path}")
    else:
        test_statcan_labourforce(lf_path)
