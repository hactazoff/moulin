# moulin map
# 0 = empty
# 1 = way
# 2 = destination point
default_map = [
    '2111112111112',
    '1000001000001',
    '1021112111201',
    '1010001000101',
    '1010212120101',
    '1010100010101',
    '2121200021212',
    '1010100010101',
    '1010212120101',
    '1010001000101',
    '1021112111201',
    '1000001000001',
    '2111112111112'
]

initial_max_pieces = 9
nb_line_piece = 3

map_points = {
    'destination_point': 2,
    'way': 1,
    'empty': 0
}

MapRaw = list[str]
MapParsed = list[list[int]]

Color = str
colors: list[Color] = [
    "BLACK",
    "WHITE",
    "RED",
    "BLUE",
    "GREEN",
    "YELLOW",
    "CYAN",
    "MAGENTA"
]

Piece = tuple[int, int]