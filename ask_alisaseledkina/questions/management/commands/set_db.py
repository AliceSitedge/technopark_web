from django.core.management.base import BaseCommand
import os


class Command(BaseCommand):
    def handle(self, *args, **options):
        os.system('python manage.py makemigrations')
        os.system('python manage.py migrate')
        os.system('python manage.py createsuperuser')
        os.system('python manage.py generate_data')
