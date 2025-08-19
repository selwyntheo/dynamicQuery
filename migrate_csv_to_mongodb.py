#!/usr/bin/env python3
"""
Script to migrate dynamicSubLedger.csv data to MongoDB collection
"""

import csv
import subprocess
import json
from datetime import datetime

def read_csv_data(csv_file_path: str) -> list:
    """
    Read data from the dynamicSubLedger.csv file
    
    Args:
        csv_file_path: Path to the CSV file
        
    Returns:
        List of dictionaries containing the CSV data
    """
    csv_data = []
    
    try:
        with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Clean up the row data
                cleaned_row = {k.strip(): v.strip() if v else '' for k, v in row.items()}
                # Add metadata
                cleaned_row['createdAt'] = datetime.now().isoformat()
                cleaned_row['status'] = 'active'
                csv_data.append(cleaned_row)
                
        print(f"Read {len(csv_data)} records from CSV file")
        return csv_data
        
    except FileNotFoundError:
        print(f"Error: CSV file not found: {csv_file_path}")
        return []
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return []

def create_mongodb_collection(collection_name: str, mongodb_container: str = "financial_data_mongodb") -> bool:
    """
    Create a new MongoDB collection with validation schema
    
    Args:
        collection_name: Name of the collection to create
        mongodb_container: Name of the MongoDB Docker container
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Create collection with validation schema
        create_cmd = [
            "docker", "exec", mongodb_container,
            "mongosh", "-u", "admin", "-p", "password123",
            "--authenticationDatabase", "admin", "financial_data",
            "--eval", f"""
            db.createCollection('{collection_name}', {{
              validator: {{
                $jsonSchema: {{
                  bsonType: 'object',
                  required: ['ruleName', 'sourceTable', 'dataDefinition'],
                  properties: {{
                    ruleName: {{
                      bsonType: 'string',
                      description: 'Name of the rule - required'
                    }},
                    sourceTable: {{
                      bsonType: 'string',
                      description: 'Source table name - required'
                    }},
                    ledgerDefinition: {{
                      bsonType: 'string',
                      description: 'Ledger account definition'
                    }},
                    dataDefinition: {{
                      bsonType: 'string',
                      description: 'Formula definition - required'
                    }},
                    filter: {{
                      bsonType: 'string',
                      description: 'Filter condition'
                    }},
                    status: {{
                      bsonType: 'string',
                      enum: ['active', 'inactive', 'draft'],
                      description: 'Status of the rule'
                    }},
                    createdAt: {{
                      bsonType: 'string',
                      description: 'Creation timestamp'
                    }}
                  }}
                }}
              }},
              validationLevel: 'moderate',
              validationAction: 'warn'
            }});
            print('Collection {collection_name} created successfully');
            """,
            "--quiet"
        ]
        
        result = subprocess.run(create_cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"Collection '{collection_name}' created successfully")
            return True
        else:
            print(f"Error creating collection: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"Error creating MongoDB collection: {e}")
        return False

def insert_data_to_mongodb(collection_name: str, data: list, mongodb_container: str = "financial_data_mongodb") -> bool:
    """
    Insert data into MongoDB collection
    
    Args:
        collection_name: Name of the collection
        data: List of dictionaries to insert
        mongodb_container: Name of the MongoDB Docker container
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Convert data to JSON string for insertion
        json_data = json.dumps(data, default=str)
        
        # Insert data using mongosh
        insert_cmd = [
            "docker", "exec", mongodb_container,
            "mongosh", "-u", "admin", "-p", "password123",
            "--authenticationDatabase", "admin", "financial_data",
            "--eval", f"""
            var data = {json_data};
            var result = db.{collection_name}.insertMany(data);
            print('Inserted ' + result.insertedIds.length + ' documents');
            print('Total documents in collection: ' + db.{collection_name}.countDocuments({{}}));
            """,
            "--quiet"
        ]
        
        result = subprocess.run(insert_cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"Data inserted successfully into '{collection_name}'")
            print(result.stdout)
            return True
        else:
            print(f"Error inserting data: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"Error inserting data to MongoDB: {e}")
        return False

def create_indexes(collection_name: str, mongodb_container: str = "financial_data_mongodb") -> bool:
    """
    Create indexes for the collection
    
    Args:
        collection_name: Name of the collection
        mongodb_container: Name of the MongoDB Docker container
        
    Returns:
        True if successful, False otherwise
    """
    try:
        index_cmd = [
            "docker", "exec", mongodb_container,
            "mongosh", "-u", "admin", "-p", "password123",
            "--authenticationDatabase", "admin", "financial_data",
            "--eval", f"""
            // Create indexes for better performance
            db.{collection_name}.createIndex({{ 'ruleName': 1 }});
            db.{collection_name}.createIndex({{ 'sourceTable': 1 }});
            db.{collection_name}.createIndex({{ 'status': 1 }});
            db.{collection_name}.createIndex({{ 'ledgerDefinition': 1 }});
            db.{collection_name}.createIndex({{ 'ruleName': 1, 'sourceTable': 1 }});
            print('Indexes created successfully');
            """,
            "--quiet"
        ]
        
        result = subprocess.run(index_cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("Indexes created successfully")
            return True
        else:
            print(f"Error creating indexes: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"Error creating indexes: {e}")
        return False

def verify_migration(collection_name: str, mongodb_container: str = "financial_data_mongodb"):
    """
    Verify the migration by displaying collection contents
    
    Args:
        collection_name: Name of the collection
        mongodb_container: Name of the MongoDB Docker container
    """
    try:
        verify_cmd = [
            "docker", "exec", mongodb_container,
            "mongosh", "-u", "admin", "-p", "password123",
            "--authenticationDatabase", "admin", "financial_data",
            "--eval", f"""
            print('=== Collection Verification ===');
            print('Collection: {collection_name}');
            print('Total documents: ' + db.{collection_name}.countDocuments({{}}));
            print('\\n=== Sample Documents ===');
            db.{collection_name}.find().limit(3).forEach(function(doc) {{
              print('Rule: ' + doc.ruleName + ', Source: ' + doc.sourceTable + ', Ledger: ' + doc.ledgerDefinition);
              print('Formula: ' + doc.dataDefinition);
              print('Filter: ' + doc.filter);
              print('---');
            }});
            
            print('\\n=== Collection Stats ===');
            var stats = db.{collection_name}.aggregate([
              {{$group: {{
                _id: '$sourceTable',
                count: {{$sum: 1}},
                rules: {{$push: '$ruleName'}}
              }}}}
            ]);
            stats.forEach(function(stat) {{
              print('Source Table: ' + stat._id + ', Rules: ' + stat.count);
            }});
            
            print('\\n=== Available Indexes ===');
            db.{collection_name}.getIndexes().forEach(function(index) {{
              print('Index: ' + index.name);
            }});
            """,
            "--quiet"
        ]
        
        result = subprocess.run(verify_cmd, capture_output=True, text=True)
        print("\n" + result.stdout)
        
    except Exception as e:
        print(f"Error verifying migration: {e}")

def migrate_csv_to_mongodb():
    """
    Main function to migrate CSV data to MongoDB
    """
    print("=== Migrating dynamicSubLedger.csv to MongoDB ===")
    
    csv_file_path = "/Volumes/D/Ai/python/dataset/dynamicSubledger.csv"
    collection_name = "derivedSubLedgerRollup"
    
    # Step 1: Read CSV data
    csv_data = read_csv_data(csv_file_path)
    if not csv_data:
        print("No data to migrate")
        return
    
    # Step 2: Create MongoDB collection
    if not create_mongodb_collection(collection_name):
        print("Failed to create collection")
        return
    
    # Step 3: Insert data
    if not insert_data_to_mongodb(collection_name, csv_data):
        print("Failed to insert data")
        return
    
    # Step 4: Create indexes
    create_indexes(collection_name)
    
    # Step 5: Verify migration
    verify_migration(collection_name)
    
    print(f"\n✅ Migration completed successfully!")
    print(f"CSV data from '{csv_file_path}' has been moved to MongoDB collection '{collection_name}'")

if __name__ == "__main__":
    migrate_csv_to_mongodb()
