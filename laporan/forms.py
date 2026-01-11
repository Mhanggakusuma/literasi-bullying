from django import forms
from .models import Laporan

MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10 MB


class LaporanForm(forms.ModelForm):
    """
    Form laporan bullying untuk SISWA.
    Identitas pelapor diambil dari akun login (request.user),
    bukan dari input form.
    """

    # =========================
    # 🔒 OPSI ANONIM
    # =========================
    is_anonymous = forms.BooleanField(
        required=False,
        label="Laporkan sebagai anonim",
        help_text="Identitas hanya dapat dilihat oleh Guru BK & Admin"
    )

    # =========================
    # 💔 DAMPAK KORBAN (MULTI PILIH)
    # =========================
    dampak_korban = forms.MultipleChoiceField(
        choices=Laporan.DAMPAK_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Dampak yang Dirasakan Korban"
    )

    # =========================
    # ✅ PERNYATAAN KEJUJURAN
    # =========================
    pernyataan_setuju = forms.BooleanField(
        required=True,
        label="Saya menyatakan laporan ini dibuat dengan jujur dan bertanggung jawab"
    )

    class Meta:
        model = Laporan
        fields = [
            # Anonimitas
            "is_anonymous",

            # 🕒 Waktu & Tempat
            "tanggal_kejadian",
            "perkiraan_waktu",
            "lokasi_kejadian",

            # 👤 Korban
            "nama_korban",
            "kelas_korban",

            # ⚠️ Terlapor
            "nama_terlapor",
            "kelas_terlapor",

            # 🚨 Detail
            "jenis_bullying",
            "isi_laporan",

            # 💔 Dampak
            "dampak_korban",
            "dampak_lainnya",

            # 📎 Bukti
            "bukti",

            # 🤝 Harapan
            "harapan_pelapor",

            # ✅ Pernyataan
            "pernyataan_setuju",
        ]

        widgets = {
            # =========================
            # WAKTU & TEMPAT
            # =========================
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

            # =========================
            # KORBAN
            # =========================
            "nama_korban": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Nama korban perundungan"
            }),
            "kelas_korban": forms.Select(attrs={
                "class": "form-select"
            }),

            # =========================
            # TERLAPOR
            # =========================
            "nama_terlapor": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Nama terlapor (opsional)"
            }),
            "kelas_terlapor": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Kelas terlapor (opsional)"
            }),

            # =========================
            # DETAIL
            # =========================
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

            # =========================
            # DAMPAK LAINNYA
            # =========================
            "dampak_lainnya": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Jika lainnya, jelaskan..."
            }),

            # =========================
            # BUKTI
            # =========================
            "bukti": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),

            # =========================
            # HARAPAN
            # =========================
            "harapan_pelapor": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Saya berharap pihak sekolah dapat menindaklanjuti..."
            }),
        }

    # =========================
    # VALIDASI FILE BUKTI
    # =========================
    def clean_bukti(self):
        file = self.cleaned_data.get("bukti")
        if file and file.size > MAX_UPLOAD_SIZE:
            raise forms.ValidationError(
                "Ukuran file terlalu besar. Maksimal 10 MB."
            )
        return file


# ==================================================
# FORM TINDAK LANJUT (KHUSUS GURU BK)
# ==================================================
class TindakLanjutForm(forms.ModelForm):
    """
    Form khusus Guru BK untuk mencatat tindak lanjut kasus bullying.
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
        if file and file.size > MAX_UPLOAD_SIZE:
            raise forms.ValidationError(
                "Ukuran file terlalu besar. Maksimal 10 MB."
            )
        return file
