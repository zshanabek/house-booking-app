from urllib.parse import urlparse, parse_qs
from channels.auth import AuthMiddlewareStack
# DRF imports
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
# Django imports
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections


class TokenAuthMiddleware:
    """
    Token authorization middleware for channels
    """

    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        query_string = scope['query_string']
        if query_string:
            try:
                parsed_query = parse_qs(query_string)
                token_key = parsed_query[b'token'][0].decode()
                token_name = 'token'
                if token_name == 'token':
                    user = Token.objects.get(key=token_key).user
                    scope['user'] = user
                    close_old_connections()
            except AuthenticationFailed:
                scope['user'] = AnonymousUser()
        else:
            scope['user'] = AnonymousUser()
        return self.inner(scope)


def TokenAuthMiddlewareStack(inner):
    return TokenAuthMiddleware(AuthMiddlewareStack(inner))
