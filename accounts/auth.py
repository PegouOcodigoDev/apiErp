from rest_framework.exceptions import APIException, AuthenticationFailed
from django.contrib.auth.hashers import check_password, make_password
from django.db import transaction

from accounts.models import User
from companies.models import Enterprise, Employee


class AuthHandler:
    @staticmethod
    def validate_user_data(name, email, password):
        if not name or name.strip() == '':
            raise APIException("O nome não pode estar vazio.")
        
        if not email or email.strip() == '':
            raise APIException("O email não pode estar vazio.")
        
        if not password or password.strip() == '':
            raise APIException("A senha não pode estar vazia.")
        
        return True


class Authentication:
    @staticmethod
    def signin(email=None, password=None) -> User:
        exception_auth = AuthenticationFailed("Email e/ou senha incorreto(s)")

        user = User.objects.filter(email=email).first()
        if user is None or not check_password(password, user.password):
            raise exception_auth
        
        return user
    
    @staticmethod
    @transaction.atomic
    def signup(name, email, password, type_account="owner", company_id=None):
        AuthHandler.validate_user_data(name, email, password)

        if type_account == 'employee' and not company_id:
            raise APIException("O id da empresa não deve ser nulo")
        
        if User.objects.filter(email=email).exists():
            raise APIException("Este email já está cadastrado na plataforma")
        
        created_user = User.objects.create(
            name=name,
            email=email,
            password=make_password(password),
            is_owner=0 if type_account == "employee" else 1
        )

        if type_account == 'owner':
            Enterprise.objects.create(name="empresa",user_id=created_user.id)
        else:
            Employee.objects.create(enterprise_id=company_id,user_id=created_user.id)

        return created_user