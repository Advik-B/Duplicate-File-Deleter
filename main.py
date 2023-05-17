from utility import QuickHasher
from utility.settings import MAX_BUFFER_SIZE
from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtCore import QFileInfo, QDir, QThread, pyqtSignal
from PyQt6.uic import loadUi
from pathlib import Path

class GUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()
        self.show()

    def setupUI(self):
        loadUi(Path(__file__).parent.joinpath("interface.xml"), self)
        with open(Path(__file__).parent.joinpath("interface.colours.css"), "rb") as file:
            self.setStyleSheet(file.read().decode("utf-8"))



if __name__ == "__main__":
    app = QApplication([])
    gui = GUI()
    app.exec()
