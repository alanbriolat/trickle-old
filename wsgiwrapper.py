import os
import os.path
import sys

os.chdir(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import trickle.webui
from trickle.delugeclient import DelugeClient

trickle.webui.client = DelugeClient('127.0.0.1', 8112, '')
application = trickle.webui.application
