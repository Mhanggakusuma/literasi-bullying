from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class Laporan(models.Model):

    # =========================
    # PILIHAN KELAS (DROPDOWN)
    # =========================
    KELAS_CHOICES = [
        ("VII A", "VII A"), ("VII B", "VII B"), ("VII C", "VII C"),
        ("VII D", "VII D"), ("VII E", "VII E"),
        ("VIII A", "VIII A"), ("VIII B", "VIII B"), ("VIII C", "VIII C"),
        ("VIII D", "VIII D"), ("VIII E", "VIII E"),
        ("IX A", "IX A"), ("IX B", "IX B"), ("IX C", "IX C"),
        ("IX D", "IX D"), ("IX E", "IX E"),
    ]

    # =========================
    # JENIS BULLYING
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

    # =========================
    # 🔒 IDENTITAS PELAPOR
    # =========================
    pelapor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="laporan_bullying"
    )

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
        choices=KELAS_CHOICES,
        help_text="Kelas korban"
    )

    # =========================
    # ⚠️ IDENTITAS TERLAPOR
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
    # 📎 BUKTI (CLOUDINARY)
    # =========================
    bukti = CloudinaryField(
        resource_type="auto",
        blank=True,
        null=True
    )

    # =========================
    # 🧾 TINDAK LANJUT BK
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
        null=True
    )

    # =========================
    # 🔑 META DATA
    # =========================
    kode_laporan = models.CharField(
        max_length=12,
        unique=True
    )

    tanggal = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Laporan {self.kode_laporan}"

    def tampilkan_pelapor(self):
        if self.is_anonymous:
            return "Anonim"
        return self.pelapor.get_full_name() or self.pelapor.username
