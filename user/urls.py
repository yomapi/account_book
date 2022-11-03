from django.urls import path
from user.views import signup, login

urlpatterns = [
    path("signup/", signup),
    path("login/", login),
]
