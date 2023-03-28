from django.urls import path

from authentication import views

app_name = "authentication"

urlpatterns = [
    path("login/", views.UserLoginApiView.as_view(), name='login'),
    path("logout/", views.UserLogoutApiView.as_view(), name='logout'),
    path("register/", views.UserRegisterApiView.as_view(), name='register'),
]