# -*- coding: utf-8 -*-
import urlparse
from helpers.html_parser import HTMLParser
from page_parse.models import TaskInfo
from page_parse.app import celery, messages, app
from page_parse.helpers.utils import html_response, save_image
from flask_socketio import SocketIO


@celery.task(bind=True)
def page_parse(self, url, session_key):
    namespace = '/%s' % (session_key, )
    socket = SocketIO(message_queue=app.config['SOCKET_QUEUE_URL'])
    task_info = TaskInfo(self.request.id, 'PROGRESS', messages['OBTAINING_PAGE'])

    def update_state():
        self.update_state(state=task_info.status, meta=task_info.get_message())
        socket.emit('update_state', {'task_id': self.request.id, 'html': task_info.get_html()}, namespace=namespace)
    update_state()
    html, error = html_response(url)
    if error:
        task_info.status = 'FAILURE'
        task_info.message = error
        return update_state()

    task_info.message = messages['PARSE_PAGE']
    update_state()
    parser = HTMLParser()
    parser.feed(html)

    result = {
        'url': url,
        'title': parser.title,
        'h1': parser.h1
    }

    if parser.img:
        task_info.message = messages['IMAGE_LOADED']
        update_state()
        filename, error = save_image(urlparse.urljoin(url, parser.img), app.config['UPLOAD_FOLDER'])
        result.update({
            'img': filename,
            'img_error': error
        })

    task_info.status = 'SUCCESS'
    task_info.message = None
    task_info.result = result
    update_state()
    return result
