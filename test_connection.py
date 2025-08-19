#!/usr/bin/env python3
"""
Simple MongoDB connection test
Secure version using environment variables
"""

from pymongo import MongoClient
import os
import sys

def get_mongo_credentials():
    """Get MongoDB credentials from environment variables"""
    return {
        'username': os.getenv('MONGO_USERNAME', 'admin'),
        'password': os.getenv('MONGO_PASSWORD', 'password123'),
        'database': os.getenv('MONGO_DATABASE_NAME', 'financial_data'),
        'host': 'localhost',
        'port': 27017
    }

def test_connections():
    """
    Test various connection strings
    """
    
    creds = get_mongo_credentials()
    
    # Test cases
    test_cases = [
        {
            "name": f"Admin with authSource=admin (User: {creds['username']})", 
            "uri": f"mongodb://{creds['username']}:{creds['password']}@{creds['host']}:{creds['port']}/?authSource=admin"
        },
        {
            "name": f"Admin direct to {creds['database']} (User: {creds['username']})", 
            "uri": f"mongodb://{creds['username']}:{creds['password']}@{creds['host']}:{creds['port']}/{creds['database']}?authSource=admin"
        },
        {
            "name": "No auth (should fail)", 
            "uri": f"mongodb://{creds['host']}:{creds['port']}/{creds['database']}"
        }
    ]
    
    for test_case in test_cases:
        print(f"\nTesting: {test_case['name']}")
        print(f"URI: {test_case['uri']}")
        
        try:
            client = MongoClient(test_case['uri'], serverSelectionTimeoutMS=5000)
            db = client['financial_data']
            
            # Test basic operations
            collections = db.list_collection_names()
            print(f"✅ SUCCESS - Collections: {collections}")
            
            # Test read access
            if 'dataNAV' in collections:
                count = db.dataNAV.count_documents({})
                print(f"✅ dataNAV records: {count}")
            
            client.close()
            
        except Exception as e:
            print(f"❌ FAILED - Error: {e}")

if __name__ == "__main__":
    print("=== MongoDB Connection Test ===")
    test_connections()
