from django.urls import path
from user.views import UserCreateView, LoginView, UserUpdateView, LogoutView

urlpatterns = [
    path("create/", UserCreateView.as_view(), name="user-create"),
    path("login/", LoginView.as_view(), name="login"),
    path("update/", UserUpdateView.as_view(), name="update"),
    path("delete/", LogoutView.as_view(), name="delete-token")
]

app_name = "user"