from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List
import json

app = FastAPI()

# كلاس لإدارة الاتصالات (مين فاتح التطبيق دلوقتي)
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"✅ جهاز جديد اتصل. الإجمالي: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        print(f"❌ جهاز قفل التطبيق. الإجمالي: {len(self.active_connections)}")

    async def broadcast(self, message: str):
        # إرسال الرسالة لكل الناس اللي فاتحين التطبيق
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.get("/")
def read_root():
    return {"message": "🚀 سيرفر تيليجرام الخاص يعمل بنجاح!"}

# مسار الـ WebSocket اللي التطبيق (Flutter) هيكلمه
@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # استلام الرسالة من أي موبايل
            data = await websocket.receive_text()
            
            # إعادة إرسالها لكل الموبايلات التانية (Real-time)
            await manager.broadcast(data)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
