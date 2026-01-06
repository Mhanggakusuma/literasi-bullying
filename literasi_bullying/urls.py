# literasi_bullying/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('users/', include('users.urls')),
    path('konten/', include('konten.urls')),
    path('laporan/', include('laporan.urls')),
    path('dashboard/', include('dashboard.urls')),

    # ROOT → landing page publik
    path('', include('dashboard.urls')),
]
