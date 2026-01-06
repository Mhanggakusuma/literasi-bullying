from django.urls import path
from . import views

urlpatterns = [
    # Halaman utama konten
    path("", views.konten_index, name="konten_index"),

    # Artikel
    path("artikel/<int:id>/", views.artikel_detail, name="artikel_detail"),

    # 🔥 DOWNLOAD PDF (LEWAT DJANGO)
    path(
        "artikel/<int:id>/download/",
        views.download_artikel_pdf,
        name="download_artikel_pdf"
    ),

    # Kuis
    path("kuis/<int:id>/", views.kuis_detail, name="konten_kuis_detail"),
]
