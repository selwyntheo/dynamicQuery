# Security Configuration Guide

## Overview
This project has been updated to remove hardcoded credentials and use environment variables for secure configuration management.

## ⚠️ **Important Security Changes**

### Removed from Code:
- ❌ Hardcoded usernames (`admin`)
- ❌ Hardcoded passwords (`password123`)
- ❌ Hardcoded database names (`financial_data`)
- ❌ Hardcoded container names (`financial_data_mongodb`)

### Now Uses Environment Variables:
- ✅ `MONGO_USERNAME` - MongoDB username
- ✅ `MONGO_PASSWORD` - MongoDB password  
- ✅ `MONGO_DATABASE_NAME` - Database name
- ✅ `MONGO_CONTAINER_NAME` - Docker container name

## 🔧 Configuration Setup

### 1. Environment Variables

Create a `.env` file in your project root (copy from `.env.example`):

```bash
# MongoDB Configuration
MONGO_USERNAME=admin
MONGO_PASSWORD=your_secure_password_here
MONGO_DATABASE_NAME=financial_data
MONGO_CONTAINER_NAME=financial_data_mongodb

# Application Configuration  
LEDGER_COLLECTION_NAME=derivedSubLedgerRollup
SOURCE_COLLECTION_NAME=dataNAV
OUTPUT_DIRECTORY=/your/output/directory
DEBUG_MODE=false
```

### 2. Docker Environment

Update your `docker-compose.yml` to use environment variables:

```yaml
environment:
  MONGO_INITDB_ROOT_USERNAME: ${MONGO_USERNAME:-admin}
  MONGO_INITDB_ROOT_PASSWORD: ${MONGO_PASSWORD:-your_secure_password}
  MONGO_INITDB_DATABASE: ${MONGO_DATABASE_NAME:-financial_data}
```

### 3. Shell Environment

Export variables in your shell session:

```bash
export MONGO_USERNAME="admin"
export MONGO_PASSWORD="your_secure_password"
export MONGO_DATABASE_NAME="financial_data"
export MONGO_CONTAINER_NAME="financial_data_mongodb"
```

## 📁 Updated Files

### Core Application
- `dynamicSubLedger.py` - Main processor (✅ Secured)
- `docker-compose.yml` - Container configuration (✅ Secured)

### Migration Tools
- `secure_migrate_csv_to_mongodb.py` - New secure migration script (✅ Secured)
- `migrate_csv_to_mongodb.py` - Original script (⚠️ Contains hardcoded credentials)

### Testing & Utilities
- `test_connection.py` - Connection testing (✅ Secured)
- `import_with_mongoimport.py` - Data import utility (✅ Secured)

## 🔒 Security Best Practices

### Production Deployment
1. **Use Strong Passwords**: Generate complex passwords for MongoDB
2. **Limit Access**: Use specific database users with minimal privileges
3. **Network Security**: Restrict MongoDB port access (27017)
4. **SSL/TLS**: Enable encryption in production
5. **Regular Updates**: Keep MongoDB and dependencies updated

### Development Environment
1. **Never Commit .env**: File is in .gitignore
2. **Use .env.example**: Template for required variables
3. **Rotate Credentials**: Change passwords regularly
4. **Monitor Access**: Review MongoDB logs for unusual activity

## 🚀 Usage After Security Updates

### 1. Set Environment Variables
```bash
# Option A: Export in shell
export MONGO_USERNAME="your_username"
export MONGO_PASSWORD="your_password"

# Option B: Create .env file
cp .env.example .env
# Edit .env with your credentials
```

### 2. Start Application
```bash
# Start MongoDB containers
docker-compose up -d

# Run the processor
python3 dynamicSubLedger.py

# Run secure migration
python3 secure_migrate_csv_to_mongodb.py
```

### 3. Verify Security
```bash
# Test connections
python3 test_connection.py

# Check environment
echo $MONGO_USERNAME
echo $MONGO_DATABASE_NAME
```

## 📋 Migration from Hardcoded Credentials

If you have an existing deployment:

1. **Stop current containers**: `docker-compose down`
2. **Set environment variables**: Follow setup instructions above
3. **Update configuration**: Ensure .env file is properly configured
4. **Restart containers**: `docker-compose up -d`
5. **Verify functionality**: Run test scripts

## 🛡️ Files Still Containing Credentials

### ⚠️ **For Manual Review:**
- `migrate_csv_to_mongodb.py` - Original migration script
- `init-mongo.js` - Database initialization script
- Any custom scripts created during development

### 🔧 **Recommended Actions:**
1. Review these files manually
2. Update them to use environment variables
3. Test thoroughly after changes
4. Remove or archive old versions

## 📞 Troubleshooting

### Environment Variable Issues
```bash
# Check if variables are set
env | grep MONGO

# Test with default values
python3 -c "import os; print('Username:', os.getenv('MONGO_USERNAME', 'admin'))"
```

### Connection Problems
```bash
# Test MongoDB connection
python3 test_connection.py

# Check container status
docker ps
docker logs financial_data_mongodb
```

### Permission Errors
```bash
# Verify MongoDB user permissions
docker exec -it financial_data_mongodb mongosh -u $MONGO_USERNAME -p $MONGO_PASSWORD --authenticationDatabase admin
```

## 📈 Next Steps

1. **Code Review**: Audit all files for remaining hardcoded credentials
2. **Automated Testing**: Set up CI/CD with secure credential management
3. **Documentation**: Update all README files with security information
4. **Monitoring**: Implement logging and monitoring for security events

---

**⚡ Remember: Never commit actual credentials to version control!**
