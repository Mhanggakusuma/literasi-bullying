from django.contrib import admin
from django.db.models import Count
from django.db.models.functions import TruncMonth
from .models import Laporan


@admin.register(Laporan)
class LaporanAdmin(admin.ModelAdmin):

    # ===============================
    # TEMPLATE ADMIN CUSTOM
    # ===============================
    change_list_template = "admin/laporan/laporan/change_list.html"

    # ===============================
    # TAMPILAN LIST
    # ===============================
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

    readonly_fields = (
        "kode_laporan",
        "tanggal",
    )

    # ===============================
    # DASHBOARD ANALITIK ADMIN
    # ===============================
    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context)

        try:
            qs = response.context_data["cl"].queryset
        except (AttributeError, KeyError):
            return response

        # ===== STATISTIK =====
        total_laporan = qs.count()
        laporan_baru = qs.filter(status="baru").count()
        sedang_diproses = qs.filter(status="diproses").count()
        selesai = qs.filter(status="selesai").count()

        # ===== GRAFIK =====
        grafik_status = qs.values("status").annotate(total=Count("id"))
        grafik_jenis = qs.values("jenis_bullying").annotate(total=Count("id"))
        grafik_kelas = qs.values("kelas_korban").annotate(total=Count("id"))

        grafik_tren = (
            qs.annotate(waktu=TruncMonth("tanggal"))
            .values("waktu")
            .annotate(total=Count("id"))
            .order_by("waktu")
        )

        extra_context = extra_context or {}
        extra_context.update({
            "total_laporan": total_laporan,
            "laporan_baru": laporan_baru,
            "sedang_diproses": sedang_diproses,
            "selesai": selesai,
            "grafik_status": list(grafik_status),
            "grafik_jenis": list(grafik_jenis),
            "grafik_kelas": list(grafik_kelas),
            "grafik_tren": list(grafik_tren),
        })

        response.context_data.update(extra_context)
        return response

    # ===============================
    # PELAPOR SELALU TERLIHAT DI ADMIN
    # ===============================
    @admin.display(description="Pelapor")
    def get_pelapor_admin(self, obj):
        return obj.pelapor.get_full_name() or obj.pelapor.username
