import csv
import os
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")

# Database name
db_name = "job_market_trends"

# NOTE by c.c, no need to check, or move to main(), otherwise will occur an error here
# # Check if database exists
# if db_name in client.list_database_names():
#     print(f"Database '{db_name}' already exists.")
# else:
#     print(f"Creating database '{db_name}'...")

# Use the database
db = client[db_name]

# Base path to the CSV folder (outside current folder)
base_path = os.path.join("..", "Data_Collection")

# Mapping of collections to their CSV file paths
collection_csv_map = {
    "labour_force_stats": os.path.join(base_path, "StatCan_Labourforce.csv"),
    "employment_stats": os.path.join(base_path, "StatCan_byIndustry.csv"),
    "employment_forecast": os.path.join(base_path, "employment_projections_2024_2033.csv"),
    "market_condition": os.path.join(base_path, "labour_market_conditions_2021_2023.csv")
}


def insert_csv_to_collection(collection_name, csv_file):
    collection = db[collection_name]
    with open(csv_file, newline='', encoding='latin-1') as file:
        reader = csv.DictReader(file)
        inserted_count = 0
        for row in reader:
            result = collection.update_one(
                row,
                {"$set": row},
                upsert=True
            )
            if result.upserted_id or result.modified_count > 0:
                inserted_count += 1
        print(f"Upserted {inserted_count} records into '{collection_name}'")


def main():
    # Load each CSV into its respective collection
    for coll, path in collection_csv_map.items():
        insert_csv_to_collection(coll, path)
