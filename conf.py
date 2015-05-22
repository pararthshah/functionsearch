import os
import base64

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

PORT = 8000

SECRET = base64.b64encode(os.urandom(32))

TEMPLATE_PATH = os.path.join(PROJECT_PATH, 'template')
STATIC_PATH = os.path.join(PROJECT_PATH, 'static')

MAX_WORKERS = 4