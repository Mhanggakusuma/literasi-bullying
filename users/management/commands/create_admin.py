from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = "Create admin user"

    def handle(self, *args, **options):
        User = get_user_model()

        if not User.objects.filter(username="adminsmp1md3").exists():
            User.objects.create_superuser(
                username="adminsmp1md3",
                email="adminsmp1md3@gmail.com",
                password="Smp1md3333"
            )
            self.stdout.write("Admin created")
        else:
            self.stdout.write("Admin already exists")
