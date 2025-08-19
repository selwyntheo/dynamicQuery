#!/usr/bin/env python3
"""
Alternative MongoDB import using mongoimport command
"""

import json
import subprocess
import os

def import_with_mongoimport():
    """
    Import JSON data using mongoimport command
    """
    json_file = "/Volumes/D/Ai/python/dataset/dataNAV_sample.json"
    
    # Read and process the JSON file
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    sample_data = data['sample_data']
    
    # Create a temporary JSONL file for mongoimport
    import_file = "/tmp/dataNAV_import.jsonl"
    
    with open(import_file, 'w') as f:
        for record in sample_data:
            # Convert date strings to proper format
            if 'valuationDt' in record:
                record['valuationDt'] = {"$date": record['valuationDt'] + "T00:00:00.000Z"}
            if 'createdAt' in record:
                record['createdAt'] = {"$date": record['createdAt']}
            
            json.dump(record, f)
            f.write('\n')
    
    print(f"Created import file: {import_file}")
    
    # Use mongoimport via docker exec
    cmd = [
        "docker", "exec", "financial_data_mongodb",
        "mongoimport",
        "--username", "admin",
        "--password", "password123",
        "--authenticationDatabase", "admin",
        "--db", "financial_data",
        "--collection", "dataNAV",
        "--file", "/tmp/dataNAV_import.jsonl",
        "--drop"
    ]
    
    # Copy file to container first
    copy_cmd = [
        "docker", "cp",
        import_file,
        "financial_data_mongodb:/tmp/dataNAV_import.jsonl"
    ]
    
    try:
        print("Copying file to container...")
        subprocess.run(copy_cmd, check=True, capture_output=True, text=True)
        
        print("Running mongoimport...")
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        print("Import successful!")
        print(result.stdout)
        
        # Cleanup
        os.remove(import_file)
        
        # Verify import
        verify_cmd = [
            "docker", "exec", "financial_data_mongodb",
            "mongosh",
            "-u", "admin", "-p", "password123",
            "--authenticationDatabase", "admin",
            "financial_data",
            "--eval", "print('Total records: ' + db.dataNAV.countDocuments({})); db.dataNAV.findOne()"
        ]
        
        print("\nVerifying import...")
        verify_result = subprocess.run(verify_cmd, check=True, capture_output=True, text=True)
        print(verify_result.stdout)
        
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print(f"Stdout: {e.stdout}")
        print(f"Stderr: {e.stderr}")

if __name__ == "__main__":
    print("=== MongoDB Import using mongoimport ===")
    import_with_mongoimport()
