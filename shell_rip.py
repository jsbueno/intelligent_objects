#!/usr/bin/env python

import os

class ExecImediate(object):
    def __getattr__(self, command):
        return os.system(command)

s = ExecImediate()


class ExecDelayed(object):
    def __getattr__(self, command):
        def call(*args):
            return os.popen(
                "%s %s" % (
                    command,
                    " ".join(args)
                )
            ).read()
        return call
sh = ExecDelayed()