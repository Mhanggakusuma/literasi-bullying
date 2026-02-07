from django.contrib import admin
from django.db.models import Count
from django.db.models.functions import TruncMonth
from .models import Laporan


@admin.register(Laporan)
class LaporanAdmin(admin.ModelAdmin):

    # Template dashboard custom
    change_list_template = "admin/laporan_change_list.html"

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
        "nama_korban",
        "nama_terlapor",
    )

    readonly_fields = ("kode_laporan", "tanggal")

    # =================================================
    # DASHBOARD ANALITIK ADMIN
    # =================================================
    def changelist_view(self, request, extra_context=None):

        queryset = self.get_queryset(request)

        # ===== SUMMARY =====
        total_laporan = queryset.count()
        laporan_baru = queryset.filter(status="baru").count()
        sedang_diproses = queryset.filter(status="diproses").count()
        selesai = queryset.filter(status="selesai").count()

        # ===== GRAFIK =====
        grafik_status = queryset.values("status").annotate(total=Count("id"))
        grafik_jenis = queryset.values("jenis_bullying").annotate(total=Count("id"))
        grafik_kelas = queryset.values("kelas_korban").annotate(total=Count("id"))

        grafik_tren = (
            queryset
            .annotate(bulan=TruncMonth("tanggal"))
            .values("bulan")
            .annotate(total=Count("id"))
            .order_by("bulan")
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

        return super().changelist_view(request, extra_context=extra_context)

    # =================================================
    @admin.display(description="Pelapor")
    def get_pelapor_admin(self, obj):
        return obj.pelapor.get_full_name() or obj.pelapor.username
