import sys, os
sys.path.insert(0, os.path.abspath(os.path.dirname('core')))
from core.server import app
app.testing = True
