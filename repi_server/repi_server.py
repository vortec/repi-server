#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import tornadoredis
import tornado.httpserver
import tornado.ioloop
import tornado.web

from connection import RepiConnection


class RepiServer(object):
    def __init__(self, r, name='master', namespace='repi:',
                 info_channel='cluster', port=8888):
        self.redis = r
        self.name = name
        self.namespace = namespace
        self.info_channel = info_channel
        self.port = port

    def subscribe(self, channel):
        channel = self._prefixChannel(channel)
        self.redis.subscribe(channel)

    def unsubscribe(self, channel):
        channel = self._prefixChannel(channel)
        self.redis.unsubscribe(channel)

    def publish(self, command, data=None, channel=None):
        if channel:
            channel = self._prefixChannel(channel)
        else:
            channel = self._prefixChannel(self.info_channel)

        message = {
            'client': self.name,
            'command': command,
            'data': data
        }
        json_message = json.dumps(message)
        self.redis.publish(channel, json_message, lambda x: None)

    def run(self):
        application = tornado.web.Application([
            (r'/', MainHandler, dict(repi=self)),
            (r'/ws', RepiConnection, dict(repi=self))
        ])
        http_server = tornado.httpserver.HTTPServer(application)
        http_server.listen(self.port)
        tornado.ioloop.IOLoop.instance().start()

    def _prefixChannel(self, channel):
        return '{}{}'.format(self.namespace, channel)


class MainHandler(tornado.web.RequestHandler):
    def initialize(self, repi, *args, **kwargs):
        self.repi = repi
        super(MainHandler, self).initialize(*args, **kwargs)

    def get(self):
        kwargs = {
            'title': 'RePi Server',
            'info_channel': self.repi.info_channel
        }
        self.render(os.path.join('view', 'index.html'), **kwargs)
