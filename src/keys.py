#! /usr/bin/env python

import Quartz
import logging
import AppKit
from daemonize import Daemonize

pid = "/tmp/expando.pid"
logger = logging.getLogger("Expando")
logger.setLevel(logging.DEBUG)
logger.propagate = False
fh = logging.FileHandler("/tmp/expando.log", "w")
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)
keep_fds = [fh.stream.fileno()]


def keyboardTapCallback(proxy, type_, event, refcon):
    # Convert the Quartz CGEvent into something more useful
    keyEvent = AppKit.NSEvent.eventWithCGEvent_(event)
    logger.debug( "hello!")
    # send the keys to expando
    logger.debug( keyEvent)
    logger.debug("keyEvent")


def main():
    logger.debug(keyboardTapCallback)
    # Set up a tap, with type of tap, location, options and event mask
    tap = Quartz.CGEventTapCreate(
        Quartz.kCGSessionEventTap, # Session level is enough for our needs
        Quartz.kCGHeadInsertEventTap, # Insert wherever, we do not filter
        Quartz.kCGEventTapOptionListenOnly, # Listening is enough
        Quartz.CGEventMaskBit(AppKit.NSSystemDefined), # NSSystemDefined for media keys
        keyboardTapCallback,
        None
        )
    logger.debug( Quartz.kCGEventKeyUp )
    logger.debug( "tapping")

    logger.debug( tap)
    runLoopSource = Quartz.CFMachPortCreateRunLoopSource(None, tap, 0)
    logger.debug( "run loop source")
    Quartz.CFRunLoopAddSource(
        Quartz.CFRunLoopGetCurrent(),
        runLoopSource,
        Quartz.kCFRunLoopDefaultMode
        )

    logger.debug( "run loop")
    # Enable the tap
    Quartz.CGEventTapEnable(tap, True)
    logger.debug( "tap enabled")
    # and run! This won't return until we exit or are terminated.
    Quartz.CFRunLoopRun()
    logger.debug( "looping")


logger.debug( "creation")
daemon = Daemonize(app="Expando", pid=pid, action=main, keep_fds=keep_fds)
daemon.start()
