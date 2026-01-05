from django import forms
from .models import Laporan
from users.models import Profile

MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10 MB


class LaporanForm(forms.ModelForm):

    nis_pelapor = forms.CharField(
        label="NIS Pelapor",
        max_length=20,
        help_text="Harus sesuai dengan NIS akun yang terdaftar",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Masukkan NIS sesuai akun"
        })
    )

    class Meta:
        model = Laporan
        fields = [
            "nama_pelapor",
            "nis_pelapor",
            "kelas_pelapor",
            "terlapor",
            "jenis_bullying",
            "isi_laporan",
            "bukti",
        ]

        widgets = {
            "nama_pelapor": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Nama lengkap pelapor"
            }),
            "kelas_pelapor": forms.Select(attrs={
                "class": "form-select"
            }),
            "terlapor": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Nama siswa yang dilaporkan"
            }),
            "jenis_bullying": forms.Select(attrs={
                "class": "form-select"
            }),
            "isi_laporan": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Ceritakan kejadian secara detail..."
            }),
            "bukti": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),
        }

    def clean_nis_pelapor(self):
        nis = self.cleaned_data.get("nis_pelapor")
        if not Profile.objects.filter(nis=nis).exists():
            raise forms.ValidationError(
                "NIS tidak terdaftar. Gunakan NIS sesuai akun siswa."
            )
        return nis

    def clean_bukti(self):
        file = self.cleaned_data.get("bukti")
        if file and file.size > MAX_UPLOAD_SIZE:
            raise forms.ValidationError(
                "Ukuran file terlalu besar! Maksimal 10 MB."
            )
        return file


class TindakLanjutForm(forms.ModelForm):
    class Meta:
        model = Laporan
        fields = ["catatan_bk", "bukti_tindak_lanjut"]
        widgets = {
            "catatan_bk": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
            }),
            "bukti_tindak_lanjut": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),
        }

    def clean_bukti_tindak_lanjut(self):
        file = self.cleaned_data.get("bukti_tindak_lanjut")
        if file and file.size > MAX_UPLOAD_SIZE:
            raise forms.ValidationError(
                "Ukuran file terlalu besar! Maksimal 10 MB."
            )
        return file
