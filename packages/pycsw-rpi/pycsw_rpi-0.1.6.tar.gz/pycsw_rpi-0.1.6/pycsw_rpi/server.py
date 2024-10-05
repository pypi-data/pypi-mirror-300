"""
Monkeypatches for pycsw.server module
"""


import pycsw.server

Csw__init__ = pycsw.server.Csw.__init__


def rpi_csw__init__(self, rtconfig=None, env=None, version="3.0.0"):

    """
    Patched version of pycsw.server.Csw.__init__ function
    """

    Csw__init__(self, rtconfig, env, version)

    self.context.transactions_webhook_url = self.config.get(
        "manager", "transactions_webhook_url", fallback=None
    )


pycsw.server.Csw.__init__ = rpi_csw__init__
