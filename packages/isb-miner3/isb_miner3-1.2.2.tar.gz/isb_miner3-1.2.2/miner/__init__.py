import datetime
from importlib.metadata import version

name = "miner3"
GIT_SHA = '$Id: f1f00718db94ef473368ef37e28a0986b0ffd93b $'

try:
    __version__ = version(name)
except:
    __version__ = 'development'

