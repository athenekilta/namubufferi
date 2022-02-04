import csv
import random

from django.core.management.base import BaseCommand

from ledger.models import Group, Product


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("file")
        parser.add_argument("--dialect", nargs="?", default="unix")

    def handle(self, *args, **options):
        with open(options["file"], newline="") as f:
            for row in csv.DictReader(f, dialect=options["dialect"]):
                product = Product.objects.create(
                    name=row.get("name", list(row.values())[0]),
                    price=row.get("price", random.randint(0, 1000)),
                )
                group, _ = Group.objects.get_or_create(name=row.get("group", "all"))
                product.group_set.add(group)
