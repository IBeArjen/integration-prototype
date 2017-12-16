# -*- coding: utf-8 -*-
"""Dummy Service which just spams print messages."""
from random import uniform
from socket import gethostname
from time import sleep, time


def main():
    """Main function."""
    host_name = gethostname()
    start_time = time()
    try:
        while True:
            elapsed = time() - start_time
            print('Hello from %s (%.1f s)' % (host_name, elapsed), flush=True)
            sleep(uniform(0.01, 0.5))
    except KeyboardInterrupt:
        print('Exiting...')


if __name__ == '__main__':
    main()
