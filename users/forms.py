from django import forms
from django.contrib.auth.models import User
from .models import Profile
from datetime import timedelta

# Form registrasi akun siswa
class RegisterForm(forms.Form):
    nama = forms.CharField(label="Nama Lengkap", max_length=100)
    username = forms.CharField(max_length=50)
    nis = forms.CharField(max_length=20)
    tanggal_masuk = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Tanggal Masuk Sekolah"
    )
    password = forms.CharField(widget=forms.PasswordInput)
    ulangi_password = forms.CharField(widget=forms.PasswordInput)
    
    # Validasi username agar tidak duplikat
    def clean_username(self):
        if User.objects.filter(username=self.cleaned_data["username"]).exists():
            raise forms.ValidationError("Username sudah dipakai")
        return self.cleaned_data["username"]
    # Validasi NIS agar tidak duplikat
    def clean_nis(self):
        if Profile.objects.filter(nis=self.cleaned_data["nis"]).exists():
            raise forms.ValidationError("NIS sudah terdaftar")
        return self.cleaned_data["nis"]
    # Validasi kecocokan password
    def clean(self):
        cleaned = super().clean()
        if cleaned.get("password") != cleaned.get("ulangi_password"):
            raise forms.ValidationError("Password tidak cocok")
        return cleaned
    # Menyimpan data registrasi ke database
    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data["username"],
            password=self.cleaned_data["password"],
            first_name=self.cleaned_data["nama"],
        )

        tanggal_masuk = self.cleaned_data["tanggal_masuk"]
        tanggal_akhir = tanggal_masuk.replace(year=tanggal_masuk.year + 3)

        Profile.objects.filter(user=user).update(
            role="siswa",
            nis=self.cleaned_data["nis"],
            tanggal_masuk=tanggal_masuk,
            tanggal_akhir_aktif=tanggal_akhir,
        )

        return user
