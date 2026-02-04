from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views import View
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from .models import Profile
from users.decorators import role_required

# ================= LOGIN =================
def login_view(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get("username"),
            password=request.POST.get("password")
        )

        if user:
            profile = user.profile

            if not profile.is_masih_aktif():
                messages.error(
                    request,
                    "Akun Anda sudah tidak aktif. Hubungi pihak sekolah."
                )
                return redirect("login")

            login(request, user)

            if profile.force_password_change:
                messages.warning(request, "Silakan ganti password terlebih dahulu")
                return redirect("password_change")

            # 🔴 WAJIB ISI KELAS JIKA SISWA
            if profile.role == "siswa" and not profile.kelas:
                return redirect("lengkapi_profil")

            return redirect(
                "dashboard_siswa" if profile.role == "siswa" else
                "dashboard_guru" if profile.role == "gurubk" else
                "dashboard_admin"
            )

        messages.error(request, "Username atau password salah")

    return render(request, "users/login.html")


# ================= REGISTER =================
def register_view(request):
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Pendaftaran berhasil")
        return redirect("login")
    return render(request, "users/register.html", {"form": form})


# ================= LENGKAPI PROFIL (ISI KELAS) =================
@login_required
@role_required(['siswa'])
def lengkapi_profil(request):
    profile = request.user.profile

    if profile.kelas_locked:
        return redirect("dashboard_siswa")

    if request.method == "POST":
        profile.kelas = request.POST.get("kelas")
        profile.kelas_locked = True
        profile.save()
        return redirect("dashboard_siswa")

    return render(request, "users/lengkapi_profil.html", {
        "kelas_choices": Profile.KELAS_CHOICES
    })


# ================= LOGOUT =================
class LogoutAllowGet(View):
    def get(self, request):
        logout(request)
        return redirect("login")


# ================= LUPA PASSWORD =================
def lupa_password_view(request):
    if request.method == "POST":
        nis = request.POST.get("nis")
        if Profile.objects.filter(nis=nis).exists():
            messages.info(
                request,
                "Akun ditemukan. Hubungi Admin / Guru BK untuk reset password."
            )
        else:
            messages.error(request, "NIS tidak terdaftar")
    return render(request, "users/lupa_password.html")


# ================= PASSWORD CHANGE DONE =================
def password_change_done_view(request):
    profile = request.user.profile
    profile.force_password_change = False
    profile.save()
    messages.success(request, "Password berhasil diganti")
    return redirect("dashboard_siswa")
