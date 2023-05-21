from PyQt6 import QtGui

from utility.algorithms import QuickHasher
from utility.settings import MAX_BUFFER_SIZE
from PyQt6.QtWidgets import QWidget, QApplication, QFrame, QPushButton
from PyQt6.QtCore import QFileInfo, QDir, QThread, pyqtSignal
from PyQt6.uic import loadUi
from pathlib import Path
from QtLogger import QtLogger
from PyQt6.QtGui import QFont


class GUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()
        self.show()

    def setupUI(self):
        loadUi(Path(__file__).parent.joinpath("interface.xml"), self)

        self.logger_placeholder: QFrame = self.findChildren(QFrame, "logs_placeholder")[0]
        # Now that we have the placeholder, we can create the logger and replace the placeholder with it
        # First get the placeholder's parent so we can replace the placeholder with the logger
        self.logger_container: QWidget = self.logger_placeholder.parent()
        self.logger = QtLogger(
            load_previous_logs=True,
            font=QFont("Consolas", 10),
            log_folder="logs",
            display_level="all",
        )
        self.logger_container.layout().replaceWidget(self.logger_placeholder, self.logger)
        self.logger_placeholder.deleteLater()
        self.logger.start()
        self.copyLogsButton: QPushButton = self.findChildren(QPushButton, "copy_logs_btn")[0]
        self.copyLogsButton.clicked.connect(self.copyLogs)




    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.logger.info("Closing application")
        self.logger.stop()
        super().closeEvent(a0)

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        self.logger.debug(f"Resizing window to {a0.size()}")
        super().resizeEvent(a0)


    def copyLogs(self):
        logs = self.logger.logger_view.toPlainText()
        clipboard = app.clipboard()
        clipboard.setText(logs)
        del logs, clipboard




if __name__ == "__main__":
    app = QApplication([])
    gui = GUI()
    app.exec()
