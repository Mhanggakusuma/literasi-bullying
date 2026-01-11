from django.contrib import admin
from .models import Laporan


@admin.register(Laporan)
class LaporanAdmin(admin.ModelAdmin):
    """
    Konfigurasi admin untuk laporan bullying.
    Identitas pelapor tetap dapat diakses oleh Admin.
    """

    # =========================
    # TAMPILAN LIST
    # =========================
    list_display = (
        "kode_laporan",
        "get_pelapor_admin",
        "is_anonymous",
        "nama_korban",
        "kelas_korban",
        "jenis_bullying",
        "status",
        "tanggal",
    )

    # =========================
    # FILTER & SEARCH
    # =========================
    list_filter = (
        "status",
        "jenis_bullying",
        "is_anonymous",
        "tanggal",
    )

    search_fields = (
        "kode_laporan",
        "pelapor__username",
        "pelapor__first_name",
        "pelapor__last_name",
        "nama_korban",
        "nama_terlapor",
    )

    # =========================
    # FIELD GROUPING
    # =========================
    fieldsets = (
        ("Identitas Pelapor (Internal)", {
            "fields": (
                "pelapor",
                "is_anonymous",
            )
        }),
        ("Korban & Terlapor", {
            "fields": (
                "nama_korban",
                "kelas_korban",
                "nama_terlapor",
                "kelas_terlapor",
            )
        }),
        ("Detail Perundungan", {
            "fields": (
                "jenis_bullying",
                "isi_laporan",
                "bukti",
            )
        }),
        ("Tindak Lanjut Guru BK", {
            "fields": (
                "status",
                "catatan_bk",
                "bukti_tindak_lanjut",
            )
        }),
        ("Meta Data", {
            "fields": (
                "kode_laporan",
                "tanggal",
            )
        }),
    )

    readonly_fields = (
        "kode_laporan",
        "tanggal",
    )

    # =========================
    # HELPER ADMIN
    # =========================
    @admin.display(description="Pelapor")
    def get_pelapor_admin(self, obj):
        """
        Di admin panel:
        Tetap tampilkan identitas asli,
        meskipun laporan anonim.
        """
        return obj.pelapor.get_full_name() or obj.pelapor.username
