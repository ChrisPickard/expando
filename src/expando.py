#!/usr/bin/env python

from time import sleep
from daemonize import Daemonize

pid = "/tmp/expando.pid"


def main():
    while True:
        print "hello"

daemon = Daemonize(app="Expando", pid=pid, action=main)
daemon.start()
