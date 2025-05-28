# utils/helpers.py
import csv
from typing import List, Any
from pathlib import Path

def chunk_list(lst: List[Any], chunk_size: int) -> List[List[Any]]:
    """Yield successive chunk_size chunks from lst."""
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]

def validate_msisdn(msisdn: str) -> bool:
    """Basic MSISDN validation for Tanzanian numbers"""
    return msisdn.startswith('255') and len(msisdn) == 12 and msisdn.isdigit()

def count_csv_rows(file_path: Path) -> int:
    """Count rows in CSV file efficiently"""
    with open(file_path, 'r') as f:
        return sum(1 for row in csv.reader(f)) - 1  # Subtract header