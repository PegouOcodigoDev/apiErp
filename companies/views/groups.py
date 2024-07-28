from companies.views.base import Base
from companies.utils.exceptions import RequiredFields
from companies.utils.permissions import GroupsPermissions
from companies.serializers import GroupSerializer
from accounts.models import Group, GroupsPermission
from rest_framework.views import Response, Request
from rest_framework.exceptions import APIException
from django.contrib.auth.models import Permission


class Groups(Base):
    permission_classes = [GroupsPermissions]

    def get(self, request:Request):
        enterprise_id = self.get_enterprise_id(request.user.id)

        groups = Group.objects.filter(enterprise_id=enterprise_id).all().order_by("name")

        serializer = GroupSerializer(groups, many=True)

        return Response({"groups": serializer.data})
    
    def post(self, request:Request):
        enterprise_id = self.get_enterprise_id(request.user.id)

        name = request.data.get("name")
        permissions = request.data.get("permissions")

        if not name:
            raise RequiredFields
        
        created_group = Group.objects.create(name=name, enterprise_id=enterprise_id)

        if permissions:
            permissions = permissions.split(",")

        try:
            for permission_id in permissions:
                permission = Permission.objects.filter(id=permission_id).exists()

                if not permission:
                    created_group.delete()
                    raise APIException("A permissão {} não existe".format(permission_id))
                
                if not GroupsPermission.objects.filter(group_id=created_group.id, permission_id=permission_id).exists():
                    GroupsPermission.objects.create(group_id=created_group.id, permission_id=permission_id)
        except ValueError:
            created_group.delete()
            raise APIException("Envie as permissões no formato correto")
        except TypeError:
            raise APIException("Envie os argumentos corretos")
        
        return Response({"sucess": True})

class GroupDetail(Base):
    permission_classes = [GroupsPermissions]

    def get(self, request:Request, id):
        enterprise_id = self.get_enterprise_id(request.user.id)

        self.get_group(id, enterprise_id)
        group = Group.objects.filter(id=id).first()

        serializer = GroupSerializer(group)

        return Response({"group": serializer.data})
    
    def put(self, request:Request, id):
        enterprise_id = self.get_enterprise_id(request.user.id)

        self.get_group(id, enterprise_id)

        name = request.data.get('name')
        permissions = request.data.get('permissions')

        if name:
            Group.objects.filter(id=id).update(name=name)
        
        if permissions:
            permissions = permissions.split(",")
            
            try:
                GroupsPermission.objects.filter(group_id=id).delete()

                for permission_id in permissions:
                    permission = Permission.objects.filter(id=permission_id).exists()

                    if not permission:
                        raise APIException("A permissão {} não existe".format(permission_id))
                    
                    if not GroupsPermission.objects.filter(group_id=id, permission_id=permission_id).exists():
                        GroupsPermission.objects.create(group_id=id, permission_id=permission_id)
            except ValueError:
                raise APIException("Envie as permissões no padrão correto")
            
            return Response({"sucess": True})
            
    def delete(self, request:Request, id):
        enterprise_id = self.get_enterprise_id(request.user.id)

        Group.objects.filter(id=id, enterprise_id=enterprise_id)

        return Response({"sucess": True})
                    