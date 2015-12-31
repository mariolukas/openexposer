from functools import wraps
from time import time
from datetime import timedelta
import Queue


class CancelJobException(Exception):
    pass


class ProgressSection(object):
    def __init__(self, name):
        self.name = name
        self.size = 100
        self.progress = 0

        self.on_change = None
        self.on_done = None

        self.started = time()
        self.ended = None

    def inc(self):
        self.progress += 1
        self.on_change()

    def set_size(self, s):
        self.size = s
        self.on_change()

    def done(self):
        self.progress = self.size
        self.ended = time()
        self.on_change()
        self.on_done()

    @property
    def took(self):
        return timedelta(seconds=self.ended - self.started)

    @property
    def percentage(self):
        if self.size:
            return self.progress * 100 / self.size  # watch -> no decimals in py2


class ProgressReporter(object):
    def __init__(self, cancel_queue=None):
        self.cancel_queue = cancel_queue
        self.cancel = False

    def check_cancel(self):
        if self.cancel_queue is None:
            return

        if not self.cancel:
            try:
                self.cancel = self.cancel_queue.get_nowait()
            except Queue.Empty:
                pass

        if self.cancel:
            raise CancelJobException('The job was cancelled')

    def on_change(self, section):
        self.check_cancel()

    def on_done(self, section):
        pass

    def on_section_add(self, section):
        pass

    def new_section(self, name):
        section = ProgressSection(name)

        def _on_change():
            self.on_change(section)

        def _on_done():
            self.on_done(section)

        section.on_change = _on_change
        section.on_done = _on_done

        return section


class ProgressReporterToPrint(ProgressReporter):
    TEMPLATE = '{section.name}: {msg}'

    def __init__(self, cancel_queue=None, delta_ms=None):
        super(ProgressReporterToPrint, self).__init__(cancel_queue)

        self.delta_ms = delta_ms
        self._last_report = None

    def on_section_add(self, section):
        super(ProgressReporterToPrint, self).on_section_add(section)
        print self.TEMPLATE.format(section=section, msg='START')

    def on_change(self, section):
        super(ProgressReporterToPrint, self).on_change(section)
        if self.delta_ms is not None:
            ts = time()
            if self._last_report is None or (ts - self._last_report) * 1000 >= self.delta_ms:
                msg = '{section.progress}/{section.size} [{section.percentage}%]'.format(section=section)
                print self.TEMPLATE.format(section=section, msg=msg)
                self._last_report = ts

    def on_done(self, section):
        super(ProgressReporterToPrint, self).on_done(section)
        msg = 'DONE in {section.took}'.format(section=section)
        print self.TEMPLATE.format(section=section, msg=msg)


reporter = None


def init(progress_reporter):
    # bind a progress reporter to global object
    global reporter
    reporter = progress_reporter


def progress_log(section):
    def decorator(method):
        @wraps(method)
        def f(*args, **kwargs):
            global reporter
            if reporter is None:
                # the default reporter
                init(ProgressReporter())

            # inject the additional progress parameter
            kwargs['progress'] = reporter.new_section(section)

            return method(*args, **kwargs)

        return f

    return decorator
