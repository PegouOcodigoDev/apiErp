from accounts.views.base import Base
from accounts.auth import Authentication
from accounts.serializers import UserSerializer

from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny

class Signin(Base):
    permission_classes = [AllowAny]
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = Authentication.signin(email=email, password=password)

        enterprise = self.get_enterprise_user(user.id)

        serializer = UserSerializer(user)

        token = RefreshToken.for_user(user)

        return Response({
            "user": serializer.data,
            "enterprise": enterprise,
            "refresh": str(token),
            "acess": str(token.access_token),
        })