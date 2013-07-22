#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import tornadoredis
import tornado.gen
import tornado.websocket


class RepiConnection(tornado.websocket.WebSocketHandler):
    def __init__(self, *args, **kwargs):
        super(RepiConnection, self).__init__(*args, **kwargs)
        self.listen()

    def initialize(self, repi, *args, **kwargs):
        self.repi = repi
        self.channel = self.repi._prefixChannel(self.repi.info_channel)
        super(RepiConnection, self).initialize(*args, **kwargs)

    @tornado.gen.engine
    def listen(self):
        self.redis = tornadoredis.Client()
        self.redis.connect()
        channel = self.repi._prefixChannel(self.repi.info_channel)
        yield tornado.gen.Task(self.redis.subscribe, channel)
        self.redis.listen(self.on_redis_message)

    def on_websocket_message(self, json_message):
        # Decode JSON
        try:
            message = json.loads(json_message)
        except ValueError, err:
            print 'Invalid JSON.'
            return

        # Sanity check
        if not {'channel', 'command', 'data'}.issubset(message):
            print 'Invalid protocol.'
            return

        self.repi.publish(message['command'], data=message['data'],
                          channel=message['channel'])

    on_message = on_websocket_message

    def on_redis_message(self, message):
        channel = message.channel
        if message.kind == 'message':
            # Decode JSON
            json_message = str(message.body)
            try:
                message = json.loads(json_message)
            except ValueError, err:
                print 'Invalid JSON.'
                return

            # Sanity check
            if not {'client', 'command', 'data'}.issubset(message):
                print 'Invalid protocol.'
                return

            # Write to WebSocket
            self.write_message(json_message)
        elif message.kind == 'disconnect':
            self.close()

    def on_close(self):
        if self.redis.subscribed:
            self.redis.unsubscribe('test_channel')
            self.redis.disconnect()
