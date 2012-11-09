import os

from fabric.api import env

from fab_deploy import *
from fab_deploy.joyent import *

setup_env(os.path.abspath(os.path.dirname(__file__)))
