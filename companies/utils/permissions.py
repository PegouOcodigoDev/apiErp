from rest_framework import permissions
from accounts.models import UserGroups, GroupsPermission
from django.contrib.auth.models import Permission
from django.http import HttpRequest

def check_permission(user, method, permission_to):
    if not user.is_authenticated:
        return False
    
    if user.is_owner:
        return True
    
    required_permision = 'view_' + permission_to
    if method == 'POST':
        required_permision = 'add_' + permission_to
    elif method == 'PUT':
        required_permision = 'change_' + permission_to
    elif method == 'DELETE':
        required_permision = 'delete_' + permission_to

    groups_permission = UserGroups.objects.values('group_id').filter(user_id=user.id).all()

    for group in groups_permission:
        permissions = GroupsPermission.objects.values('permission_id').filter(group_id=group).all()

        for permission in permissions:
            if Permission.objects.filter(id=permission, codename=required_permision).exists():
                return True


class EmployeesPermission(permissions.BasePermission):
    message = 'O usuario não tem permissao para gerenciar os funcionarios'

    def has_permission(self, request: HttpRequest, _view):
        return check_permission(HttpRequest.user, HttpRequest.method, permission_to='employee')

class GroupsPermission(permissions.BasePermission):
    message = 'O usuario não tem permissao para gerenciar os grupos'

    def has_permission(self, request: HttpRequest, _view):
        return check_permission(HttpRequest.user, HttpRequest.method, permission_to='group')

class GroupsPermissionsPermission(permissions.BasePermission):
    message = 'O usuario não tem permissao para gerenciar as permissoes'

    def has_permission(self, request: HttpRequest, _view):
        return check_permission(HttpRequest.user, HttpRequest.method, permission_to='permission')

class TaskPermission(permissions.BasePermission):
    message = 'O usuario não tem permissao para gerenciar as tarefas'

    def has_permission(self, request: HttpRequest, _view):
        return check_permission(HttpRequest.user, HttpRequest.method, permission_to='task')           
