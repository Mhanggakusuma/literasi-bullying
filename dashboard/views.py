from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from users.decorators import role_required

# Halaman landing page publik sebelum login
def dashboard_home(request):
    return render(request, "dashboard/dashboard_home.html")


# Mengarahkan user ke dashboard sesuai role setelah login
@login_required
def dashboard_redirect(request):
    role = request.user.profile.role

    if role == "siswa":
        return redirect("dashboard_siswa")
    elif role == "gurubk":
        return redirect("dashboard_guru")
    elif role == "admin":
        return redirect("dashboard_admin")

    return redirect("login")


# Dashboard khusus siswa
@login_required
@role_required(['siswa'])
def dashboard_siswa(request):
    if request.user.profile.role != "siswa":
        return redirect("dashboard_redirect")
    return render(request, "dashboard/dashboard_siswa.html")

# Dashboard khusus Guru BK
@login_required
@role_required(['gurubk'])
def dashboard_guru(request):
    if request.user.profile.role != "gurubk":
        return redirect("dashboard_redirect")
    return render(request, "dashboard/dashboard_guru.html")

# Dashboard khusus admin
@login_required
@role_required(['admin'])
def dashboard_admin(request):
    if request.user.profile.role != "admin":
        return redirect("dashboard_redirect")
    return render(request, "dashboard/dashboard_admin.html")


# Halaman edukasi bullying untuk pengguna umum
def tentang_bullying_public(request):
    return render(request, "dashboard/tentang_bullying_public.html")

# Halaman edukasi bullying untuk pengguna yang sudah login
@login_required
def tentang_bullying_login(request):
    return render(request, "dashboard/tentang_bullying_login.html")
