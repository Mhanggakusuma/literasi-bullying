from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Profile

# Menampilkan data Profile secara inline pada halaman admin User
class ProfileInline(admin.StackedInline):
    model = Profile
    extra = 0

# Custom admin User untuk menambahkan Profile dalam halaman User
class CustomUserAdmin(UserAdmin):
    inlines = [ProfileInline]

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
