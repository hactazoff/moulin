import random
import time
from src.constants import Color, Piece, colors


class Actor:
    __name: str = str(int(time.time()))
    __color: Color = random.choice(colors)

    def __init__(self, name: str, color: Color | None = None, max_pieces: int | None = None):
        self.set_name(name)
        if color is not None:
            self.set_color(color)
        if max_pieces is not None:
            self.set_max_pieces(max_pieces)

    def set_color(self, color: Color) -> Color | None:
        if color not in colors:
            return None
        self.__color = color
        return self.__color

    def set_name(self, name: str) -> str:
        self.__name = name

    def get_color(self) -> Color:
        return self.__color
    
    def get_name(self) -> str:
        return self.__name
    
    def get_instance(self) -> 'Model':
        return self.__instance
    
    def set_instance(self, instance: 'Model') -> 'Model':
        self.__instance = instance
        return self.__instance
    
    __max_pieces: int = 0

    def set_max_pieces(self, max_pieces: int) -> int:
        self.__max_pieces = max_pieces
        return self.__max_pieces
    
    def get_max_pieces(self) -> int:
        return self.__max_pieces
    
    __pieces: list[Piece] = []
    def get_pieces(self) -> list[Piece]:
        return self.__pieces
    
    def add_piece(self, piece: Piece) -> list[Piece] | None:
        if len(self.__pieces) >= self.__max_pieces:
            return None
        self.__pieces.append(piece)
        return self.__pieces
    
    def remove_piece(self, piece: Piece) -> list[Piece]:
        self.__pieces.remove(piece)
        return self.__pieces
    
    def reset(self):
        self.__pieces = []
        
    def owner_piece(self, x: int, y: int) -> bool:
        return (x, y) in self.__pieces
        