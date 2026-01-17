from django.urls import path
from . import views

urlpatterns = [
    path("", views.konten_index, name="konten_index"),
    path("artikel/<int:id>/", views.artikel_detail, name="artikel_detail"),
    path("kuis/<int:id>/", views.kuis_detail, name="konten_kuis_detail"),
]
