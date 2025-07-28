import csv
import os
from pymongo import MongoClient

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["job_market_trends"]

# List of collection names to clear
collections_to_clear = ["labour_force_stats", "employment_stats", "employment_forecast", "market_condition"]

# Delete all documents from each collection
for coll_name in collections_to_clear:
    result = db[coll_name].delete_many({})
    print(f"Cleared {result.deleted_count} documents from '{coll_name}'")


# Base path to the CSV folder (outside current folder)
base_path = os.path.join(".", "CLEANED_DATA")

# Mapping of collections to their CSV file paths
collection_csv_map = {
    "labour_force_stats": os.path.join(base_path, "CLEANED_StatCan_Labourforce.csv"),
    "employment_stats": os.path.join(base_path, "CLEANED_StatCan_byIndustry.csv"),
    "employment_forecast": os.path.join(base_path, "CLEANED_employment_projections_2024_2033.csv"),
    "market_condition": os.path.join(base_path, "CLEANED_labour_market_conditions_2021_2023.csv")
}

def insert_csv_to_collection(collection_name, csv_file):
    collection = db[collection_name]
    with open(csv_file, newline='', encoding='latin-1') as file:
        reader = csv.DictReader(file)
        data = list(reader)
        if data:
            collection.insert_many(data)
            print(f"Inserted {len(data)} records into '{collection_name}'")
        else:
            print(f"No data found in '{csv_file}'")

# Load each CSV into its respective collection
for coll, path in collection_csv_map.items():
    insert_csv_to_collection(coll, path)