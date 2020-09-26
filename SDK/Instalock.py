from SDK.MainWindow import *

class instaLock(QThread):
    instaLockAppendText = QtCore.pyqtSignal(str)
    instaLockEnd = QtCore.pyqtSignal()

    def __init__(self, roleCall, instaLock, champion):
        QThread.__init__(self)
        self.continue_run = True
        self.roleCall = roleCall
        self.instaLock = instaLock
        self.champion = champion

    def run(self):
        while self.continue_run:
            if self.roleCall:
                # Give some time for the role call function to work
                time.sleep(1.5)

            championSearch = pyautogui.locateOnScreen(resource_path("imgs/search.png"), confidence = 0.9)
            if championSearch is not None:
                pyautogui.moveTo(championSearch)
                pyautogui.move(10, 0)
                pyautogui.click()
                pyautogui.write(self.champion)
                topLane = pyautogui.locateOnScreen(resource_path("imgs/top.png"), confidence = 0.9)
                if topLane is not None:
                    pyautogui.moveTo(topLane)
                    pyautogui.move(20, 55)
                    pyautogui.click()
                    time.sleep(1)
                    if self.instaLock:
                        while True:
                            lockIn = pyautogui.locateOnScreen(resource_path("imgs/lock_in.png"), confidence = 0.9)
                            if lockIn is not None:
                                pyautogui.moveTo(lockIn)
                                pyautogui.click()
                                self.instaLockAppendText.emit(f"Selected \"{self.champion}\" and locked...")
                                self.instaLockEnd.emit()
                                break
                    else:
                        self.instaLockAppendText.emit(f"Selected \"{self.champion}\"...")
                        self.instaLockEnd.emit()
            time.sleep(3)



    def stop(self):
        self.continue_run = False