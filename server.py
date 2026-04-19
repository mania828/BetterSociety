from fastapi import FastAPI, WebSocket

app = FastAPI()

clients = []

@app.get("/")
def home():
    return {"status": "online"}

@app.websocket("/ws")
async def ws(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)

    try:
        while True:
            msg = await websocket.receive_text()

            for c in clients:
                if c != websocket:
                    await c.send_text(msg)

    except:
        clients.remove(websocket)