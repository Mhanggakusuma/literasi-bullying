from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Laporan


@admin.register(Laporan)
class LaporanAdmin(admin.ModelAdmin):

    # =================================================
    # TEMPLATE CUSTOM UNTUK TOMBOL DASHBOARD
    # =================================================
    change_list_template = "admin/laporan/change_list.html"

    # =================================================
    # TAMPILAN LIST DATA ADMIN
    # =================================================
    list_display = (
        "kode_laporan",
        "get_pelapor_admin",
        "nama_korban",
        "kelas_korban",
        "jenis_bullying",
        "status",
        "tanggal",
        "dashboard_button",   # ⭐ Tombol Dashboard
    )

    list_filter = (
        "status",
        "jenis_bullying",
        "kelas_korban",
        "tanggal",
    )

    search_fields = (
        "kode_laporan",
        "pelapor__username",
        "pelapor__first_name",
        "pelapor__last_name",
        "nama_korban",
        "nama_terlapor",
        "lokasi_kejadian",
    )

    readonly_fields = (
        "kode_laporan",
        "tanggal",
    )

    # =================================================
    # FIELDSET TAMPILAN ADMIN
    # =================================================
    fieldsets = (
        ("🔒 Identitas Pelapor (Internal)", {
            "fields": (
                "pelapor",
                "is_anonymous",
            )
        }),

        ("🕒 Waktu & Tempat Kejadian", {
            "fields": (
                "tanggal_kejadian",
                "perkiraan_waktu",
                "lokasi_kejadian",
            )
        }),

        ("👤 Korban & Terlapor", {
            "fields": (
                "nama_korban",
                "kelas_korban",
                "nama_terlapor",
                "kelas_terlapor",
            )
        }),

        ("🚨 Detail Perundungan", {
            "fields": (
                "jenis_bullying",
                "isi_laporan",
                "bukti",
            )
        }),

        ("💔 Dampak & Harapan", {
            "fields": (
                "dampak_korban",
                "dampak_lainnya",
                "harapan_pelapor",
            )
        }),

        ("🧾 Tindak Lanjut Guru BK", {
            "fields": (
                "status",
                "catatan_bk",
                "bukti_tindak_lanjut",
            )
        }),

        ("🔑 Meta Data", {
            "fields": (
                "kode_laporan",
                "tanggal",
            )
        }),
    )

    # =================================================
    # TAMPILKAN NAMA PELAPOR
    # =================================================
    @admin.display(description="Pelapor")
    def get_pelapor_admin(self, obj):
        return obj.pelapor.get_full_name() or obj.pelapor.username

    # =================================================
    # TOMBOL DASHBOARD BK
    # =================================================
    @admin.display(description="Dashboard")
    def dashboard_button(self, obj=None):
        url = reverse("bk_dashboard")
        return format_html(
            '<a class="button" href="{}" target="_blank">📊 Dashboard BK</a>',
            url
        )
