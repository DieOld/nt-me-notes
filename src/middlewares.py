from utils import SECRET, ALGORITHM
import jwt
from aiohttp.web import json_response


async def auth_middleware(app, handler):
    async def middleware(request):
        request.user = None
        jwt_token = request.headers.get('Authorization', None)
        if jwt_token:
            try:
                payload = jwt.decode(jwt_token, SECRET, ALGORITHM)
            except (jwt.DecodeError, jwt.ExpiredSignatureError):
                return json_response({'message': 'Token is invalid'}, status=400)
            request.user = payload
        return await handler(request)
    return middleware


middleware_list = [
    auth_middleware
]
