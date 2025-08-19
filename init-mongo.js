// MongoDB initialization script
// This script runs when the container starts for the first time

// Switch to the financial_data database
db = db.getSiblingDB('financial_data');

// Create a user for the financial_data database
db.createUser({
  user: 'financial_user',
  pwd: 'financial_pass',
  roles: [
    {
      role: 'readWrite',
      db: 'financial_data'
    }
  ]
});

// Create the dataNAV collection with validation schema
db.createCollection('dataNAV', {
  validator: {
    $jsonSchema: {
      bsonType: 'object',
      required: ['valuationDt', 'shareClass', 'account', 'NAV'],
      properties: {
        valuationDt: {
          bsonType: 'date',
          description: 'Valuation date - required'
        },
        shareClass: {
          bsonType: 'string',
          enum: ['A', 'B', 'C', 'I', 'R', 'Z'],
          description: 'Share class - required'
        },
        account: {
          bsonType: 'string',
          description: 'Account identifier - required'
        },
        userBank: {
          bsonType: 'string',
          description: 'User bank name'
        },
        accountBaseCurrency: {
          bsonType: 'string',
          description: 'Account base currency'
        },
        accountName: {
          bsonType: 'string',
          description: 'Account name'
        },
        acctBasis: {
          bsonType: 'string',
          enum: ['GAAP', 'IFRS', 'STAT', 'TAX'],
          description: 'Accounting basis'
        },
        capstock: {
          bsonType: 'number',
          minimum: 0,
          description: 'Capital stock amount'
        },
        NAV: {
          bsonType: 'number',
          minimum: 0,
          description: 'Net Asset Value - required'
        },
        netAssets: {
          bsonType: 'number',
          minimum: 0,
          description: 'Net assets'
        },
        sharesOutstanding: {
          bsonType: 'number',
          minimum: 0,
          description: 'Outstanding shares'
        },
        isComposite: {
          bsonType: 'bool',
          description: 'Is composite fund flag'
        },
        isMulticlass: {
          bsonType: 'bool',
          description: 'Is multiclass fund flag'
        },
        isPrimaryBasis: {
          bsonType: 'bool',
          description: 'Is primary basis flag'
        },
        isSleeve: {
          bsonType: 'bool',
          description: 'Is sleeve account flag'
        }
      }
    }
  },
  validationLevel: 'moderate',
  validationAction: 'warn'
});

// Create indexes for better performance
db.dataNAV.createIndex({ 'valuationDt': 1 });
db.dataNAV.createIndex({ 'account': 1 });
db.dataNAV.createIndex({ 'shareClass': 1 });
db.dataNAV.createIndex({ 'eagleEntityId': 1 });
db.dataNAV.createIndex({ 'account': 1, 'valuationDt': -1 });

print('Database financial_data initialized successfully!');
print('Created dataNAV collection with validation schema and indexes');
print('Created user: financial_user with readWrite permissions');
