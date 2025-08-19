#!/usr/bin/env python3
"""
Working MongoDB connection example
Since PyMongo authentication has issues, this shows how to query via subprocess
"""

import subprocess
import json

def query_mongodb_via_shell():
    """
    Query MongoDB using the shell command
    """
    print("=== MongoDB Query via Shell ===")
    
    # Query 1: Count all records
    cmd1 = [
        "docker", "exec", "financial_data_mongodb",
        "mongosh", "-u", "admin", "-p", "password123",
        "--authenticationDatabase", "admin", "financial_data",
        "--eval", "print(db.dataNAV.countDocuments({}))", "--quiet"
    ]
    
    result = subprocess.run(cmd1, capture_output=True, text=True)
    total_records = result.stdout.strip()
    print(f"Total records in dataNAV collection: {total_records}")
    
    # Query 2: Find records by share class
    cmd2 = [
        "docker", "exec", "financial_data_mongodb",
        "mongosh", "-u", "admin", "-p", "password123",
        "--authenticationDatabase", "admin", "financial_data",
        "--eval", "db.dataNAV.find({shareClass: 'A'}).forEach(function(doc) { print(JSON.stringify({account: doc.account, NAV: doc.NAV, currency: doc.accountBaseCurrency})); })", "--quiet"
    ]
    
    result = subprocess.run(cmd2, capture_output=True, text=True)
    print(f"\nShare Class A records:")
    for line in result.stdout.strip().split('\n'):
        if line.strip():
            print(f"  {line}")
    
    # Query 3: Aggregation example
    cmd3 = [
        "docker", "exec", "financial_data_mongodb",
        "mongosh", "-u", "admin", "-p", "password123",
        "--authenticationDatabase", "admin", "financial_data",
        "--eval", """
        db.dataNAV.aggregate([
          {$group: {_id: '$accountBaseCurrency', totalAssets: {$sum: '$netAssets'}, count: {$sum: 1}}},
          {$sort: {totalAssets: -1}}
        ]).forEach(function(doc) {
          print(JSON.stringify(doc));
        });
        """, "--quiet"
    ]
    
    result = subprocess.run(cmd3, capture_output=True, text=True)
    print(f"\nAssets by Currency:")
    for line in result.stdout.strip().split('\n'):
        if line.strip():
            try:
                data = json.loads(line)
                print(f"  {data['_id']}: ${data['totalAssets']:,} ({data['count']} accounts)")
            except:
                print(f"  {line}")

def show_connection_examples():
    """
    Show connection examples for different tools
    """
    print("\n=== Connection Examples ===")
    
    print("\n1. MongoDB Shell (via Docker):")
    print("   docker exec -it financial_data_mongodb mongosh -u admin -p password123 --authenticationDatabase admin financial_data")
    
    print("\n2. MongoDB Compass:")
    print("   Connection String: mongodb://admin:password123@localhost:27017/financial_data?authSource=admin")
    
    print("\n3. Python (using subprocess for now):")
    print("   Use subprocess to call mongosh as shown in this script")
    
    print("\n4. Mongo Express Web UI:")
    print("   URL: http://localhost:8081")
    print("   Username: admin")
    print("   Password: admin123")

if __name__ == "__main__":
    print("=== MongoDB dataNAV Collection - Working Examples ===")
    query_mongodb_via_shell()
    show_connection_examples()
    
    print("\n=== Database Setup Complete! ===")
    print("Your MongoDB database 'financial_data' is ready with the dataNAV collection.")
    print("Use the Mongo Express web interface or MongoDB shell for queries.")
