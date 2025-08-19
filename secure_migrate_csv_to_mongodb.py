#!/usr/bin/env python3
"""
Script to migrate dynamicSubLedger.csv data to MongoDB collection
Secure version with environment variable support
"""

import csv
import subprocess
import json
import os
from datetime import datetime

class MongoCredentials:
    """Handle MongoDB credentials securely"""
    
    def __init__(self):
        self.username = os.getenv('MONGO_USERNAME', 'admin')
        self.password = os.getenv('MONGO_PASSWORD', 'password123')
        self.database = os.getenv('MONGO_DATABASE_NAME', 'financial_data')
        self.container = os.getenv('MONGO_CONTAINER_NAME', 'financial_data_mongodb')

def execute_mongo_command(creds: MongoCredentials, command: str) -> bool:
    """
    Execute a MongoDB command via mongosh
    
    Args:
        creds: MongoDB credentials object
        command: MongoDB command to execute
        
    Returns:
        True if successful, False otherwise
    """
    try:
        cmd = [
            "docker", "exec", creds.container,
            "mongosh", "-u", creds.username, "-p", creds.password,
            "--authenticationDatabase", "admin", creds.database,
            "--eval", command,
            "--quiet"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"MongoDB command error: {result.stderr}")
            return False
            
        return True
        
    except Exception as e:
        print(f"Error executing MongoDB command: {e}")
        return False

def read_csv_data(csv_file_path: str) -> list:
    """
    Read data from the dynamicSubLedger.csv file
    
    Args:
        csv_file_path: Path to the CSV file
        
    Returns:
        List of dictionaries containing the CSV data
    """
    data = []
    
    try:
        with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Clean up the row data
                cleaned_row = {k.strip(): v.strip() if v else '' for k, v in row.items()}
                data.append(cleaned_row)
                
        print(f"Read {len(data)} records from CSV file")
        return data
        
    except FileNotFoundError:
        print(f"Error: CSV file not found: {csv_file_path}")
        return []
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return []

def create_collection_with_schema(creds: MongoCredentials, collection_name: str = "derivedSubLedgerRollup") -> bool:
    """
    Create the collection with validation schema
    
    Args:
        creds: MongoDB credentials
        collection_name: Name of the collection to create
        
    Returns:
        True if successful, False otherwise
    """
    command = f"""
    try {{
        db.createCollection('{collection_name}', {{
          validator: {{
            $jsonSchema: {{
              bsonType: 'object',
              required: ['ruleName', 'sourceTable', 'dataDefinition'],
              properties: {{
                ruleName: {{
                  bsonType: 'string',
                  description: 'Name of the ledger rule'
                }},
                sourceTable: {{
                  bsonType: 'string',
                  description: 'Source table/collection name'
                }},
                ledgerDefinition: {{
                  bsonType: 'string',
                  description: 'Target ledger account'
                }},
                dataDefinition: {{
                  bsonType: 'string',
                  description: 'Formula/calculation definition'
                }},
                filter: {{
                  bsonType: 'string',
                  description: 'Filter condition for the rule'
                }},
                status: {{
                  bsonType: 'string',
                  enum: ['active', 'inactive'],
                  description: 'Status of the rule'
                }},
                createdAt: {{
                  bsonType: 'string',
                  description: 'Creation timestamp'
                }}
              }}
            }}
          }}
        }});
        
        // Create indexes for better performance
        db.{collection_name}.createIndex({{ "ruleName": 1 }});
        db.{collection_name}.createIndex({{ "sourceTable": 1 }});
        db.{collection_name}.createIndex({{ "status": 1 }});
        
        print('Collection {collection_name} created successfully with validation schema');
        
    }} catch (e) {{
        if (e.codeName === 'NamespaceExists') {{
            print('Collection {collection_name} already exists');
        }} else {{
            print('Error creating collection: ' + e.message);
            throw e;
        }}
    }}
    """
    
    if execute_mongo_command(creds, command):
        print(f"Collection '{collection_name}' setup completed successfully")
        return True
    else:
        print(f"Failed to create collection '{collection_name}'")
        return False

