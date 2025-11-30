import asyncio
import os
from dataclasses import astuple
from typing import Annotated

from fastapi import Body, FastAPI, HTTPException, WebSocket, WebSocketDisconnect

from backend.Game import Game
from shared.Coordinate import Coordinate
from shared.enums import BoardLayout, Direction, GameEvent, MoveType

app = FastAPI()
_game: Game | None = None
_event_queue: asyncio.Queue[GameEvent] = asyncio.Queue()

"""
GameServerController

The 'backend' side of the controller layer, allows view to interface with model

Could not be implemented as a class due to FastAPI limitations, tried to 
keep it pseudo-object-oriented

"""


"""Game Initialization & Destruction"""


@app.post("/game")
def create_game(board_layout: Annotated[BoardLayout, Body(embed=True)]):
    """Create a new game"""
    global _game
    _game = Game(board_layout)
    _event_queue.put_nowait(GameEvent.GameCreated)


@app.delete("/game")
def clear_game():
    """Delete the active game"""
    global _game
    _game = None
    _event_queue.put_nowait(GameEvent.GameCleared)


"""Movement Selection"""


@app.post("/move_type")
def set_move_type(move_type: Annotated[MoveType, Body(embed=True)]):
    if not _game:
        raise HTTPException(status_code=400, detail="No game is active")
    _game.set_move_type(move_type)
    _event_queue.put_nowait(GameEvent.GameStateUpdated)


@app.get("/move_type")
def get_move_type():
    if not _game:
        raise HTTPException(status_code=400, detail="No game is active")
    return _game.get_move_type()


"""Coordinate Selection"""


@app.post("/deselect_coordinate")
def deselect_coords(c: Coordinate):
    if not _game:
        raise HTTPException(status_code=400, detail="No game is active")
    _game.deselect_coord(c)
    _event_queue.put_nowait(GameEvent.GameStateUpdated)


@app.post("/select_coordinate")
def select_coord(c: Coordinate):
    if not _game:
        raise HTTPException(status_code=400, detail="No game is active")
    _game.select_coord(c)
    _event_queue.put_nowait(GameEvent.GameStateUpdated)


@app.get("/coordinates")
def get_selected_coords():
    if not _game:
        raise HTTPException(status_code=400, detail="No game is active")
    return _game.get_selected_coords()


@app.get("/selectable_coordinates")
def get_selectable_coords():
    if not _game:
        raise HTTPException(status_code=400, detail="No game is active")
    return _game.get_selectable_coords()


"""Direction Selection"""


@app.post("/shift_direction")
def set_shift_direction(direction: Annotated[Direction, Body(embed=True)]):
    if not _game:
        raise HTTPException(status_code=400, detail="No game is active")
    _event_queue.put_nowait(GameEvent.GameStateUpdated)
    return _game.set_shift_direction(direction)


@app.get("/shift_direction")
def get_shift_direction():
    """Returns a list of valid directions which a pair of coordinates can move in on the active game board"""
    if not _game:
        raise HTTPException(status_code=400, detail="No game is active")
    return _game.get_shift_direction()


@app.get("/valid_shift_directions")
def get_valid_shift_directions():
    if not _game:
        raise HTTPException(status_code=400, detail="No game is active")
    return _game.get_valid_shift_directions()


"""Movement Execution"""


@app.get("/is_move_playable")
def is_move_playable():
    """Returns True if the actively selected move is valid and playable, False otherwise"""
    if not _game:
        raise HTTPException(status_code=400, detail="No game is active")
    return _game.is_move_playable()


@app.post("/play_move")
def play_move():
    """Play a single move"""
    if not _game:
        raise HTTPException(status_code=400, detail="No game is active")
    _game.play_move()
    _event_queue.put_nowait(GameEvent.GameStateUpdated)


"""Getting Game State"""


@app.get("/is_game_active")
def is_game_active():
    """Returns True if there is an active game, False otherwise"""
    return _game != None


@app.get("/active_player")
def get_active_player():
    """Returns the token type of the active player in the game"""
    if not _game:
        raise HTTPException(status_code=400, detail="No game is active")
    return _game.current_player


@app.get("/board_array")
def get_board_array():
    """Returns the game board as a 2D array of tiles"""
    if not _game:
        raise HTTPException(status_code=400, detail="No game is active")
    board_array = _game.board.get_2d_cell_list()
    frozen_board = [[(astuple(tile.coord), tile.token) for tile in row] for row in board_array]
    return frozen_board


@app.get("/board_dict")
def get_board_dict():
    """Returns the game board as a dict mapping tile coordinates to their token types"""
    if not _game:
        raise HTTPException(status_code=400, detail="No game is active")
    board_dict = _game.board.get_board_dict()
    frozen_board = [(astuple(item[0]), item[1].value) for item in board_dict.items()]
    return frozen_board


@app.get("/winning_lines")
def get_winning_lines():
    """Returns all lines which meet the requirements to win"""
    if not _game:
        raise HTTPException(status_code=400, detail="No game is active")
    return _game.get_winning_lines()


"""Game Saving & Loading"""


@app.post("/save_game")
def save_game(save_name: Annotated[str, Body(embed=True)]):
    """Create a save with a given name for the active game"""
    if not _game:
        raise HTTPException(status_code=400, detail="No game is active")

    os.makedirs("saves", exist_ok=True)
    _game.save_to_file(f"saves/{save_name}")
    _event_queue.put_nowait(GameEvent.GameSaved)


@app.get("/save_games")
def get_save_games():
    """Returns a list of the save games in the 'saves' folder"""
    os.makedirs("saves", exist_ok=True)
    return [os.fsdecode(save_files) for save_files in os.listdir("saves")]


@app.post("/load_game")
def load_game(save_name: Annotated[str, Body(embed=True)]):
    """Load a game save from the saves folder as the new active game"""
    global _game
    _game = Game.load_from_file(f"saves/{save_name}")
    _event_queue.put_nowait(GameEvent.GameCreated)


"""WebSocket"""


class ConnectionManager:
    """Manages individual websocket connections, template from FastAPI docs"""

    def __init__(self):
        self.active_connections: set[WebSocket] = set()

    async def connect(self, websocket: WebSocket):
        """Accept a websocket connection, adding it to our set of tracked connections"""
        await websocket.accept()
        self.active_connections.add(websocket)

    def disconnect(self, ws: WebSocket):
        """Kill a websocket connection"""
        self.active_connections.discard(ws)

    async def send_indv_message(self, message: str, ws: WebSocket):
        """Send a message to a single websocket client"""
        await ws.send_text(message)

    async def broadcast(self, message: str):
        """Broadcast a message to a all connected websocket client"""
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                print(f"Error broadcasting message: {e.__str__()}")


_ws_manager = ConnectionManager()


@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await _ws_manager.connect(ws)
    try:
        # While the websocket is active:
        while True:
            # Check for events to broadcast
            try:
                event = await asyncio.wait_for(_event_queue.get(), timeout=0.05)
                await _ws_manager.broadcast(event.value)

            # If no events found, ping the websocket
            except asyncio.TimeoutError:
                await ws.send_text("ping")

    except WebSocketDisconnect:
        print(f"Client disconnected: {ws.client}")
    finally:
        _ws_manager.disconnect(ws)
        print(f"Active clients: {len(_ws_manager.active_connections)}")
