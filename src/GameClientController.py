import requests

from backend.Board import Tile
from shared.Coordinate import Coordinate
from shared.enums import BoardLayout, Direction, TokenType
from shared.Move import Move
from shared.TokenLine import TokenLine


class GameClientController:
    def __init__(self) -> None:
        self._port = "8000"
        self._api = f"http://127.0.0.1:{self._port}"

    """Game Initialization & Destruction"""

    def create_game(self, board_layout: BoardLayout) -> None:
        body = {"board_layout": board_layout.value}
        r = requests.post(f"{self._api}/create_game", json=body)
        r.raise_for_status()

    def clear_game(self) -> None:
        r = requests.post(f"{self._api}/clear_game")
        r.raise_for_status()

    """Game Saving & Loading"""

    def save_game(self, save_name: str) -> None:
        body = {"save_name": save_name}
        r = requests.post(f"{self._api}/save_game", json=body)
        r.raise_for_status()

    def get_save_games(self) -> list[str]:
        r = requests.get(f"{self._api}/save_games")
        r.raise_for_status()
        return r.json()

    def load_game(self, save_name: str) -> None:
        body = {"save_name": save_name}
        r = requests.post(f"{self._api}/load_game", json=body)
        r.raise_for_status()

    """Movement"""

    def play_move(self, move: Move) -> None:
        body = {"move": move}
        r = requests.post(f"{self._api}/play_move", json=body)
        r.raise_for_status()

    def get_valid_shift_directions(self, c1: Coordinate, c2: Coordinate) -> list[Direction]:
        body = {"c1": c1, "c2": c2}
        r = requests.get(f"{self._api}/valid_shift_directions", json=body)
        r.raise_for_status()
        return r.json()

    """Game State"""

    def is_game_active(self) -> bool:
        r = requests.get(f"{self._api}/is_game_active")
        r.raise_for_status()
        return r.json()

    def get_active_player(self) -> TokenType:
        r = requests.get(f"{self._api}/active_player")
        r.raise_for_status()
        return TokenType(r.json())

    def get_board_array(self) -> list[list[Tile]]:
        r = requests.get(f"{self._api}/board_array")
        r.raise_for_status()
        
        board_dict: list[list[dict]] = r.json()
        board_list = [item for row in board_dict for item]
        
        raise Exception(r.json())
        # return 

    def get_board_dict(self) -> dict[Coordinate, TokenType]:
        r = requests.get(f"{self._api}/board_dict")
        r.raise_for_status()
    
        dict_list: list[tuple[tuple[int, int, int], int]] = r.json()
        board_dict = {Coordinate(*item[0]): TokenType(item[1])  for item in dict_list}
        
        return board_dict

    def get_winning_lines(self) -> list[TokenLine]:
        r = requests.get(f"{self._api}/winning_lines")
        r.raise_for_status()
        return r.json()
