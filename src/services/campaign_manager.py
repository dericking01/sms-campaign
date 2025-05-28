# src/services/campaign_manager.py (updated)
class CampaignManager:
    def __init__(self):
        self.sender = None
        self.sent_count = 0

    async def start_campaign(self, csv_path: Path, message: str, sender_id: str):
        total_recipients = helpers.count_csv_rows(csv_path)
        campaign = Campaign(
            id=f"campaign_{int(time.time())}",
            message=message,
            sender_id=sender_id,
            dlr_callback_url=settings.DLR_CALLBACK_URL,
            status="running",
            total_recipients=total_recipients
        )

        try:
            await CampaignRepository.create_campaign(campaign)
            self.sender = SMSSender(settings.SMS_GATEWAY_URL, 
                                   settings.SMS_GATEWAY_USER, 
                                   settings.SMS_GATEWAY_PASS)

            # Initialize progress
            await progress_tracker.update_progress(campaign.id, 0, total_recipients)

            async for msisdn_chunk in FileProcessor.process_csv(csv_path, campaign):
                dlrs = await self.sender.send_batch(campaign, msisdn_chunk)
                await asyncio.gather(*[DLRRepository.save_dlr(dlr) for dlr in dlrs])
                
                # Update progress
                self.sent_count += len(msisdn_chunk)
                await progress_tracker.update_progress(
                    campaign.id, 
                    self.sent_count, 
                    total_recipients
                )
                
                await asyncio.sleep(0.1)

            await CampaignRepository.update_campaign_status(campaign.id, "completed")

        except Exception as e:
            logger.error(f"Campaign failed: {str(e)}")
            await CampaignRepository.update_campaign_status(campaign.id, "failed")
            raise

        finally:
            if self.sender:
                await self.sender.close()