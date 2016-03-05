import os
import configparser

commonpath = os.path.dirname(os.path.realpath(__file__))
configpath = os.path.join(commonpath, "../etc/general.cfg")
config = configparser.ConfigParser()
config.read(configpath)

prefix = config['global']['prefix']

#
# c:<year> - current counter (string)
# d:<year>:id - {description} - value
#               {title}       - value
#               {state}       - allocated, published
# r:<year>:id (set) of refs (URL)
# cpe:<year>:id (set) of cpe 2.3
#
# sub:<user> (set) of <year>:id
