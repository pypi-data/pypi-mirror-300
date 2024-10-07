#!/usr/bin/env python3
# ------------------------------------------------------------------------------------------------------
# -- Time & Delay methods
# ------------------------------------------------------------------------------------------------------
# ======================================================================================================

# PYTHON_ARGCOMPLETE_OK
import argcomplete, argparse

import sys
import os
import time
from datetime import datetime

from quickcolor.color_def import colors

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

def sec_sleep_ticks(sleepMsg, numSec):
    # sleep avoidance
    if numSec == 0:
        print(f" --> {sleepMsg} (no sleep)")
        return

    print(f" --> {sleepMsg} ({numSec} sec)", end=' ', flush=True)
    for sec in range(0,numSec):
        time.sleep(0.92)
        print(".", end='', flush=True)

    print(" - done!")

# ------------------------------------------------------------------------------------------------------

def timedelta_formatter(timedelta: datetime):
    hours, minutes_and_seconds = divmod(timedelta.seconds, 3600)
    minutes, seconds = divmod(minutes_and_seconds, 60)
    hrStr = ''
    if hours:
        hrStr=f"{hours:02} hours "
    return f"{hrStr}{minutes:02} minutes {seconds:02} seconds"

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

def time_show(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        retval = func(*args, **kwargs)
        dt = datetime.fromtimestamp(time.time() - start)
        print (f" ..... {colors.fg.boldred}runtime: {colors.fg.boldwhite}{dt.strftime('%M min %S sec %f')[:-3]} msec{colors.off}")
        return retval
    return wrapper

# ------------------------------------------------------------------------------------------------------

def time_execution(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        retval = func(*args, **kwargs)
        dt = datetime.fromtimestamp(time.time() - start)
        print(f"{colors.fg.green}{func.__name__}{colors.off} ran in {colors.fg.yellow}{dt.strftime('%M min %S sec %f')[:-3]} msec{colors.off}")
        return retval
    return wrapper

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

