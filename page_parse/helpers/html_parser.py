# -*- coding: utf-8 -*-
from HTMLParser import HTMLParser


class SimpleParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.title = None
        self.h1 = None
        self.img = None

    def handle_starttag(self, tag, attrs):
        if self.img is None and tag.startswith('img'):
            self.img = (filter(lambda attr: attr[0] == 'src', attrs)[:1] or [(None, None)])[0][1]

    def handle_data(self, data):
        if self.title is None and self.lasttag.startswith('title'):
            self.title = data
        elif self.h1 is None and self.lasttag.startswith('h1'):
            self.h1 = data
