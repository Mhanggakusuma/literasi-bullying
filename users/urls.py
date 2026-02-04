from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
# Routing URL untuk fitur autentikasi user seperti login, register, logout, profil, dan ganti password
urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.LogoutAllowGet.as_view(), name="logout"),

    path("lengkapi-profil/", views.lengkapi_profil, name="lengkapi_profil"),

    path("lupa-password/", views.lupa_password_view, name="lupa_password"),

    path(
        "password/change/",
        auth_views.PasswordChangeView.as_view(
            template_name="users/change_password.html",
            success_url="/users/password/change/done/"
        ),
        name="password_change"
    ),

    path(
        "password/change/done/",
        views.password_change_done_view,
        name="password_change_done"
    ),
]
