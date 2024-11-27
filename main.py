# Эспрессо (программа для отображения информации о кофе из базы данных)
import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem
import sqlite3


class Coffee(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.create_database()

    def create_database(self):
        self.database = sqlite3.connect('coffee.sqlite').cursor()
        result = self.database.execute("""
        SELECT * FROM coffee
        """).fetchall()

        titles = ["ID", 'название сорта', 'степень обжарки',
                  'молотый/в зернах', 'описание вкуса', 'цена', 'объем упаковки']
        self.tableWidget.setColumnCount(len(titles))
        self.tableWidget.setHorizontalHeaderLabels(titles)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnWidth(0, 50)
        self.tableWidget.setColumnWidth(2, 150)
        self.tableWidget.setColumnWidth(3, 150)

        for i, x in enumerate(result):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for e, y in enumerate(x):
                self.tableWidget.setItem(i, e, QTableWidgetItem(str(y)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Coffee()
    win.show()
    sys.exit(app.exec())

