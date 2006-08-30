#!/bin/sh
grep -v Traceback | \
grep -v ":   File" | \
grep -v "IOError: Write failed, client closed connection." | \
grep -v "does NOT match server name"
