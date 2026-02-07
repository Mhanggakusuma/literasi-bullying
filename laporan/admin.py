from django.contrib import admin
from django.db.models import Count
from django.db.models.functions import TruncDay, TruncMonth, TruncYear
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

    list_filter = (
        "status",
        "jenis_bullying",
        "kelas_korban",
        "tanggal",
    )

    search_fields = (
        "kode_laporan",
        "nama_korban",
        "nama_terlapor",
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

    # ================= DASHBOARD DATA =================
    def changelist_view(self, request, extra_context=None):

        qs = Laporan.objects.all()

        # ===== FILTER MANUAL =====
        jenis = request.GET.get("jenis")
        kelas = request.GET.get("kelas")
        status = request.GET.get("status")
        periode = request.GET.get("periode", "bulan")

        if jenis:
            qs = qs.filter(jenis_bullying=jenis)

        if kelas:
            qs = qs.filter(kelas_korban=kelas)

        if status:
            qs = qs.filter(status=status)

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
            "periode": periode
        })

        return super().changelist_view(request, extra_context=extra_context)
