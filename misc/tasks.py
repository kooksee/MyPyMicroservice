# -*- coding:utf-8 -*-
import logging
import threading
import time

logger = logging.getLogger("tasks.project")


class PeriodicCallback(object):
    def __init__(self, callback, callback_time):
        self.callback = callback
        if callback_time <= 0:
            raise ValueError("Periodic callback must have a positive callback_time")
        self.callback_time = callback_time
        self._running = False

    def start(self):
        self._running = True
        threading.Thread(target=self._schedule_next).start()

    def stop(self):
        """Stops the timer."""
        self._running = False

    def _schedule_next(self):
        while self._running:
            time.sleep(self.callback_time)
            self.callback()
