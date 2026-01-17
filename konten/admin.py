from django.contrib import admin
from .models import Artikel, Video, Kuis, Pertanyaan, Opsi


class OpsiInline(admin.TabularInline):
    model = Opsi
    extra = 2


class PertanyaanInline(admin.TabularInline):
    model = Pertanyaan
    extra = 1
    show_change_link = True


@admin.register(Kuis)
class KuisAdmin(admin.ModelAdmin):
    list_display = ("judul",)
    inlines = [PertanyaanInline]


@admin.register(Pertanyaan)
class PertanyaanAdmin(admin.ModelAdmin):
    list_display = ("teks", "kuis")
    inlines = [OpsiInline]


@admin.register(Opsi)
class OpsiAdmin(admin.ModelAdmin):
    list_display = ("teks_opsi", "pertanyaan", "is_benar")


@admin.register(Artikel)
class ArtikelAdmin(admin.ModelAdmin):
    list_display = ("judul", "tanggal_upload")
    search_fields = ("judul",)
    fields = ("judul", "deskripsi", "konten")


admin.site.register(Video)
