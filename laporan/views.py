import random
import string
import csv

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Count

from .models import Laporan
from .forms import LaporanForm, TindakLanjutForm
from users.models import Profile  # ⬅️ WAJIB (FIX ERROR 500)


# =========================
# GENERATE KODE LAPORAN
# =========================
def generate_kode():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))


# =========================
# HOME LAPORAN (SISWA)
# =========================
@login_required
def laporan_home(request):
    return render(request, "laporan/laporan_home.html")


# =========================
# BUAT LAPORAN (SISWA)
# =========================
@login_required
def buat_laporan(request):
    if request.method == "POST":
        form = LaporanForm(request.POST, request.FILES)
        if form.is_valid():
            laporan = form.save(commit=False)

            # 🔑 WAJIB: set pelapor dari user login
            laporan.pelapor = request.user

            # 🔑 generate kode laporan
            laporan.kode_laporan = generate_kode()

            laporan.save()

            return render(
                request,
                "laporan/pelapor_kode.html",
                {"kode": laporan.kode_laporan}
            )
    else:
        form = LaporanForm()

    # 🔒 AMAN: pastikan Profile SELALU ADA
    profile, _ = Profile.objects.get_or_create(user=request.user)

    return render(
        request,
        "laporan/buat_laporan.html",
        {
            "form": form,
            "profile": profile,
        }
    )


# =========================
# CEK STATUS LAPORAN (SISWA)
# =========================
@login_required
def cek_laporan(request):
    laporan = None
    if request.method == "POST":
        kode = request.POST.get("kode")
        laporan = Laporan.objects.filter(kode_laporan=kode).first()

    return render(
        request,
        "laporan/cek_laporan.html",
        {"laporan": laporan}
    )


# =========================
# DASHBOARD GURU BK
# =========================
@login_required
def bk_dashboard(request):
    status_filter = request.GET.get("status", "all")
    query = request.GET.get("q", "")

    laporan_qs = Laporan.objects.all()

    if status_filter != "all":
        laporan_qs = laporan_qs.filter(status=status_filter)

    if query:
        laporan_qs = laporan_qs.filter(kode_laporan__icontains=query)

    laporan_qs = laporan_qs.order_by("-tanggal")

    context = {
        "laporan": laporan_qs,

        # Ringkasan
        "total_laporan": Laporan.objects.count(),
        "laporan_baru": Laporan.objects.filter(status="baru").count(),
        "sedang_diproses": Laporan.objects.filter(status="diproses").count(),
        "selesai": Laporan.objects.filter(status="selesai").count(),

        # Filter state
        "status_filter": status_filter,
        "query": query,

        # Statistik kelas korban
        "statistik_kelas": (
            Laporan.objects.values("kelas_korban")
            .annotate(total=Count("id"))
            .order_by("-total")
        ),

        # Aktivitas terkini
        "aktivitas_terkini": Laporan.objects.order_by("-tanggal")[:5],
    }

    return render(request, "laporan/bk_dashboard.html", context)


# =========================
# DETAIL & TINDAK LANJUT (GURU BK)
# =========================
@login_required
def bk_tindak_lanjut(request, pk):
    laporan = get_object_or_404(Laporan, pk=pk)

    if request.method == "POST":
        form = TindakLanjutForm(request.POST, request.FILES, instance=laporan)
        if form.is_valid():
            form.save()
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


# =========================
# DOWNLOAD CSV (ADMIN / BK)
# =========================
@login_required
def bk_download_laporan(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="laporan_bullying.csv"'

    writer = csv.writer(response)
    writer.writerow([
        "Kode",
        "Pelapor",
        "Anonim",
        "Korban",
        "Kelas Korban",
        "Jenis",
        "Status",
        "Tanggal",
    ])

    for lap in Laporan.objects.all().order_by("-tanggal"):
        writer.writerow([
            lap.kode_laporan,
            lap.pelapor.username,
            "Ya" if lap.is_anonymous else "Tidak",
            lap.nama_korban,
            lap.kelas_korban,
            lap.get_jenis_bullying_display(),
            lap.get_status_display(),
            lap.tanggal.strftime("%d-%m-%Y"),
        ])

    return response
