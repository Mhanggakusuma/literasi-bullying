from django.shortcuts import render, get_object_or_404
from .models import Artikel, Video, Kuis, Opsi


# ===============================
# HALAMAN INDEX KONTEN (TAB)
# ===============================
def konten_index(request):
    tab = request.GET.get("tab", "artikel")

    return render(
        request,
        "konten/index.html",
        {
            "tab": tab,
            "artikel": Artikel.objects.all().order_by("-tanggal_upload"),
            "video": Video.objects.all().order_by("-tanggal_upload"),
            "kuis": Kuis.objects.all(),
        },
    )


# ===============================
# DETAIL ARTIKEL (PDF)
# ===============================
def artikel_detail(request, id):
    artikel = get_object_or_404(Artikel, id=id)
    return render(
        request,
        "konten/artikel_detail.html",
        {
            "artikel": artikel
        },
    )


# ===============================
# DETAIL KUIS (SOAL)
# ===============================
def kuis_detail(request, id):
    kuis = get_object_or_404(
        Kuis.objects.prefetch_related("pertanyaan__opsi"),
        id=id
    )

    skor = None
    total = 0
    hasil = {}

    # ===== SUBMIT KUIS =====
    if request.method == "POST":
        skor = 0
        total = 0

        for key, value in request.POST.items():
            if key.startswith("pertanyaan_"):
                pertanyaan_id = int(key.replace("pertanyaan_", ""))
                opsi_id = int(value)

                hasil[pertanyaan_id] = opsi_id
                total += 1

                try:
                    opsi = Opsi.objects.get(id=opsi_id)
                    if opsi.is_benar:
                        skor += 1
                except Opsi.DoesNotExist:
                    pass

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
