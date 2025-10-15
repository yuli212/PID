#!/bin/bash

echo "🔍 Airflow IoT Demo - Status Check"
echo "=================================="

# Check if services are running
echo ""
echo "📊 Service Status:"
docker compose ps

# Check Airflow UI accessibility
echo ""
echo "🌐 Testing Airflow UI..."
if curl -f http://localhost:8080/health > /dev/null 2>&1; then
    echo "✅ Airflow UI is accessible at http://localhost:8080"
else
    echo "❌ Airflow UI is not accessible"
fi

# Check database connectivity
echo ""
echo "🗄️ Testing Database Connection..."
if docker compose exec postgres pg_isready -U airflow -d dwh -h localhost -p 5432 > /dev/null 2>&1; then
    echo "✅ Database 'dwh' is accessible"
    
    # Show available tables
    echo ""
    echo "📋 Tables in DWH database:"
    docker compose exec postgres psql -U airflow -d dwh -c "\dt" 2>/dev/null || echo "No tables found (expected on first run)"
else
    echo "❌ Database is not accessible"
fi

# Check data files
echo ""
echo "📁 Data Files Status:"
echo "Sensors: $(wc -l < data/sensors.csv) lines"
echo "Readings: $(wc -l < data/readings.csv) lines"

echo ""
echo "🔧 Quick Commands:"
echo "   ./start.sh                           # Start/restart environment"
echo "   docker compose logs -f               # Follow logs"
echo "   docker compose down                  # Stop environment"
echo "   docker compose exec postgres psql -U airflow -d dwh  # Connect to DB"

echo ""
echo "📊 Next Steps:"
echo "1. Open http://localhost:8080 (admin/admin)"
echo "2. Enable and trigger the DAGs:"
echo "   - etl_iot_pipeline"
echo "   - elt_iot_pipeline"
echo "3. Compare the results in both summary tables"