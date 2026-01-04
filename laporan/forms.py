from django import forms
from .models import Laporan
from users.models import Profile

MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10 MB


class LaporanForm(forms.ModelForm):
    nis_pelapor = forms.CharField(
        label="NIS Pelapor",
        max_length=20,
        help_text="Harus sesuai dengan NIS saat registrasi",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "NIS sesuai akun terdaftar"
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
            "kelas_pelapor": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Contoh: VII A"
            }),
            "terlapor": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Nama siswa yang dilaporkan"
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
                "NIS tidak terdaftar. Gunakan NIS yang sesuai akun."
            )
        return nis

    def clean_bukti(self):
        file = self.cleaned_data.get("bukti")
        if file and file.size > MAX_UPLOAD_SIZE:
            raise forms.ValidationError(
                "Ukuran file terlalu besar! Maksimal 10 MB."
            )
        return file


# =============================
# FORM TINDAK LANJUT BK
# =============================
class TindakLanjutForm(forms.ModelForm):
    class Meta:
        model = Laporan
        fields = [
            "catatan_bk",
            "bukti_tindak_lanjut"
        ]

        widgets = {
            "catatan_bk": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Tuliskan hasil penanganan / tindak lanjut..."
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
