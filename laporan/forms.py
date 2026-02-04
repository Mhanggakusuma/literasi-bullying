from django import forms
from .models import Laporan

MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10 MB


# Form laporan bullying yang digunakan siswa untuk mengisi laporan
class LaporanForm(forms.ModelForm):
    """
    Form laporan bullying untuk SISWA.
    Identitas pelapor diambil dari akun login.
    """

    # OPSI ANONIM
    is_anonymous = forms.BooleanField(
        required=False,
        label="Laporkan sebagai anonim"
    )

    # DAMPAK KORBAN (MULTI PILIH)
    dampak_korban = forms.MultipleChoiceField(
        choices=Laporan.DAMPAK_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Dampak yang Dirasakan Korban"
    )

    # PERNYATAAN KEJUJURAN
    pernyataan_setuju = forms.BooleanField(
        required=True,
        label="Saya menyatakan laporan ini dibuat dengan jujur dan bertanggung jawab"
    )

    class Meta:
        model = Laporan
        fields = [
            # Anonimitas
            "is_anonymous",

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
                "class": "form-control",
                "placeholder": ""
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
                "rows": 5,
                "placeholder": (
                    "Ceritakan kejadian secara jelas dan jujur.\n"
                    "Gunakan bahasa sopan dan fokus pada kejadian."
                )
            }),
            "dampak_lainnya": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Jika lainnya, jelaskan..."
            }),
            "bukti": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),
            "harapan_pelapor": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Saya berharap pihak sekolah dapat menindaklanjuti..."
            }),
        }

 # Validasi ukuran file bukti upload
    def clean_bukti(self):
        file = self.cleaned_data.get("bukti")

        # Jika file lama dari Cloudinary (bukan upload baru)
        if file and not hasattr(file, "size"):
            return file

        if file and file.size > MAX_UPLOAD_SIZE:
            raise forms.ValidationError(
                "Ukuran file terlalu besar. Maksimal 10 MB."
            )

        return file


# Form tindak lanjut laporan yang digunakan Guru BK
class TindakLanjutForm(forms.ModelForm):
    """
    Guru BK hanya mengisi catatan & bukti.
    Status laporan diatur OTOMATIS oleh sistem.
    """

    class Meta:
        model = Laporan
        fields = [
            "catatan_bk",
            "bukti_tindak_lanjut",
        ]

        widgets = {
            "catatan_bk": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Tuliskan hasil penanganan atau tindak lanjut..."
            }),
            "bukti_tindak_lanjut": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),
        }

# Validasi ukuran file bukti tindak lanjut BK
    def clean_bukti_tindak_lanjut(self):
        file = self.cleaned_data.get("bukti_tindak_lanjut")

       
        if file and not hasattr(file, "size"):
            return file

        if file and file.size > MAX_UPLOAD_SIZE:
            raise forms.ValidationError(
                "Ukuran file terlalu besar. Maksimal 10 MB."
            )

        return file
