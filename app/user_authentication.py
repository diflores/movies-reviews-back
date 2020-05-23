from fastapi_users.authentication import JWTAuthentication

from app.config import SECRET_KEY

auth_backends = []

jwt_authentication = JWTAuthentication(secret=SECRET_KEY, lifetime_seconds=3600)

auth_backends.append(jwt_authentication)
