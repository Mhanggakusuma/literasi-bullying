from django import forms
from .models import Laporan

MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10 MB


# =================================================
# FORM LAPORAN SISWA
# =================================================
class LaporanForm(forms.ModelForm):

    # ================= ANONIM PELAPOR =================
    is_anonymous = forms.BooleanField(
        required=False,
        label="Laporkan sebagai anonim"
    )

    # ================= ANONIM KORBAN =================
    is_korban_anonim = forms.BooleanField(
        required=False,
        label="Sembunyikan identitas korban"
    )

    # ================= DAMPAK MULTI PILIH =================
    dampak_korban = forms.MultipleChoiceField(
        choices=Laporan.DAMPAK_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Dampak yang Dirasakan Korban"
    )

    # ================= PERNYATAAN =================
    pernyataan_setuju = forms.BooleanField(
        required=True,
        label="Saya menyatakan laporan ini dibuat dengan jujur dan bertanggung jawab"
    )

    class Meta:
        model = Laporan
        fields = [
            "is_anonymous",
            "is_korban_anonim",

            # Waktu & Tempat
            "tanggal_kejadian",
            "perkiraan_waktu",
            "lokasi_kejadian",

            # Korban
            "nama_korban",
            "kelas_korban",

            # Terlapor
            "nama_terlapor",
            "kelas_terlapor",

            # Detail
            "jenis_bullying",
            "isi_laporan",

            # Dampak
            "dampak_korban",
            "dampak_lainnya",

            # Bukti
            "bukti",

            # Harapan
            "harapan_pelapor",

            # Pernyataan
            "pernyataan_setuju",
        ]

        widgets = {
            "tanggal_kejadian": forms.DateInput(attrs={
                "type": "date",
                "class": "form-control"
            }),
            "perkiraan_waktu": forms.Select(attrs={
                "class": "form-select"
            }),
            "lokasi_kejadian": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Contoh: Ruang kelas / Lapangan sekolah"
            }),
            "nama_korban": forms.TextInput(attrs={
                "class": "form-control"
            }),
            "kelas_korban": forms.Select(attrs={
                "class": "form-select"
            }),
            "nama_terlapor": forms.TextInput(attrs={
                "class": "form-control"
            }),
            "kelas_terlapor": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Opsional"
            }),
            "jenis_bullying": forms.Select(attrs={
                "class": "form-select"
            }),
            "isi_laporan": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 5
            }),
            "dampak_lainnya": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Jika memilih lainnya, jelaskan..."
            }),
            "bukti": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),
            "harapan_pelapor": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3
            }),
        }

    # =================================================
    # VALIDASI UKURAN FILE BUKTI
    # =================================================
    def clean_bukti(self):
        file = self.cleaned_data.get("bukti")

        # File lama Cloudinary
        if file and not hasattr(file, "size"):
            return file

        if file and file.size > MAX_UPLOAD_SIZE:
            raise forms.ValidationError(
                "Ukuran file maksimal 10 MB"
            )

        return file

    # =================================================
    # SIMPAN MULTIPLE CHOICE → JSON
    # =================================================
    def clean_dampak_korban(self):
        return self.cleaned_data.get("dampak_korban")


# =================================================
# FORM TINDAK LANJUT BK
# =================================================
class TindakLanjutForm(forms.ModelForm):

    class Meta:
        model = Laporan
        fields = [
            "catatan_bk",
            "bukti_tindak_lanjut",
        ]

        widgets = {
            "catatan_bk": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4
            }),
            "bukti_tindak_lanjut": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),
        }

    # =================================================
    # VALIDASI FILE TINDAK LANJUT
    # =================================================
    def clean_bukti_tindak_lanjut(self):
        file = self.cleaned_data.get("bukti_tindak_lanjut")

        if file and not hasattr(file, "size"):
            return file

        if file and file.size > MAX_UPLOAD_SIZE:
            raise forms.ValidationError(
                "Ukuran file maksimal 10 MB"
            )

        return file
