__author__  = 'Chris Joakim'
__email__   = "chjoakim@microsoft.com"
__license__ = "MIT"
__version__ = "May 2022"

import redis


class RCache(object):

    def __init__(self, host, port):
        self.client = redis.Redis(host=host, port=port)  #, db=0)  localhost, 6379

    def set(self, key, value):
        return self.client.set(key, value)

    def get(self, key):
        return self.client.get(key)

    def client(self):
        return self.client
