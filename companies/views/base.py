from companies.utils.exceptions import NotFoundEmployee, NotFoundGroup, NotFoundTaskStatus, NotFoundTask
from rest_framework.views import APIView
from companies.models import Employee, Enterprise, Task, TaskStatus
from accounts.models import Group

class Base(APIView):
    def get_enterprise_id(self, user_id):
        emplpoyee = Employee.objects.filter(user_id=user_id).first()
        owner = Enterprise.objects.filter(user_id=user_id).first()

        if emplpoyee:
            return emplpoyee.enterprise.id
        
        return owner.id
    
    def get_employee(self, user_id):
        enterprise_id = self.get_enterprise_id(user_id)

        employee = Employee.objects.filter(enterprise_id=enterprise_id).first()

        if not employee:
            raise NotFoundEmployee
        
        return employee
    
    def get_group(self, group_id, enterprise_id):
        group = Group.objects.values('name').filter(id=group_id, enterprise_id=enterprise_id).firts()

        if not group:
            raise NotFoundGroup
        
        return group
    
    def get_status(self, status_id):
        status = TaskStatus.objects.filter(status_id=status_id).first()

        if not status:
            raise NotFoundTaskStatus
        
        return status
    
    def get_task(self, task_id):
        task = Task.objects.filter(task_id=task_id).first()

        if not task:
            raise NotFoundTask
        
        return task
