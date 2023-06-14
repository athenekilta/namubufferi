import csv
from decimal import Decimal

from django.core.management.base import BaseCommand

from ledger.models import Product


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("file")
        parser.add_argument("--dialect", nargs="?", default="unix")

    def handle(self, *args, **options):
        with open(options["file"]) as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                product = Product()
                product.name = row['Name']
                product.price = Decimal(row['Price'].replace(',', '.'))
                product.save()
                product.tags.set(row['Tags'].split(','))