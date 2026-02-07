from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.db.models import Count
from django.db.models.functions import TruncMonth

from .models import Laporan


@admin.register(Laporan)
class LaporanAdmin(admin.ModelAdmin):

    change_list_template = "admin/laporan/change_list.html"

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

    # =================================================
    # TAMBAH URL ADMIN DASHBOARD
    # =================================================
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

    # =================================================
    # VIEW DASHBOARD ADMIN
    # =================================================
    def dashboard_view(self, request):

        laporan = Laporan.objects.all()

        jenis = laporan.values("jenis_bullying").annotate(total=Count("id"))
        kelas = laporan.values("kelas_korban").annotate(total=Count("id"))
        status = laporan.values("status").annotate(total=Count("id"))

        waktu = laporan.annotate(
            bulan=TruncMonth("tanggal")
        ).values("bulan").annotate(total=Count("id")).order_by("bulan")

        context = dict(
            self.admin_site.each_context(request),
            jenis=list(jenis),
            kelas=list(kelas),
            status=list(status),
            waktu=list(waktu),
        )

        return render(request, "admin/laporan/dashboard.html", context)

    @admin.display(description="Pelapor")
    def get_pelapor_admin(self, obj):
        return obj.pelapor.get_full_name() or obj.pelapor.username
