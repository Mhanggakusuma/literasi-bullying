from django.contrib import admin
from django.db.models import Count
from django.db.models.functions import TruncDay, TruncMonth
from .models import Laporan


@admin.register(Laporan)
class LaporanAdmin(admin.ModelAdmin):

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

    list_filter = ()

    # ================= FILTER UTAMA =================
    def get_queryset(self, request):

        qs = super().get_queryset(request)

        jenis = request.GET.get("jenis")
        kelas = request.GET.get("kelas")
        status = request.GET.get("status")

        if jenis:
            qs = qs.filter(jenis_bullying=jenis)

        if kelas:
            qs = qs.filter(kelas_korban=kelas)

        if status:
            qs = qs.filter(status=status)

        return qs

    # ================= DASHBOARD =================
    def changelist_view(self, request, extra_context=None):

        response = super().changelist_view(request, extra_context)

        try:
            cl = response.context_data["cl"]
            qs = cl.queryset
        except:
            return response

        # SUMMARY
        total_laporan = qs.count()
        laporan_baru = qs.filter(status="baru").count()
        diproses = qs.filter(status="diproses").count()
        selesai = qs.filter(status="selesai").count()

        # GRAFIK
        grafik_status = list(
            qs.values("status").annotate(total=Count("id"))
        )

        grafik_jenis = list(
            qs.values("jenis_bullying").annotate(total=Count("id"))
        )

        grafik_kelas = list(
            qs.values("kelas_korban").annotate(total=Count("id"))
        )

        grafik_tren = list(
            qs.annotate(waktu=TruncMonth("tanggal"))
            .values("waktu")
            .annotate(total=Count("id"))
            .order_by("waktu")
        )

        response.context_data.update({
            "total_laporan": total_laporan,
            "laporan_baru": laporan_baru,
            "diproses": diproses,
            "selesai": selesai,
            "grafik_status": grafik_status,
            "grafik_jenis": grafik_jenis,
            "grafik_kelas": grafik_kelas,
            "grafik_tren": grafik_tren,
            "jenis_choices": Laporan.JENIS_BULLYING_CHOICES,
            "kelas_choices": Laporan.KELAS_CHOICES,
        })

        return response

    def get_pelapor_admin(self, obj):
        return obj.pelapor.username