def migrate_data_to_mongodb(creds: MongoCredentials, csv_data: list, collection_name: str = "derivedSubLedgerRollup") -> bool:
    """
    Migrate CSV data to MongoDB collection
    
    Args:
        creds: MongoDB credentials
        csv_data: List of CSV records
        collection_name: Target collection name
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Convert CSV data to MongoDB documents
        documents = []
        for row in csv_data:
            doc = {
                'ruleName': row.get('ruleName', ''),
                'sourceTable': row.get('sourceTable', ''),
                'ledgerDefinition': row.get('ledgerDefinition', ''),
                'dataDefinition': row.get('dataDefinition', ''),
                'filter': row.get('filter', 'none'),
                'status': 'active',
                'createdAt': datetime.now().isoformat()
            }
            documents.append(doc)
        
        # Create the insert command
        docs_json = json.dumps(documents, indent=2)
        command = f"""
        try {{
            var docs = {docs_json};
            var result = db.{collection_name}.insertMany(docs);
            print('Inserted ' + result.insertedIds.length + ' documents');
        }} catch (e) {{
            print('Error inserting documents: ' + e.message);
            throw e;
        }}
        """
        
        if execute_mongo_command(creds, command):
            print(f"Successfully migrated {len(documents)} records to '{collection_name}' collection")
            return True
        else:
            print("Failed to migrate data to MongoDB")
            return False
            
    except Exception as e:
        print(f"Error migrating data: {e}")
        return False

def verify_migration(creds: MongoCredentials, collection_name: str = "derivedSubLedgerRollup") -> bool:
    """
    Verify the migration by checking document count and sample data
    
    Args:
        creds: MongoDB credentials
        collection_name: Collection to verify
        
    Returns:
        True if verification passes, False otherwise
    """
    command = f"""
    try {{
        var count = db.{collection_name}.countDocuments();
        print('Total documents in {collection_name}: ' + count);
        
        if (count > 0) {{
            print('\\nSample documents:');
            db.{collection_name}.find().limit(2).forEach(function(doc) {{
                print(JSON.stringify(doc, null, 2));
            }});
        }}
    }} catch (e) {{
        print('Error verifying migration: ' + e.message);
        throw e;
    }}
    """
    
    if execute_mongo_command(creds, command):
        print(f"Migration verification completed for '{collection_name}' collection")
        return True
    else:
        print("Failed to verify migration")
        return False

def main():
    """
    Main function to execute the migration
    """
    print("=== CSV to MongoDB Migration Tool ===")
    print("Using environment variables for MongoDB credentials")
    
    # Initialize credentials
    creds = MongoCredentials()
    print(f"Connecting to MongoDB container: {creds.container}")
    print(f"Database: {creds.database}")
    print(f"Username: {creds.username}")
    
    # Set paths and collection name
    csv_file_path = "/Volumes/D/Ai/python/dataset/dynamicSubledger.csv"
    collection_name = "derivedSubLedgerRollup"
    
    # Step 1: Read CSV data
    print(f"\\nStep 1: Reading CSV file: {csv_file_path}")
    csv_data = read_csv_data(csv_file_path)
    
    if not csv_data:
        print("No data to migrate. Exiting.")
        return
    
    # Step 2: Create collection with schema
    print(f"\\nStep 2: Creating collection '{collection_name}' with validation schema")
    if not create_collection_with_schema(creds, collection_name):
        print("Failed to create collection. Exiting.")
        return
    
    # Step 3: Migrate data
    print(f"\\nStep 3: Migrating {len(csv_data)} records to MongoDB")
    if not migrate_data_to_mongodb(creds, csv_data, collection_name):
        print("Migration failed. Exiting.")
        return
    
    # Step 4: Verify migration
    print(f"\\nStep 4: Verifying migration")
    if verify_migration(creds, collection_name):
        print("\\n✅ Migration completed successfully!")
        print(f"\\nNext steps:")
        print(f"1. Use the collection in your application: {collection_name}")
        print(f"2. Run the dynamic sub-ledger processor")
        print(f"3. Verify the processed results")
    else:
        print("\\n❌ Migration verification failed!")

if __name__ == "__main__":
    main()
