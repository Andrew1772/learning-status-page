from fastapi import FastAPI, WebSocket, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from pydantic import BaseModel
import json

import database

# ============================================================
# GAME VARIABLES
# Change these from Python
# ============================================================

app = FastAPI()
templates = Jinja2Templates(directory="templates")

default_players = [
    {
        "name": "Player 1",
        "color": "red"
    },
    {
        "name": "Player 2",
        "color": "green"
    },
    {
        "name": "Player 3",
        "color": "purple"
    },
    {
        "name": "Player 4",
        "color": "yellow"
    }
]


# ============================================================
# WEB SERVER
# ============================================================


#class ConnectionManager:
#    def __init__(self):
#        self.active_connection: Websocket
#
#    def connect(self, websocket: WebSocket):
#        websocket.accept()
#        self.active_connection.append(websocket)
#
#    def disconnect(self, websocket: WebSocket):
#        self.active_connection.remove(websocket)
#
#
#manager = ConnectionManager()


@app.get("/")
async def homepage(request: Request):
    players = database.get_players()
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "players": players,
        }
    )

@app.get("/create_player")
async def create_player_page():
    return FileResponse("static/create_player.html")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    while True:
        data = await websocket.receive_json()

        database.create_new_player(data["username"], data["color"])



print("MTG Life Tracker running!")
print("Open http://localhost:8000")
