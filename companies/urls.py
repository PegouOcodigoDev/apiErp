from django.urls import path

from companies.views.employee import Employees, EmployeeDetail
from companies.views.permissions import PermissionDetail

urlpatterns = [
    path('employees', Employees.as_view()),
    path('employee/<int:id>', EmployeeDetail.as_view()),
    path('permissions', PermissionDetail.as_view())
]


