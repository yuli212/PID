#!/bin/bash

echo "🧪 Testing Airflow IoT ETL/ELT Pipelines"
echo "======================================="

# Test database connectivity
echo ""
echo "🔗 Testing database connections..."
docker compose exec postgres psql -U airflow -d dwh -c "SELECT 'DWH Database Connected!' as status;" || exit 1

# Check DAG status via API
echo ""
echo "📋 Checking DAGs status..."
DAGS_RESPONSE=$(curl -s -u admin:admin http://localhost:8080/api/v1/dags)

if echo $DAGS_RESPONSE | grep -q "etl_iot_pipeline"; then
    echo "✅ ETL Pipeline DAG found"
else
    echo "❌ ETL Pipeline DAG not found"
fi

if echo $DAGS_RESPONSE | grep -q "elt_iot_pipeline"; then
    echo "✅ ELT Pipeline DAG found"
else
    echo "❌ ELT Pipeline DAG not found"
fi

# Test data files
echo ""
echo "📊 Data files verification..."
echo "Sensors data sample:"
head -3 data/sensors.csv

echo ""
echo "Readings data sample:"
head -5 data/readings.csv

echo ""
echo "🎯 Ready for Demo!"
echo ""
echo "📖 Demo Steps:"
echo "1. Open http://localhost:8080"
echo "2. Login: admin / admin"
echo "3. Find and enable these DAGs:"
echo "   - etl_iot_pipeline (Transform in Memory)"
echo "   - elt_iot_pipeline (Transform in Database)" 
echo "4. Trigger both DAGs manually"
echo "5. Compare execution times and results"
echo ""
echo "🔍 After running DAGs, check results:"
echo "   docker compose exec postgres psql -U airflow -d dwh"
echo "   SELECT * FROM daily_sensor_summary_etl;"
echo "   SELECT * FROM daily_sensor_summary_elt;"
echo ""
echo "🏁 Have fun exploring ETL vs ELT patterns!"