#!/bin/bash

echo "🚀 Starting Airflow IoT ETL/ELT Demo..."
echo "📁 Project directory: $(pwd)"

# Check if all required files exist
echo "🔍 Checking project files..."
required_files=("docker-compose.yml" ".env" "dags/etl_iot_pipeline.py" "dags/elt_iot_pipeline.py" "data/sensors.csv" "data/readings.csv")

for file in "${required_files[@]}"; do
    if [[ -f "$file" ]]; then
        echo "✅ $file"
    else
        echo "❌ $file - MISSING!"
        exit 1
    fi
done

# Start services
echo ""
echo "🐳 Starting Docker services..."
docker compose up -d

# Wait for services to be healthy
echo ""
echo "⏳ Waiting for services to be ready..."
echo "This may take a few minutes on first run..."

# Wait for postgres
echo "📦 Waiting for PostgreSQL..."
while ! docker compose exec postgres pg_isready -U airflow -d airflow_db -h localhost -p 5432 > /dev/null 2>&1; do
    sleep 2
    echo -n "."
done
echo " ✅ PostgreSQL is ready!"

# Wait for webserver
echo "🌐 Waiting for Airflow webserver..."
for i in {1..60}; do
    if curl -f http://localhost:8080/health > /dev/null 2>&1; then
        echo " ✅ Airflow webserver is ready!"
        break
    fi
    if [ $i -eq 60 ]; then
        echo " ❌ Timeout waiting for webserver"
        docker compose logs airflow-webserver
        exit 1
    fi
    sleep 5
    echo -n "."
done

echo ""
echo "🎉 Environment is ready!"
echo ""
echo "📊 Access points:"
echo "   Airflow UI: http://localhost:8080"
echo "   Username: admin"
echo "   Password: admin"
echo ""
echo "🔧 Useful commands:"
echo "   docker compose ps                    # Check services status"
echo "   docker compose logs -f               # Follow all logs"
echo "   docker compose logs airflow-webserver # Check webserver logs"
echo "   docker compose exec postgres psql -U airflow -d dwh # Connect to database"
echo ""
echo "📚 Available DAGs:"
echo "   - etl_iot_pipeline: Transform data in memory (pandas)"
echo "   - elt_iot_pipeline: Transform data in database (SQL)"
echo ""
echo "🚀 Ready to go! Open http://localhost:8080 in your browser!"