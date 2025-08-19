# Dynamic Sub-Ledger Processing Function

## Overview

The `dynamicSubLedger.py` function processes a CSV file containing ledger definitions and creates dynamic queries on the source table (dataNAV MongoDB collection) to generate ledger entries based on formulas and filter conditions.

## Key Features

### 1. CSV Parsing
- Reads `dynamicSubledger.csv` file with columns:
  - `ruleName`: Name of the ledger rule
  - `sourceTable`: Source collection name (e.g., dataNAV)
  - `ledgerDefinition`: Target ledger account code
  - `dataDefinition`: Formula to apply (e.g., `[subscriptionBalance] * -1`)
  - `filter`: Filter condition (e.g., `shareClass='A'`)

### 2. Formula Processing
- **Field Extraction**: Parses formulas to extract field names using regex pattern `\[([^\]]+)\]`
- **Mathematical Operations**: Supports +, -, *, /, parentheses
- **Safe Evaluation**: Uses controlled `eval()` with character validation
- **Examples**:
  - `[subscriptionBalance] * -1`
  - `[redemptionBalance] + [redemptionPayBase]`
  - `([incomeDistribution] - [ltcglDistribution]) * 1.2`

### 3. Dynamic MongoDB Queries
- **Aggregation Pipeline**: Creates MongoDB aggregation queries
- **Filter Support**: Handles various filter conditions:
  - String filters: `shareClass='A'`
  - Boolean filters: `isComposite=true`
  - Numeric filters: `NAV>100`
- **Grouping**: Groups by `valuationDt` and `account`
- **Field Selection**: Includes `valuationDt`, `account`, `eagleEntityId`, and formula fields

### 4. Query Execution
- **Docker Integration**: Executes queries via MongoDB Docker container
- **Authentication**: Uses admin credentials for database access
- **Result Parsing**: Parses JSON output from mongosh commands

### 5. Result Generation
- **Ledger Entries**: Creates structured ledger entries with:
  - Rule name and metadata
  - Calculated values from formulas
  - Source data references
  - Processing timestamps
- **Aggregation**: Sums values when grouping by account and valuation date
- **Output Formats**: JSON file export and summary reports

## Usage Examples

### Basic Usage
```python
from dynamicSubLedger import DynamicSubLedgerProcessor

# Initialize processor
processor = DynamicSubLedgerProcessor("dynamicSubledger.csv")

# Process all definitions
results = processor.process_all_definitions()

# Generate summary report
summary = processor.generate_summary_report()
print(summary)

# Save results
processor.save_results_to_json("ledger_results.json")
```

### Sample CSV Format
```csv
ruleName,sourceTable,ledgerDefinition,dataDefinition,filter
Capital Subs,dataNAV,3002000110,"[subscriptionBalance]*-1",none
Net Assets Class A,dataNAV,3002000130,"[netAssets]","shareClass='A'"
Daily Yield USD,dataNAV,3002000140,"[dailyYeild] * 100","accountBaseCurrency='USD'"
```

## Processing Flow

1. **Parse CSV**: Read ledger definitions from CSV file
2. **Extract Fields**: Parse formulas to identify required database fields
3. **Build Query**: Create MongoDB aggregation pipeline with filters and projections
4. **Execute Query**: Run query against dataNAV collection via Docker
5. **Apply Formula**: Calculate values using extracted data and formulas
6. **Generate Entries**: Create structured ledger entries
7. **Group & Summarize**: Aggregate results by account and valuation date

## Sample Output

### Ledger Entry Structure
```json
{
  "ruleName": "Capital Subs",
  "valuationDt": "2024-08-19T00:00:00.000Z",
  "account": "ACC12345678",
  "eagleLedgerAcct": "3002000110",
  "eagleEntityId": "ENT_123456",
  "calculatedValue": -3000000.0,
  "dataDefinition": "[subscriptionBalance]*-1",
  "sourceData": {
    "_id": {
      "valuationDt": "2024-08-19T00:00:00.000Z",
      "account": "ACC12345678"
    },
    "eagleEntityId": "ENT_123456",
    "subscriptionBalance": 3000000
  },
  "processedAt": "2025-08-19T17:09:49.758468"
}
```

### Summary Report
```
============================================================
DYNAMIC SUB-LEDGER PROCESSING SUMMARY
============================================================
Total Entries Generated: 16
Processing Date: 2025-08-19 17:09:53

Ledger Account  Rule Name            Count    Total Value    
------------------------------------------------------------
3002000110      Capital Subs         5        -16,800,000.00 
3002000120      Redemption Total     5        15,680,000.00  
3002000130      Net Assets Class A   2        375,000,000.00 
3002000140      Daily Yield USD      2        4.70           
3002000150      Composite Capital    2        350,000,000.00 
```

## Supported Formula Types

### Mathematical Operations
- **Multiplication**: `[field] * -1`
- **Addition**: `[field1] + [field2]`
- **Division**: `[netAssets] / [sharesOutstanding]`
- **Complex**: `([field1] - [field2]) * 1.2`

### Filter Conditions
- **String**: `shareClass='A'`
- **Boolean**: `isComposite=true`
- **Numeric**: `NAV>100`
- **No filter**: `none` or empty

## Error Handling

- **File Not Found**: Graceful handling of missing CSV files
- **Invalid Formulas**: Safe evaluation with character validation
- **MongoDB Errors**: Connection and query error handling
- **Missing Fields**: Default values for undefined fields
- **JSON Parsing**: Robust parsing of MongoDB output

## Dependencies

- **Python Standard Library**: csv, re, subprocess, json, datetime
- **MongoDB**: Via Docker container with authentication
- **Docker**: For MongoDB query execution

## Files Generated

1. **`ledger_results.json`**: Detailed ledger entries
2. **Console Output**: Processing logs and summary reports
3. **Test Files**: Comprehensive test suite and examples

## Performance Considerations

- **Indexing**: Uses MongoDB indexes on valuationDt, account, shareClass
- **Aggregation**: Efficient grouping and projection
- **Batch Processing**: Processes multiple rules in sequence
- **Memory Management**: Streams results without loading full datasets

This implementation provides a flexible, robust solution for dynamic sub-ledger processing that can handle complex financial calculations and various data filtering requirements.
