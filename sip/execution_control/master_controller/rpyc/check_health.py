# -*- coding: utf-8 -*-
"""Docker health check script.

See: https://docs.docker.com/engine/reference/builder/#healthcheck

- exit state of 0 == healthy
- exit state of 1 == un-healthy
"""
import sys
import rpyc

if __name__ == '__main__':
    host = sys.argv[1]
    port = int(sys.argv[2])
    try:
        connection = rpyc.connect(host, port)
        health = connection.root.health_check()
        print('health =', health)
    except ConnectionRefusedError as error:
        sys.exit(1)

