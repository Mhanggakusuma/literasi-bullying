from django.contrib import admin
from .models import Laporan

# Konfigurasi tampilan dan pengelolaan data laporan bullying pada Django Admin
@admin.register(Laporan)
class LaporanAdmin(admin.ModelAdmin):
    """
    Konfigurasi Admin untuk Laporan Bullying.
    - Guru BK: status diubah otomatis via sistem
    - Admin: tetap bisa memantau & mengoreksi jika diperlukan
    """

    list_display = (
        "kode_laporan",
        "get_pelapor_admin",
        "nama_korban",
        "kelas_korban",
        "jenis_bullying",
        "status",
        "tanggal",
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


    readonly_fields = (
        "kode_laporan",
        "tanggal",
    )

    # Menampilkan nama pelapor pada halaman admin
    @admin.display(description="Pelapor")
    def get_pelapor_admin(self, obj):
        """
        Di Admin:
        - Identitas pelapor selalu terlihat
        - Anonimitas hanya berlaku di UI siswa/BK
        """
        return obj.pelapor.get_full_name() or obj.pelapor.username
