# src/api/endpoints.py (updated)
from fastapi import WebSocket, WebSocketDisconnect
from services.progress_tracker import progress_tracker

@app.websocket("/ws/progress/{campaign_id}")
async def websocket_progress(websocket: WebSocket, campaign_id: str):
    await progress_tracker.connect(campaign_id, websocket)
    try:
        while True:
            # Keep connection alive
            await websocket.receive_text()
            
            # Send current progress immediately when client asks
            progress = await progress_tracker.get_progress(campaign_id)
            if progress:
                await websocket.send_json({
                    "type": "progress_update",
                    "data": progress
                })
                
    except WebSocketDisconnect:
        await progress_tracker.disconnect(campaign_id)

app.mount("/static", StaticFiles(directory="src/static"), name="static")

@app.get("/dashboard")
async def get_dashboard(campaign_id: str):
    return FileResponse("src/static/dashboard.html")