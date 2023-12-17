from enum import Enum


class GameState(Enum):
    NORMAL = 1010
    BATTLE = 1009
    CHANGING_MAPS = 1008
    DIALOG = 1011
