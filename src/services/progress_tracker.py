# src/services/progress_tracker.py
import asyncio
from typing import Dict, Optional
from fastapi import WebSocket
from collections import defaultdict

class ProgressTracker:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.campaign_progress = defaultdict(dict)
        self.lock = asyncio.Lock()

    async def connect(self, campaign_id: str, websocket: WebSocket):
        await websocket.accept()
        async with self.lock:
            self.active_connections[campaign_id] = websocket

    async def disconnect(self, campaign_id: str):
        async with self.lock:
            if campaign_id in self.active_connections:
                del self.active_connections[campaign_id]

    async def update_progress(self, campaign_id: str, sent: int, total: int):
        progress = {
            "sent": sent,
            "total": total,
            "percentage": (sent / total) * 100 if total > 0 else 0
        }
        
        async with self.lock:
            self.campaign_progress[campaign_id] = progress
            if campaign_id in self.active_connections:
                try:
                    await self.active_connections[campaign_id].send_json({
                        "type": "progress_update",
                        "data": progress
                    })
                except Exception as e:
                    await self.disconnect(campaign_id)

    async def get_progress(self, campaign_id: str) -> Optional[dict]:
        async with self.lock:
            return self.campaign_progress.get(campaign_id)

progress_tracker = ProgressTracker()

class RedisProgressTracker:
    async def update_progress(self, campaign_id: str, sent: int, total: int):
        progress = {
            "sent": sent,
            "total": total,
            "percentage": (sent / total) * 100 if total > 0 else 0,
            "timestamp": time.time()
        }
        await redis_client.hset(
            f"campaign:{campaign_id}",
            mapping=progress
        )
        await redis_client.publish(
            f"progress:{campaign_id}",
            json.dumps(progress)
        )