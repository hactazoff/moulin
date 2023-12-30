from src.actor import Actor
from src.constants import Piece
from src.controller import Controller


class View:
    __controller: Controller = None

    def __init__(self):
        pass

    def set_controller(self, controller):
        pass
        
    def add_log(self, message: str):
        pass
    
    def event_player_turn(self, player: Actor, callback: callable):
        pass
        
    def event_player_move(self, player: Actor, piece: Piece, callback: callable):
        pass
    
    def event_player_remove(self, player: Actor, callback: callable):
        pass