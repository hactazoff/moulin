from src.actor import Actor
from src.constants import Color

class Player(Actor):
    def __init__(self, name: str, color: Color | None = None, max_pieces: int | None = None):
        super().__init__(name, color, max_pieces)