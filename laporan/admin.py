from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.db.models import Count
from django.db.models.functions import TruncDay, TruncMonth
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

    # ===== URL DASHBOARD =====
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

    # ===== DASHBOARD VIEW =====
    def dashboard_view(self, request):

        qs = Laporan.objects.all()

        # ===== FILTER DASAR =====
        jenis = request.GET.get("jenis")
        kelas = request.GET.get("kelas")
        status = request.GET.get("status")

        periode = request.GET.get("periode")
        tanggal = request.GET.get("tanggal")
        bulan = request.GET.get("bulan")
        tahun = request.GET.get("tahun")

        if jenis:
            qs = qs.filter(jenis_bullying=jenis)

        if kelas:
            qs = qs.filter(kelas_korban=kelas)

        if status:
            qs = qs.filter(status=status)

        # ===== FILTER PERIODE =====
        if periode == "hari" and tanggal:
            qs = qs.filter(tanggal__date=tanggal)

        elif periode == "bulan" and bulan and tahun:
            qs = qs.filter(
                tanggal__month=bulan,
                tanggal__year=tahun
            )

        elif periode == "tahun" and tahun:
            qs = qs.filter(tanggal__year=tahun)

        # ===== GRAFIK =====
        grafik_status = qs.values("status").annotate(total=Count("id"))
        grafik_jenis = qs.values("jenis_bullying").annotate(total=Count("id"))
        grafik_kelas = qs.values("kelas_korban").annotate(total=Count("id"))

        # ===== GRAFIK TREN =====
        if periode == "hari":
            grafik_tren = (
                qs.annotate(waktu=TruncDay("tanggal"))
                .values("waktu")
                .annotate(total=Count("id"))
                .order_by("waktu")
            )
        else:
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

            jenis_choices=Laporan.JENIS_BULLYING_CHOICES,
            kelas_choices=Laporan.KELAS_CHOICES,
            daftar_tahun=Laporan.objects.dates("tanggal", "year"),
        )

        return render(request, "admin/laporan/dashboard.html", context)

    @admin.display(description="Pelapor")
    def get_pelapor_admin(self, obj):
        return obj.pelapor.get_full_name() or obj.pelapor.username
