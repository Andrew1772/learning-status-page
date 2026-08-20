from fastapi import FastAPI, WebSocket, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from pydantic import BaseModel
import json

# ============================================================
# GAME VARIABLES
# Change these from Python
# ============================================================

app = FastAPI()
templates = Jinja2Templates(directory="templates")

default_players = [
    {
        "name": "Player 1",
        "life": 40,
        "color": "red"
    },
    {
        "name": "Player 2",
        "life": 40,
        "color": "green"
    },
    {
        "name": "Player 3",
        "life": 40,
        "color": "purple"
    },
    {
        "name": "Player 4",
        "life": 40,
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
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "players": default_players,
        }
    )

@app.get("/create_player")
async def create_player_page():
    return FileResponse("static/create_player.html")


# Data coming FROM the browser
class CreatePlayer(BaseModel):
    username: str
    color: str


# Your actual Player object
class Player():
    def __init__(self, username, color):
        self.username = username
        self.color = color



@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    data = await websocket.receive_json()

    player_data = CreatePlayer(**data)

    player = Player(
        username=player_data.username,
        color=player_data.color,
    )


    await websocket.send_json({
        "success": True,
        "message": f"Created user {player.username}"
    })



print("MTG Life Tracker running!")
print("Open http://localhost:8000")

