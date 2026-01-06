from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import requests

from .models import Artikel, Video, Kuis, Opsi


@login_required
def konten_index(request):
    tab = request.GET.get("tab", "artikel")
    return render(
        request,
        "konten/index.html",
        {
            "tab": tab,
            "artikel": Artikel.objects.all(),
            "video": Video.objects.all(),
            "kuis": Kuis.objects.all(),
        },
    )


@login_required
def artikel_detail(request, id):
    artikel = get_object_or_404(Artikel, id=id)
    return render(request, "konten/artikel_detail.html", {"artikel": artikel})


# 🔥 VIEW BARU: DOWNLOAD PDF VIA DJANGO (PROXY)
@login_required
def download_artikel_pdf(request, id):
    artikel = get_object_or_404(Artikel, id=id)

    if not artikel.file_pdf:
        return HttpResponse("File PDF tidak tersedia", status=404)

    pdf_url = artikel.file_pdf.url

    # Ambil file dari Cloudinary (server-to-server)
    response = requests.get(pdf_url, stream=True)

    if response.status_code != 200:
        return HttpResponse("Gagal mengambil file PDF", status=500)

    # Kirim ke browser sebagai file download
    resp = HttpResponse(
        response.content,
        content_type="application/pdf"
    )
    resp["Content-Disposition"] = f'attachment; filename="{artikel.judul}.pdf"'
    return resp


@login_required
def kuis_detail(request, id):
    kuis = get_object_or_404(
        Kuis.objects.prefetch_related("pertanyaan__opsi"),
        id=id
    )

    skor = None
    total = 0
    hasil = {}

    if request.method == "POST":
        skor = 0
        total = 0
        for key, value in request.POST.items():
            if key.startswith("pertanyaan_"):
                opsi = Opsi.objects.get(id=int(value))
                total += 1
                if opsi.is_benar:
                    skor += 1

    return render(
        request,
        "konten/kuis_detail.html",
        {
            "kuis": kuis,
            "skor": skor,
            "total": total,
            "hasil": hasil,
        },
    )
