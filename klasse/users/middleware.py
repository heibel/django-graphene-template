from jwt import InvalidTokenError

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.utils.encoding import smart_text
from django.utils.functional import SimpleLazyObject

from klasse.users.utils import jwt_decode_handler


def get_authorization_header(request):
    return request.META.get('HTTP_AUTHORIZATION', b'')


def get_jwt_token(request):
    auth = get_authorization_header(request).split()

    if not auth or not len(auth) == 2:
        return None

    if smart_text(auth[0]) != 'Bearer':
        return None

    return auth[1]


def get_user(request):
    token = get_jwt_token(request)

    if not token:
        return AnonymousUser()

    try:
        payload = jwt_decode_handler(token)
        email = payload.get('email')
        user = get_user_model().objects.get(email=email)

        return user
    except (InvalidTokenError, KeyError, get_user_model().DoesNotExist):
        return AnonymousUser()


class JWTAuthenticationMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not hasattr(request, 'user'):
            request.user = SimpleLazyObject(lambda: get_user(request))

        response = self.get_response(request)

        return response
