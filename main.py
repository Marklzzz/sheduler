from plyer import notification
import sqlite3
import datetime
import time
import threading

task = ''


class Window:
    def __init__(self):
        pass

    def check_tasks(self):
        con = sqlite3.connect("scheduler_db.db")
        cur = con.cursor()

        result = sorted(cur.execute("""SELECT * from jobs""").fetchall(), key=lambda x: x[0])

        return result


class Scheduler:
    def __init__(self, list_of_tasks):
        self.list_of_tasks = list_of_tasks

    def start(self):
        global task
        for i in range(len(self.list_of_tasks)):
            date_and_time = self.list_of_tasks[i][0]  # 27.06.2021 18:00 -> (2021, 6, 27, 18, 0, 0)
            task_ = self.list_of_tasks[i][1]
            time_now = datetime.datetime.now()
            time_now -= datetime.timedelta(0, 0, time_now.microsecond)

            task_time = datetime.datetime(int(date_and_time[6:10]),
                                          int(date_and_time[3:5]),
                                          int(date_and_time[0:2]),
                                          int(date_and_time[11:13]),
                                          int(date_and_time[14:]))
            timedelta = task_time - time_now
            time_in_sec = timedelta.seconds
            task = task_

            do_something_delayed = make_delayed(time_in_sec)(foo)
            do_something_delayed()


def foo():
    global task
    notification.notify("Новая задача начата", task, app_name="scheduler", timeout=10)


def make_delayed(delay_in_seconds):
    class CallDelayer:
        def __init__(self):
            self.call_event = threading.Event()
            self.last_call_time = time.time()

        def launch_with_delay(self, function):
            def launched_with_delay(*args, **kwargs):
                self.last_call_time += delay_in_seconds
                wait_sec = self.last_call_time - time.time()
                self.call_event.wait(wait_sec)
                function(*args, **kwargs)

            return launched_with_delay

    call_delayer = CallDelayer()
    return call_delayer.launch_with_delay


win = Window()
sched = Scheduler(win.check_tasks())

sched.start()
