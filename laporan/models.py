from django.db import models
from django.core.exceptions import ValidationError
from cloudinary.models import CloudinaryField


def validate_file_size(value):
    max_size = 10 * 1024 * 1024  # 10 MB
    if value.size > max_size:
        raise ValidationError("Ukuran file maksimal 10 MB.")


class Laporan(models.Model):

    JENIS_BULLYING_CHOICES = [
        ("Fisik", "Bullying Fisik"),
        ("Verbal", "Bullying Verbal"),
        ("Sosial", "Bullying Sosial"),
        ("Cyber", "Cyberbullying"),
    ]

    KELAS_CHOICES = [
        ("VII A", "VII A"), ("VII B", "VII B"), ("VII C", "VII C"),
        ("VII D", "VII D"), ("VII E", "VII E"),
        ("VIII A", "VIII A"), ("VIII B", "VIII B"), ("VIII C", "VIII C"),
        ("VIII D", "VIII D"), ("VIII E", "VIII E"),
        ("IX A", "IX A"), ("IX B", "IX B"), ("IX C", "IX C"),
        ("IX D", "IX D"), ("IX E", "IX E"),
    ]

    STATUS_CHOICES = [
        ("baru", "Laporan Baru"),
        ("diproses", "Sedang Diproses"),
        ("selesai", "Selesai Ditangani"),
    ]

    nama_pelapor = models.CharField(max_length=100)
    nis_pelapor = models.CharField(max_length=20)
    kelas_pelapor = models.CharField(max_length=10, choices=KELAS_CHOICES)
    terlapor = models.CharField(max_length=100)

    jenis_bullying = models.CharField(max_length=20, choices=JENIS_BULLYING_CHOICES)
    isi_laporan = models.TextField()

    # 🔥 CLOUDINARY FIELD
    bukti = CloudinaryField(
        resource_type="auto",
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default="baru"
    )

    catatan_bk = models.TextField(blank=True, null=True)

    # 🔥 CLOUDINARY FIELD
    bukti_tindak_lanjut = CloudinaryField(
        resource_type="auto",
        blank=True,
        null=True
    )

    kode_laporan = models.CharField(max_length=12, unique=True)
    tanggal = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Laporan {self.kode_laporan}"
