from django import forms
from .models import Laporan

MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10 MB


class LaporanForm(forms.ModelForm):
    """
    Form laporan bullying untuk SISWA.
    Identitas pelapor diambil dari akun (request.user),
    bukan dari input form.
    """

    # =========================
    # 🔒 OPSI ANONIM
    # =========================
    is_anonymous = forms.BooleanField(
        required=False,
        label="Laporkan sebagai anonim",
        help_text="Identitas Anda hanya dapat dilihat oleh Guru BK & Admin"
    )

    class Meta:
        model = Laporan
        fields = [
            # Anonimitas
            "is_anonymous",

            # Identitas korban
            "nama_korban",
            "kelas_korban",

            # Identitas terlapor (opsional)
            "nama_terlapor",
            "kelas_terlapor",

            # Detail perundungan
            "jenis_bullying",
            "isi_laporan",

            # Bukti
            "bukti",
        ]

        widgets = {
            "nama_korban": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Nama korban perundungan"
            }),
            "kelas_korban": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Contoh: VIII B"
            }),
            "nama_terlapor": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Nama terlapor (boleh dikosongkan)"
            }),
            "kelas_terlapor": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Kelas terlapor (opsional)"
            }),
            "jenis_bullying": forms.Select(attrs={
                "class": "form-select"
            }),
            "isi_laporan": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 5,
                "placeholder": (
                    "Ceritakan kejadian secara jelas dan jujur.\n"
                    "Gunakan bahasa sopan dan fokus pada kejadian."
                )
            }),
            "bukti": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),
        }

    # =========================
    # VALIDASI FILE BUKTI
    # =========================
    def clean_bukti(self):
        file = self.cleaned_data.get("bukti")
        if file:
            if file.size > MAX_UPLOAD_SIZE:
                raise forms.ValidationError(
                    "Ukuran file terlalu besar. Maksimal 10 MB."
                )
        return file


# ==================================================
# FORM TINDAK LANJUT (KHUSUS GURU BK)
# ==================================================
class TindakLanjutForm(forms.ModelForm):
    """
    Form khusus Guru BK untuk mencatat tindak lanjut.
    """

    class Meta:
        model = Laporan
        fields = [
            "status",
            "catatan_bk",
            "bukti_tindak_lanjut",
        ]

        widgets = {
            "status": forms.Select(attrs={
                "class": "form-select"
            }),
            "catatan_bk": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Tuliskan hasil penanganan atau tindak lanjut..."
            }),
            "bukti_tindak_lanjut": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),
        }

    def clean_bukti_tindak_lanjut(self):
        file = self.cleaned_data.get("bukti_tindak_lanjut")
        if file:
            if file.size > MAX_UPLOAD_SIZE:
                raise forms.ValidationError(
                    "Ukuran file terlalu besar. Maksimal 10 MB."
                )
        return file
