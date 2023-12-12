import constants.window as WindowBook
import constants.game_actions as GameActions

class Game:

    def __init__(self, codex):
        super().__init__()
        self.codex = codex

    def openInventory(self):
        self.codex.communicator.sendCommandToWindow(self.codex.player.name + WindowBook.WINDOW_TITLE_INVENTORY,
                                                    GameActions.GAME_ACTION_OPEN_INVENTORY)

    def closeInventory(self):
        self.codex.communicator.closeWindow(self.codex.player.name + WindowBook.WINDOW_TITLE_INVENTORY)

    def openHumanAttributes(self):
        self.codex.communicator.sendCommandToWindow(self.codex.player.name + WindowBook.WINDOW_TITLE_HUMAN_ATTRIBUTES,
                                                    GameActions.GAME_ACTION_OPEN_HUMAN_ATTRIBUTES)

    def closeHumanAttributes(self):
        self.codex.communicator.closeWindow(self.codex.player.name + WindowBook.WINDOW_TITLE_HUMAN_ATTRIBUTES)

    def openWuxingOven(self):
        self.codex.communicator.sendCommandToWindow(WindowBook.WINDOW_TITLE_WUXING_OVEN,
                                                    GameActions.GAME_ACTION_OPEN_WUXING_OVEN)

    def closeWuxingOven(self):
        self.codex.communicator.closeWindow(WindowBook.WINDOW_TITLE_WUXING_OVEN)

    def beginBattle(self):
        self.codex.communicator.sendCommand(GameActions.GAME_ACTION_BEGIN_BATTLE)