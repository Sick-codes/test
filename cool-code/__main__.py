from fastapi import FastAPI, WebSocket
import uvicorn
import websockets


app = FastAPI()


class handler:
    def __init__(self) -> None:
        self.test = []

    async def add_client(self):
        async with websockets.connect("ws://127.0.0.1:8080") as websocket:
            self.test.append(websocket.host)
        
    async def Send(self, webSocket:WebSocket):
        for i in self.test:
            await webSocket.send_text("hello from real server")
        

    
inst = handler()

@app.websocket("/test")
async def e(wb:WebSocket):
    await wb.accept
    await inst.Send(wb)