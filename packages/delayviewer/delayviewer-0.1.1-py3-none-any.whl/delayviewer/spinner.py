#!/usr/bin/env python3
# ------------------------------------------------------------------------------------------------------
# -- Spinner controls for displayed shell content
# ------------------------------------------------------------------------------------------------------
# ======================================================================================================

from itertools import cycle
from threading import Thread

import time
from datetime import datetime

from quickcolor.color_def import color

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

class Spinner:
    def __init__(self):
        self._running = True
        self._active = False

    def start(self, startingMsg='', startingMsgSpacer=70):
        if startingMsgSpacer > 0:
            print(f'{startingMsg:<{startingMsgSpacer}}', end='       ', flush=True)
        else:
            print(f'{startingMsg} ... ', end='  ', flush=True)
        self._active = True
        self.startTime = time.time()

    def stop(self, endingMsg='Done!'):
        self._active = False
        print(f'\b \b', sep='', end='', flush=True)
        delay = time.time() - self.startTime
        self.dt = datetime.fromtimestamp(delay)
        delayColor = f'{color.CYELLOW}' if delay < 60.0 else f'{color.CRED2}'
        print(f"{endingMsg} (took {delayColor}{self.dt.strftime('%Mm %Ss')}{color.CEND})")
        # return f"{self.dt.strftime('%M min %S sec %f')[:-3]} msec"

    def terminate(self):
        self._running = False

    def thread_loop(self):
        while self._running:
            if not self._active:
                continue
            for self._next_chevron in cycle(r'-\|/'):
                print(f"\b{self._next_chevron}", sep='', end='', flush=True)
                time.sleep(0.1)
                if not self._active:
                    break

# ------------------------------------------------------------------------------------------------------

def handle_spinner(f):
    def wrapper(*args, **kwargs):
        spinnerInstance = Spinner()
        spinnerThread = Thread(target=spinnerInstance.thread_loop)
        spinnerThread.daemon = True
        spinnerThread.start()

        retVal = f(*args, **kwargs, spinner=spinnerInstance)

        spinnerInstance.terminate()
        spinnerThread.join()

        return retVal
    return wrapper

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

