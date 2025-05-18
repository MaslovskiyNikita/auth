from typing import Any, Awaitable, Callable

from fastapi import Request


class MiddlewareManager:
    def __init__(self):
        self._middlewares = []

    def add_middleware(self, middleware_func: Callable[[Request, Any], Awaitable[Any]]):
        self._middlewares.append(middleware_func)

    def init_middleware(self, app):
        for middleware in self._middlewares:

            @app.middleware("http")  # type: ignore[misc]
            async def wrapper(request: Request, call_next):
                return await middleware(request, call_next)

            wrapper.__name__ = middleware.__name__


middleware_manager = MiddlewareManager()
