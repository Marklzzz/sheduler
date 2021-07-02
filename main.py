from plyer import notification
import sqlite3
import datetime
import threading
from PyQt5.QtWidgets import *
import sys


def check_tasks():
    con = sqlite3.connect("scheduler_db.db")
    cur = con.cursor()
    result = list(sorted(cur.execute("""SELECT * from jobs""").fetchall(), key=lambda x: x[0]))

    return result


class Scheduler(QWidget):
    def __init__(self):
        super().__init__()
        self.con = sqlite3.connect('scheduler_db.db')
        self.cur = self.con.cursor()

        self.btn_add = QPushButton('Добавить', self)
        self.count_of_notification = 0

        self.list_qlines = []

        self.initUI()

    def initUI(self):
        self.setFixedSize(400, 150)
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
        self.setFixedSize(400, 150 + self.count_of_notification * 100)
        self.draw()

    def save(self):
        for i in self.list_qlines:
            if not i[0].text() or not i[1].text():
                break
        else:
            self.cur.execute('DELETE FROM jobs')
            for i in self.list_qlines:
                self.update_db(str(i[0].text()), str(i[1].text()))
        # self.hide()
        self.con.close()
        shed = START(check_tasks())
        self.hide()
        hide(ex)
        shed.start()

    def update_db(self, time, job):
        self.cur.execute('INSERT INTO jobs VALUES ("{}", "{}")'.format(str(time), str(job)))
        self.con.commit()


class START:
    def __init__(self, list_of_tasks):
        self.list_of_tasks = list_of_tasks


    def start(self):
        for i in range(len(self.list_of_tasks)):
            date_and_time = self.list_of_tasks[i][0]  # 27.06.2021 18:00 -> (2021, 6, 27, 18, 0, 0)
            task = self.list_of_tasks[i][1]
            time_now = datetime.datetime.now()
            time_now -= datetime.timedelta(0, 0, time_now.microsecond)

            task_time = datetime.datetime(int(date_and_time[6:10]),
                                          int(date_and_time[3:5]),
                                          int(date_and_time[0:2]),
                                          int(date_and_time[11:13]),
                                          int(date_and_time[14:]))
            timedelta = task_time - time_now

            threading.Timer(timedelta.total_seconds(), print_notification, [task]).start()
        raise SystemExit(1)


def print_notification(task):
    notification.notify("Новая задача начата", task, app_name="sheduler", timeout=10)

def hide(obj):
    obj.hide()


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Планировщик')
        self.setFixedSize(410, 450)
        self.scrollArea = QScrollArea()
        self.scrollArea.setFixedSize(410, 450)
        self.setCentralWidget(self.scrollArea)
        self.widget = Scheduler()
        self.scrollArea.setWidget(self.widget)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())
