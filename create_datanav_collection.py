#!/usr/bin/env python3
"""
Script to create and populate MongoDB collection for dataNAV table
with all specified fields and test data.
"""

from pymongo import MongoClient
from faker import Faker
import random
from datetime import datetime, timedelta
from decimal import Decimal
import uuid

# Initialize Faker for generating test data
fake = Faker()

def connect_to_mongodb(connection_string="mongodb://admin:password123@localhost:27017/", db_name="financial_data"):
    """
    Connect to MongoDB and return the database instance
    """
    try:
        client = MongoClient(connection_string)
        db = client[db_name]
        print(f"Connected to MongoDB database: {db_name}")
        return db, client
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None, None

def generate_sample_nav_data(num_records=100):
    """
    Generate sample data for dataNAV collection
    """
    data = []
    
    # Sample data pools
    share_classes = ['A', 'B', 'C', 'I', 'R', 'Z']
    currencies = ['USD', 'EUR', 'GBP', 'JPY', 'CAD', 'AUD', 'CHF']
    account_types = ['EQUITY', 'BOND', 'MIXED', 'MONEY_MARKET', 'ALTERNATIVE']
    banks = ['Goldman Sachs', 'JP Morgan', 'Bank of America', 'Wells Fargo', 'Citibank', 'HSBC']
    regions = ['North America', 'Europe', 'Asia Pacific', 'Latin America', 'Middle East']
    
    for i in range(num_records):
        # Generate random dates within the last year
        valuation_date = fake.date_between(start_date='-1y', end_date='today')
        
        record = {
            'valuationDt': valuation_date,
            'shareClass': random.choice(share_classes),
            'account': f"ACC{fake.random_number(digits=8)}",
            'userBank': random.choice(banks),
            'accountBaseCurrency': random.choice(currencies),
            'accountName': f"{fake.company()} {random.choice(account_types)} Fund",
            'acctBasis': random.choice(['GAAP', 'IFRS', 'STAT', 'TAX']),
            'capstock': round(random.uniform(1000000, 100000000), 2),
            'chartOfAccounts': f"COA_{fake.random_number(digits=4)}",
            'distribution': round(random.uniform(0, 1000000), 2),
            'eagleAcctBasis': random.choice(['GAAP', 'IFRS', 'STAT']),
            'eagleClass': random.choice(share_classes),
            'eagleEntityId': f"ENT_{fake.random_number(digits=6)}",
            'eagleRegion': random.choice(regions),
            'entityBaseCurrency': random.choice(currencies),
            'incomeDistribution': round(random.uniform(0, 500000), 2),
            'isComposite': random.choice([True, False]),
            'isMulticlass': random.choice([True, False]),
            'isPrimaryBasis': random.choice([True, False]),
            'isSleeve': random.choice([True, False]),
            'ltcglDistribution': round(random.uniform(0, 200000), 2),
            'mergerPic': random.choice([None, f"MERGER_{fake.random_number(digits=4)}"]),
            'parentAccount': f"PARENT_{fake.random_number(digits=6)}" if random.choice([True, False]) else None,
            'settleCapstock': round(random.uniform(1000000, 100000000), 2),
            'settleDistribution': round(random.uniform(0, 1000000), 2),
            'shareClassCurrency': random.choice(currencies),
            'NAV': round(random.uniform(10, 1000), 4),
            'capstockRedsPay': round(random.uniform(0, 5000000), 2),
            'capstockSubsRec': round(random.uniform(0, 5000000), 2),
            'dailyDistribution': round(random.uniform(0, 10000), 2),
            'dailyYeild': round(random.uniform(0, 0.1), 6),
            'distributionPayable': round(random.uniform(0, 100000), 2),
            'netAssets': round(random.uniform(10000000, 1000000000), 2),
            'redemptionBalance': round(random.uniform(0, 10000000), 2),
            'redemptionPayBase': round(random.uniform(0, 5000000), 2),
            'redemptionPayLocal': round(random.uniform(0, 5000000), 2),
            'reinvestmentDistribution': round(random.uniform(0, 500000), 2),
            'settledShares': round(random.uniform(100000, 10000000), 0),
            'sharesOutstanding': round(random.uniform(100000, 10000000), 0),
            'subscriptionBalance': round(random.uniform(0, 10000000), 2),
            'subscriptionRecBase': round(random.uniform(0, 5000000), 2),
            'subscriptionRecLocal': round(random.uniform(0, 5000000), 2),
            # Add metadata
            'createdAt': datetime.utcnow(),
            'recordId': str(uuid.uuid4())
        }
        
        data.append(record)
    
    return data

