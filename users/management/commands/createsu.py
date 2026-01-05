from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = "Create default admin user"

    def handle(self, *args, **options):
        User = get_user_model()

        username = "adminsmp1md3"
        email = "admin@admin.com"
        password = "Smp1md3333"

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING("Admin user already exists"))
            return

        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )

        self.stdout.write(self.style.SUCCESS("Admin user created successfully"))
