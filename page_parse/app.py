# -*- coding: utf-8 -*-
from flask import Flask
from flask_redis import FlaskRedis
from flask_socketio import SocketIO
from datetime import timedelta
from celery import Celery

import eventlet
eventlet.monkey_patch()

app = Flask(__name__)
app.config.from_pyfile('settings.py')
app.permanent_session_lifetime = timedelta(hours=1)

messages = app.config['MESSAGES']

redis = FlaskRedis(app)

socketio = SocketIO(app, async_mode='eventlet', message_queue=app.config['SOCKET_QUEUE_URL'])

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

from page_parse import views
