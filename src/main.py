# src/main.py
import asyncio
from pathlib import Path
from config import settings
from models.campaign import Campaign
from services.file_processor import FileProcessor
from services.sms_sender import SMSSender
from utils.logger import logger

async def run_campaign(csv_path: Path, message: str, sender_id: str):
    campaign = Campaign(
        id="campaign_001",
        message=message,
        sender_id=sender_id,
        dlr_callback_url=settings.DLR_CALLBACK_URL
    )
    
    sender = SMSSender(
        base_url=settings.SMS_GATEWAY_URL,
        username=settings.SMS_GATEWAY_USER,
        password=settings.SMS_GATEWAY_PASS
    )
    
    try:
        async for msisdn_chunk in FileProcessor.process_csv(csv_path, campaign):
            await sender.send_batch(campaign, msisdn_chunk)
            await asyncio.sleep(0.1)  # Brief pause between chunks
            
    finally:
        await sender.close()

if __name__ == "__main__":
    csv_path = Path("data/input/msisdns.csv")
    message = "Your predefined message here"
    sender_id = "AFYACALL"
    
    asyncio.run(run_campaign(csv_path, message, sender_id))