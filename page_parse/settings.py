# -*- coding: utf-8 -*-
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
# secret key for app
SECRET_KEY = '!secret'
CSRF_ENABLED = True
# url for management client list
SOCKET_QUEUE_URL = 'redis://localhost:6379/0'
# celery settings [worker]
CELERY_BROKER_URL = 'redis://localhost:6379/1'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
# celery settings [result]
CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'
CELERY_RESULT_SERIALIZER = 'json'
# url for management session list
REDIS_URL = 'redis://localhost:6379/2'
# maximum urls for parse
MAX_URLS = 5
# messages
MESSAGES = {
    'IS_BUSY': u'Некоторые задачи не завершены',
    'OBTAINING_PAGE': u'Получение страницы',
    'PARSE_PAGE': u'Поиск тегов <title>, <h1>, <img>',
    'IMAGE_LOADED': u'Загрузка изображения',
}
