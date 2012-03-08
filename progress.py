# stdlib
import sys
import time


class Progress(object):
    '''A context manager to indicate progress at intervals via a callback.'''

    def __init__(self, total, timeout=0, callback=None):
        # item count
        self.current = None
        self.total = total
        # elapsed time
        self.begun = None
        # callback
        self.prev = None
        self.timeout = timeout
        if callback is None:
            def fn(current, total, elapsed):
                print 'Completed {} of {} items; {} elapsed.'.format(
                    current, total, format_time(1000 * elapsed))
            self.callback = fn
        else:
            self.callback = callback

    def __enter__(self):
        # local
        now = time.time()
        # item count
        self.current = 0
        # elapsed time
        self.begun = now
        # callback
        self.prev = now
        self.callback(0, self.total, 0)
        return self # this cm is meant to be used like "Progress(...) as smth"

    def next(self, did=1):
        # local
        now = time.time()
        # item count
        self.current += did
        # determine if we're done
        if self.current >= self.total:
            self.next = None
        # callback
        if (now - self.prev) > self.timeout or self.next is None:
            self.prev = now
            return self.callback(self.current, self.total, now - self.begun)

    def __exit__(self, e_type, e_value, e_traceback):
        # make final call to callback
        self.timeout = 0
        if self.next is not None:
            self.next(self.total - self.current)
            self.next = None
        return False # this cm doesn't care about exceptions


def bar(message=None, width=10):
    '''Generate a callback for Progress which makes a bar like [##---].'''
    message = '' if message is None else (message + ' ')
    def fn(current, total, elapsed):
        blocks = int(float(current) / total * width)
        sys.stdout.write('\r{}[{}{}] {:{w}}/{} {}{}'.format(
            message,
            blocks * '#',
            (width - blocks) * '-',
            current,
            total,
            format_time(1000 * elapsed),
            '\n' if current == total else '',
            w=len(str(total)),
            ))
        sys.stdout.flush()
    return fn


def format_time(milliseconds):
    '''Return a human-readable string from the given number of milliseconds.

    >>> format_length_of_time(3723004)
    '01:02:03.004'
    >>> format_length_of_time(123004)
    '02:03.004'
    >>> format_length_of_time(3004)
    '03.004'
    >>> format_length_of_time(4)
    '004'
    >>> format_length_of_time(0)
    '000'
    '''
    ms = int(milliseconds)
    h = ms / 3600000
    m = ms % 3600000 / 60000
    s = ms % 3600000 % 60000 / 1000
    ms = ms % 3600000 % 60000 % 1000
    #         ms/hr,    ms/min, ms/s
    return ('{:02}:'.format(h) if h else '') + \
           ('{:02}:'.format(m) if h or m else '') + \
           ('{:02}.'.format(s) if h or m or s else '') + \
           '{:03}'.format(ms)
