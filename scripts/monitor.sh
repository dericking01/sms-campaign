#!/bin/bash
# scripts/monitor.sh

# Monitor the SMS campaign progress
watch -n 5 '
echo "Container Status:"
docker-compose ps | grep sms-campaign
echo
echo "Logs:"
docker-compose logs --tail=5 sms-campaign
'