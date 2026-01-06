from django.db import models
from cloudinary.models import CloudinaryField


# =====================================================
# ⬇️ WAJIB ADA (UNTUK MIGRATION LAMA)
# JANGAN DIHAPUS
# =====================================================
def artikel_upload_path(instance, filename):
    return f"artikel_pdf/{filename}"


# =========================
# MODEL ARTIKEL (PDF)
# =========================
class Artikel(models.Model):
    judul = models.CharField(max_length=200)
    deskripsi = models.TextField(blank=True)

    # 🔥 PDF DISIMPAN SEBAGAI IMAGE (AGAR TIDAK 401)
    # Cloudinary akan memperlakukan PDF sebagai image multi-page
    file_pdf = CloudinaryField(
        resource_type="image",
        blank=True,
        null=True
    )

    tanggal_upload = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.judul


# =========================
# MODEL VIDEO (YOUTUBE)
# =========================
class Video(models.Model):
    judul = models.CharField(max_length=200)
    youtube_id = models.CharField(max_length=50)
    tanggal_upload = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.judul


# =========================
# MODEL KUIS
# =========================
class Kuis(models.Model):
    judul = models.CharField(max_length=200)
    deskripsi = models.TextField(blank=True)

    def __str__(self):
        return self.judul


# =========================
# MODEL PERTANYAAN
# =========================
class Pertanyaan(models.Model):
    kuis = models.ForeignKey(
        Kuis,
        on_delete=models.CASCADE,
        related_name="pertanyaan"
    )
    teks = models.TextField()

    def __str__(self):
        return self.teks


# =========================
# MODEL OPSI JAWABAN
# =========================
class Opsi(models.Model):
    pertanyaan = models.ForeignKey(
        Pertanyaan,
        on_delete=models.CASCADE,
        related_name="opsi"
    )
    teks_opsi = models.CharField(max_length=255)
    is_benar = models.BooleanField(default=False)

    def __str__(self):
        return self.teks_opsi
