from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QSlider
from PyQt5.QtCore import pyqtSignal, QThread, Qt
from PyQt5.QtGui import QKeySequence, QPalette, QColor
import time, pyautogui, keyboard, os, sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

from SDK.AutoAccept import *
from SDK.RoleCall import *
from SDK.Instalock import *

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setObjectName("MainWindow")
        self.setFixedSize(271, 410)
        self.setWindowTitle("League Tool")
        self.setWindowIcon(QtGui.QIcon(resource_path("imgs/icon.png")))
        self.SetupUI()

    def SetupUI(self):
        self.centralWidget = QtWidgets.QWidget(self)
        self.centralWidget.setObjectName("centralwidget")
        self.setCentralWidget(self.centralWidget)

        # Client Label
        self.clientLabel = QtWidgets.QLabel(self.centralWidget)
        self.clientLabel.setGeometry(QtCore.QRect(10, 10, 251, 21))
        self.clientLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.clientLabel.setObjectName("clientLabel")

        # Auto-Accept Checkbox
        self.aaCheckBox = QtWidgets.QCheckBox(self.centralWidget)
        self.aaCheckBox.setGeometry(QtCore.QRect(10, 30, 101, 31))
        self.aaCheckBox.setObjectName("aaCheckBox")

        # Auto-Role Call
        self.arCheckBox = QtWidgets.QCheckBox(self.centralWidget)
        self.arCheckBox.setGeometry(QtCore.QRect(10, 60, 101, 31))
        self.arCheckBox.setObjectName("arCheckBox")

        # Instalock Select
        self.instaCheckBox = QtWidgets.QCheckBox(self.centralWidget)
        self.instaCheckBox.setGeometry(QtCore.QRect(150, 30, 111, 31))
        self.instaCheckBox.setObjectName("instaCheckBox")

        # Non-Instalock Select
        self.nonInstaCheckBox = QtWidgets.QCheckBox(self.centralWidget)
        self.nonInstaCheckBox.setGeometry(QtCore.QRect(150, 60, 111, 31))
        self.nonInstaCheckBox.setObjectName("nonInstaCheckBox")

        # Pick-A-Role Label
        self.roleLabel = QtWidgets.QLabel(self.centralWidget)
        self.roleLabel.setGeometry(QtCore.QRect(10, 110, 47, 13))
        self.roleLabel.setObjectName("roleLabel")

        # Pick-A-Role TextBox
        self.roleTextBox = QtWidgets.QLineEdit(self.centralWidget)
        self.roleTextBox.setGeometry(QtCore.QRect(10, 130, 251, 20))
        self.roleTextBox.setPlaceholderText("Set text first before checking the box!")
        self.roleTextBox.setObjectName("roleTextBox")

        # Pick-A-Champion Label
        self.championLabel = QtWidgets.QLabel(self.centralWidget)
        self.championLabel.setGeometry(QtCore.QRect(10, 160, 60, 13))
        self.championLabel.setObjectName("championLabel")

        # Pick-A-Champion TextBox
        self.championTextBox = QtWidgets.QLineEdit(self.centralWidget)
        self.championTextBox.setGeometry(QtCore.QRect(10, 180, 251, 20))
        self.championTextBox.setPlaceholderText("Set text first before checking the box!")
        self.championTextBox.setObjectName("championTextBox")

        # Logging
        self.loggingBox = QtWidgets.QTextBrowser(self.centralWidget)
        self.loggingBox.setGeometry(QtCore.QRect(10, 220, 251, 131))
        self.loggingBox.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.loggingBox.setObjectName("loggingBox")

        # Clear Logs Button
        self.clearLogs = QtWidgets.QPushButton(self.centralWidget)
        self.clearLogs.setGeometry(QtCore.QRect(10, 360, 251, 23))
        self.clearLogs.setObjectName("clearLogs")

        # ForceStop Text
        self.forceStopText = QtWidgets.QLabel(self.centralWidget)
        self.forceStopText.setGeometry(QtCore.QRect(80, 90, 111, 31))
        self.forceStopText.setAlignment(QtCore.Qt.AlignCenter)
        self.forceStopText.setObjectName("forceStopText")

        # Events
        self.arCheckBox.stateChanged.connect(self.arCheckBoxChanged)
        self.aaCheckBox.stateChanged.connect(self.aaCheckBoxChanged)
        self.instaCheckBox.stateChanged.connect(self.instaCheckBoxChanged)
        self.nonInstaCheckBox.stateChanged.connect(self.nonInstaCheckBoxChanged)
        self.clearLogs.clicked.connect(lambda: self.loggingBox.clear())

        # Keyboard events
        keyboard.on_press(self.HookKeyboard)

        # UI related
        self.retranslateUI()
        QtCore.QMetaObject.connectSlotsByName(self)


    def retranslateUI(self):
        _translate = QtCore.QCoreApplication.translate
        self.clientLabel.setText(_translate("MainWindow", "Make sure LeagueClient is opened!"))
        self.aaCheckBox.setText(_translate("MainWindow", "Auto-Accept"))
        self.arCheckBox.setText(_translate("MainWindow", "Auto-Role Call"))
        self.instaCheckBox.setText(_translate("MainWindow", "Insta-Lock"))
        self.nonInstaCheckBox.setText(_translate("MainWindow", "Non Insta-Lock"))
        self.forceStopText.setText(_translate("MainWindow", "F1 to force stop!"))
        self.roleLabel.setText(_translate("MainWindow", "Role:"))
        self.championLabel.setText(_translate("MainWindow", "Champion:"))
        self.clearLogs.setText(_translate("MainWindow", "Clear Logs"))

    def arCheckBoxChanged(self, state):
        if state == QtCore.Qt.Checked:
            self.roleCallThread = autoRoleCall(role=self.roleTextBox.text())
            self.roleCallThread.start()
            self.loggingBox.append(f"Role-Call thread started with string: \"{self.roleTextBox.text()}\"")
            self.roleCallThread.roleCallAppendText.connect(self.loggingBox.append)
            self.roleCallThread.roleCallEnd.connect(lambda: self.arCheckBox.setChecked(False))
        else:
            self.loggingBox.append("Role-Call thread stopped.")
            self.roleCallThread.stop()
            self.roleCallThread.quit()

    def aaCheckBoxChanged(self, state):
        if state == QtCore.Qt.Checked:
            self.autoAcceptThread = autoAccept()
            self.autoAcceptThread.start()
            self.loggingBox.append("Auto-Accept thread started.")
            self.autoAcceptThread.autoAcceptAppendText.connect(self.loggingBox.append)
            self.autoAcceptThread.autoAcceptEnd.connect(lambda: self.aaCheckBox.setChecked(False))
        else:
            self.loggingBox.append("Auto-Accept thread stopped.")
            self.autoAcceptThread.stop()
            self.autoAcceptThread.quit()

    def instaCheckBoxChanged(self, state):
        if state == QtCore.Qt.Checked:
            if self.nonInstaCheckBox.isChecked():
                self.nonInstaCheckBox.setChecked(False)
            
            if self.arCheckBox.isChecked():
                self.instaLockThread = instaLock(roleCall = True, instaLock = True, champion = self.championTextBox.text())
            else:
                self.instaLockThread = instaLock(roleCall = False, instaLock = True, champion = self.championTextBox.text())

            self.instaLockThread.start()
            self.loggingBox.append(f"Insta-Lock thread started with string: \"{self.championTextBox.text()}\"")
            self.instaLockThread.instaLockAppendText.connect(self.loggingBox.append)
            self.instaLockThread.instaLockEnd.connect(lambda: self.instaCheckBox.setChecked(False))
        else:
            self.loggingBox.append("Insta-Lock thread stopped.")
            self.instaLockThread.stop()
            self.instaLockThread.quit()

    def nonInstaCheckBoxChanged(self, state):
        if state == QtCore.Qt.Checked:
            if self.instaCheckBox.isChecked():
                self.instaCheckBox.setChecked(False)

            if self.arCheckBox.isChecked():
                self.nonInstaLockThread = instaLock(roleCall = True, instaLock = False, champion = self.championTextBox.text())
            else:
                self.nonInstaLockThread = instaLock(roleCall = False, instaLock = False, champion = self.championTextBox.text())

            self.nonInstaLockThread.start()
            self.loggingBox.append(f"Non Insta-Lock thread started with string: \"{self.championTextBox.text()}\"")
            self.nonInstaLockThread.instaLockAppendText.connect(self.loggingBox.append)
            self.nonInstaLockThread.instaLockEnd.connect(lambda: self.nonInstaCheckBox.setChecked(False))
        else:
            self.loggingBox.append("Non Insta-Lock thread stopped.")
            self.nonInstaLockThread.stop()
            self.nonInstaLockThread.quit()

    def HookKeyboard(self, key):
        if key.name == "f1":
            self.aaCheckBox.setCheckState(False)
            self.arCheckBox.setCheckState(False)
            self.instaCheckBox.setCheckState(False)
            self.nonInstaCheckBox.setCheckState(False)