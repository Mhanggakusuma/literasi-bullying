from django.contrib import admin
from django.db.models import Count
from django.db.models.functions import TruncDay, TruncMonth, TruncYear
from .models import Laporan


@admin.register(Laporan)
class LaporanAdmin(admin.ModelAdmin):

    change_list_template = "admin/laporan/laporan_change_list.html"

    list_display = (
        "kode_laporan",
        "get_pelapor_admin",
        "nama_korban",
        "kelas_korban",
        "jenis_bullying",
        "status",
        "tanggal",
    )

    readonly_fields = ("kode_laporan", "tanggal")


    # ================= FILTER CUSTOM =================
    def filter_queryset(self, request):

        qs = Laporan.objects.all()

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

        if periode == "hari" and tanggal:
            qs = qs.filter(tanggal__date=tanggal)

        elif periode == "bulan" and bulan and tahun:
            qs = qs.filter(
                tanggal__month=bulan,
                tanggal__year=tahun
            )

        elif periode == "tahun" and tahun:
            qs = qs.filter(tanggal__year=tahun)

        return qs


    # ================= DASHBOARD ADMIN =================
    def changelist_view(self, request, extra_context=None):

        response = super().changelist_view(request, extra_context=extra_context)

        # 🔥 Gunakan filter custom
        qs = self.filter_queryset(request)

        # ===== Grafik =====
        grafik_status = list(qs.values("status").annotate(total=Count("id")))
        grafik_jenis = list(qs.values("jenis_bullying").annotate(total=Count("id")))
        grafik_kelas = list(qs.values("kelas_korban").annotate(total=Count("id")))

        periode = request.GET.get("periode")

        if periode == "hari":
            grafik_tren = list(
                qs.annotate(waktu=TruncDay("tanggal"))
                .values("waktu")
                .annotate(total=Count("id"))
                .order_by("waktu")
            )

        elif periode == "tahun":
            grafik_tren = list(
                qs.annotate(waktu=TruncYear("tanggal"))
                .values("waktu")
                .annotate(total=Count("id"))
                .order_by("waktu")
            )

        else:
            grafik_tren = list(
                qs.annotate(waktu=TruncMonth("tanggal"))
                .values("waktu")
                .annotate(total=Count("id"))
                .order_by("waktu")
            )

        daftar_tahun = Laporan.objects.dates("tanggal", "year")

        response.context_data.update({
            "total_laporan": qs.count(),
            "laporan_baru": qs.filter(status="baru").count(),
            "diproses": qs.filter(status="diproses").count(),
            "selesai": qs.filter(status="selesai").count(),

            "grafik_status": grafik_status,
            "grafik_jenis": grafik_jenis,
            "grafik_kelas": grafik_kelas,
            "grafik_tren": grafik_tren,

            "jenis_choices": Laporan.JENIS_BULLYING_CHOICES,
            "kelas_choices": Laporan.KELAS_CHOICES,
            "daftar_tahun": daftar_tahun,
        })

        return response


    @admin.display(description="Pelapor")
    def get_pelapor_admin(self, obj):
        return obj.pelapor.get_full_name() or obj.pelapor.username
