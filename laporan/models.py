from django.db import models
from django.core.exceptions import ValidationError


# =========================
# VALIDATOR UKURAN FILE
# =========================
def validate_file_size(value):
    max_size = 10 * 1024 * 1024  # 10 MB
    if value.size > max_size:
        raise ValidationError("Ukuran file maksimal 10 MB.")


class Laporan(models.Model):

    JENIS_BULLYING_CHOICES = [
        ("Fisik", "Bullying Fisik (memukul, mendorong, dll)"),
        ("Verbal", "Bullying Verbal (mengejek, menghina, dll)"),
        ("Sosial", "Bullying Sosial (mengucilkan, menyebarkan gosip)"),
        ("Cyber", "Cyberbullying (media sosial / online)"),
    ]

    nama_pelapor = models.CharField(max_length=100)
    nis_pelapor = models.CharField(max_length=20)
    kelas_pelapor = models.CharField(max_length=20)
    terlapor = models.CharField(max_length=100)

    jenis_bullying = models.CharField(
        max_length=20,
        choices=JENIS_BULLYING_CHOICES
    )

    # KRONOLOGI / CERITA KEJADIAN
    isi_laporan = models.TextField()

    # =========================
    # BUKTI LAPORAN (FILE BEBAS)
    # =========================
    bukti = models.FileField(
        upload_to="laporan_bukti/",
        blank=True,
        null=True,
        validators=[validate_file_size]
    )

    status = models.CharField(
        max_length=50,
        default="Menunggu Ditindaklanjuti"
    )

    catatan_bk = models.TextField(blank=True, null=True)

    # =========================
    # BUKTI TINDAK LANJUT BK
    # =========================
    bukti_tindak_lanjut = models.FileField(
        upload_to="laporan_tindak_lanjut/",
        blank=True,
        null=True,
        validators=[validate_file_size]
    )

    kode_laporan = models.CharField(max_length=12, unique=True)
    tanggal = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Laporan {self.kode_laporan}"
