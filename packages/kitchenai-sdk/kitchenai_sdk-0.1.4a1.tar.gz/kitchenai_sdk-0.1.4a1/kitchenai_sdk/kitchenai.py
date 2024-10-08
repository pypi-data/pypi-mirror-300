from fastapi import FastAPI, UploadFile, File, Body
from typing import Callable, Optional
import functools
import logging
import requests

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class KitchenAIApp:
    def __init__(self, app_instance: FastAPI = None, namespace: str = 'default'):
        self._namespace = namespace
        self._app = app_instance if app_instance else FastAPI()

    def _create_decorator(self, route_type: str, label: str) -> Callable:
        def decorator(func: Callable):
            @functools.wraps(func)
            async def wrapper(*args, **kwargs):
                logger.debug(f"Executing {route_type} function '{label}'")
                return await func(*args, **kwargs)

            # Register the route with the standardized path
            route_path = f"/{self._namespace}/{route_type}/{label}"
            self._app.add_api_route(route_path, wrapper, name=label, methods=["POST"])

            logger.debug(f"Registered route: {route_path}")
            return wrapper
        return decorator

    def query(self, label: str):
        return self._create_decorator('query', label)

    def storage(self, label: str):
        return self._create_decorator('storage', label)

    def embedding(self, label: str):
        return self._create_decorator('embedding', label)

    def runnable(self, label: str):
        return self._create_decorator('runnable', label)

    @property
    def app(self):
        return self._app