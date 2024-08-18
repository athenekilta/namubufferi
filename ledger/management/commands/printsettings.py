from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Print all Django settings'

    def handle(self, *args, **options):
        self.stdout.write("Current Django settings:\n")
        for setting in dir(settings):
            if setting.isupper():
                value = getattr(settings, setting)
                self.stdout.write(f"{setting}: {value}\n")
