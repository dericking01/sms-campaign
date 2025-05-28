# SMS Campaign Service

A FastAPI microservice for sending bulk SMS using Kannel's `sendsms` interface with delivery report tracking support.

## Features
- Async bulk SMS dispatch (2M+ records supported)
- Delivery Report (DLR) endpoint
- Dockerized for microservice environments

## Run
```bash
docker-compose up --build
```

## Start Campaign
```bash
curl http://localhost:8000/start
```

## CSV Format
Ensure the file `csv_data/msisdns.csv` exists with a `msisdn` column.
