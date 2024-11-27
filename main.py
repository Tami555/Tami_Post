import sys
import random
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt6.QtGui import QPainter, QColor, QBrush


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 524, 550)

        self.btn = QPushButton('клик', self)
        self.btn.setGeometry(170, 430, 211, 41)
        self.btn.clicked.connect(self.update)

        self.painter = QPainter(self)
        self.way = False

    def update(self):
        self.way = True
        self.repaint()

    @staticmethod
    def random_color():
        color_lst = []
        for x in range(3):
            color_lst.append(random.randint(0, 255))
        return QColor(*color_lst)

    def paintEvent(self, event):
        if self.way:
            self.painter.begin(self)
            coords = (0, 0)
            for x in range(5):
                side = random.randint(20, 140)
                self.painter.setBrush(QBrush(self.random_color(), Qt.BrushStyle.Dense1Pattern))
                self.painter.drawEllipse(*coords, side, side)
                x = random.randint(20, 250)
                y = random.randint(20, 250)
                coords = (coords[0] + x, coords[0] + y)
            self.painter.end()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MyWidget()
    win.show()
    sys.exit(app.exec())

