from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# ================= PUBLIC LANDING PAGE =================
def dashboard_home(request):
    return render(request, "dashboard/dashboard_home.html")


# ================= DASHBOARD REDIRECT =================
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


# ================= DASHBOARD ROLE =================
@login_required
def dashboard_siswa(request):
    if request.user.profile.role != "siswa":
        return redirect("dashboard_redirect")
    return render(request, "dashboard/dashboard_siswa.html")


@login_required
def dashboard_guru(request):
    if request.user.profile.role != "gurubk":
        return redirect("dashboard_redirect")
    return render(request, "dashboard/dashboard_guru.html")


@login_required
def dashboard_admin(request):
    if request.user.profile.role != "admin":
        return redirect("dashboard_redirect")
    return render(request, "dashboard/dashboard_admin.html")


# ================= TENTANG BULLYING =================
def tentang_bullying_public(request):
    return render(request, "dashboard/tentang_bullying_public.html")


@login_required
def tentang_bullying_login(request):
    return render(request, "dashboard/tentang_bullying_login.html")
