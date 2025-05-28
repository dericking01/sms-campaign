# config/settings.py
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # SMS Gateway
    SMS_GATEWAY_URL = os.getenv("SMS_GATEWAY_URL")
    SMS_GATEWAY_USER = os.getenv("SMS_GATEWAY_USER")
    SMS_GATEWAY_PASS = os.getenv("SMS_GATEWAY_PASS")
    
    # Database
    DB_HOST = os.getenv("DB_HOST", "192.168.1.11")
    DB_PORT = int(os.getenv("DB_PORT", 3306))
    DB_USER = os.getenv("DB_USER", "prodafya")
    DB_PASS = os.getenv("DB_PASS", "Afyacall@2021qazWSX")
    DB_NAME = os.getenv("DB_NAME", "afyacallproduction")

    # Redis
    REDIS_HOST = os.getenv("REDIS_HOST", "redis")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
    
    # Campaign
    DLR_CALLBACK_URL = os.getenv("DLR_CALLBACK_URL", "http://localhost:8000/api/dlr")
    MAX_REQUESTS_PER_SECOND = int(os.getenv("MAX_REQUESTS_PER_SECOND", 100))
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 1000))

settings = Settings()