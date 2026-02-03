from django.db import models


class Artikel(models.Model):
    # Model untuk menyimpan data artikel literasi
    judul = models.CharField(max_length=200)
    deskripsi = models.TextField(blank=True)
    konten = models.TextField(help_text="Isi artikel dalam bentuk teks")
    tanggal_upload = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.judul


class Video(models.Model):
    # Model untuk menyimpan video edukasi dari YouTube
    judul = models.CharField(max_length=200)
    youtube_id = models.CharField(max_length=50)
    tanggal_upload = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.judul


class Kuis(models.Model):
    # Model untuk menyimpan data kuis
    judul = models.CharField(max_length=200)
    deskripsi = models.TextField(blank=True)

    def __str__(self):
        return self.judul

# Model untuk menyimpan pertanyaan dalam sebuah kuis
class Pertanyaan(models.Model):
    kuis = models.ForeignKey(
        Kuis,
        on_delete=models.CASCADE,
        related_name="pertanyaan"
    )
    teks = models.TextField()

    def __str__(self):
        return self.teks

# Model untuk menyimpan pilihan jawaban
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
