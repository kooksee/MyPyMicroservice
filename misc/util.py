# -*- coding:utf-8 -*-
import itertools
import numbers


class _Timeout(object):
    """An IOLoop timeout, a UNIX timestamp and a callback"""

    # Reduce memory overhead when there are lots of pending callbacks
    __slots__ = ['deadline', 'callback', 'tdeadline']

    def __init__(self, deadline, callback):
        if not isinstance(deadline, numbers.Real):
            raise TypeError("Unsupported deadline %r" % deadline)
        self.deadline = deadline
        self.callback = callback
        self.tdeadline = (deadline, next(itertools.count()))

    # Comparison methods to sort by deadline, with object id as a tiebreaker
    # to guarantee a consistent ordering.  The heapq module uses __le__
    # in python2.5, and __lt__ in 2.6+ (sort() and most other comparisons
    # use __lt__).
    def __lt__(self, other):
        return self.tdeadline < other.tdeadline

    def __le__(self, other):
        return self.tdeadline <= other.tdeadline


def timedelta_to_seconds(td):
    # type: (datetime.timedelta) -> float
    """Equivalent to td.total_seconds() (introduced in python 2.7)."""
    return (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10 ** 6) / float(10 ** 6)



class Paginator(object):

    def __init__(self, results, total, page, perpage, url, glue='?page='):
        self.results = results
        self.total = total
        self.page = page
        self.first = 'First'
        self.last = 'Last'
        self._next = 'Next'
        self._prev = 'Previous'
        self.perpage = perpage
        self.url = url
        self._index = 0
        self.glue = glue

    def next_link(self, text=None, default=''):
        text = text or self._next
        pages = (self.total / self.perpage) + 1
        if self.page < pages:
            page = self.page + 1
            return '<a href="' + self.url + self.glue + str(page) + '">' + text + '</a>'

        return default

    def pre_link(self, text=None, default=''):
        text = text or self._prev
        if self.page > 1:
            page = self.page - 1
            return '<a href="' + self.url + self.glue + str(page) + '">' + text + '</a>'

        return default

    def links(self):
        html = ''
        pages = (self.total / self.perpage)
        if self.total % self.perpage != 0:
            pages += 1
        ranged = 4
        if pages > 1:
            if self.page > 1:
                page = self.page - 1
                html += '<a href="' + self.url + '">' + self.first + '</a>' + \
                    '<a href="' + self.url + self.glue + str(page) + '">' + self._prev + '</a>'
            for i in range(self.page - ranged, self.page + ranged):
                if i < 0:
                    continue
                page = i + 1
                if page > pages:
                    break

                if page == self.page:
                    html += '<strong id="current-page">' + str(page) + '</strong>'
                else:
                    html += '<a href="' + self.url + self.glue + str(page) + '">' + str(page) + '</a>'

            if self.page < pages:
                page = self.page + 1

                html += '<a href="' + self.url + self.glue + str(page) + '">' + self._next + '</a> <a href="' + \
                    self.url + self.gule + str(pages) + '">' + self.last + '</a>'

        return html

    def __len__(self):
        return len(self.results)

    def __iter__(self):
        return self

    def next(self):
        try:
            result = self.results[self._index]
        except IndexError:
            raise StopIteration
        self._index += 1
        return result

    __next__ = next