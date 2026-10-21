"""TLS roots shared by the Discord HTTP and gateway connector."""

import os
import ssl

import aiohttp
import certifi


def create_connector():
    context = ssl.create_default_context(
        cafile=os.environ.get("SSL_CERT_FILE") or certifi.where(),
        capath=os.environ.get("SSL_CERT_DIR"),
    )
    return aiohttp.TCPConnector(ssl=context)
