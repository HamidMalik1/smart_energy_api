'''Common configuration parameters, also see ../config.toml.example'''

import toml

DEFAULT_FILENAME = 'config.toml'

def load():
    '''Configuration as dict'''
    return toml.load(DEFAULT_FILENAME)

CONFIG = load()

MYSQL_CONNECTION = {
	'host': CONFIG['db']['host'],
	'port': CONFIG['db']['port'],
	'user': CONFIG['db']['user'],
	'passwd': CONFIG['db']['passwd']
}
