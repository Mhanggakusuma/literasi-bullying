from django.contrib import admin
from django.db.models import Count
from django.db.models.functions import (
    TruncDay, TruncMonth, TruncYear, ExtractYear
)

from .models import Laporan


@admin.register(Laporan)
class LaporanAdmin(admin.ModelAdmin):

    change_list_template = "admin/laporan_dashboard.html"

    list_display = (
        "kode_laporan",
        "pelapor_display",
        "korban_display",
        "kelas_korban",
        "jenis_bullying",
        "status",
        "tanggal",
    )

    # ================= DISPLAY =================
    def pelapor_display(self, obj):
        return "Anonim 🔒" if obj.is_anonymous else obj.pelapor

    def korban_display(self, obj):
        return "Anonim 🔒" if obj.is_korban_anonim else obj.nama_korban

    # ================= FILTER QUERY =================
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        jenis = request.GET.get("jenis")
        kelas = request.GET.get("kelas")
        status = request.GET.get("status")

        periode = request.GET.get("periode")

        tahun = request.GET.get("tahun")
        bulan = request.GET.get("bulan")
        hari = request.GET.get("hari")

        # FILTER UMUM
        if jenis:
            qs = qs.filter(jenis_bullying=jenis)

        if kelas:
            qs = qs.filter(kelas_korban=kelas)

        if status:
            qs = qs.filter(status=status)

        # FILTER WAKTU
        if periode == "tahun":
            if tahun:
                qs = qs.filter(tanggal__year=tahun)

        elif periode == "bulan":
            if tahun:
                qs = qs.filter(tanggal__year=tahun)

            if bulan:
                qs = qs.filter(tanggal__month=bulan)

        elif periode == "hari":
            if hari:
                qs = qs.filter(tanggal=hari)

        return qs

    # ================= DASHBOARD =================
    def changelist_view(self, request, extra_context=None):

        qs = self.get_queryset(request)
        periode = request.GET.get("periode", "all")

        # ===== SUMMARY =====
        total = qs.count()
        baru = qs.filter(status="baru").count()
        diproses = qs.filter(status="diproses").count()
        selesai = qs.filter(status="selesai").count()

        # ===== GRAFIK =====
        grafik_status = qs.values("status").annotate(total=Count("id"))
        grafik_jenis = qs.values("jenis_bullying").annotate(total=Count("id"))
        grafik_kelas = qs.values("kelas_korban").annotate(total=Count("id"))

        # ===== TREN =====
        if periode == "hari":
            grafik_tren = qs.annotate(
                waktu=TruncDay("tanggal")
            ).values("waktu").annotate(total=Count("id")).order_by("waktu")

        elif periode == "tahun":
            grafik_tren = qs.annotate(
                waktu=TruncYear("tanggal")
            ).values("waktu").annotate(total=Count("id")).order_by("waktu")

        else:
            grafik_tren = qs.annotate(
                waktu=TruncMonth("tanggal")
            ).values("waktu").annotate(total=Count("id")).order_by("waktu")

        tahun_list = (
            Laporan.objects
            .annotate(tahun=ExtractYear("tanggal"))
            .values_list("tahun", flat=True)
            .distinct()
            .order_by("tahun")
        )

        extra_context = extra_context or {}
        extra_context.update({

            "total_laporan": total,
            "laporan_baru": baru,
            "laporan_diproses": diproses,
            "laporan_selesai": selesai,

            "grafik_status": list(grafik_status),
            "grafik_jenis": list(grafik_jenis),
            "grafik_kelas": list(grafik_kelas),
            "grafik_tren": list(grafik_tren),

            "jenis_choices": Laporan.JENIS_BULLYING_CHOICES,
            "kelas_choices": Laporan.KELAS_CHOICES,

            "tahun_list": tahun_list,
            "periode": periode,
            "request": request,
        })

        return super().changelist_view(request, extra_context=extra_context)
