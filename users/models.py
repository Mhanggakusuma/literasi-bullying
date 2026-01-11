from django.db import models
from django.contrib.auth.models import User
from datetime import date

class Profile(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('gurubk', 'Guru BK'),
        ('siswa', 'Siswa'),
    ]

    KELAS_CHOICES = [
        ("VII A", "VII A"), ("VII B", "VII B"), ("VII C", "VII C"),
        ("VII D", "VII D"), ("VII E", "VII E"),
        ("VIII A", "VIII A"), ("VIII B", "VIII B"), ("VIII C", "VIII C"),
        ("VIII D", "VIII D"), ("VIII E", "VIII E"),
        ("IX A", "IX A"), ("IX B", "IX B"), ("IX C", "IX C"),
        ("IX D", "IX D"), ("IX E", "IX E"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='siswa')

    kelas = models.CharField(
        max_length=10,
        choices=KELAS_CHOICES,
        blank=True,
        null=True
    )

    # 🔒 dikunci setelah diisi pertama kali
    kelas_locked = models.BooleanField(default=False)

    nis = models.CharField(max_length=20, unique=True, null=True, blank=True)

    force_password_change = models.BooleanField(default=False)

    tanggal_masuk = models.DateField(null=True, blank=True)
    tanggal_akhir_aktif = models.DateField(null=True, blank=True)

    def is_masih_aktif(self):
        if not self.tanggal_akhir_aktif:
            return True
        return date.today() <= self.tanggal_akhir_aktif

    def __str__(self):
        return f"{self.user.first_name} - {self.kelas or 'Belum isi kelas'}"
