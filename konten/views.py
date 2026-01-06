from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from cloudinary.utils import private_download_url
import time

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


# =====================================================
# 🔥 DOWNLOAD PDF VIA SIGNED CLOUDINARY URL (FIXED)
# =====================================================
@login_required
def download_artikel_pdf(request, id):
    artikel = get_object_or_404(Artikel, id=id)

    if not artikel.file_pdf:
        return HttpResponse("File PDF tidak tersedia", status=404)

    public_id = artikel.file_pdf.public_id

    # ⬅️ FIX UTAMA: expires_at HARUS UNIX TIMESTAMP
    expires_at = int(time.time()) + 3600  # berlaku 1 jam

    download_url = private_download_url(
        public_id,
        format="pdf",
        resource_type="image",
        expires_at=expires_at
    )

    return redirect(download_url)


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
