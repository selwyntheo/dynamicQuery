#!/usr/bin/env python3
"""
MongoDB Import Script for dataNAV Collection
This script imports the generated JSON data into MongoDB
"""

import json
from pymongo import MongoClient
from datetime import datetime

def import_to_mongodb(json_file_path, connection_string="mongodb://admin:password123@localhost:27017/financial_data?authSource=admin", db_name="financial_data"):
    """
    Import JSON data to MongoDB
    """
    try:
        # Connect to MongoDB with authentication
        client = MongoClient(connection_string)
        db = client[db_name]
        print(f"Connected to MongoDB database: {db_name}")
        
        # Read JSON data
        with open(json_file_path, 'r') as f:
            data = json.load(f)
        
        collection_name = data['collection_name']
        sample_data = data['sample_data']
        
        # Drop collection if it exists
        if collection_name in db.list_collection_names():
            db[collection_name].drop()
            print(f"Dropped existing collection: {collection_name}")
        
        # Create collection and insert data
        collection = db[collection_name]
        
        # Convert date strings back to datetime objects for MongoDB
        for record in sample_data:
            if 'valuationDt' in record:
                record['valuationDt'] = datetime.fromisoformat(record['valuationDt'])
            if 'createdAt' in record:
                record['createdAt'] = datetime.fromisoformat(record['createdAt'])
        
        # Insert data
        result = collection.insert_many(sample_data)
        print(f"Successfully inserted {len(result.inserted_ids)} records")
        
        # Create indexes
        print("Creating indexes...")
        collection.create_index("valuationDt")
        collection.create_index("account")
        collection.create_index("shareClass")
        collection.create_index("eagleEntityId")
        collection.create_index([("account", 1), ("valuationDt", -1)])
        
        print("Collection created and data imported successfully!")
        
        # Display collection info
        total_docs = collection.count_documents({})
        print(f"Total documents in collection: {total_docs}")
        
        # Sample query examples
        print("\n=== Sample Queries ===")
        print("1. Count by share class:")
        pipeline = [
            {"$group": {"_id": "$shareClass", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        for result in collection.aggregate(pipeline):
            print(f"   Share Class {result['_id']}: {result['count']} records")
        
        print("\n2. Average NAV by currency:")
        pipeline = [
            {"$group": {"_id": "$accountBaseCurrency", "avgNAV": {"$avg": "$NAV"}}},
            {"$sort": {"avgNAV": -1}}
        ]
        for result in collection.aggregate(pipeline):
            print(f"   {result['_id']}: {result['avgNAV']:.2f}")
        
        client.close()
        
    except FileNotFoundError:
        print(f"JSON file not found: {json_file_path}")
    except Exception as e:
        print(f"Error importing data: {e}")

def main():
    """
    Main function
    """
    print("=== MongoDB Import for dataNAV Collection ===")
    
    json_file = "/Volumes/D/Ai/python/dataset/dataNAV_sample.json"
    import_to_mongodb(json_file)

if __name__ == "__main__":
    main()
