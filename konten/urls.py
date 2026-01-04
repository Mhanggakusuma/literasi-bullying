from django.urls import path
from . import views

urlpatterns = [
    # Halaman utama konten (tab Artikel / Video / Kuis)
    path("", views.konten_index, name="konten_index"),

    # Artikel
    path("artikel/<int:id>/", views.artikel_detail, name="artikel_detail"),

    # Kuis
    path("kuis/<int:id>/", views.kuis_detail, name="konten_kuis_detail"),
]
