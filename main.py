import playsound
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QSlider,
    QProgressBar,
)
from PyQt5.QtCore import QTimer, Qt, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

import sys

sys.path.insert(0, "Systems")

from Systems.ui import EngineSimulator


if __name__ == "__main__":
    app = QApplication([])
    ex = EngineSimulator()
    app.exec_()
