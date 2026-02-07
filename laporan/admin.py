from django.contrib import admin
from django.db.models import Count
from django.db.models.functions import TruncMonth
from .models import Laporan


@admin.register(Laporan)
class LaporanAdmin(admin.ModelAdmin):

    change_list_template = "admin/laporan/laporan/change_list.html"

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
    )

    readonly_fields = ("kode_laporan", "tanggal")

    # ===============================
    # ADMIN DASHBOARD ANALITIK
    # ===============================
    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context)

        cl = response.context_data.get("cl")
        if not cl:
            return response

        qs = cl.queryset

        extra_context = extra_context or {}
        extra_context.update({
            "total_laporan": qs.count(),
            "laporan_baru": qs.filter(status="baru").count(),
            "sedang_diproses": qs.filter(status="diproses").count(),
            "selesai": qs.filter(status="selesai").count(),

            "grafik_status": list(qs.values("status").annotate(total=Count("id"))),
            "grafik_jenis": list(qs.values("jenis_bullying").annotate(total=Count("id"))),
            "grafik_kelas": list(qs.values("kelas_korban").annotate(total=Count("id"))),
            "grafik_tren": list(
                qs.annotate(waktu=TruncMonth("tanggal"))
                  .values("waktu")
                  .annotate(total=Count("id"))
                  .order_by("waktu")
            ),
        })

        response.context_data.update(extra_context)
        return response

    @admin.display(description="Pelapor")
    def get_pelapor_admin(self, obj):
        return obj.pelapor.get_full_name() or obj.pelapor.username
