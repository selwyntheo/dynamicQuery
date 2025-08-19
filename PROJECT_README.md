# Financial Data Processing System

A MongoDB-based dynamic sub-ledger processing system for financial data management and reporting.

## 🚀 Features

- **MongoDB-First Architecture**: Pure MongoDB implementation for all data operations
- **Dynamic Formula Processing**: Parse and execute financial formulas from database rules
- **Docker Containerized**: Easy setup with Docker Compose
- **Aggregation Pipeline**: Optimized MongoDB queries for financial calculations
- **Flexible Rule Engine**: Add/modify ledger rules without code changes
- **Comprehensive Reporting**: Detailed financial reports and JSON exports

## 📋 Prerequisites

- Docker and Docker Compose
- Python 3.8+
- macOS/Linux environment

## 🔧 Quick Start

### 1. Start MongoDB Environment
```bash
docker-compose up -d
```

### 2. Run the Processor
```bash
python3 dynamicSubLedger.py
```

### 3. Access Web Interface
- MongoDB Express: http://localhost:8081
- Username: `admin`
- Password: `password123`

## 📁 Project Structure

```
.
├── dynamicSubLedger.py          # Main processing engine
├── docker-compose.yml          # MongoDB container setup
├── init-mongo.js               # Database initialization
├── migrate_csv_to_mongodb.py   # Data migration utilities
├── generate_sample_data.py     # Test data generation
└── docs/                       # Documentation files
```

## 🗄️ Database Collections

### `dataNAV`
Source financial data with 42 fields including:
- Account information
- Financial metrics
- Date/time stamps
- Entity relationships

### `derivedSubLedgerRollup` 
Ledger processing rules containing:
- Rule definitions
- Formula expressions
- Filter conditions
- Target ledger accounts

## 💡 Usage Examples

### Basic Processing
```python
from dynamicSubLedger import DynamicSubLedgerProcessor

# Initialize processor
processor = DynamicSubLedgerProcessor(
    collection_name="derivedSubLedgerRollup"
)

# Process all rules
results = processor.process_all_definitions()

# Generate report
summary = processor.generate_summary_report()
print(summary)
```

### Adding New Rules
```javascript
// In MongoDB shell or Mongo Express
db.derivedSubLedgerRollup.insertOne({
    "ruleName": "Net Income Calculation",
    "sourceTable": "dataNAV", 
    "ledgerDefinition": "3002000200",
    "dataDefinition": "[totalIncome] - [totalExpenses]",
    "filter": "accountType='Revenue'",
    "status": "active",
    "createdAt": new Date()
})
```

## 🔍 Formula Syntax

The system supports mathematical expressions with field references:

```
[subscriptionBalance] * -1
[redemptionBalance] + [redemptionPayBase]  
[netAssets] / [shareCount]
[totalIncome] - [totalExpenses] * 0.15
```

## 📊 Sample Output

```
============================================================
DYNAMIC SUB-LEDGER PROCESSING SUMMARY
============================================================
Total Entries Generated: 16
Processing Date: 2025-08-19 17:22:51

Ledger Account  Rule Name            Count    Total Value    
------------------------------------------------------------
3002000110      Capital Subs         5        -16,800,000.00 
3002000120      Redemption Total     5        15,680,000.00  
3002000130      Net Assets Class A   2        375,000,000.00 
3002000140      Daily Yield USD      2        4.70           
3002000150      Composite Capital    2        350,000,000.00 
```

## 🛠️ Development

### Running Tests
```bash
python3 test_dynamicSubLedger.py
```

### Database Management
```bash
# Start containers
./mongodb-docker.sh start

# Stop containers  
./mongodb-docker.sh stop

# View logs
./mongodb-docker.sh logs
```

### Data Migration
```bash
# Migrate CSV data to MongoDB
python3 migrate_csv_to_mongodb.py
```

## 📝 Configuration

### MongoDB Settings
Edit `docker-compose.yml` to modify:
- Database credentials
- Port mappings
- Volume mounts
- Memory limits

### Processing Rules
Modify rules directly in MongoDB:
- Add new formulas
- Update filter conditions
- Change target accounts
- Enable/disable rules

## 🔐 Security

- MongoDB authentication enabled
- Non-root database user
- Environment-based credentials
- Network isolation via Docker

## 📚 Documentation

- `DYNAMIC_SUBLEDGER_README.md` - Detailed processing logic
- `DOCKER_README.md` - Container setup guide
- `MONGODB_MIGRATION_SUMMARY.md` - Migration process
- `CLEANUP_SUMMARY.md` - Code optimization notes

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
1. Check the documentation files
2. Review MongoDB logs: `docker logs financial_data_mongodb`
3. Verify container status: `docker ps`
4. Test database connection: `python3 test_connection.py`

---

**Built with MongoDB, Python, and Docker** 🐍 🐳 🍃
