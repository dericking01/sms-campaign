# src/services/file_processor.py
import csv
import asyncio
from typing import AsyncIterator, List
from pathlib import Path
from models.campaign import Campaign
from utils.logger import logger

class FileProcessor:
    CHUNK_SIZE = 1000  # Adjust based on memory constraints
    
    @staticmethod
    async def process_csv(file_path: Path, campaign: Campaign) -> AsyncIterator[List[str]]:
        """Yield chunks of MSISDNs from CSV file"""
        try:
            with open(file_path, 'r') as f:
                reader = csv.DictReader(f)
                chunk = []
                
                for row in reader:
                    msisdn = row['msisdn'].strip()
                    if msisdn:
                        chunk.append(msisdn)
                    
                    if len(chunk) >= self.CHUNK_SIZE:
                        yield chunk
                        chunk = []
                
                if chunk:  # Yield remaining records
                    yield chunk
        
        except Exception as e:
            logger.error(f"Error processing file: {str(e)}")
            raise