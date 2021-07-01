import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *

import sqlite3


class Scheduler(QWidget):
    def __init__(self):
        super().__init__()
        self.btn_add = QPushButton('Добавить', self)
        self.count_of_notification = 0

        self.list_qlines = []

        self.initUI()

    def initUI(self):
        self.setFixedSize(400, 485)
        self.move(300, 300)
        self.setWindowTitle('Планировщик')

        self.btn_add.resize(200, 30)
        self.btn_add.clicked.connect(self.update_widget)

        self.btn_save = QPushButton('Сохранить', self)
        self.btn_save.resize(200, 30)
        self.btn_save.clicked.connect(self.save)
        self.draw()

    def draw(self):
        name = QLineEdit(self)
        num = QLineEdit(self)
        label1 = QLabel(self)
        label2 = QLabel(self)

        name.resize(150, 20)
        num.resize(150, 20)

        label1.setText('Время в формате <дд.мм.гггг чч:мм>')
        label2.setText('Введите напоминание\nв произвольной форме')

        label1.move(10, 10 + 100 * self.count_of_notification)
        name.move(220, 10 + 100 * self.count_of_notification)
        label2.move(10, 40 + 100 * self.count_of_notification)
        num.move(220, 40 + 100 * self.count_of_notification)
        self.btn_add.move(10, 75 + 100 * self.count_of_notification)
        self.btn_save.move(10, 105 + 100 * self.count_of_notification)
        self.list_qlines.append([name, num])

        label1.show()
        label2.show()
        name.show()
        num.show()

    def update_widget(self):
        self.count_of_notification += 1
        self.draw()

    def save(self):
        for i in self.list_qlines:
            if not i[0].text() or not i[1].text():
                break
        else:
            for i in self.list_qlines:
                self.update_db(i[0].text(), i[1].text())

    def update_db(self, time, job):
        con = sqlite3.connect('scheduler_db.db')
        cur = con.cursor()
        spisok = cur.execute('SELECT * FROM jobs WHERE time = {} AND task = {}'.format(time, job)).fetchall()
        print(spisok)
        if not spisok:
            cur.execute('INSERT INTO jobs VALUES ({}, {})'.format(time, job))
            con.commit()



class Example(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(500, 250)
        self.scrollArea = QtWidgets.QScrollArea()
        self.scrollArea.setFixedSize(500, 250)
        self.setCentralWidget(self.scrollArea)
        self.widget = Scheduler()
        self.scrollArea.setWidget(self.widget)
        self.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = Scheduler()
    ex.show()
    sys.exit(app.exec_())
