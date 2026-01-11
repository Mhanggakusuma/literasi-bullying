from django.urls import path
from . import views

urlpatterns = [

    # =========================
    # SISWA
    # =========================
    path(
        "",
        views.laporan_home,
        name="laporan_home"
    ),

    path(
        "lapor/",
        views.buat_laporan,
        name="buat_laporan"
    ),

    path(
        "cek/",
        views.cek_laporan,
        name="cek_laporan"
    ),

    # =========================
    # GURU BK / ADMIN
    # =========================
    path(
        "bk/dashboard/",
        views.bk_dashboard,
        name="bk_dashboard"
    ),

    path(
        "bk/laporan/<int:pk>/",
        views.bk_tindak_lanjut,
        name="bk_tindak_lanjut"
    ),

    path(
        "bk/download/",
        views.bk_download_laporan,
        name="bk_download_laporan"
    ),
]
