# -*- coding: utf-8 -*-
import os
import time
import requests
from dateutil.parser import parse
from page_parse.models import TaskInfo


def score():
    return time.time() + time.clock()


def random_hash():
    return os.urandom(16).encode('hex')


def datetime_parse(string_object):
    return parse(string_object) if string_object else None


def get_task_info(task_cls, task_id):
    task = task_cls.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = TaskInfo(task_id, task.state)
    elif task.state != 'FAILURE':
        response = TaskInfo(task_id, task.state, task.info.get('message'), result=task.info)
    else:
        # something wrong, exception raised in task.info
        response = TaskInfo(task_id, task.state, message=str(task.info))
    return response.to_dict()


def safe_response(url, stream=False):
    try:
        response = requests.get(url, stream=stream)
        return response, None
    except requests.ConnectionError as e:  # network problem
        return None, e.message
    except requests.RequestException as e:  # wrong url, wrong http status and etc.
        return None, e.message


def html_response(url):
    response, error = safe_response(url)
    return unicode(response.content, response.encoding) if response else None, error


def save_image(url, upload_dir):
    response, error = safe_response(url, stream=True)
    filename = None
    if response:
        filename = random_hash() + os.path.splitext(url)[1]
        with open(os.path.join(upload_dir, filename), 'wb') as handle:
            for block in response.iter_content(1024):
                if not block:
                    break
                handle.write(block)
    return filename, error
