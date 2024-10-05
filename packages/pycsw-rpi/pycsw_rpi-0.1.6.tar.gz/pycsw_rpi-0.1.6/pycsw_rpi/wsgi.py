"""
Wrapper (with monkeypatched behaviour) for original pycsw WSGI application object
"""

# Imports from . import * are needed to override original PyCSW behaviour
# pylint: disable=unused-import

import sys

from pycsw.wsgi import application

# pylint: disable=no-name-in-module
from . import apiso, config, metadata, repository, server

if __name__ == "__main__":  # run inline using WSGI reference implementation

    from wsgiref.simple_server import make_server

    PORT = 8000
    if len(sys.argv) > 1:
        PORT = int(sys.argv[1])
    httpd = make_server("", PORT, application)
    print(f"Serving on port {PORT}")
    httpd.serve_forever()
