from companies.views.base import Base
from companies.utils.permissions import EmployeesPermission, GroupsPermission
from companies.models import Employee, Enterprise
from companies.serializers import EmployeeSerializer, EmployeesSerializer
from accounts.auth import Authentication
from accounts.models import User, UserGroups
from rest_framework.views import Request,Response, status
from rest_framework.exceptions import APIException
from django.db.models import F

class Employees(Base):
    permission_classes=[EmployeesPermission]

    def get(self, request):
        enterprise_id = self.get_enterprise_id(request.user.id)

        owner_id = Enterprise.objects.values('user_id').filter(id=enterprise_id).first()

        employees = Employee.objects.filter(enterprise_id=enterprise_id).exclude(user_id=owner_id['user_id']).annotate(user_name=F('user_name')).order_by('user_name')

        serializer = EmployeesSerializer(employees, many=True)

        return Response({'employees': serializer.data})
    
    def post(self, request:Request):
        name = request.data.get('name')
        email = request.data.get('email')
        password = request.data.get('password')

        enterprise = self.get_enterprise_id(request.user.id)
        signup_user = Authentication.signup(name=name, email=email, password=password, type_account='employee', company_id=enterprise)

        if isinstance(signup_user, User):
            return Response({'sucess': True}, status=status.HTTP_201_CREATED)
        
        return Response(signup_user, status=status.HTTP_400_BAD_REQUEST)
    
class EmployeeDetail(Base):
    permission_classes = [EmployeesPermission]

    def get(self, id):
        employee = self.get_employee(id)

        serializer = EmployeeSerializer(employee)

        return Response(serializer.data)
    
    def put(self, request:Request, id):
        groups = request.data.get('group')
        employee = self.get_employee(id)
        user = employee.user
        name = request.data.get('name') or user.name
        email = request.data.get('email') or user.email

        if email != user.email and User.objects.filter(email=email).exists():
            raise APIException("O email ja esta em uso", code="email_already_exists")
        
        User.objects.filter(id=user.id).update(name=name, email=email)

        if groups:
            groups = groups.split(",")

            for group in groups:
                self.get_group(group, employee.enterprise.id)
                UserGroups.objects.create(group_id=group, user_id=user.id)
        
        return Response({"sucess":True})
    
    def delete(self, id):
        employee = self.get_employee(id)
        check_if_owner = User.objects.filter(id=employee.user.id, is_owner=1).exists()
        if check_if_owner:
            raise APIException("Um funcionario não pode excluir o dono")
        employee.delete()
        User.objects.filter(id=employee.user.id).delete()
        return Response({"sucess":True})
    

        

        