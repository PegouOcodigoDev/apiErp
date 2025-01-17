from accounts.models import UserGroups, GroupsPermission, Group
from companies.models import Employee, TaskStatus, Task

from rest_framework import serializers
from django.contrib.auth.models import Permission


class EmployeesSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = (
            'id',
            'name',
            'email'
        )

    def get_name(self, obj):
        return obj.user.name
    
    def get_email(self, obj):
        return obj.user.email
    
class EmployeeSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    group = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = (
            'id',
            'name',
            'email',
            'group'
        )

    def get_name(self, obj):
        return obj.user.name
    
    def get_email(self, obj):
        return obj.user.email
    
    def get_group(self, obj):
        groups_db = UserGroups.objects.filter(user_id=obj.user.id).all()
        groups_data = []

        for group in groups_db:
            groups_data.append(
                {
                    'id':group.group.id,
                    'name':group.group.name
                }
            )

        return groups_data
    
class GroupSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = (
            'id',
            'name',
            'permissions',
        )

    def get_permissions(self, obj):
        groups = GroupsPermission.objects.filter(group_id=obj.id).all()
        permissions = []

        for group in groups:
            permissions.append(
                {
                    'id': group.permission.id,
                    'label': group.permission.name,
                    'code_name': group.permission.codename,
                }
            )

        return permissions
    
class PermissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = (
            'id',
            'name',
            'codename',
        )
    
class TaskSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    employee = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = (
            'id',
            'title',
            'description',
            'due_date',
            'created_at',
            'status',
            'employee'
        )

    def get_status(self, obj):
        return obj.status.name

    def get_employee(self, obj):
        return EmployeeSerializer(obj.employee).data
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.status_id = validated_data.get('status_id', instance.status_id)
        instance.employee_id = validated_data.get('employee_id', instance.employee_id)
        instance.due_data = validated_data.get('due_data', instance.due_data)

        instance.save()