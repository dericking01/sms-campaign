# tests/test_file_processor.py
import pytest
from pathlib import Path
from src.services.file_processor import FileProcessor
from src.models.campaign import Campaign

@pytest.fixture
def sample_csv(tmp_path):
    csv_path = tmp_path / "test.csv"
    csv_path.write_text("msisdn\n255123456789\n255987654321")
    return csv_path

@pytest.mark.asyncio
async def test_process_csv(sample_csv):
    campaign = Campaign(
        id="test",
        message="Test",
        sender_id="TEST",
        dlr_callback_url="http://test.com/dl"
    )
    
    processor = FileProcessor()
    chunks = []
    
    async for chunk in processor.process_csv(sample_csv, campaign):
        chunks.append(chunk)
    
    assert len(chunks) == 1
    assert chunks[0] == ["255123456789", "255987654321"]