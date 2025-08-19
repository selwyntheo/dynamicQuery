# dataNAV MongoDB Collection

This directory contains scripts to create and populate a MongoDB collection for the `dataNAV` table with all specified financial data fields.

## Files

1. **generate_sample_data.py** - Generates sample test data and saves to JSON
2. **create_datanav_collection.py** - Complete MongoDB setup script (requires running MongoDB)
3. **import_to_mongodb.py** - Imports JSON data to MongoDB
4. **dataNAV_sample.json** - Generated sample data in JSON format
5. **README.md** - This file

## dataNAV Fields

The collection includes all 42 specified fields:

### Core Fields
- `valuationDt` - Valuation date
- `shareClass` - Share class (A, B, C, I, R, Z)
- `account` - Account identifier
- `userBank` - User bank name
- `accountBaseCurrency` - Base currency for account
- `accountName` - Account name
- `acctBasis` - Accounting basis (GAAP, IFRS, STAT, TAX)

### Capital and Distribution Fields
- `capstock` - Capital stock amount
- `chartOfAccounts` - Chart of accounts identifier
- `distribution` - Distribution amount
- `incomeDistribution` - Income distribution
- `ltcglDistribution` - Long-term capital gains distribution
- `dailyDistribution` - Daily distribution amount
- `settleDistribution` - Settlement distribution
- `distributionPayable` - Distribution payable
- `reinvestmentDistribution` - Reinvestment distribution

### Eagle System Fields
- `eagleAcctBasis` - Eagle accounting basis
- `eagleClass` - Eagle class
- `eagleEntityId` - Eagle entity identifier
- `eagleRegion` - Eagle region

### Financial Metrics
- `NAV` - Net Asset Value
- `netAssets` - Net assets
- `dailyYeild` - Daily yield
- `capstockRedsPay` - Capital stock redemptions payable
- `capstockSubsRec` - Capital stock subscriptions receivable

### Shares and Balances
- `settledShares` - Settled shares count
- `sharesOutstanding` - Outstanding shares count
- `redemptionBalance` - Redemption balance
- `redemptionPayBase` - Redemption pay base currency
- `redemptionPayLocal` - Redemption pay local currency
- `subscriptionBalance` - Subscription balance
- `subscriptionRecBase` - Subscription receivable base currency
- `subscriptionRecLocal` - Subscription receivable local currency

### Configuration Flags
- `isComposite` - Is composite fund
- `isMulticlass` - Is multiclass fund
- `isPrimaryBasis` - Is primary basis
- `isSleeve` - Is sleeve account

### Optional Fields
- `mergerPic` - Merger picture/identifier
- `parentAccount` - Parent account identifier
- `entityBaseCurrency` - Entity base currency
- `shareClassCurrency` - Share class currency
- `settleCapstock` - Settlement capital stock

## Usage

### Option 1: Generate Sample Data Only
```bash
python generate_sample_data.py
```
This creates `dataNAV_sample.json` with 20 sample records.

### Option 2: Full MongoDB Setup (requires MongoDB running)
```bash
python create_datanav_collection.py
```
This will:
- Connect to MongoDB (localhost:27017 by default)
- Create the `dataNAV` collection in `financial_data` database
- Generate and insert 100 sample records
- Create performance indexes
- Display sample data and statistics

### Option 3: Import Existing JSON Data
```bash
python import_to_mongodb.py
```
This imports the generated JSON data into MongoDB.

## MongoDB Connection

Default connection: `mongodb://localhost:27017/`
Default database: `financial_data`
Collection name: `dataNAV`

## Sample Queries

Once data is loaded, you can run these MongoDB queries:

### Find records by date range
```javascript
db.dataNAV.find({
  "valuationDt": {
    $gte: ISODate("2024-01-01"),
    $lt: ISODate("2024-12-31")
  }
})
```

### Find by share class
```javascript
db.dataNAV.find({"shareClass": "A"})
```

### High NAV records
```javascript
db.dataNAV.find({"NAV": {$gt: 500}})
```

### Aggregate by currency
```javascript
db.dataNAV.aggregate([
  {
    $group: {
      _id: "$accountBaseCurrency",
      avgNAV: {$avg: "$NAV"},
      count: {$sum: 1}
    }
  },
  {$sort: {avgNAV: -1}}
])
```

### Complex query with multiple conditions
```javascript
db.dataNAV.find({
  "shareClass": "A",
  "accountBaseCurrency": "USD",
  "isComposite": true,
  "NAV": {$gte: 100}
})
```

## Data Types

- **Dates**: ISO date format (YYYY-MM-DD)
- **Numbers**: Decimal values with appropriate precision
- **Booleans**: true/false for flag fields
- **Strings**: Text identifiers and names
- **Nullable**: Some fields like `mergerPic` and `parentAccount` can be null

## Dependencies

- pymongo
- faker
- datetime
- uuid
- json

Install with:
```bash
pip install pymongo faker
```
