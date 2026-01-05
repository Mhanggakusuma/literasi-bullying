import random
import string
import csv

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.contrib.auth.decorators import login_required

from .models import Laporan
from .forms import LaporanForm, TindakLanjutForm


def generate_kode():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))


@login_required
def laporan_home(request):
    return render(request, "laporan/laporan_home.html")


@login_required
def buat_laporan(request):
    if request.method == "POST":
        form = LaporanForm(request.POST, request.FILES)
        if form.is_valid():
            laporan = form.save(commit=False)
            laporan.kode_laporan = generate_kode()
            laporan.save()
            return render(
                request,
                "laporan/pelapor_kode.html",
                {"kode": laporan.kode_laporan}
            )
    else:
        form = LaporanForm()

    return render(request, "laporan/buat_laporan.html", {"form": form})


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


@login_required
def bk_dashboard(request):
    laporan_qs = Laporan.objects.all().order_by("-tanggal")

    statistik_kelas = (
        laporan_qs
        .values("kelas_pelapor")
        .annotate(total=Count("id"))
        .order_by("-total")
    )

    tren_qs = (
        laporan_qs
        .annotate(bulan=TruncMonth("tanggal"))
        .values("bulan")
        .annotate(total=Count("id"))
        .order_by("bulan")
    )

    context = {
        "laporan": laporan_qs,
        "statistik_kelas": statistik_kelas,
        "chart_labels": [t["bulan"].strftime("%b %Y") for t in tren_qs],
        "chart_data": [t["total"] for t in tren_qs],
    }

    return render(request, "laporan/bk_dashboard.html", context)


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
            laporan.status = "Sudah Ditindaklanjuti"
            laporan.save()
            return redirect("bk_dashboard")
    else:
        form = TindakLanjutForm(instance=laporan)

    return render(
        request,
        "laporan/bk_tindak_lanjut.html",
        {"laporan": laporan, "form": form}
    )


@login_required
def bk_download_laporan(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="laporan_bullying.csv"'

    writer = csv.writer(response)
    writer.writerow([
        "Kode", "Nama", "NIS", "Kelas", "Jenis", "Status", "Tanggal"
    ])

    for lap in Laporan.objects.all().order_by("-tanggal"):
        writer.writerow([
            lap.kode_laporan,
            lap.nama_pelapor,
            lap.nis_pelapor,
            lap.kelas_pelapor,
            lap.get_jenis_bullying_display(),
            lap.status,
            lap.tanggal.strftime("%d-%m-%Y"),
        ])

    return response
