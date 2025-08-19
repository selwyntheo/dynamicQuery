#!/usr/bin/env python3
"""
Script to generate sample dataNAV data structure and save as JSON
This can be used to understand the data structure and import into MongoDB later
"""

import json
from faker import Faker
import random
from datetime import datetime, timedelta
import uuid

# Initialize Faker for generating test data
fake = Faker()

def generate_sample_nav_data(num_records=20):
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
            'valuationDt': valuation_date.isoformat(),
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
            'createdAt': datetime.utcnow().isoformat(),
            'recordId': str(uuid.uuid4())
        }
        
        data.append(record)
    
    return data

def create_json_output():
    """
    Generate sample data and save to JSON file
    """
    print("Generating sample dataNAV records...")
    
    # Generate sample data
    sample_data = generate_sample_nav_data(20)
    
    # Create the collection structure
    collection_data = {
        "collection_name": "dataNAV",
        "description": "MongoDB collection for NAV (Net Asset Value) financial data",
        "total_records": len(sample_data),
        "fields": [
            "valuationDt", "shareClass", "account", "userBank", "accountBaseCurrency",
            "accountName", "acctBasis", "capstock", "chartOfAccounts", "distribution",
            "eagleAcctBasis", "eagleClass", "eagleEntityId", "eagleRegion", "entityBaseCurrency",
            "incomeDistribution", "isComposite", "isMulticlass", "isPrimaryBasis", "isSleeve",
            "ltcglDistribution", "mergerPic", "parentAccount", "settleCapstock", "settleDistribution",
            "shareClassCurrency", "NAV", "capstockRedsPay", "capstockSubsRec", "dailyDistribution",
            "dailyYeild", "distributionPayable", "netAssets", "redemptionBalance", "redemptionPayBase",
            "redemptionPayLocal", "reinvestmentDistribution", "settledShares", "sharesOutstanding",
            "subscriptionBalance", "subscriptionRecBase", "subscriptionRecLocal"
        ],
        "sample_data": sample_data
    }
    
    # Save to JSON file
    with open('/Volumes/D/Ai/python/dataset/dataNAV_sample.json', 'w') as f:
        json.dump(collection_data, f, indent=2, default=str)
    
    print(f"Sample data saved to dataNAV_sample.json")
    print(f"Generated {len(sample_data)} sample records")
    
    # Display first few records
    print("\n--- Sample Records ---")
    for i, record in enumerate(sample_data[:3], 1):
        print(f"\nRecord {i}:")
        for key, value in record.items():
            print(f"  {key}: {value}")
    
    return collection_data

def main():
    """
    Main function to generate sample data
    """
    print("=== dataNAV Collection Data Generator ===")
    
    try:
        collection_data = create_json_output()
        
        print("\n=== Generation Complete ===")
        print("Files created:")
        print("1. dataNAV_sample.json - Sample data in JSON format")
        print("2. create_datanav_collection.py - MongoDB setup script")
        
        print("\nTo use with MongoDB:")
        print("1. Ensure MongoDB is running")
        print("2. Run: python create_datanav_collection.py")
        print("3. Or import the JSON data manually into MongoDB")
        
        print(f"\nCollection contains {len(collection_data['fields'])} fields:")
        for field in collection_data['fields']:
            print(f"  - {field}")
            
    except Exception as e:
        print(f"Error generating data: {e}")

if __name__ == "__main__":
    main()
