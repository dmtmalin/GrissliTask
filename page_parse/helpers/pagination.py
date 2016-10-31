# -*- coding: utf-8 -*-
from math import ceil


class Pagination(object):
    def __init__(self, page, per_page, total_count):
        self.page = page
        self.per_page = per_page
        self.total_count = total_count

    @property
    def pages(self):
        return int(ceil(self.total_count / float(self.per_page)))

    @property
    def has_prev(self):
        return self.page > 0

    @property
    def has_next(self):
        return self.page < self.pages - 1

    @property
    def range(self):
        start = 0
        for i in range(0, self.page):
            start += self.per_page
        return start, start + self.per_page - 1
