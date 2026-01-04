from django.db import models


# ⬇️ WAJIB ADA UNTUK MIGRATION LAMA
def artikel_upload_path(instance, filename):
    return f"artikel_pdf/{filename}"


class Artikel(models.Model):
    judul = models.CharField(max_length=200)
    deskripsi = models.TextField(blank=True)
    file_pdf = models.FileField(
        upload_to=artikel_upload_path
    )
    tanggal_upload = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.judul


class Video(models.Model):
    judul = models.CharField(max_length=200)
    youtube_id = models.CharField(max_length=50)
    tanggal_upload = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.judul


class Kuis(models.Model):
    judul = models.CharField(max_length=200)
    deskripsi = models.TextField(blank=True)

    def __str__(self):
        return self.judul


class Pertanyaan(models.Model):
    kuis = models.ForeignKey(
        Kuis,
        on_delete=models.CASCADE,
        related_name="pertanyaan"
    )
    teks = models.TextField()

    def __str__(self):
        return self.teks


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
