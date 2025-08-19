#!/bin/bash

# MongoDB Docker Setup Script
# This script manages the MongoDB Docker container setup

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if Docker is running
check_docker() {
    if ! docker --version > /dev/null 2>&1; then
        print_error "Docker is not installed or not in PATH"
        exit 1
    fi
    
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker daemon is not running"
        exit 1
    fi
    
    print_status "Docker is running"
}

# Function to start MongoDB
start_mongodb() {
    print_status "Starting MongoDB with Docker Compose..."
    
    # Stop any existing containers
    docker-compose down --remove-orphans
    
    # Start the services
    docker-compose up -d
    
    print_status "Waiting for MongoDB to be ready..."
    sleep 10
    
    # Check if MongoDB is responding
    for i in {1..30}; do
        if docker exec financial_data_mongodb mongosh --eval "db.runCommand('ping')" > /dev/null 2>&1; then
            print_status "MongoDB is ready!"
            break
        fi
        if [ $i -eq 30 ]; then
            print_error "MongoDB failed to start after 30 attempts"
            exit 1
        fi
        print_status "Waiting for MongoDB... ($i/30)"
        sleep 2
    done
}

# Function to show connection info
show_connection_info() {
    echo ""
    print_status "=== MongoDB Connection Information ==="
    echo "Database Name: financial_data"
    echo "MongoDB URI: mongodb://admin:password123@localhost:27017/financial_data"
    echo "Admin User: admin / password123"
    echo "App User: financial_user / financial_pass"
    echo ""
    print_status "=== Mongo Express Web UI ==="
    echo "URL: http://localhost:8081"
    echo "Username: admin"
    echo "Password: admin123"
    echo ""
    print_status "=== Docker Container Info ==="
    echo "MongoDB Container: financial_data_mongodb"
    echo "Mongo Express Container: financial_data_mongo_express"
    echo ""
}

# Function to test connection
test_connection() {
    print_status "Testing MongoDB connection..."
    
    # Test basic connection with authentication
    if docker exec financial_data_mongodb mongosh -u admin -p password123 --authenticationDatabase admin --eval "
        db = db.getSiblingDB('financial_data');
        print('Connected to database: ' + db.getName());
        print('Collections: ' + db.getCollectionNames());
    " --quiet; then
        print_status "Connection test successful!"
    else
        print_error "Connection test failed!"
        exit 1
    fi
}

# Function to show logs
show_logs() {
    print_status "Showing MongoDB logs (press Ctrl+C to exit)..."
    docker-compose logs -f mongodb
}

# Function to stop MongoDB
stop_mongodb() {
    print_status "Stopping MongoDB containers..."
    docker-compose down
    print_status "MongoDB stopped"
}

# Function to cleanup (remove containers and volumes)
cleanup() {
    print_warning "This will remove all MongoDB data permanently!"
    read -p "Are you sure? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_status "Removing containers and volumes..."
        docker-compose down -v --remove-orphans
        docker volume prune -f
        print_status "Cleanup complete"
    else
        print_status "Cleanup cancelled"
    fi
}

# Function to import sample data
import_sample_data() {
    print_status "Importing sample dataNAV data..."
    
    if [ ! -f "dataNAV_sample.json" ]; then
        print_warning "Sample data file not found. Generating..."
        /Volumes/D/Ai/python/dataset/.venv/bin/python generate_sample_data.py
    fi
    
    # Use the Python import script with correct Python path
    /Volumes/D/Ai/python/dataset/.venv/bin/python import_to_mongodb.py
    
    print_status "Sample data imported successfully!"
}

# Main script logic
case "${1:-}" in
    "start")
        check_docker
        start_mongodb
        show_connection_info
        test_connection
        ;;
    "stop")
        stop_mongodb
        ;;
    "restart")
        check_docker
        stop_mongodb
        start_mongodb
        show_connection_info
        test_connection
        ;;
    "logs")
        show_logs
        ;;
    "status")
        docker-compose ps
        ;;
    "test")
        test_connection
        ;;
    "import")
        import_sample_data
        ;;
    "cleanup")
        cleanup
        ;;
    "info")
        show_connection_info
        ;;
    *)
        echo "MongoDB Docker Management Script"
        echo ""
        echo "Usage: $0 {start|stop|restart|logs|status|test|import|cleanup|info}"
        echo ""
        echo "Commands:"
        echo "  start    - Start MongoDB and Mongo Express containers"
        echo "  stop     - Stop all containers"
        echo "  restart  - Restart all containers"
        echo "  logs     - Show MongoDB logs"
        echo "  status   - Show container status"
        echo "  test     - Test MongoDB connection"
        echo "  import   - Import sample dataNAV data"
        echo "  cleanup  - Remove containers and volumes (DESTRUCTIVE)"
        echo "  info     - Show connection information"
        echo ""
        exit 1
        ;;
esac
