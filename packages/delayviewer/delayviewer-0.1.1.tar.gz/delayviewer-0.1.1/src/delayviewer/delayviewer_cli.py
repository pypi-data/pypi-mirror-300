#!/usr/bin/env python3
# ------------------------------------------------------------------------------------------------------
# -- CLI for delay viewer constructs (Spinner, Stopwatch, delays, etc)
# ------------------------------------------------------------------------------------------------------
# ======================================================================================================

# PYTHON_ARGCOMPLETE_OK
import argcomplete, argparse

import time
import sys

from quickcolor.color_def import color, colors
from showexception.showexception import exception_details

from .spinner import Spinner, handle_spinner
from .stopwatch import Stopwatch, handle_stopwatch

from .time_and_delay import time_execution, time_show, sec_sleep_ticks

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

@handle_spinner
@time_execution
def test_spinner(spinner=None):
    for run, seconds in enumerate([1, 5, 10]):
        spinner.start(f'Testing Spinner {color.CBLUE2}{run+1:<3}{color.CEND} for {color.CYELLOW2}{seconds:>3} sec{color.CEND} ....... ', startingMsgSpacer=100)
        time.sleep(seconds)
        spinner.stop()

# ------------------------------------------------------------------------------------------------------

@handle_stopwatch
@time_execution
def test_stopwatch(stopwatch=None):
    for run, seconds in enumerate([1, 5, 10]):
        stopwatch.start(f'Testing Stopwatch {color.CBLUE2}{run+1:<3}{color.CEND} for {color.CYELLOW2}{seconds:>3} sec{color.CEND} ....... ', startingMsgSpacer=100)
        time.sleep(seconds)
        stopwatch.stop()

# ------------------------------------------------------------------------------------------------------

@time_show
def test_time_show(seconds:int):
    print(f"Testing the time show function wrapper delaying execution for {color.CYELLOW2}{seconds} sec{color.CEND}!")
    time.sleep(seconds)

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

def cli():
    try:
        parser = argparse.ArgumentParser(
                    description=f'{"-." * 3}  {color.CBLUE2}Delay viewer {color.CYELLOW2}elements{color.CEND} for python scripts',
                    epilog='-.' * 40)

        subparsers = parser.add_subparsers(dest='cmd')

        parser_testSpinner = subparsers.add_parser('spinner', help="test Spinner graphic for viewing thru execution delays")
        parser_testStopwatch = subparsers.add_parser('stopwatch', help="test StopWatch for viewing thru execution delays")

        parser_testTimeShow = subparsers.add_parser('time.show', help="test time show wrapper")
        parser_testTimeShow.add_argument(
                '--sec',
                metavar='<sec>',
                type=int,
                default=5,
                help='number of seconds to delay for time show')

        parser_testSleepTicks = subparsers.add_parser('sleep.ticks', help="test sleeping ticks progress viewer")
        parser_testSleepTicks.add_argument(
                '--sec',
                metavar='<numSec>',
                help='num sec to sleep',
                type=int,
                choices=range(1, 20),
                default=3)
        parser_testSleepTicks.add_argument(
                '--fc',
                metavar='<colorName>',
                help='foreground color',
                choices=[
                    'black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'lightgrey',
                    'boldgrey', 'boldred', 'boldgreen', 'boldyellow', 'boldblue', 'boldmagenta',
                    'boldcyan', 'boldwhite', 'darkgrey', 'lightred', 'lightgreen', 'lightyellow',
                    'lightblue', 'lightmagenta', 'lightcyan' ],
                default='green')
        parser_testSleepTicks.add_argument(
                '--bc',
                metavar='<colorName>',
                help='background color',
                choices=[ 'black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'lightgrey' ],
                default=None)

        argcomplete.autocomplete(parser)
        args = parser.parse_args()
        # print(args)

        if len(sys.argv) == 1:
            parser.print_help(sys.stderr)
            sys.exit(1)

        if args.cmd == 'spinner':
            test_spinner()

        elif args.cmd == 'stopwatch':
            test_stopwatch()

        elif args.cmd == 'time.show':
            test_time_show(seconds=int(args.sec))

        elif args.cmd == 'sleep.ticks':
            colorStore = colors()
            fgcol = getattr(colorStore.fg, args.fc)
            bgcol = getattr(colorStore.bg, args.bc) if args.bc else ''
            sec_sleep_ticks(sleepMsg = f"{bgcol}{fgcol} Testing {colorStore.off}", numSec = args.sec)

    except Exception as e:
        exception_details(e, "Delay Viewer Utility")

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