def create_collection_and_insert_data(db, collection_name="dataNAV", num_records=100):
    """
    Create the collection and insert sample data
    """
    try:
        # Drop collection if it exists (for testing purposes)
        if collection_name in db.list_collection_names():
            db[collection_name].drop()
            print(f"Dropped existing collection: {collection_name}")
        
        # Create the collection
        collection = db[collection_name]
        
        # Generate sample data
        print(f"Generating {num_records} sample records...")
        sample_data = generate_sample_nav_data(num_records)
        
        # Insert the data
        result = collection.insert_many(sample_data)
        print(f"Successfully inserted {len(result.inserted_ids)} records into {collection_name}")
        
        # Create indexes for better performance
        print("Creating indexes...")
        collection.create_index("valuationDt")
        collection.create_index("account")
        collection.create_index("shareClass")
        collection.create_index("eagleEntityId")
        collection.create_index([("account", 1), ("valuationDt", -1)])
        
        print("Indexes created successfully")
        
        return collection
        
    except Exception as e:
        print(f"Error creating collection and inserting data: {e}")
        return None

def display_sample_records(collection, num_samples=5):
    """
    Display sample records from the collection
    """
    print(f"\n--- Sample Records from {collection.name} ---")
    
    sample_records = list(collection.find().limit(num_samples))
    
    for i, record in enumerate(sample_records, 1):
        print(f"\nRecord {i}:")
        for key, value in record.items():
            if key != '_id':  # Skip MongoDB's internal ID
                print(f"  {key}: {value}")
    
    # Display collection stats
    total_records = collection.count_documents({})
    print(f"\nCollection Statistics:")
    print(f"  Total Records: {total_records}")
    print(f"  Collection Name: {collection.name}")
    
    # Display unique values for some key fields
    unique_share_classes = collection.distinct("shareClass")
    unique_currencies = collection.distinct("accountBaseCurrency")
    unique_banks = collection.distinct("userBank")
    
    print(f"  Unique Share Classes: {unique_share_classes}")
    print(f"  Unique Currencies: {unique_currencies}")
    print(f"  Unique Banks: {unique_banks}")

def main():
    """
    Main function to execute the MongoDB setup
    """
    print("=== MongoDB dataNAV Collection Setup ===")
    
    # Connect to MongoDB
    db, client = connect_to_mongodb()
    if not db:
        print("Failed to connect to MongoDB. Please ensure MongoDB is running.")
        return
    
    try:
        # Create collection and insert data
        collection = create_collection_and_insert_data(db, "dataNAV", 100)
        
        if collection:
            # Display sample records
            display_sample_records(collection)
            
            print("\n=== Setup Complete ===")
            print("You can now query the dataNAV collection using MongoDB commands or tools")
            print("\nExample queries:")
            print("1. Find all records for a specific date:")
            print("   db.dataNAV.find({'valuationDt': ISODate('2024-01-01')})")
            print("\n2. Find records by share class:")
            print("   db.dataNAV.find({'shareClass': 'A'})")
            print("\n3. Find records with NAV greater than 100:")
            print("   db.dataNAV.find({'NAV': {$gt: 100}})")
            
    except Exception as e:
        print(f"Error in main execution: {e}")
    
    finally:
        if client:
            client.close()
            print("\nMongoDB connection closed.")

if __name__ == "__main__":
    main()
