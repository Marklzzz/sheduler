string = "abcdea fghebi baj kl f jbmn aopqjqc jekehj"
import threading
import time


def make_delayed(delay_in_seconds):
    """
    Decorator with parameter for making functions
    launched with minimal delay between calls
    """

    if delay_in_seconds <= 0:
        raise ValueError("Non-positive delay: {}".format(delay_in_seconds))

    class CallDelayer:
        def __init__(self):
            self.call_event = threading.Event()
            self.last_call_time = time.time()

        def launch_with_delay(self, function):
            def launched_with_delay(*args, **kwargs):
                self.last_call_time += delay_in_seconds
                function(*args, **kwargs)
                wait_sec = self.last_call_time - time.time()
                self.call_event.wait(wait_sec)

            return launched_with_delay

    call_delayer = CallDelayer()
    return call_delayer.launch_with_delay


def foo():
    print('aaa')


do_something_delayed = make_delayed(1)(foo)
for i in range(10):
    do_something_delayed()
