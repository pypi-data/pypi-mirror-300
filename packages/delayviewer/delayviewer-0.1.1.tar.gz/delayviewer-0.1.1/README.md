# DelayViewer

**DelayViewer** is a Python assistant for showing progress info visually within the shell running a python command with long exposure. This library provides a simple spinner graphic and a stopwatch. The predominant use case is to display progress for sections within a decorated function.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install **delayviewer**.

```bash
pip install delayviewer
```


## Spinner Usage
```python
from delayviewer.spinner import handle_spinner
import time

@handle_spinner
def test_spinner(spinner=None):
    spinner.start('delaying 5 sec')
    time.sleep(5)
    spinner.stop()

test_spinner()
```

## Stopwatch Usage
```python
from delayviewer.stopwatch import handle_stopwatch
import time

@handle_stopwatch
def test_stopwatch(stopwatch=None):
    stopwatch.start('clocking 5 sec')
    time.sleep(5)
    stopwatch.stop('Finished timing!')

test_stopwatch()
```


## CLI Utility

The following CLI is included with this package for testing the various progress and timing indicators.

```bash
# dlyview -h
usage: dlyview [-h] {spinner,stopwatch,time.show,sleep.ticks} ...

-.-.-. Delay viewer elements for python scripts

positional arguments:
  {spinner,stopwatch,time.show,sleep.ticks}
    spinner             test Spinner graphic for viewing thru execution delays
    stopwatch           test StopWatch for viewing thru execution delays
    time.show           test time show wrapper
    sleep.ticks         test sleeping ticks progress viewer

options:
  -h, --help            show this help message and exit

.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
```


## License

[MIT](https://choosealicense.com/licenses/mit/)


## Acknowledgements

Thanks to several posts on StackOverflow regarding basic Spinner class implementation. Took that concept and generated the Stopwatch class to mimic behavior.
