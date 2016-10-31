# -*- coding: utf-8 -*-
from jinja2 import Environment, PackageLoader

render_env = Environment(loader=PackageLoader('page_parse', 'templates'))


class TaskInfo(object):
    def __init__(self, task_id, status, message=None, result=None):
        self.task_id = task_id
        self.status = status
        self.message = message
        self.result = result

    def to_dict(self):
        return self.__dict__

    def get_message(self):
        return {'message': self.message}

    def get_html(self):
        template = render_env.get_template('task_block.html')
        return template.render(list_task_info=(self, ))
