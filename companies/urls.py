from django.urls import path

from companies.views.employee import Employees, EmployeeDetail

urlpatterns = [
    path('employees', Employees.as_view()),
    path('employee/<int:id>', EmployeeDetail.as_view()),
]


