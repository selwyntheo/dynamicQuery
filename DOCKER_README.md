# Docker MongoDB Setup for dataNAV Collection

This directory contains a complete Docker-based MongoDB setup for the `financial_data` database with the `dataNAV` collection.

## 🐳 Docker Setup Files

- **`docker-compose.yml`** - Docker Compose configuration for MongoDB and Mongo Express
- **`init-mongo.js`** - MongoDB initialization script (creates database, user, collection with validation)
- **`mongodb-docker.sh`** - Management script for MongoDB Docker operations
- **`.env`** - Environment variables for configuration

## 🚀 Quick Start

### 1. Start MongoDB with Docker

```bash
./mongodb-docker.sh start
```

This will:
- Start MongoDB container on port 27017
- Start Mongo Express web UI on port 8081
- Create the `financial_data` database
- Create the `dataNAV` collection with validation schema
- Set up indexes for performance
- Create database users

### 2. Import Sample Data

```bash
./mongodb-docker.sh import
```

This imports the sample dataNAV data into the MongoDB collection.

## 📋 Available Commands

```bash
./mongodb-docker.sh {command}
```

### Commands:
- **`start`** - Start MongoDB and Mongo Express containers
- **`stop`** - Stop all containers
- **`restart`** - Restart all containers
- **`logs`** - Show MongoDB logs (real-time)
- **`status`** - Show container status
- **`test`** - Test MongoDB connection
- **`import`** - Import sample dataNAV data
- **`cleanup`** - Remove containers and volumes (⚠️ DESTRUCTIVE)
- **`info`** - Show connection information

## 🔗 Connection Information

### MongoDB Connection
- **Host:** localhost
- **Port:** 27017
- **Database:** financial_data
- **Admin URI:** `mongodb://admin:password123@localhost:27017/financial_data`
- **App URI:** `mongodb://financial_user:financial_pass@localhost:27017/financial_data`

### Users
- **Admin User:** `admin` / `password123` (full access)
- **App User:** `financial_user` / `financial_pass` (readWrite on financial_data)

### Mongo Express Web UI
- **URL:** http://localhost:8081
- **Username:** `admin`
- **Password:** `admin123`

## 🗂️ Database Schema

### Collection: `dataNAV`

The collection includes validation schema for key fields:

**Required Fields:**
- `valuationDt` (date)
- `shareClass` (string: A, B, C, I, R, Z)
- `account` (string)
- `NAV` (number, minimum: 0)

**Indexed Fields:**
- `valuationDt`
- `account`
- `shareClass`
- `eagleEntityId`
- Compound index: `account + valuationDt`

## 🐍 Python Integration

### Updated Connection Strings
The Python scripts have been updated to use the Docker MongoDB credentials:

```python
# For admin access
connection_string = "mongodb://admin:password123@localhost:27017/"

# For application access
connection_string = "mongodb://financial_user:financial_pass@localhost:27017/"
```

### Import Sample Data
```bash
python import_to_mongodb.py
```

### Generate New Sample Data
```bash
python generate_sample_data.py
```

## 📊 Sample Queries

Once the data is imported, you can run these queries:

### MongoDB Shell (via Docker)
```bash
docker exec -it financial_data_mongodb mongosh -u admin -p password123 --authenticationDatabase admin financial_data
```

### Sample Queries in MongoDB Shell
```javascript
// Count total records
db.dataNAV.countDocuments()

// Find by share class
db.dataNAV.find({"shareClass": "A"})

// Find high NAV records
db.dataNAV.find({"NAV": {$gt: 500}})

// Aggregate by currency
db.dataNAV.aggregate([
  {$group: {_id: "$accountBaseCurrency", avgNAV: {$avg: "$NAV"}, count: {$sum: 1}}},
  {$sort: {avgNAV: -1}}
])

// Recent records (last 30 days)
db.dataNAV.find({
  "valuationDt": {
    $gte: new Date(new Date().setDate(new Date().getDate() - 30))
  }
}).sort({"valuationDt": -1})
```

## 🔧 Troubleshooting

### MongoDB Won't Start
```bash
# Check Docker status
docker ps -a

# View logs
./mongodb-docker.sh logs

# Restart containers
./mongodb-docker.sh restart
```

### Connection Issues
```bash
# Test connection
./mongodb-docker.sh test

# Check container status
./mongodb-docker.sh status
```

### Reset Everything
```bash
# ⚠️ This will delete all data
./mongodb-docker.sh cleanup
./mongodb-docker.sh start
```

## 📁 Volume Persistence

Data is persisted in Docker volumes:
- **`mongodb_data`** - Database files
- **`mongodb_config`** - Configuration files

Data persists between container restarts unless you run `cleanup`.

## 🔒 Security Notes

**For Production Use:**
1. Change default passwords in `.env` file
2. Use environment variables instead of hardcoded credentials
3. Enable SSL/TLS
4. Configure proper network security
5. Regular backups

## 📋 Prerequisites

- Docker and Docker Compose installed
- Python 3.7+ with pymongo and faker packages
- Port 27017 and 8081 available

## 🆘 Support

If you encounter issues:
1. Check Docker is running: `docker --version`
2. Check container logs: `./mongodb-docker.sh logs`
3. Verify connections: `./mongodb-docker.sh test`
4. Check container status: `./mongodb-docker.sh status`
