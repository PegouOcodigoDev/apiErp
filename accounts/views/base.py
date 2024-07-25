from rest_framework.views import APIView
from rest_framework.exceptions import APIException

from companies.models import Enterprise, Employee
from accounts.models import UserGroups, GroupsPermission

class Base(APIView):
    def get_enterprise_permissions(self, id):
        enterprise = {
            "is_owner": False,
            "permissions": []
        }

        enterprise["is_owner"] = Enterprise.objects.filter(user_id=id).exists()

        if enterprise["is_owner"]: return enterprise

        employee = Employee.objects.filter(user_id=id).first()

        if not employee:
            raise APIException("Funcionario não encontrado")
        
        groups = UserGroups.objects.values('id').filter(user_id=id).all()

        for group in groups:
            permissions = GroupsPermission.objects.filter(group_id=group).all()
            for permission in permissions:
                enterprise["permissions"].append({
                    "id":permission.id,
                    "label":permission.name,
                    "code_name":permission.codename
                })

        return enterprise