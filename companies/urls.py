from django.urls import path

from companies.views.employee import Employees, EmployeeDetail
from companies.views.permissions import PermissionDetail
from companies.views.groups import Groups, GroupDetail
from companies.views.tasks import Tasks, TaskDetail

urlpatterns = [
    path('employees', Employees.as_view(), name="employees"),
    path('employees/<int:id>', EmployeeDetail.as_view(),name="employee_datail"),
    path('permissions', PermissionDetail.as_view(), name="permissions"),
    path('groups', Groups.as_view(), name="groups"),
    path('groups/<int:id>', GroupDetail.as_view(), name="group_datail"),
    path('tasks', Tasks.as_view(), name="tasks"),
    path('tasks/<int:id>', TaskDetail.as_view(), name="task_detail")
]


