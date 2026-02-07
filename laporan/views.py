import random
import string
import csv

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.db.models.functions import TruncDay, TruncMonth, TruncYear

from .models import Laporan
from .forms import LaporanForm, TindakLanjutForm
from users.models import Profile
from users.decorators import role_required


# =================================================
# GENERATE KODE LAPORAN
# =================================================
def generate_kode():
    while True:
        kode = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        if not Laporan.objects.filter(kode_laporan=kode).exists():
            return kode


# =================================================
# HOME SISWA
# =================================================
@login_required
@role_required(['siswa'])
def laporan_home(request):
    return render(request, "laporan/laporan_home.html")


# =================================================
# BUAT LAPORAN SISWA
# =================================================
@login_required
@role_required(['siswa'])
def buat_laporan(request):

    if request.method == "POST":
        form = LaporanForm(request.POST, request.FILES)

        if form.is_valid():
            laporan = form.save(commit=False)

            laporan.pelapor = request.user
            laporan.kode_laporan = generate_kode()
            laporan.dampak_korban = form.cleaned_data.get("dampak_korban")

            laporan.save()

            return render(
                request,
                "laporan/pelapor_kode.html",
                {"kode": laporan.kode_laporan}
            )
    else:
        form = LaporanForm()

    profile, _ = Profile.objects.get_or_create(user=request.user)

    return render(request, "laporan/buat_laporan.html", {
        "form": form,
        "profile": profile
    })


# =================================================
# CEK STATUS LAPORAN SISWA
# =================================================
@login_required
@role_required(['siswa'])
def cek_laporan(request):

    laporan = None

    if request.method == "POST":
        kode = request.POST.get("kode")
        laporan = Laporan.objects.filter(kode_laporan=kode).first()

    return render(request, "laporan/cek_laporan.html", {"laporan": laporan})


# =================================================
# DASHBOARD BK + ANALITIK
# =================================================
@login_required
@role_required(['gurubk', 'admin'])
def bk_dashboard(request):

    laporan_qs = Laporan.objects.all()

    # ===== FILTER DASAR =====
    jenis_filter = request.GET.get("jenis")
    kelas_filter = request.GET.get("kelas")
    status_filter = request.GET.get("status")

    periode = request.GET.get("periode", "semua")
    tanggal = request.GET.get("tanggal")
    bulan = request.GET.get("bulan")
    tahun = request.GET.get("tahun")

    if jenis_filter:
        laporan_qs = laporan_qs.filter(jenis_bullying=jenis_filter)

    if kelas_filter:
        laporan_qs = laporan_qs.filter(kelas_korban=kelas_filter)

    if status_filter:
        laporan_qs = laporan_qs.filter(status=status_filter)

    # ===== FILTER PERIODE =====
    if periode == "hari" and tanggal:
        laporan_qs = laporan_qs.filter(tanggal__date=tanggal)

    elif periode == "bulan" and bulan and tahun:
        laporan_qs = laporan_qs.filter(
            tanggal__month=bulan,
            tanggal__year=tahun
        )

    elif periode == "tahun" and tahun:
        laporan_qs = laporan_qs.filter(
            tanggal__year=tahun
        )

    # ===== GRAFIK =====
    grafik_status = laporan_qs.values("status").annotate(total=Count("id"))
    grafik_jenis = laporan_qs.values("jenis_bullying").annotate(total=Count("id"))
    grafik_kelas = laporan_qs.values("kelas_korban").annotate(total=Count("id"))

    # ===== GRAFIK TREN =====
    if periode == "hari":
        grafik_tren = laporan_qs.annotate(
            waktu=TruncDay("tanggal")
        ).values("waktu").annotate(total=Count("id")).order_by("waktu")

    elif periode == "tahun":
        grafik_tren = laporan_qs.annotate(
            waktu=TruncYear("tanggal")
        ).values("waktu").annotate(total=Count("id")).order_by("waktu")

    else:
        grafik_tren = laporan_qs.annotate(
            waktu=TruncMonth("tanggal")
        ).values("waktu").annotate(total=Count("id")).order_by("waktu")

    # ===== OPTION TAHUN DINAMIS =====
    daftar_tahun = Laporan.objects.dates("tanggal", "year")

    context = {
        "laporan": laporan_qs.order_by("-tanggal"),

        "total_laporan": laporan_qs.count(),
        "laporan_baru": laporan_qs.filter(status="baru").count(),
        "sedang_diproses": laporan_qs.filter(status="diproses").count(),
        "selesai": laporan_qs.filter(status="selesai").count(),

        "grafik_status": list(grafik_status),
        "grafik_jenis": list(grafik_jenis),
        "grafik_kelas": list(grafik_kelas),
        "grafik_tren": list(grafik_tren),

        "periode": periode,
        "jenis_choices": Laporan.JENIS_BULLYING_CHOICES,
        "kelas_choices": Laporan.KELAS_CHOICES,
        "daftar_tahun": daftar_tahun,

        "selected_jenis": jenis_filter,
        "selected_kelas": kelas_filter,
        "selected_status": status_filter,
    }

    return render(request, "laporan/bk_dashboard.html", context)


# =================================================
# TINDAK LANJUT BK
# =================================================
@login_required
@role_required(['gurubk', 'admin'])
def bk_tindak_lanjut(request, pk):

    laporan = get_object_or_404(Laporan, pk=pk)

    if request.method == "POST":
        form = TindakLanjutForm(request.POST, request.FILES, instance=laporan)

        if form.is_valid():
            laporan = form.save(commit=False)

            if "selesai" in request.POST:
                laporan.status = "selesai"
            elif laporan.status == "baru":
                laporan.status = "diproses"

            laporan.save()
            return redirect("bk_dashboard")

    else:
        form = TindakLanjutForm(instance=laporan)

    return render(request, "laporan/bk_tindak_lanjut.html", {
        "laporan": laporan,
        "form": form
    })


# =================================================
# DOWNLOAD CSV
# =================================================
@login_required
@role_required(['gurubk', 'admin'])
def bk_download_laporan(request):

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="laporan_bullying.csv"'

    writer = csv.writer(response)

    writer.writerow([
        "Kode",
        "Pelapor",
        "Korban",
        "Kelas Korban",
        "Jenis",
        "Status",
        "Tanggal"
    ])

    for lap in Laporan.objects.all().order_by("-tanggal"):
        writer.writerow([
            lap.kode_laporan,
            lap.tampilkan_pelapor(),
            lap.tampilkan_korban(),
            lap.kelas_korban,
            lap.get_jenis_bullying_display(),
            lap.get_status_display(),
            lap.tanggal.strftime("%d-%m-%Y"),
        ])

    return response
