from aiohttp.web import json_response
import functools


def login_required(func):
    @functools.wraps(func)
    def wrapper(request):
        if not request.user:
            return json_response({'message': 'Auth required'}, status=401)
        return func(request)
    return wrapper
