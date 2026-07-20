from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
)

from PySide6.QtGui import QFont

from actions import open_program
from program_scanner import load_database


class ProgramsWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Jarvis - Programme & Spiele")
        self.resize(550, 700)

        self.setStyleSheet("""
            QWidget{
                background:#16181d;
                color:white;
            }

            QLineEdit{
                background:#252830;
                border:1px solid #444;
                border-radius:6px;
                padding:8px;
                font-size:14px;
            }

            QListWidget{
                background:#1d2027;
                border:none;
                font-size:14px;
            }

            QListWidget::item{
                padding:8px;
            }

            QListWidget::item:selected{
                background:#ff6a21;
                color:white;
            }
        """)

        layout = QVBoxLayout(self)

        self.search = QLineEdit()
        self.search.setPlaceholderText("Programm suchen...")

        self.list = QListWidget()

        layout.addWidget(self.search)
        layout.addWidget(self.list)

        self.programme = load_database()

        self.search.textChanged.connect(self.filter)
        self.list.itemDoubleClicked.connect(self.start_program)

        self.fill()

    def fill(self):

        self.list.clear()

        for name in sorted(self.programme):

            item = QListWidgetItem(name.title())

            font = QFont()
            font.setPointSize(11)

            item.setFont(font)

            self.list.addItem(item)

    def filter(self, text):

        text = text.lower()

        self.list.clear()

        for name in sorted(self.programme):

            if text in name:

                item = QListWidgetItem(name.title())

                font = QFont()
                font.setPointSize(11)

                item.setFont(font)

                self.list.addItem(item)

    def start_program(self, item):

        open_program(item.text())