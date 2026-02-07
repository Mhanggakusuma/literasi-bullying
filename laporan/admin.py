from django.contrib import admin
from django.db.models import Count
from django.db.models.functions import (
    TruncDay, TruncMonth, TruncYear, ExtractYear
)
from datetime import datetime

from .models import Laporan


@admin.register(Laporan)
class LaporanAdmin(admin.ModelAdmin):

    list_display = (
        "kode_laporan",
        "pelapor_display",
        "korban_display",
        "kelas_korban",
        "jenis_bullying",
        "status",
        "tanggal",
    )

    change_list_template = "admin/laporan_dashboard.html"

    # ================= DISPLAY =================
    @admin.display(description="Pelapor")
    def pelapor_display(self, obj):
        if obj.is_anonymous:
            return "Anonim 🔒"
        return obj.pelapor.get_full_name() or obj.pelapor.username

    @admin.display(description="Korban")
    def korban_display(self, obj):
        if obj.is_korban_anonim:
            return "Anonim 🔒"
        return obj.nama_korban

    # ================= DASHBOARD =================
    def changelist_view(self, request, extra_context=None):

        qs = Laporan.objects.all()

        jenis = request.GET.get("jenis")
        kelas = request.GET.get("kelas")
        status = request.GET.get("status")

        periode = request.GET.get("periode", "all")
        tanggal_full = request.GET.get("tanggal_full")

        # ===== FILTER DASAR =====
        if jenis:
            qs = qs.filter(jenis_bullying=jenis)

        if kelas:
            qs = qs.filter(kelas_korban=kelas)

        if status:
            qs = qs.filter(status=status)

        # ===== FILTER TANGGAL DARI DATEPICKER =====
        if tanggal_full:
            try:
                dt = datetime.strptime(tanggal_full, "%Y-%m-%d")

                qs = qs.filter(
                    tanggal__year=dt.year,
                    tanggal__month=dt.month,
                    tanggal__day=dt.day
                )

            except:
                pass

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

        elif periode == "bulan":
            grafik_tren = qs.annotate(
                waktu=TruncMonth("tanggal")
            ).values("waktu").annotate(total=Count("id")).order_by("waktu")

        elif periode == "tahun":
            grafik_tren = qs.annotate(
                waktu=TruncYear("tanggal")
            ).values("waktu").annotate(total=Count("id")).order_by("waktu")

        else:
            grafik_tren = qs.annotate(
                waktu=TruncMonth("tanggal")
            ).values("waktu").annotate(total=Count("id")).order_by("waktu")

        # ===== LIST TAHUN DINAMIS =====
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

            "periode": periode,
            "tanggal_full": tanggal_full,
            "tahun_list": tahun_list,
        })

        return super().changelist_view(request, extra_context=extra_context)
