from django.urls import path
from user.views import UserCreateView, LoginView, UserUpdateView

urlpatterns = [
    path("create/", UserCreateView.as_view(), name="user-create"),
    path("login/", LoginView.as_view(), name="login"),
    path("update/", UserUpdateView.as_view(), name="update")
]

app_name = "user"