from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.db.models import Count
from django.db.models.functions import TruncDay, TruncMonth, TruncYear

from .models import Laporan


@admin.register(Laporan)
class LaporanAdmin(admin.ModelAdmin):

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
    )

    # ===== TAMBAH MENU DASHBOARD ADMIN =====
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "dashboard/",
                self.admin_site.admin_view(self.dashboard_view),
                name="laporan_dashboard",
            ),
        ]
        return custom_urls + urls

    # ===== VIEW DASHBOARD =====
    def dashboard_view(self, request):

        qs = Laporan.objects.all()

        grafik_status = qs.values("status").annotate(total=Count("id"))
        grafik_jenis = qs.values("jenis_bullying").annotate(total=Count("id"))
        grafik_kelas = qs.values("kelas_korban").annotate(total=Count("id"))

        grafik_tren = (
            qs.annotate(waktu=TruncMonth("tanggal"))
            .values("waktu")
            .annotate(total=Count("id"))
            .order_by("waktu")
        )

        context = dict(
            self.admin_site.each_context(request),

            grafik_status=list(grafik_status),
            grafik_jenis=list(grafik_jenis),
            grafik_kelas=list(grafik_kelas),
            grafik_tren=list(grafik_tren),

            total_laporan=qs.count(),
            laporan_baru=qs.filter(status="baru").count(),
            diproses=qs.filter(status="diproses").count(),
            selesai=qs.filter(status="selesai").count(),
        )

        return render(request, "admin/laporan/dashboard.html", context)

    @admin.display(description="Pelapor")
    def get_pelapor_admin(self, obj):
        return obj.pelapor.get_full_name() or obj.pelapor.username
