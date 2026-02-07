from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # ⭐ WAJIB untuk django-admin-charts
    path('admin_tools_stats/', include('admin_tools_stats.urls')),

    path('users/', include('users.urls')),
    path('konten/', include('konten.urls')),
    path('laporan/', include('laporan.urls')),
    path('dashboard/', include('dashboard.urls')),

    path('', include('dashboard.urls')),
]
