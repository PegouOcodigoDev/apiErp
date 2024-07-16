from rest_framework.views import APIView
from rest_framework.exceptions import APIException

from companies.models import Enterprise, Employee
from accounts.models import UserPermission, GroupsPermission

class Base(APIView):
    def get_enterprise_user(self, user_id):
        enterprise = {
            "is_owner": False,
            "permissions": []
        }

        enterprise["is_owner"] = Enterprise.objects.filter(user_id=user_id).exists()

        if enterprise["is_owner"]: return enterprise

        employee = Employee.objects.filter(user_id=user_id).first()

        if not employee:
            raise APIException("Este usuario não é um funcionario")
        
        groups = UserPermission.objects.filter(user_id=user_id).all()

        for group in groups:
            permissions = GroupsPermission.objects.filter(group_id=group.id).all()
            for permission in permission:
                enterprise["permissions"].append({
                    "id":permission.id,
                    "label":permission.name,
                    "code_name":permission.codename
                })

        return enterprise