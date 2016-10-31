# -*- coding: utf-8 -*-
import os
from decorators import check_is_busy
from page_parse.app import app, redis, celery
from flask import render_template, request
from flask.helpers import make_response, send_file
from page_parse.helpers.util import datetime_parse, score,\
    get_task_info, random_hash
from page_parse.tasks import page_parse


@app.route('/')
def index():
    # get or set session in cookies
    session_key = request.cookies.get('session_key') or random_hash()
    response = make_response(render_template('index.html'))
    response.set_cookie('session_key', session_key)
    return response


@app.route('/task/new', methods=['POST'])
@check_is_busy
def new_task():
    session_key = request.cookies['session_key']
    estimated_time = datetime_parse(request.form.get('estimated_time'))
    urls = filter(None, request.form.getlist('url[]'))
    list_task_info = []
    for url in urls:
        # run page_parse task for each url
        task = page_parse.apply_async((url, ), eta=estimated_time)
        # get task info for response
        task_info = get_task_info(page_parse, task.id)
        list_task_info.append(task_info)
        # save task in redis for remember in session
        redis.zadd(session_key, score(), task.id)
    return render_template('task_block.html', list_task_info=list_task_info)


@app.route('/task/cancel/<task_id>')
def cancel_task(task_id):
    celery.control.revoke(task_id, terminate=True, signal='SIGKILL')


@app.route("/uploads/<filename>")
def get_image(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename))
