# src/services/rate_limiter.py
import asyncio
from time import time
from typing import Optional
from collections import deque

class RateLimiter:
    def __init__(self, max_calls: int, period: float):
        self.max_calls = max_calls
        self.period = period
        self.calls = deque()
        self.lock = asyncio.Lock()

    async def wait(self) -> Optional[float]:
        async with self.lock:
            now = time()
            
            # Remove calls older than the period
            while self.calls and now - self.calls[0] > self.period:
                self.calls.popleft()
            
            if len(self.calls) >= self.max_calls:
                sleep_time = self.period - (now - self.calls[0])
                await asyncio.sleep(sleep_time)
                return self.wait()
            
            self.calls.append(now)
            return None