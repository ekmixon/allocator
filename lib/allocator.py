#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import configparser
import datetime
import redis

commonpath = os.path.dirname(os.path.realpath(__file__))
configpath = os.path.join(commonpath, "../etc/general.cfg")
config = configparser.ConfigParser()
config.read(configpath)

prefix = config['global']['prefix'].upper()


def _getyear():
    return datetime.datetime.now().year


def _getprefix():
    return "{}-{}-".format(prefix, _getyear())


class identifier:

    def __init__(self, username='core'):
        self.db = redis.StrictRedis(host=config['redis']['host'],
                                    port=config['redis']['port'], db=3,
                                    charset="utf-8", decode_responses=True)

    def new(self, title=None, description=None):
        val = self.db.incr(_getyear())
        identifier = "{}{}".format(_getprefix(), val)
        return identifier
#
# c:<year> - current counter (string)
# d:<year>:id - {description} - value
#               {title}       - value
#               {state}       - allocated, published
# r:<year>:id (set) of refs (URL)
# cpe:<year>:id (set) of cpe 2.3
#
# sub:<user> (set) of <year>:id

# tests
if __name__ == "__main__":
    print (_getprefix())
    i = identifier()
    print (i.new())
