# src/services/sms_sender.py
import httpx
import asyncio
from typing import List
from models.campaign import Campaign
from models.dlr import DLR
from utils.logger import logger
from utils.helpers import chunk_list

class SMSSender:
    def __init__(self, base_url: str, username: str, password: str):
        self.base_url = base_url
        self.auth = (username, password)
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def send_single(self, campaign: Campaign, msisdn: str) -> DLR:
        params = {
            'username': self.auth[0],
            'password': self.auth[1],
            'from': campaign.sender_id,
            'to': msisdn,
            'text': campaign.message,
            'dlr-mask': 31,
            'dlr-url': f"{campaign.dlr_callback_url}?campaign_id={campaign.id}&msisdn={msisdn}"
        }
        
        try:
            response = await self.client.get(self.base_url, params=params)
            return DLR(
                campaign_id=campaign.id,
                msisdn=msisdn,
                status_code=response.status_code,
                response_text=response.text
            )
        except Exception as e:
            logger.error(f"Failed to send to {msisdn}: {str(e)}")
            return DLR(
                campaign_id=campaign.id,
                msisdn=msisdn,
                status_code=500,
                response_text=str(e)
            )
    
    async def send_batch(self, campaign: Campaign, msisdns: List[str]) -> List[DLR]:
        tasks = [self.send_single(campaign, msisdn) for msisdn in msisdns]
        return await asyncio.gather(*tasks, return_exceptions=True)
    
    async def close(self):
        await self.client.aclose()