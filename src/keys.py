#! /usr/bin/env python

import Quartz
from logging import Logger, FileHandler
from AppKit import NSKeyUp, NSSystemDefined, NSEvent
from daemonize import Daemonize

pid = "/tmp/expando.pid"
fileHandler = FileHandler("/Users/pickardc/expando.txt")
logger=Logger(name="Expando")


def keyboardTapCallback(proxy, type_, event, refcon):
    # Convert the Quartz CGEvent into something more useful
    keyEvent = NSEvent.eventWithCGEvent_(event)
    print "hello!"
    # send the keys to expando
    print keyEvent
    logger.debug("keyEvent")

def main():
    # Set up a tap, with type of tap, location, options and event mask
    tap = Quartz.CGEventTapCreate(
        Quartz.kCGSessionEventTap, # Session level is enough for our needs
        Quartz.kCGHeadInsertEventTap, # Insert wherever, we do not filter
        Quartz.kCGEventTapOptionListenOnly, # Listening is enough
        Quartz.CGEventMaskBit(Quartz.kCGEventLeftMouseDown), # NSSystemDefined for media keys
        keyboardTapCallback,
        None
        )
    print Quartz.kCGEventKeyUp
    print "tapping"

    print tap
    runLoopSource = Quartz.CFMachPortCreateRunLoopSource(None, tap, 0)
    print "run loop source"
    Quartz.CFRunLoopAddSource(
        Quartz.CFRunLoopGetCurrent(),
        runLoopSource,
        Quartz.kCFRunLoopDefaultMode
        )

    print "run loop"
    # Enable the tap
    Quartz.CGEventTapEnable(tap, True)
    print "tap enabled"
    # and run! This won't return until we exit or are terminated.
    Quartz.CFRunLoopRun()
    print "running"


logger.addHandler(fileHandler)
daemon = Daemonize(app="Expando", pid=pid, action=main, verbose=True, logger=logger)
print "running"
daemon.start()
