from django.db import models
from django.contrib.auth.models import User
from datetime import date

class Profile(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('gurubk', 'Guru BK'),
        ('siswa', 'Siswa'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='siswa')
    kelas = models.CharField(max_length=50, blank=True, null=True)

    nis = models.CharField(max_length=20, unique=True, null=True, blank=True)

    # 🔐 WAJIB GANTI PASSWORD
    force_password_change = models.BooleanField(default=False)

    # 🕒 MASA AKTIF AKUN
    tanggal_masuk = models.DateField(null=True, blank=True)
    tanggal_akhir_aktif = models.DateField(null=True, blank=True)

    def is_masih_aktif(self):
        """
        Akun aktif jika:
        - tanggal_akhir_aktif belum terlewati
        """
        if not self.tanggal_akhir_aktif:
            return True
        return date.today() <= self.tanggal_akhir_aktif

    def __str__(self):
        return f"{self.user.username} – {self.role}"
