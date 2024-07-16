from accounts.views.signin import Signin
from accounts.views.signup import Signup
from accounts.views.user import UserView
from django.urls import path

urlpatterns = [
    path('signin', Signin.as_view(), name='signin'),
    path('signup', Signup.as_view(), name='signup' ),
    path("user", UserView.as_view(), name="user"),
]