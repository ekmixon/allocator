#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import configparser
import datetime
import time
import redis

commonpath = os.path.dirname(os.path.realpath(__file__))
configpath = os.path.join(commonpath, "../etc/general.cfg")
config = configparser.ConfigParser()
config.read(configpath)

prefix = config['global']['prefix'].upper()


def _getyear():
    return datetime.datetime.now().year


def _getepoch():
    return int(time.time())


def _getprefix():
    return f"{prefix}-{_getyear()}-"


class identifier:

    def __init__(self, username='core'):
        self.db = redis.StrictRedis(host=config['redis']['host'],
                                    port=config['redis']['port'], db=3,
                                    charset="utf-8", decode_responses=True)
        self.username = username

    def new(self, title=None, description=None, state='Allocated'):
        val = self.db.incr(_getyear())
        identifier = f"{_getprefix()}{val}"
        hkey = f"d:{identifier}"
        self.db.hset(hkey, 'requestor', self.username)
        self.db.hset(hkey, 'title', title)
        self.db.hset(hkey, 'description', description)
        if state == "Allocated":
            self.db.sadd('allocated', identifier)
        self.db.hset(hkey, 'state', state)
        self.db.hset(hkey, 'requested', _getepoch())
        return identifier

    def addref(self, identifier=False, ref=False):
        if not identifier or not ref:
            return False
        rkey = f"r:{identifier}"
        hkey = f"d:{identifier}"
        return self.db.sadd(rkey, ref) if self.db.exists(hkey) else False

    def publish(self, identifier=False):
        if not identifier:
            return False
        hkey = f"d:{identifier}"
        if not self.db.exists(hkey):
            return False
        self.db.hset(hkey, 'state', 'Published')
        return self.db.sadd('published', identifier)

    def expired(self, identifier=False):
        if not identifier:
            return False
        hkey = f"d:{identifier}"
        if not self.db.exists(hkey):
            return False
        if self.db.sismember('published', identifier):
            return False
        requested = int(self.db.hget(hkey, 'requested'))
        now = int(_getepoch())
        return int(now-requested)


#
# c:<year> - current counter (string)
# d:<identifier> - {description} - value
#               {title}       - value
#               {state}       - allocated, published
# d:<identifier> - {requestor}   - value
# d:<identifier> - {requested} - value (epoch)
# r:<identifier> (set) of refs (URL)
# allocated (set of allocated identifiers)
# published (set of published identifiers)
# cpe:<year>:id (set) of cpe 2.3
#
# sub:<user> (set) of <year>:id

# tests
if __name__ == "__main__":
    print (_getprefix())
    i = identifier()
    print (i.new())
    print (i.addref(identifier='SHVI-2016-2', ref='http://www.foo.be/'))
    print (i.publish(identifier='SHVI-2016-2'))
    print (i.expired(identifier='SHVI-2016-4'))
