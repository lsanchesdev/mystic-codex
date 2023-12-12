import win32gui
import win32con


class Communicator:

    def __init__(self, codex):
        super().__init__()
        self.codex = codex

    def sendCommandToWindow(self, title, command_id=0, class_name='TPUtilWindow'):
        # Find window by title
        window = win32gui.FindWindow(None, title)

        if title is None or window == 0:  # No window found by title
            # Iterate through all windows
            def handle_windows(window_id, parameter):
                if win32gui.GetClassName(window_id) == class_name:
                    win32gui.PostMessage(window_id, win32con.WM_COMMAND, command_id, 0)
                    return True

            win32gui.EnumWindows(handle_windows, None)

    def sendCommand(self, command_id):
        self.sendCommandToWindow(None, command_id)

    def closeWindow(self, title, class_name='TPUtilWindow'):
        # Find window by title
        window = win32gui.FindWindow(None, title)

        if window != 0:
            win32gui.PostMessage(window, win32con.WM_CLOSE, 0, 0)
