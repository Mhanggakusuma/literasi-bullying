from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.core.serializers.json import DjangoJSONEncoder
import json

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
    # TAMBAH URL DASHBOARD ADMIN
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

        jenis = list(
            laporan.values("jenis_bullying")
            .annotate(total=Count("id"))
        )

        kelas = list(
            laporan.values("kelas_korban")
            .annotate(total=Count("id"))
        )

        status = list(
            laporan.values("status")
            .annotate(total=Count("id"))
        )

        waktu = list(
            laporan.annotate(bulan=TruncMonth("tanggal"))
            .values("bulan")
            .annotate(total=Count("id"))
            .order_by("bulan")
        )

        context = dict(
            self.admin_site.each_context(request),

            jenis_json=json.dumps(jenis, cls=DjangoJSONEncoder),
            kelas_json=json.dumps(kelas, cls=DjangoJSONEncoder),
            status_json=json.dumps(status, cls=DjangoJSONEncoder),
            waktu_json=json.dumps(waktu, cls=DjangoJSONEncoder),
        )

        return render(request, "admin/laporan/dashboard.html", context)

    # =================================================
    # TAMPILKAN NAMA PELAPOR
    # =================================================
    @admin.display(description="Pelapor")
    def get_pelapor_admin(self, obj):
        return obj.pelapor.get_full_name() or obj.pelapor.username
