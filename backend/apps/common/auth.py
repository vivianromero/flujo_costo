from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model
from django.conf import settings
import jwt

class DRFGraphQLJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('JWT '):
            return None

        token = auth_header.split(' ')[1]
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token expirado')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Token inválido')

        User = get_user_model()
        try:
            user = User.objects.get(username=payload.get('username'))
        except User.DoesNotExist:
            raise AuthenticationFailed('Usuario no encontrado')

        return (user, None)

    def authenticate_header(self, request):
        return 'JWT'
