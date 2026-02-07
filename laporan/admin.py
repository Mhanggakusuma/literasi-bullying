from django.contrib import admin
from django.db.models import Count
from django.db.models.functions import TruncDay, TruncMonth, TruncYear
from django.contrib.admin import SimpleListFilter
from django.utils.translation import gettext_lazy as _
from .models import Laporan


# ================= CUSTOM FILTER PERIODE =================
class FilterPeriode(SimpleListFilter):
    title = _("Periode Laporan")
    parameter_name = "periode"

    def lookups(self, request, model_admin):
        return (
            ("hari", "Per Hari"),
            ("bulan", "Per Bulan"),
            ("tahun", "Per Tahun"),
        )

    def queryset(self, request, queryset):

        periode = self.value()

        tanggal = request.GET.get("tanggal")
        bulan = request.GET.get("bulan")
        tahun = request.GET.get("tahun")

        if periode == "hari" and tanggal:
            return queryset.filter(tanggal__date=tanggal)

        if periode == "bulan" and bulan and tahun:
            return queryset.filter(
                tanggal__month=bulan,
                tanggal__year=tahun
            )

        if periode == "tahun" and tahun:
            return queryset.filter(tanggal__year=tahun)

        return queryset


# ================= ADMIN =================
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

    # ===== FILTER ADMIN =====
    list_filter = (
        "status",
        "jenis_bullying",
        "kelas_korban",
        FilterPeriode,
    )

    search_fields = (
        "kode_laporan",
        "pelapor__username",
        "pelapor__first_name",
        "pelapor__last_name",
        "nama_korban",
        "nama_terlapor",
        "lokasi_kejadian",
    )

    fieldsets = (
        ("🔒 Identitas Pelapor (Internal)", {
            "fields": ("pelapor", "is_anonymous")
        }),
        ("🕒 Waktu & Tempat Kejadian", {
            "fields": ("tanggal_kejadian", "perkiraan_waktu", "lokasi_kejadian")
        }),
        ("👤 Korban & Terlapor", {
            "fields": ("nama_korban", "kelas_korban", "nama_terlapor", "kelas_terlapor")
        }),
        ("🚨 Detail Perundungan", {
            "fields": ("jenis_bullying", "isi_laporan", "bukti")
        }),
        ("💔 Dampak & Harapan", {
            "fields": ("dampak_korban", "dampak_lainnya", "harapan_pelapor")
        }),
        ("🧾 Tindak Lanjut Guru BK", {
            "fields": ("status", "catatan_bk", "bukti_tindak_lanjut")
        }),
        ("🔑 Meta Data", {
            "fields": ("kode_laporan", "tanggal")
        }),
    )

    readonly_fields = ("kode_laporan", "tanggal")

    # ================= DASHBOARD GRAFIK DINAMIS =================
    def changelist_view(self, request, extra_context=None):

        response = super().changelist_view(request, extra_context=extra_context)

        try:
            qs = response.context_data["cl"].queryset
        except:
            return response

        # ===== GRAFIK STATUS =====
        grafik_status = list(
            qs.values("status").annotate(total=Count("id"))
        )

        # ===== GRAFIK JENIS =====
        grafik_jenis = list(
            qs.values("jenis_bullying").annotate(total=Count("id"))
        )

        # ===== GRAFIK KELAS =====
        grafik_kelas = list(
            qs.values("kelas_korban").annotate(total=Count("id"))
        )

        # ===== GRAFIK TREN =====
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

        response.context_data.update({
            "total_laporan": qs.count(),
            "laporan_baru": qs.filter(status="baru").count(),
            "diproses": qs.filter(status="diproses").count(),
            "selesai": qs.filter(status="selesai").count(),

            "grafik_status": grafik_status,
            "grafik_jenis": grafik_jenis,
            "grafik_kelas": grafik_kelas,
            "grafik_tren": grafik_tren,
        })

        return response

    # ================= TAMPIL PELAPOR =================
    @admin.display(description="Pelapor")
    def get_pelapor_admin(self, obj):
        return obj.pelapor.get_full_name() or obj.pelapor.username
