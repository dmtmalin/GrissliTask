# -*- coding: utf-8 -*-

from page_parse.app import app, socketio

if __name__ == "__main__":
    socketio.run(app, debug=True)
