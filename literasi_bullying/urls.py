from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static

def home(request):
    return HttpResponse("Literasi Bullying – Railway OK")

urlpatterns = [
    path('', home),  # ⬅️ TEST ROOT (WAJIB)
    path('admin/', admin.site.urls),

    path('users/', include('users.urls')),
    path('konten/', include('konten.urls')),
    path('laporan/', include('laporan.urls')),
    path('dashboard/', include('dashboard.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
