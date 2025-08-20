#!/usr/bin/env python3
"""
Dynamic Sub Ledger Parser

This module processes ledger definitions from MongoDB collection and creates dynamic queries
on the source table (dataNAV collection) based on data definitions and formulas.

Functions:
1. Read ledger definitions from MongoDB collection
2. Extract fields from formulas 
3. Create dynamic MongoDB queries
4. Apply formulas and group results
5. Generate ledger entries
"""

import re
import subprocess
import json
import os
from typing import Dict, List, Tuple, Any, Optional
from datetime import datetime

class DynamicSubLedgerProcessor:
    """
    Processes dynamic sub-ledger definitions and generates ledger entries
    """
    
    def __init__(self, mongodb_container: str = "financial_data_mongodb", 
                 collection_name: str = "derivedSubLedgerRollup",
                 db_name: str = "financial_data"):
        """
        Initialize the processor
        
        Args:
            mongodb_container: Name of the MongoDB Docker container
            collection_name: Name of the MongoDB collection containing ledger definitions
            db_name: Name of the MongoDB database
        """
        self.mongodb_container = mongodb_container
        self.collection_name = collection_name
        self.db_name = db_name
        
        # Get credentials from environment variables
        self.db_username = os.getenv('MONGO_USERNAME', 'admin')
        self.db_password = os.getenv('MONGO_PASSWORD', 'password123')
        
        self.ledger_definitions = []
        self.results = []
        
    def read_ledger_definitions_from_mongodb(self) -> List[Dict]:
        """
        Read ledger definitions from MongoDB collection
        
        Returns:
            List of dictionaries containing ledger definitions
        """
        try:
            # Query the MongoDB collection
            cmd = [
                "docker", "exec", self.mongodb_container,
                "mongosh", "-u", self.db_username, "-p", self.db_password,
                "--authenticationDatabase", "admin", self.db_name,
                "--eval", f"""
                db.{self.collection_name}.find({{status: 'active'}}).forEach(function(doc) {{
                    print(JSON.stringify(doc));
                }});
                """,
                "--quiet"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"MongoDB query error: {result.stderr}")
                return []
            
            # Parse the JSON results
            ledger_definitions = []
            for line in result.stdout.strip().split('\n'):
                if line.strip():
                    try:
                        doc = json.loads(line)
                        # Remove MongoDB-specific fields and convert to expected format
                        cleaned_doc = {
                            'ruleName': doc.get('ruleName', ''),
                            'sourceTable': doc.get('sourceTable', ''),
                            'ledgerDefinition': doc.get('ledgerDefinition', ''),
                            'dataDefinition': doc.get('dataDefinition', ''),
                            'filter': doc.get('filter', ''),
                            'status': doc.get('status', 'active'),
                            '_id': str(doc.get('_id', ''))
                        }
                        ledger_definitions.append(cleaned_doc)
                    except json.JSONDecodeError:
                        continue
            
            self.ledger_definitions = ledger_definitions
            print(f"Read {len(ledger_definitions)} ledger definitions from MongoDB collection '{self.collection_name}'")
            return ledger_definitions
            
        except Exception as e:
            print(f"Error reading from MongoDB: {e}")
            return []
    
    def extract_fields_from_formula(self, formula: str) -> List[str]:
        """
        Extract field names from a formula string
        
        Args:
            formula: Formula string like "[subscriptionBalance] * -1"
            
        Returns:
            List of field names found in the formula
        """
        # Pattern to match field names in square brackets
        pattern = r'\[([^\]]+)\]'
        matches = re.findall(pattern, formula)
        
        # Remove duplicates while preserving order
        fields = []
        for field in matches:
            if field not in fields:
                fields.append(field)
                
        return fields
    
    def build_mongodb_query(self, source_table: str, filter_condition: str, fields: List[str]) -> str:
        """
        Build MongoDB aggregation query
        
        Args:
            source_table: Name of the source collection
            filter_condition: Filter condition for the query
            fields: List of fields to select
            
        Returns:
            MongoDB aggregation query as string
        """
        # Base fields to always include
        base_fields = ['valuationDt', 'account']
        
        # Add eagleEntityId if it exists, otherwise use account as fallback
        base_fields.append('eagleEntityId')
        
        # Add the fields from the formula
        all_fields = list(set(base_fields + fields))
        
        # Build the projection
        projection = {}
        for field in all_fields:
            projection[field] = 1
        
        # Build the match stage
        match_stage = {}
        if filter_condition and filter_condition.lower() != 'none' and filter_condition.strip():
            # Parse simple filter conditions
            # For now, handle basic conditions like "shareClass='A'"
            if '=' in filter_condition:
                parts = filter_condition.split('=')
                if len(parts) == 2:
                    field_name = parts[0].strip()
                    field_value = parts[1].strip().strip("'\"")
                    
                    # Handle boolean values
                    if field_value.lower() == 'true':
                        field_value = True
                    elif field_value.lower() == 'false':
                        field_value = False
                    # Handle numeric values
                    elif field_value.replace('.', '').isdigit():
                        field_value = float(field_value) if '.' in field_value else int(field_value)
                    
                    match_stage[field_name] = field_value
        
        # Build aggregation pipeline
        pipeline = []
        
        if match_stage:
            pipeline.append({"$match": match_stage})
        
        pipeline.extend([
            {"$project": projection},
            {"$group": {
                "_id": {
                    "valuationDt": "$valuationDt",
                    "account": "$account"
                },
                "eagleEntityId": {"$first": "$eagleEntityId"},
                **{field: {"$sum": f"${field}"} for field in fields}  # Changed to $sum for aggregation
            }}
        ])
        
        return json.dumps(pipeline, indent=2)
    
    def execute_mongodb_query(self, source_table: str, pipeline: str) -> List[Dict]:
        """
        Execute MongoDB aggregation query
        
        Args:
            source_table: Name of the collection
            pipeline: MongoDB aggregation pipeline as JSON string
            
        Returns:
            List of query results
        """
        try:
            # Create the mongosh command
            cmd = [
                "docker", "exec", self.mongodb_container,
                "mongosh", "-u", self.db_username, "-p", self.db_password,
                "--authenticationDatabase", "admin", self.db_name,
                "--eval", f"db.{source_table}.aggregate({pipeline}).forEach(function(doc) {{ print(JSON.stringify(doc)); }});",
                "--quiet"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"MongoDB query error: {result.stderr}")
                return []
            
            # Parse the JSON results
            results = []
            for line in result.stdout.strip().split('\n'):
                if line.strip():
                    try:
                        doc = json.loads(line)
                        results.append(doc)
                    except json.JSONDecodeError:
                        continue
            
            return results
            
        except Exception as e:
            print(f"Error executing MongoDB query: {e}")
            return []
    
    def apply_formula(self, formula: str, data: Dict) -> float:
        """
        Apply formula to data values with support for mathematical functions
        
        Supported functions: ABS, ROUND, MAX, MIN, SUM, AVG, CEIL, FLOOR, SQRT
        
        Args:
            formula: Formula string like "ABS([bookValueBase])*-1" or "[subscriptionBalance] * -1"
            data: Dictionary containing field values
            
        Returns:
            Calculated result
        """
        try:
            # Replace field references with actual values
            expression = formula
            
            # Extract fields from formula
            fields = self.extract_fields_from_formula(formula)
            
            # Replace field references with actual values
            for field in fields:
                field_value = data.get(field, 0)
                if field_value is None:
                    field_value = 0
                
                # Replace [fieldName] with the actual value
                expression = expression.replace(f'[{field}]', str(field_value))
            
            # Define safe mathematical functions
            import math
            safe_functions = {
                'ABS': abs,
                'ROUND': round,
                'MAX': max,
                'MIN': min,
                'CEIL': math.ceil,
                'FLOOR': math.floor,
                'SQRT': math.sqrt,
                'POW': pow,
                'LOG': math.log,
                'LOG10': math.log10,
                'EXP': math.exp,
                'SIN': math.sin,
                'COS': math.cos,
                'TAN': math.tan
            }
            
            # Replace function calls with Python equivalents
            for func_name, func in safe_functions.items():
                # Handle function calls like ABS(value) -> abs(value)
                pattern = rf'\b{func_name}\s*\('
                expression = re.sub(pattern, f'{func.__name__}(', expression, flags=re.IGNORECASE)
            
            # Create a safe evaluation environment
            safe_dict = {
                "__builtins__": {},
                **{func.__name__: func for func in safe_functions.values()}
            }
            
            # Additional safety check - remove function names and check remaining characters
            allowed_chars = set('0123456789+-*/.(), ')
            allowed_function_names = set(func.__name__ for func in safe_functions.values())
            
            # Create a version of the expression without function names for validation
            validation_expr = expression
            for func_name in allowed_function_names:
                validation_expr = re.sub(rf'\b{func_name}\b', '', validation_expr, flags=re.IGNORECASE)
            
            # Check if remaining characters are safe
            if all(c in allowed_chars for c in validation_expr):
                # Evaluate the mathematical expression safely
                result = eval(expression, safe_dict, {})
                return float(result)
            else:
                print(f"Warning: Unsafe expression detected: {expression}")
                print(f"Validation expression: {validation_expr}")
                return 0.0
                
        except Exception as e:
            print(f"Error applying formula '{formula}': {e}")
            return 0.0
    
    def process_ledger_definition(self, definition: Dict) -> List[Dict]:
        """
        Process a single ledger definition
        
        Args:
            definition: Single ledger definition from CSV
            
        Returns:
            List of ledger entries
        """
        print(f"\nProcessing rule: {definition.get('ruleName', 'Unknown')}")
        
        source_table = definition.get('sourceTable', '').strip()
        data_definition = definition.get('dataDefinition', '').strip()
        ledger_definition = definition.get('ledgerDefinition', '').strip()
        filter_condition = definition.get('filter', '').strip()
        
        # Extract fields from the formula
        fields = self.extract_fields_from_formula(data_definition)
        print(f"Fields extracted from formula: {fields}")
        
        # Build and execute MongoDB query
        pipeline = self.build_mongodb_query(source_table, filter_condition, fields)
        print(f"MongoDB pipeline: {pipeline}")
        
        query_results = self.execute_mongodb_query(source_table, pipeline)
        print(f"Query returned {len(query_results)} results")
        
        # Apply formula to each result
        ledger_entries = []
        for result in query_results:
            try:
                # Extract the grouped data
                valuation_dt = result['_id']['valuationDt']
                account = result['_id']['account']
                eagle_entity_id = result.get('eagleEntityId', '')
                
                # Apply the formula
                calculated_value = self.apply_formula(data_definition, result)
                
                # Create ledger entry
                ledger_entry = {
                    'ruleName': definition.get('ruleName', ''),
                    'valuationDt': valuation_dt,
                    'account': account,
                    'eagleLedgerAcct': ledger_definition,
                    'eagleEntityId': eagle_entity_id,
                    'calculatedValue': calculated_value,
                    'dataDefinition': data_definition,
                    'sourceData': result,
                    'processedAt': datetime.now().isoformat()
                }
                
                ledger_entries.append(ledger_entry)
                
            except Exception as e:
                print(f"Error processing result: {e}")
                continue
        
        print(f"Generated {len(ledger_entries)} ledger entries")
        return ledger_entries
    
    def process_all_definitions(self) -> List[Dict]:
        """
        Process all ledger definitions from the MongoDB collection
        
        Returns:
            List of all generated ledger entries
        """
        if not self.ledger_definitions:
            self.ledger_definitions = self.read_ledger_definitions_from_mongodb()
        
        all_ledger_entries = []
        
        for definition in self.ledger_definitions:
            ledger_entries = self.process_ledger_definition(definition)
            all_ledger_entries.extend(ledger_entries)
        
        self.results = all_ledger_entries
        return all_ledger_entries
    
    def generate_summary_report(self) -> str:
        """
        Generate a summary report of the processing results
        
        Returns:
            Summary report as string
        """
        if not self.results:
            return "No results to summarize"
        
        # Group by ledger account
        ledger_summary = {}
        for entry in self.results:
            ledger_acct = entry.get('eagleLedgerAcct', 'Unknown')
            if ledger_acct not in ledger_summary:
                ledger_summary[ledger_acct] = {
                    'count': 0,
                    'total_value': 0,
                    'rule_name': entry.get('ruleName', '')
                }
            
            ledger_summary[ledger_acct]['count'] += 1
            ledger_summary[ledger_acct]['total_value'] += entry.get('calculatedValue', 0)
        
        # Generate report
        report = f"\n{'='*60}\n"
        report += f"DYNAMIC SUB-LEDGER PROCESSING SUMMARY\n"
        report += f"{'='*60}\n"
        report += f"Total Entries Generated: {len(self.results)}\n"
        report += f"Processing Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        report += f"{'Ledger Account':<15} {'Rule Name':<20} {'Count':<8} {'Total Value':<15}\n"
        report += f"{'-'*60}\n"
        
        for ledger_acct, summary in ledger_summary.items():
            report += f"{ledger_acct:<15} {summary['rule_name']:<20} {summary['count']:<8} {summary['total_value']:<15,.2f}\n"
        
        return report
    
    def save_results_to_json(self, output_file: str) -> bool:
        """
        Save processing results to JSON file
        
        Args:
            output_file: Path to output JSON file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(output_file, 'w') as f:
                json.dump(self.results, f, indent=2, default=str)
            
            print(f"Results saved to {output_file}")
            return True
            
        except Exception as e:
            print(f"Error saving results: {e}")
            return False

def main():
    """
    Main function to demonstrate the dynamic sub-ledger processing
    """
    print("=== Dynamic Sub-Ledger Processor ===")
    
    # Initialize processor
    processor = DynamicSubLedgerProcessor(
        collection_name="derivedSubLedgerRollup"
    )
    
    # Process all definitions
    results = processor.process_all_definitions()
    
    # Generate and display summary
    summary = processor.generate_summary_report()
    print(summary)
    
    # Save results
    output_file = "/Volumes/D/Ai/python/dataset/ledger_results.json"
    processor.save_results_to_json(output_file)
    
    # Display sample results
    if results:
        print(f"\n{'='*60}")
        print("SAMPLE LEDGER ENTRIES")
        print(f"{'='*60}")
        
        for i, entry in enumerate(results[:3], 1):
            print(f"\nEntry {i}:")
            print(f"  Rule: {entry.get('ruleName', 'N/A')}")
            print(f"  Account: {entry.get('account', 'N/A')}")
            print(f"  Valuation Date: {entry.get('valuationDt', 'N/A')}")
            print(f"  Ledger Account: {entry.get('eagleLedgerAcct', 'N/A')}")
            print(f"  Formula: {entry.get('dataDefinition', 'N/A')}")
            print(f"  Calculated Value: {entry.get('calculatedValue', 0):,.2f}")

if __name__ == "__main__":
    main()