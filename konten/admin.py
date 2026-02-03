from django.contrib import admin
from .models import Artikel, Video, Kuis, Pertanyaan, Opsi

# Menampilkan opsi jawaban secara inline (tabel) pada form pertanyaan
class OpsiInline(admin.TabularInline):
    model = Opsi
    extra = 2

# Menampilkan pertanyaan secara inline pada form kuis
class PertanyaanInline(admin.TabularInline):
    model = Pertanyaan
    extra = 1
    show_change_link = True

# Konfigurasi tampilan admin untuk model Kuis
@admin.register(Kuis)
class KuisAdmin(admin.ModelAdmin):
    list_display = ("judul",)
    inlines = [PertanyaanInline]

# Konfigurasi admin untuk model Pertanyaan
@admin.register(Pertanyaan)
class PertanyaanAdmin(admin.ModelAdmin):
    list_display = ("teks", "kuis")
    inlines = [OpsiInline]


# Konfigurasi admin untuk model Opsi jawaban
@admin.register(Opsi)
class OpsiAdmin(admin.ModelAdmin):
    list_display = ("teks_opsi", "pertanyaan", "is_benar")

# Konfigurasi admin untuk model Artikel
@admin.register(Artikel)
class ArtikelAdmin(admin.ModelAdmin):
    list_display = ("judul", "tanggal_upload")
    search_fields = ("judul",)
    fields = ("judul", "deskripsi", "konten")

# Mendaftarkan model Video ke Django Admin dengan konfigurasi default
admin.site.register(Video)
