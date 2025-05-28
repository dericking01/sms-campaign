#!/bin/bash
# scripts/deploy.sh

# Build and deploy the SMS campaign system
docker-compose down
docker-compose build
docker-compose up -d --scale sms-campaign=4  # Adjust number of workers as needed

# Wait for services to start
sleep 10

# Monitor deployment status
docker-compose ps