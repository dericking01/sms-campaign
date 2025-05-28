# src/repositories/campaign_repo.py
import aiomysql
from models.campaign import Campaign
from config.database import Database

class CampaignRepository:
    @staticmethod
    async def create_campaign(campaign: Campaign):
        async with (await Database.get_pool()).acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    """
                    INSERT INTO sms_campaigns 
                    (id, message, sender_id, dlr_callback_url, status, total_recipients)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (campaign.id, campaign.message, campaign.sender_id, 
                     campaign.dlr_callback_url, campaign.status, campaign.total_recipients)
                )

    @staticmethod
    async def update_campaign_status(campaign_id: str, status: str):
        async with (await Database.get_pool()).acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    "UPDATE sms_campaigns SET status = %s WHERE id = %s",
                    (status, campaign_id)
                )