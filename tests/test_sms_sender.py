# tests/test_sms_sender.py
import pytest
from unittest.mock import AsyncMock, patch
from src.services.sms_sender import SMSSender
from src.models.campaign import Campaign

@pytest.mark.asyncio
async def test_send_single():
    mock_client = AsyncMock()
    mock_client.get.return_value.status_code = 200
    mock_client.get.return_value.text = "OK"
    
    with patch('httpx.AsyncClient', return_value=mock_client):
        sender = SMSSender("http://test.com", "user", "pass")
        campaign = Campaign(
            id="test",
            message="Test message",
            sender_id="TEST",
            dlr_callback_url="http://test.com/dl"
        )
        
        result = await sender.send_single(campaign, "255123456789")
        assert result.status_code == 200
        await sender.close()