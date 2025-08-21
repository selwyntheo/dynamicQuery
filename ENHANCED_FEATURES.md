# Enhanced Dynamic Sub-Ledger Processor

## 🎯 **New Capabilities Added**

### 1. Enhanced Formula Support
The `apply_formula` method now supports mathematical functions beyond basic arithmetic.

#### Supported Functions:
- **ABS()** - Absolute value
- **ROUND()** - Round to specified decimal places
- **MAX()** - Maximum of multiple values
- **MIN()** - Minimum of multiple values
- **CEIL()** - Round up to nearest integer
- **FLOOR()** - Round down to nearest integer
- **SQRT()** - Square root
- **POW()** - Power/exponentiation
- **LOG()** - Natural logarithm
- **LOG10()** - Base-10 logarithm
- **EXP()** - Exponential function
- **SIN(), COS(), TAN()** - Trigonometric functions

#### Example Formulas:
```
ABS([bookValueBase]) * -1
ROUND([netAssets] * [yield], 2)
MAX([subscriptionBalance], [redemptionBalance])
CEIL([dailyYield] * 100)
SQRT(ABS([variance]))
```

### 2. Dynamic Ledger Account Resolution
Ledger accounts can now contain field references that are resolved from source data.

#### Static vs Dynamic Accounts:
```
Static:     "3002000110"              -> "3002000110"
Dynamic:    "[accountCode]"           -> "3002000110" (from data)
Pattern:    "300[categoryCode]001"    -> "300200001" (prefix + field + suffix)
Complex:    "[type]_[code]_LEDGER"    -> "ASSET_200_LEDGER"
```

## 🔧 **Implementation Details**

### Enhanced Formula Processing
```python
def apply_formula(self, formula: str, data: Dict) -> float:
    # Supports: ABS([bookValueBase])*-1
    # Returns: Calculated float value using safe evaluation
```

### Dynamic Ledger Resolution
```python
def resolve_ledger_account(self, ledger_definition: str, data: Dict) -> str:
    # Supports: "300[shareClass]0001" 
    # Returns: "300A0001" (if shareClass = "A")
```

### Enhanced Processing Pipeline
```python
def process_ledger_definition(self, definition: Dict) -> List[Dict]:
    # 1. Extract fields from formula AND ledger definition
    # 2. Build MongoDB query including all required fields
    # 3. Apply enhanced formulas with functions
    # 4. Resolve dynamic ledger accounts
    # 5. Generate enriched ledger entries
```

## 📊 **Example Usage**

### Test Results from Live System:
```
=== Dynamic Sub-Ledger Processor ===
Read 6 ledger definitions from MongoDB collection

Processing rule: Dynamic Ledger Test
Dynamic ledger account fields detected: ['shareClass']
Fields extracted from formula: ['netAssets', 'shareClass']
Query returned 5 results
Resolved ledger account: '300[shareClass]0001' -> '30000001'
Generated 5 ledger entries

Total Entries Generated: 21
```

### Sample Enhanced Rules:
```javascript
// MongoDB Collection: derivedSubLedgerRollup
{
  "ruleName": "Enhanced Capital Calculation",
  "ledgerDefinition": "300[shareClass]001",      // Dynamic account
  "dataDefinition": "ABS([netAssets]) * -1",     // Enhanced formula
  "sourceTable": "dataNAV",
  "filter": "accountType='EQUITY'",
  "status": "active"
}

{
  "ruleName": "Rounded Yield Calculation", 
  "ledgerDefinition": "[baseAccount]",           // Direct field mapping
  "dataDefinition": "ROUND([yield] * 100, 2)",   // Mathematical function
  "sourceTable": "dataNAV",
  "filter": "none",
  "status": "active"
}
```

## 🚀 **Benefits**

### 1. **Flexibility**
- Create dynamic account mappings based on data attributes
- Use sophisticated mathematical formulas
- Reduce manual rule configuration

### 2. **Accuracy** 
- Consistent mathematical function evaluation
- Safe expression parsing prevents injection attacks
- Comprehensive error handling

### 3. **Scalability**
- Rules adapt automatically to data changes
- No code changes needed for new account patterns
- Supports complex financial calculations

### 4. **Maintainability**
- Self-documenting rule definitions
- Clear separation of logic and configuration
- Easy to add new mathematical functions

## 📋 **Configuration Examples**

### Adding Dynamic Rules to MongoDB:
```javascript
// Via MongoDB shell or Mongo Express
db.derivedSubLedgerRollup.insertOne({
  "ruleName": "Dynamic Asset Allocation",
  "sourceTable": "dataNAV",
  "ledgerDefinition": "[assetClass]_[riskLevel]_ACCT",
  "dataDefinition": "ROUND(ABS([marketValue]) * [allocation], 2)",
  "filter": "status='ACTIVE'",
  "status": "active",
  "createdAt": new Date()
});
```

### Using Environment Variables:
```bash
export MONGO_USERNAME="your_username"
export MONGO_PASSWORD="secure_password"
export MONGO_DATABASE_NAME="financial_data"

python3 dynamicSubLedger.py
```

## 🔍 **Field Detection & Resolution**

### Automatic Field Extraction:
The system automatically detects field references in both:
- **Formula expressions**: `ABS([netAssets]) + [yield]`
- **Ledger definitions**: `300[categoryCode]001`

### MongoDB Query Optimization:
Only required fields are fetched from the database, improving performance:
```json
{
  "$project": {
    "valuationDt": 1,
    "account": 1, 
    "eagleEntityId": 1,
    "netAssets": 1,        // From formula
    "shareClass": 1        // From ledger definition
  }
}
```

## ⚡ **Performance & Security**

### Safe Evaluation:
- Mathematical expressions are evaluated in restricted environment
- Only whitelisted functions are allowed
- Character validation prevents code injection

### Optimized Queries:
- Dynamic field detection minimizes data transfer
- MongoDB aggregation pipelines for efficient processing
- Proper indexing recommendations for scale

## 🎯 **Future Enhancements**

### Potential Additions:
1. **Conditional Logic**: IF/THEN statements in formulas
2. **Date Functions**: DATE_ADD, DATE_DIFF, etc.
3. **String Functions**: CONCAT, SUBSTRING, etc.
4. **Lookup Functions**: Reference external data sources
5. **Validation Rules**: Data quality checks in formulas

---

**The enhanced system provides enterprise-grade flexibility while maintaining security and performance standards.**
