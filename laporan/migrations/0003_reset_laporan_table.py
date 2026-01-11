from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('laporan', '0002_alter_laporan_kelas_korban'),
    ]

    operations = [
        migrations.RunSQL(
            sql="DROP TABLE IF EXISTS laporan_laporan CASCADE;",
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]
