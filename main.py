import sys
import random
from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QPainter, QColor, QBrush


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('UI.ui', self)
        self.color = QColor('#FFFD14')
        self.painter = QPainter(self)
        self.btn.clicked.connect(self.update)
        self.way = False

    def update(self):
        self.way = True
        self.repaint()

    def paintEvent(self, event):
        if self.way:
            try:
                self.painter.begin(self)
                self.painter.setBrush(QBrush(Qt.GlobalColor.yellow, Qt.BrushStyle.Dense1Pattern))
                self.painter.setPen(Qt.GlobalColor.red)
                coords = (0, 0)
                for x in range(3):
                    side = random.randint(20, 90)
                    self.painter.drawEllipse(*coords, side, side)
                    x = random.randint(20, 100)
                    y = random.randint(30, 110)
                    coords = (coords[0] + x, coords[0] + y)
                self.painter.end()

            except Exception as e:
                print(e)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MyWidget()
    win.show()
    sys.exit(app.exec())

