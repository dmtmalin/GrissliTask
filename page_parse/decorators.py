# -*- coding: utf-8 -*-
from functools import wraps
from flask import request, Response

from page_parse.app import app, redis, messages
from tasks import page_parse


# help function
def is_busy(session_key):
    # check last tasks
    list_task_id = redis.zrevrange(session_key, 0, app.config['MAX_URLS'])
    for task_id in list_task_id:
        if page_parse.AsyncResult(task_id).state in ['PROGRESS', 'PENDING']:
            return True
    return False


def check_is_busy(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        session_key = request.cookies['session_key']
        if is_busy(session_key):
            return Response(response=messages['IS_BUSY'], status=400)
        return f(*args, **kwargs)
    return decorated_function
