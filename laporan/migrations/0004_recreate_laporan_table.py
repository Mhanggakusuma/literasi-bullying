from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings
import cloudinary.models

class Migration(migrations.Migration):

    dependencies = [
        ('laporan', '0003_reset_laporan_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='Laporan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_anonymous', models.BooleanField(default=False)),
                ('nama_korban', models.CharField(max_length=100)),
                ('kelas_korban', models.CharField(max_length=10)),
                ('nama_terlapor', models.CharField(blank=True, max_length=100, null=True)),
                ('kelas_terlapor', models.CharField(blank=True, max_length=10, null=True)),
                ('jenis_bullying', models.CharField(max_length=20)),
                ('isi_laporan', models.TextField()),
                ('bukti', cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, resource_type='auto')),
                ('status', models.CharField(default='baru', max_length=20)),
                ('catatan_bk', models.TextField(blank=True, null=True)),
                ('bukti_tindak_lanjut', cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, resource_type='auto')),
                ('kode_laporan', models.CharField(max_length=12, unique=True)),
                ('tanggal', models.DateTimeField(auto_now_add=True)),
                ('pelapor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='laporan_bullying', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
