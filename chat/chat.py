from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import datetime

import chat.redis_chat as redis

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat Room</title>
    </head>
    <body>
        <h1>WebSocket Login</h1>
        <h2>Your ID: <span id="ws-id"></span></h2>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            let client_id = prompt("Enter your name: ")
            document.querySelector("#ws-id").textContent = client_id;
            var ws = new WebSocket(`ws://localhost:8000/ws/${client_id}`);
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        await load_messages(websocket)
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str, exclude = None):
        for connection in self.active_connections:
            if connection is not exclude:
                await connection.send_text(message)


manager = ConnectionManager()


@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket)
    connection = redis.connect_to_redis()
    try:
        while True:
            data = await websocket.receive_text()
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            await manager.send_personal_message(f"{current_time}: You wrote: {data}", websocket)
            await connection.rpush(client_id, data)
            await manager.broadcast(f"{current_time}: {client_id} says: {data}", exclude = websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")


async def load_messages(websocket):
    connection = redis.connect_to_redis()
    keys = [key async for key in connection.scan_iter("*")]
    for key in keys:
        values = await connection.lrange(key, 0, -1)
        for value in values:
            await manager.send_personal_message(f"Client {key} says {value}", websocket)
    await manager.send_personal_message("All caught up, note that messages may not appear in order", websocket)



