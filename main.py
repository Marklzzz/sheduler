from plyer import notification
import sqlite3
import datetime
import threading


def check_tasks():
    con = sqlite3.connect("scheduler_db.db")
    cur = con.cursor()

    result = sorted(cur.execute("""SELECT * from jobs""").fetchall(), key=lambda x: x[0])

    return result


class Scheduler:
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


def print_notification(task):
    notification.notify("Новая задача начата", task, app_name="scheduler", timeout=10)


sched = Scheduler(check_tasks())

sched.start()
