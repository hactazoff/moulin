from src.controller import Controller
from src.view import View


class ViewConsole(View):
    def __init__(self):
        super().__init__()
        print('Moulin Game')
