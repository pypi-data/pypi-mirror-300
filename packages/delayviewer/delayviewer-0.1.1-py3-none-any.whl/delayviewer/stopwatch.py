#!/usr/bin/env python3
# ------------------------------------------------------------------------------------------------------
# -- Stopwatch controls for displayed shell content
# ------------------------------------------------------------------------------------------------------
# ======================================================================================================

from itertools import cycle
from threading import Thread

import time
from datetime import datetime

from quickcolor.color_def import color

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

class Stopwatch:
    def __init__(self):
        self._running = True
        self._active = False

    def start(self, startingMsg='', startingMsgSpacer=70):
        print(f'{startingMsg:<{startingMsgSpacer}}', end='       ', flush=True)
        self._active = True
        self.startTime = time.time()

    def stop(self, endingMsg='Done!'):
        self._active = False
        print(f'\b\b\b\b\b     \b\b\b\b\b', sep='', end='', flush=True)
        delay = time.time() - self.startTime
        self.dt = datetime.fromtimestamp(delay)
        delayColor = f'{color.CYELLOW2}' if delay < 60.0 else f'{color.CRED2}'
        print(f"{endingMsg} (took {delayColor}{self.dt.strftime('%Mm %Ss')}{color.CEND})")
        # return f"{self.dt.strftime('%M min %S sec %f')[:-3]} msec"

    def terminate(self):
        self._running = False

    def thread_loop(self):
        while self._running:
            if self._active:
                time.sleep(0.92)
                self.dt = datetime.fromtimestamp(time.time() - self.startTime + 1)
                if self._running:
                    print(f"\b\b\b\b\b{self.dt.strftime('%M:%S')}", sep='', end='', flush=True)

# ------------------------------------------------------------------------------------------------------

def handle_stopwatch(f):
    def wrapper(*args, **kwargs):
        stopwatchInstance = Stopwatch()
        stopwatchThread = Thread(target=stopwatchInstance.thread_loop)
        stopwatchThread.daemon = True
        stopwatchThread.start()

        retVal = f(*args, **kwargs, stopwatch=stopwatchInstance)

        stopwatchInstance.terminate()
        stopwatchThread.join()

        return retVal
    return wrapper

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

