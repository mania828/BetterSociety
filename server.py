from fastapi import FastAPI, WebSocket
import asyncio
app = FastAPI()

clients = set()

@app.get("/")
def home():
    return {"status": "online"}

@app.websocket("/ws")
async def ws(websocket: WebSocket):
    await websocket.accept()
    clients.add(websocket)

    try:
        while True:
            msg = await websocket.receive_text()

            for c in list(clients):
                try:
                    await c.send_text(msg)
                except:
                    clients.discard(c)
                    asyncio.create_task(keep_alive(websocket))

    except:
        clients.discard(websocket)

        

async def keep_alive(websocket: WebSocket):
    while True:
        try:
            await websocket.send_text("__ping__")
            await asyncio.sleep(20)
        except:
            break
