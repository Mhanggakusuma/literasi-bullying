from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Artikel, Video, Kuis, Opsi


@login_required
def konten_index(request):
    # Menampilkan halaman utama konten (artikel, video, dan kuis) berdasarkan tab yang dipilih
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
    # Menampilkan detail artikel berdasarkan ID yang dipilih penggun
    artikel = get_object_or_404(Artikel, id=id)
    return render(
        request,
        "konten/artikel_detail.html",
        {"artikel": artikel}
    )


@login_required
def kuis_detail(request, id):
    # Menampilkan kuis dan menghitung skor berdasarkan jawaban yang dikirim pengguna
    kuis = get_object_or_404(
        Kuis.objects.prefetch_related("pertanyaan__opsi"),
        id=id
    )

    skor = None
    total = 0

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
        },
    )
