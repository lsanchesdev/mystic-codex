from modules.battle import Battle
from enums.game_state import GameState
import constants.window as WindowBook
import constants.game_actions as GameActionsBook
import constants.game as GameBook


class Game:

    def __init__(self, codex):
        super().__init__()
        self.codex = codex
        self.state = GameState.NORMAL
        self.battle = Battle(codex)

    def update(self):
        self.state = GameState(self.codex.gatekeeper.read(GameBook.GAME_STATE, 4))

    def openInventory(self):
        self.codex.communicator.sendCommandToWindow(self.codex.player.name + WindowBook.WINDOW_TITLE_INVENTORY,
                                                    GameActionsBook.GAME_ACTION_OPEN_INVENTORY)

    def closeInventory(self):
        self.codex.communicator.closeWindow(self.codex.player.name + WindowBook.WINDOW_TITLE_INVENTORY)

    def openHumanAttributes(self):
        self.codex.communicator.sendCommandToWindow(self.codex.player.name + WindowBook.WINDOW_TITLE_HUMAN_ATTRIBUTES,
                                                    GameActionsBook.GAME_ACTION_OPEN_HUMAN_ATTRIBUTES)

    def closeHumanAttributes(self):
        self.codex.communicator.closeWindow(self.codex.player.name + WindowBook.WINDOW_TITLE_HUMAN_ATTRIBUTES)

    def openWuxingOven(self):
        self.codex.communicator.sendCommandToWindow(WindowBook.WINDOW_TITLE_WUXING_OVEN,
                                                    GameActionsBook.GAME_ACTION_OPEN_WUXING_OVEN)

    def closeWuxingOven(self):
        self.codex.communicator.closeWindow(WindowBook.WINDOW_TITLE_WUXING_OVEN)

    def getState(self, returnValue=False):
        if returnValue:
            return self.state.value
        else:
            return self.state
