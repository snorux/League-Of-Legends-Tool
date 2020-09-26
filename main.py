import SDK.MainWindow as sdk
import traceback

def excepthook(exc_type, exc_value, exc_tb):
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    print("error catched!:")
    print("error message:\n", tb)
    sdk.QtWidgets.QApplication.quit()

if __name__ == "__main__":
    import sys
    sys.excepthook = excepthook
    app = sdk.QApplication(sys.argv)
    app.setStyle("Fusion")
    palette = sdk.QPalette()
    palette.setColor(sdk.QPalette.Window, sdk.QColor(53, 53, 53))
    palette.setColor(sdk.QPalette.WindowText, sdk.Qt.white)
    palette.setColor(sdk.QPalette.Base, sdk.QColor(25, 25, 25))
    palette.setColor(sdk.QPalette.AlternateBase, sdk.QColor(53, 53, 53))
    palette.setColor(sdk.QPalette.ToolTipBase, sdk.Qt.white)
    palette.setColor(sdk.QPalette.ToolTipText, sdk.Qt.white)
    palette.setColor(sdk.QPalette.Text, sdk.Qt.white)
    palette.setColor(sdk.QPalette.Button, sdk.QColor(53, 53, 53))
    palette.setColor(sdk.QPalette.ButtonText, sdk.Qt.white)
    palette.setColor(sdk.QPalette.BrightText, sdk.Qt.red)
    palette.setColor(sdk.QPalette.Link, sdk.QColor(42, 130, 218))
    palette.setColor(sdk.QPalette.Highlight, sdk.QColor(42, 130, 218))
    palette.setColor(sdk.QPalette.HighlightedText, sdk.Qt.black)
    app.setPalette(palette)
    win = sdk.MainWindow()
    win.show()
    sys.exit(app.exec_())