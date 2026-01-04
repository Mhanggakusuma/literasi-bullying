from django.contrib import admin
from .models import Laporan

@admin.register(Laporan)
class LaporanAdmin(admin.ModelAdmin):
    list_display = (
        "kode_laporan",
        "nama_pelapor",
        "kelas_pelapor",
        "terlapor",
        "status",
        "tanggal",
    )

    search_fields = ("kode_laporan", "nama_pelapor", "terlapor")
    list_filter = ("status", "tanggal")
