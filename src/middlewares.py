from db import SECRET, ALGORITHM
import jwt
from aiohttp.web import Response


async def login_required(app, handler):
    async def middleware(request):
        request.user = None
        _token = request.headers.get('Authorization')
        if _token:
            try:
                payload = jwt.decode(_token, SECRET, ALGORITHM)
            except (jwt.DecodeError, jwt.ExpiredSignatureError):
                return Response(text='{"message": "Token is invalid"}', status=400)
            request.user = payload
        else:
            return Response(text='{"message": "Login required"}', status=401)
        return await handler(request)
    return middleware


middleware_list = [
    login_required
]
