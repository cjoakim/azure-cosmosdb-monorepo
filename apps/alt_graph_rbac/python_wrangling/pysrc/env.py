# Chris Joakim, Microsoft, June 2022

import os
import time

import arrow

class Env(object):

    @classmethod
    def var(cls, name, default=None):
        if name in os.environ:
            return os.environ[name]
        else:
            return default

    @classmethod
    def epoch(cls):
        return arrow.utcnow().timestamp

    @classmethod
    def sleep(cls, sec=1):
        time.sleep(sec)
