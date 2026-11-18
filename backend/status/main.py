"""ASGI entry point: uvicorn status.main:app"""

import logging

from .api import create_app

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logging.getLogger("httpx").setLevel(logging.WARNING)

app = create_app()
