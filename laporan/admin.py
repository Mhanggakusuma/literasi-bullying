from django.contrib import admin
from django.db.models import Count
from django.db.models.functions import TruncMonth
from .models import Laporan


@admin.register(Laporan)
class LaporanAdmin(admin.ModelAdmin):
    """
    Konfigurasi Admin untuk Laporan Bullying.
    """

    # ================= TEMPLATE DASHBOARD =================
    change_list_template = "admin/laporan/laporan_change_list.html"

    # ================= LIST DATA =================
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

    # ================= FORM ADMIN =================
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

    # ================= DATA GRAFIK DASHBOARD =================
    def changelist_view(self, request, extra_context=None):

        qs = Laporan.objects.all()

        grafik_status = list(
            qs.values("status").annotate(total=Count("id"))
        )

        grafik_jenis = list(
            qs.values("jenis_bullying").annotate(total=Count("id"))
        )

        grafik_kelas = list(
            qs.values("kelas_korban").annotate(total=Count("id"))
        )

        grafik_tren = list(
            qs.annotate(waktu=TruncMonth("tanggal"))
            .values("waktu")
            .annotate(total=Count("id"))
            .order_by("waktu")
        )

        extra_context = extra_context or {}
        extra_context.update({
            "total_laporan": qs.count(),
            "laporan_baru": qs.filter(status="baru").count(),
            "diproses": qs.filter(status="diproses").count(),
            "selesai": qs.filter(status="selesai").count(),

            "grafik_status": grafik_status,
            "grafik_jenis": grafik_jenis,
            "grafik_kelas": grafik_kelas,
            "grafik_tren": grafik_tren,
        })

        return super().changelist_view(request, extra_context=extra_context)

    # ================= TAMPIL PELAPOR =================
    @admin.display(description="Pelapor")
    def get_pelapor_admin(self, obj):
        return obj.pelapor.get_full_name() or obj.pelapor.username
