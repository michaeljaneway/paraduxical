from dataclasses import astuple
from typing import Annotated

from fastapi import Body, FastAPI

from backend.GameService import GameService
from shared.Coordinate import Coordinate
from shared.enums import BoardLayout
from shared.Move import Move

app = FastAPI()
service = GameService()

"""Game Initialization & Destruction"""


@app.post("/create_game")
def create_game(board_layout: Annotated[BoardLayout, Body(embed=True)]):
    service.create_game(board_layout)


@app.post("/clear_game")
def clear_game():
    service.clear_game()


"""Game Saving & Loading"""


@app.post("/save_game")
def save_game(save_name: Annotated[str, Body(embed=True)]):
    service.save_game(save_name)


@app.get("/save_games")
def get_save_games():
    return service.get_save_games()


@app.post("/load_game")
def load_game(save_name: Annotated[str, Body(embed=True)]):
    service.load_game(save_name)


"""Movement"""


@app.post("/play_move")
def play_move(move: Move):
    service.play_move(move)


@app.get("/valid_shift_directions")
def get_valid_shift_directions(c1: Coordinate, c2: Coordinate):
    return service.get_valid_shift_directions(c1, c2)


"""Game State"""


@app.get("/is_game_active")
def is_game_active():
    return service.is_game_active()


@app.get("/active_player")
def get_active_player():
    return service.get_active_player()


@app.get("/board_array")
def get_board_array():
    return service.get_board_array()


@app.get("/board_dict")
def get_board_dict():
    board = service.get_board_dict()
    frozen_board = [(astuple(item[0]), item[1].value) for item in board.items()]
    return frozen_board


@app.get("/winning_lines")
def get_winning_lines():
    return service.get_winning_lines()
