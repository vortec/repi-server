#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import tornadoredis
from repi_server import RepiServer


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--name', help='Name of Repi client', type=str,
                        default='master')
    parser.add_argument('-H', '--host', help='Redis host (default: localhost)',
                        type=str, default='localhost')
    parser.add_argument('-p', '--port', help='Redis port (default: 6379)',
                        type=int, default=6379)
    parser.add_argument('-P', '--http-port', help='HTTP port (default:8888',
                        type=int, default=8888)
    parser.add_argument('-ns', '--namespace',
                        help='Redis namespace (default: repi)', type=str,
                        default='repi')
    parser.add_argument('-i', '--info-channel',
                        help='Redis general PubSub channel (default: cluster)',
                        type=str, default='cluster')
    args = parser.parse_args()

    name = args.name
    redis_host = args.host
    redis_port = args.port
    http_port = args.http_port
    namespace = args.namespace
    info_channel = args.info_channel

    if not namespace.endswith(':'):
        namespace = '{}:'.format(namespace)

    r = tornadoredis.Client(host=redis_host, port=redis_port)
    repi_server = RepiServer(r, name=name,  namespace=namespace,
                             info_channel=info_channel, port=http_port)
    repi_server.run()

if __name__ == '__main__':
    main()
