from fastapi import FastAPI, WebSocket, Request
from fastapi.templating import Jinja2Templates
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
def homepage(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "players": default_players,
        }
    )

class Player(BaseModel):
    uid: str
    username: str
    color: str


@app.post("/create_player")
def create_player(player: Player):
    return





print("MTG Life Tracker running!")
print("Open http://localhost:8000")

