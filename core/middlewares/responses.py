from collections.abc import Callable

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response


class StructuredResponseMiddleware:
    def __init__(self, get_response: Callable[[Request], Response]) -> None:
        self.get_response = get_response

    def __call__(self, request: Request) -> Response:
        response = self.get_response(request)

        # Check if the response is a DRF Response object
        # and if the status code indicates success, redirect, or informational
        # if status code is 4xx or 5xx, it will be handled by the exception handler
        # and will not reach this point
        if isinstance(response, Response) and (
            status.is_success(response.status_code)
            or status.is_redirect(response.status_code)
            or status.is_informational(response.status_code)
        ):
            response.data = {'data': response.data, 'code': 0}
            response._is_rendered = False  # type: ignore[attr-defined]
            response.render()

        return response