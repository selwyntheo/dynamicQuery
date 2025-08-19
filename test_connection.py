#!/usr/bin/env python3
"""
Simple MongoDB connection test
"""

from pymongo import MongoClient
import sys

def test_connections():
    """
    Test various connection strings
    """
    
    # Test cases
    test_cases = [
        {
            "name": "Admin with authSource=admin", 
            "uri": "mongodb://admin:password123@localhost:27017/?authSource=admin"
        },
        {
            "name": "Admin direct to financial_data", 
            "uri": "mongodb://admin:password123@localhost:27017/financial_data?authSource=admin"
        },
        {
            "name": "Financial user with authSource=financial_data", 
            "uri": "mongodb://financial_user:financial_pass@localhost:27017/financial_data?authSource=financial_data"
        },
        {
            "name": "No auth (should fail)", 
            "uri": "mongodb://localhost:27017/financial_data"
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
