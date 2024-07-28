from companies.views.base import Base
from companies.utils.permissions import TaskPermission
from companies.serializers import TaskSerializer
from companies.models import Task
from rest_framework.views import Response, Request
from companies.utils.validators import Validate

class Tasks(Base):
    permission_classes = [TaskPermission]

    def get(self, request:Request):
        enterprise_id = self.get_enterprise_id(request.user.id)
        tasks = Task.objects.filter(enterprise_id=enterprise_id).all().order_by("id")
        serializer = TaskSerializer(tasks, many=True)
        return Response({"tasks": serializer.data})
    
    def post(self, request:Request):
        title = request.data.get('title')
        description = request.data.get('description')
        status_id = request.data.get('status_id')
        due_data = request.data.get('due_data')

        employee = self.get_employee(request.user.id)

        
        validated_data = Validate.validate_data(due_data, title)

        task = Task.objects.create(title=validated_data['title'], 
                                   description=description, 
                                   due_data=validated_data['due_data'], 
                                   employee_id=employee.id, 
                                   enterprise_id=employee.enterprise.id, 
                                   status_id=status_id)
        
        serializer = TaskSerializer(task)

        return Response({"tasks": serializer.data})
    
class TaskDetail(Base):
    permission_classes = [TaskPermission]

    def get(self, id):
        task = self.get_task(id)
        serializer = TaskSerializer(task)
        return Response({"task": serializer.data})

    def put(self, request:Request, id):
        task = self.get_task(id)

        title = request.data.get('title', task.title)
        description = request.data.get('description', task.description)
        status_id = request.data.get('status_id', task.status.id)
        due_date = request.data.get('due_date', task.due_date)

        if due_date != task.due_data:
            due_date = Validate.data_validate(due_date)
        
        task = Validate.updated_data(task, title, description, status_id, due_date)

        task.save()

        serializer = TaskSerializer(task)

        return Response({"task": serializer.data})
        

    def delete(self, id):
        task = self.get_task(id)
        task.delete()
        return Response({"sucess": True})
