import inspect
from collections import OrderedDict
from http import HTTPMethod

import structlog

from selva.web.exception import HTTPNotFoundException
from selva.web.routing.decorator import (
    ACTION_ATTRIBUTE,
    CONTROLLER_ATTRIBUTE,
    ActionInfo,
    ControllerInfo,
)
from selva.web.routing.exception import (
    ControllerWithoutDecoratorError,
    DuplicateRouteError,
)
from selva.web.routing.route import Route, RouteMatch

logger = structlog.get_logger()


def _path_with_prefix(path: str, prefix: str):
    path = path.strip("/")
    prefix = prefix.strip("/")
    return f"{prefix}/{path}"


class Router:
    def __init__(self):
        self.routes: OrderedDict[str, Route] = OrderedDict()

    def route(self, controller: type):
        controller_info: ControllerInfo = getattr(
            controller, CONTROLLER_ATTRIBUTE, None
        )

        if not controller_info:
            raise ControllerWithoutDecoratorError(controller)

        path_prefix = controller_info.path

        logger.debug(
            "controller registered",
            path_prefix=path_prefix or "/",
            controller=f"{controller.__module__}.{controller.__qualname__}",
        )

        for name, action in inspect.getmembers(controller, inspect.isfunction):
            action_info: ActionInfo = getattr(action, ACTION_ATTRIBUTE, None)
            if not action_info:
                continue

            action_type = action_info.type
            method: HTTPMethod = action_type.value  # type: ignore
            path = action_info.path
            path = _path_with_prefix(path, path_prefix)
            route_name = f"{controller.__module__}.{controller.__qualname__}:{name}"

            route = Route(method, path, controller, action, route_name)

            for current_route in self.routes.values():
                if (
                    current_route.action != route.action
                    and current_route.method == route.method
                    and current_route.regex == route.regex
                ):
                    raise DuplicateRouteError(route.name, current_route.name)

            self.routes[route_name] = route
            logger.debug(
                "action registered",
                controller=f"{controller.__module__}.{controller.__qualname__}",
                action=route.action.__name__,
                method=route.method,
                path=route.path,
            )

    def match(self, method: HTTPMethod | None, path: str) -> RouteMatch | None:
        for route in self.routes.values():
            if (match := route.match(method, path)) is not None:
                return RouteMatch(route, method, path, match)

        return None

    def reverse(self, name: str, **kwargs) -> str:
        if route := self.routes.get(name):
            return route.reverse(**kwargs)

        raise HTTPNotFoundException()
