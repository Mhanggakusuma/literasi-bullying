from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from cloudinary.models import CloudinaryField


# =========================
# VALIDASI UKURAN FILE
# =========================
def validate_file_size(value):
    max_size = 10 * 1024 * 1024  # 10 MB
    if value.size > max_size:
        raise ValidationError("Ukuran file maksimal 10 MB.")


# =========================
# MODEL LAPORAN BULLYING
# =========================
class Laporan(models.Model):

    # =========================
    # PILIHAN JENIS BULLYING
    # (MULTI DIMENSI – AKADEMIK)
    # =========================
    JENIS_BULLYING_CHOICES = [
        ("verbal", "Verbal"),
        ("fisik", "Fisik"),
        ("sosial", "Sosial"),
        ("siber", "Siber"),
        ("psikologis", "Psikologis"),
        ("lainnya", "Lainnya"),
    ]

    # =========================
    # STATUS PENANGANAN
    # =========================
    STATUS_CHOICES = [
        ("baru", "Laporan Baru"),
        ("diproses", "Sedang Diproses"),
        ("selesai", "Selesai Ditangani"),
    ]

    # ==================================================
    # 🔒 IDENTITAS ASLI PELAPOR (TIDAK PERNAH HILANG)
    # ==================================================
    pelapor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="laporan_bullying"
    )

    # Checkbox "Laporkan sebagai anonim"
    is_anonymous = models.BooleanField(
        default=False,
        help_text="Jika dicentang, identitas pelapor disembunyikan di tampilan"
    )

    # =========================
    # 👤 IDENTITAS KORBAN
    # =========================
    nama_korban = models.CharField(
        max_length=100,
        help_text="Nama korban perundungan"
    )

    kelas_korban = models.CharField(
        max_length=10,
        help_text="Kelas korban"
    )

    # =========================
    # ⚠️ IDENTITAS TERLAPOR
    # (BOLEH KOSONG JIKA BUKAN SISWA)
    # =========================
    nama_terlapor = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    kelas_terlapor = models.CharField(
        max_length=10,
        blank=True,
        null=True
    )

    # =========================
    # 🚨 DETAIL PERUNDUNGAN
    # =========================
    jenis_bullying = models.CharField(
        max_length=20,
        choices=JENIS_BULLYING_CHOICES
    )

    isi_laporan = models.TextField(
        help_text="Kronologi kejadian bullying"
    )

    # =========================
    # 📎 BUKTI PENDUKUNG
    # =========================
    bukti = CloudinaryField(
        resource_type="auto",
        blank=True,
        null=True,
    )

    # =========================
    # 🧾 TINDAK LANJUT GURU BK
    # =========================
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="baru"
    )

    catatan_bk = models.TextField(
        blank=True,
        null=True,
        help_text="Catatan internal Guru BK"
    )

    bukti_tindak_lanjut = CloudinaryField(
        resource_type="auto",
        blank=True,
        null=True,
    )

    # =========================
    # 🔑 META DATA
    # =========================
    kode_laporan = models.CharField(
        max_length=12,
        unique=True
    )

    tanggal = models.DateTimeField(
        auto_now_add=True
    )

    # =========================
    # REPRESENTASI STRING
    # =========================
    def __str__(self):
        return f"Laporan {self.kode_laporan}"

    # =========================
    # HELPER (UI LOGIC)
    # =========================
    def tampilkan_pelapor(self):
        """
        Digunakan di template.
        Jika anonim → tampil 'Anonim'
        Jika tidak → tampil nama user
        """
        if self.is_anonymous:
            return "Anonim"
        return self.pelapor.get_full_name() or self.pelapor.username
