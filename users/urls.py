from django.urls import path

from .views import CustomLoginView, CustomLogoutView, RegisterView, UsersListView, UserProfileDetailView

app_name = "users"

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("all-users/", UsersListView.as_view(), name="all-users"),
    path("user-profile/<int:pk>/", UserProfileDetailView.as_view(), name="user-profile")
]
