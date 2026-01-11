import random
import string
import csv

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Count

from .models import Laporan
from .forms import LaporanForm, TindakLanjutForm
from users.models import Profile


# ==================================================
# GENERATE KODE LAPORAN UNIK
# ==================================================
def generate_kode():
    while True:
        kode = ''.join(
            random.choices(string.ascii_uppercase + string.digits, k=8)
        )
        if not Laporan.objects.filter(kode_laporan=kode).exists():
            return kode


# ==================================================
# HOME LAPORAN (SISWA)
# ==================================================
@login_required
def laporan_home(request):
    return render(request, "laporan/laporan_home.html")


# ==================================================
# BUAT LAPORAN (SISWA)
# ==================================================
@login_required
def buat_laporan(request):
    if request.method == "POST":
        form = LaporanForm(request.POST, request.FILES)
        if form.is_valid():
            laporan = form.save(commit=False)

            # Set pelapor dari akun login
            laporan.pelapor = request.user

            # Generate kode laporan
            laporan.kode_laporan = generate_kode()

            # Simpan dampak korban (list -> JSON)
            laporan.dampak_korban = form.cleaned_data.get("dampak_korban")

            laporan.save()

            return render(
                request,
                "laporan/pelapor_kode.html",
                {"kode": laporan.kode_laporan}
            )
    else:
        form = LaporanForm()

    # Data profil siswa (read-only)
    profile, _ = Profile.objects.get_or_create(user=request.user)

    return render(
        request,
        "laporan/buat_laporan.html",
        {
            "form": form,
            "profile": profile
        }
    )


# ==================================================
# CEK STATUS LAPORAN (SISWA)
# ==================================================
@login_required
def cek_laporan(request):
    laporan = None

    if request.method == "POST":
        kode = request.POST.get("kode")
        laporan = Laporan.objects.filter(
            kode_laporan=kode
        ).first()

    return render(
        request,
        "laporan/cek_laporan.html",
        {"laporan": laporan}
    )


# ==================================================
# DASHBOARD GURU BK
# ==================================================
@login_required
def bk_dashboard(request):
    status_filter = request.GET.get("status", "all")
    query = request.GET.get("q", "")

    laporan_qs = Laporan.objects.all()

    # Filter status
    if status_filter in ["baru", "diproses", "selesai"]:
        laporan_qs = laporan_qs.filter(status=status_filter)

    # Search kode laporan
    if query:
        laporan_qs = laporan_qs.filter(
            kode_laporan__icontains=query
        )

    laporan_qs = laporan_qs.order_by("-tanggal")

    context = {
        # Data utama
        "laporan": laporan_qs,

        # Ringkasan
        "total_laporan": Laporan.objects.count(),
        "laporan_baru": Laporan.objects.filter(status="baru").count(),
        "sedang_diproses": Laporan.objects.filter(status="diproses").count(),
        "selesai": Laporan.objects.filter(status="selesai").count(),

        # Filter UI
        "status_filter": status_filter,
        "query": query,

        # Statistik kelas korban
        "statistik_kelas": (
            Laporan.objects
            .values("kelas_korban")
            .annotate(total=Count("id"))
            .order_by("-total")
        ),

        # Aktivitas terbaru
        "aktivitas_terkini": (
            Laporan.objects
            .order_by("-tanggal")[:5]
        ),
    }

    return render(
        request,
        "laporan/bk_dashboard.html",
        context
    )


# ==================================================
# TINDAK LANJUT GURU BK (STATUS OTOMATIS)
# ==================================================
@login_required
def bk_tindak_lanjut(request, pk):
    laporan = get_object_or_404(Laporan, pk=pk)

    if request.method == "POST":
        form = TindakLanjutForm(
            request.POST,
            request.FILES,
            instance=laporan
        )
        if form.is_valid():
            laporan = form.save(commit=False)

            # =========================
            # STATUS OTOMATIS
            # =========================
            if "selesai" in request.POST:
                laporan.status = "selesai"
            elif laporan.status == "baru":
                laporan.status = "diproses"

            laporan.save()
            return redirect("bk_dashboard")
    else:
        form = TindakLanjutForm(instance=laporan)

    return render(
        request,
        "laporan/bk_tindak_lanjut.html",
        {
            "laporan": laporan,
            "form": form,
        }
    )


# ==================================================
# DOWNLOAD CSV (GURU BK)
# ==================================================
@login_required
def bk_download_laporan(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = (
        'attachment; filename="laporan_bullying.csv"'
    )

    writer = csv.writer(response)
    writer.writerow([
        "Kode Laporan",
        "Pelapor",
        "Tanggal Kejadian",
        "Waktu",
        "Lokasi",
        "Korban",
        "Kelas Korban",
        "Jenis Bullying",
        "Status",
        "Tanggal Lapor",
    ])

    for lap in Laporan.objects.all().order_by("-tanggal"):
        writer.writerow([
            lap.kode_laporan,
            lap.tampilkan_pelapor(),
            lap.tanggal_kejadian.strftime("%d-%m-%Y")
            if lap.tanggal_kejadian else "-",
            lap.get_perkiraan_waktu_display()
            if lap.perkiraan_waktu else "-",
            lap.lokasi_kejadian or "-",
            lap.nama_korban,
            lap.kelas_korban,
            lap.get_jenis_bullying_display(),
            lap.get_status_display(),
            lap.tanggal.strftime("%d-%m-%Y"),
        ])

    return response
