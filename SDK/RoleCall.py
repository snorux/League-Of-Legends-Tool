from SDK.MainWindow import *

class autoRoleCall(QThread):
    roleCallAppendText = QtCore.pyqtSignal(str)
    roleCallEnd = QtCore.pyqtSignal()

    def __init__(self, role):
        QThread.__init__(self)
        self.continue_run = True
        self.role = role

    def run(self):
        while self.continue_run:
            roleCallBox = pyautogui.locateOnScreen(resource_path("imgs/top.png"), confidence = 0.9)
            if roleCallBox is not None:
                pyautogui.moveTo(roleCallBox)
                pyautogui.move(-200, 577)
                pyautogui.click()
                pyautogui.write(self.role)
                pyautogui.press("enter")
                self.roleCallAppendText.emit(f"Entered role: \"{self.role}\"")
                self.roleCallEnd.emit()
            time.sleep(0.1)

    def stop(self):
        self.continue_run = False