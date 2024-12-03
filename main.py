# Эспрессо (программа для отображения информации о кофе из базы данных)
import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QPushButton, QPlainTextEdit
import sqlite3


class AddWidget(QMainWindow):
    def __init__(self, parent):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.parent = parent
        self.sender = ''

    def know_sender(self, sender: str):
        self.sender = sender
        print(self.sender)
        self.update_view()

    def update_view(self):
        if self.sender == "Добавить данные":
            print('I1 - > add')
            self.id_form.setEnabled(False)
            self.pushButton.setText('Добавить')
            self.pushButton.clicked.connect(self.adding)
        else:
            print('I2 - > update')
            self.id_form.setEnabled(True)
            ids = self.parent.cur.execute("""SELECT ID FROM coffee""").fetchall()
            self.id_form.addItems([str(x[0]) for x in ids])
            self.pushButton.setText('Обновить')
            self.pushButton.clicked.connect(self.updating)

    def check_forms(self):
        title = self.title_form.toPlainText().strip()
        degree_roasting = self.degree_roasting_form.currentText()
        ground_or_grains = self.ground_or_grains_form.currentText()
        taste = self.description_taste_form.toPlainText().strip()
        price = self.price_form.toPlainText().strip()
        pack = self.packaging_form.currentText()
        try:
            if not all([title, taste, price]):
                self.statusBar().showMessage('Неверно заполнена форма')
            elif not price.isdigit():
                self.statusBar().showMessage('Ошибка в указании цены')
            else:
                return title, degree_roasting, ground_or_grains, taste, price, pack,

        except Exception as e:
            print(e)
            self.statusBar().showMessage('Неверно заполнена форма')
        return None

    def adding(self):
        print('add_11')
        lst = self.check_forms()
        if lst is not None:
            self.parent.adding_main(*lst)
            self.close()

    def updating(self):
        print('upp__2')
        lst = self.check_forms()
        if lst is not None:
            self.parent.updating_main(self.id_form.currentText(), *lst)
            self.close()


class Coffee(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.database = sqlite3.connect('coffee.sqlite')
        self.cur = self.database.cursor()
        self.full_table()

        self.update_btn = QPushButton('Обновить данные', self)
        self.update_btn.setGeometry(100, 550, 150, 30)
        self.update_btn.clicked.connect(self.update_data)

        self.create_btn = QPushButton('Добавить данные', self)
        self.create_btn.setGeometry(300, 550, 150, 30)
        self.create_btn.clicked.connect(self.create_data)

        #  Окно добавления и обновления
        self.adding_widget = AddWidget(self)

    def full_table(self):
        result = self.cur.execute("""SELECT * FROM coffee""").fetchall()

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

    def update_data(self):
        self.adding_widget = AddWidget(self)
        self.adding_widget.know_sender(self.sender().text())
        self.adding_widget.show()

    def create_data(self):
        self.adding_widget = AddWidget(self)
        self.adding_widget.know_sender(self.sender().text())
        self.adding_widget.show()

    def adding_main(self, title, degree_roasting, ground_or_grains, taste, price, pack):
        print("ADD")
        self.cur.execute(""" INSERT INTO coffee
         (title, degree_roasting, ground_or_grains, description_taste, price, packaging)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (title, degree_roasting, ground_or_grains, taste, price, pack))
        self.database.commit()
        self.full_table()

    def updating_main(self, id, title, degree_roasting, ground_or_grains, taste, price, pack):
        print('UPDATE', id)
        self.cur.execute("""
         UPDATE coffee
         SET title = ?, degree_roasting = ?, ground_or_grains = ?, description_taste = ?, price = ?, packaging = ?
         WHERE ID = ?""", (title, degree_roasting, ground_or_grains, taste, price, pack, id))
        self.database.commit()
        self.full_table()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Coffee()
    win.show()
    sys.exit(app.exec())

