from accounts.views.base import Base
from accounts.models import User
from accounts.serializers import UserSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

class UserView(Base):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = User.objects.filter(id=request.user.id).first()
        enterprise = self.get_enterprise_permissions(user.id)

        serializer = UserSerializer(user)

        return Response({
            "user": serializer.data,
            "enterprise": enterprise
        })