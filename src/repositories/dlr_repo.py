# src/repositories/dlr_repo.py
import aiomysql
from models.dlr import DLR
from config.database import Database

class DLRRepository:
    @staticmethod
    async def save_dlr(dlr: DLR):
        async with (await Database.get_pool()).acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    """
                    INSERT INTO sms_delivery_reports 
                    (campaign_id, msisdn, status_code, response_text, status, error_code)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (dlr.campaign_id, dlr.msisdn, dlr.status_code, 
                     dlr.response_text, dlr.status, dlr.error_code)
                )

    @staticmethod
    async def update_dlr_status(update):
        async with (await Database.get_pool()).acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    """
                    UPDATE sms_delivery_reports 
                    SET status = %s, error_code = %s 
                    WHERE campaign_id = %s AND msisdn = %s
                    """,
                    (update.status, update.error_code, update.campaign_id, update.msisdn)
                )