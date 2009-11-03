"""
This package handles configuration variables. The settings are stored in
the file settings.py which is not i version control. You have to create it yourself.
"""
class Config(object):
    pass

try:
    import settings
except ImportError:
    print "No settings.py file available"
    print "Using settingsexample.py instead"
    import settingsexample as settings

server = settings.server
