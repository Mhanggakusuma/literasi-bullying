from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

User = get_user_model()

class Command(BaseCommand):
    help = "Create default admin if not exists"

    def handle(self, *args, **options):
        username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "")

        if not username or not password:
            self.stdout.write("Admin env not set, skipping.")
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write("Admin already exists.")
            return

        User.objects.create_superuser(
            username=username,
            password=password,
            email=email
        )

        self.stdout.write("Admin user created.")
