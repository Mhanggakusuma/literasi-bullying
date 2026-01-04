from django.urls import path
from . import views

urlpatterns = [
    # PUBLIC
    path('', views.dashboard_home, name='dashboard_home'),

    # REDIRECT SETELAH LOGIN
    path('home/', views.dashboard_redirect, name='dashboard_redirect'),

    # DASHBOARD ROLE
    path('siswa/', views.dashboard_siswa, name='dashboard_siswa'),
    path('guru/', views.dashboard_guru, name='dashboard_guru'),
    path('admin/', views.dashboard_admin, name='dashboard_admin'),

    # TENTANG BULLYING
    path('tentang-bullying/', views.tentang_bullying_public, name='tentang_bullying_public'),
    path('tentang-bullying/login/', views.tentang_bullying_login, name='tentang_bullying_login'),
]
