import csv
from decimal import Decimal
from translate import Translator
from django.core.management.base import BaseCommand
from django.conf import settings
from ledger.models import Product,ProductTag
import datetime

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("file")
        parser.add_argument("--dialect", nargs="?", default="unix")

    def handle(self, *args, **options):
        with open(options["file"], encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                print(row['Name'] + ' ' + row['Price'] + ' ' + row['Tags'] + ' ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                if not Product.objects.filter(name=row['Name']).exists():
                    product = Product()
                    product.name = row['Name']
                else:
                    product = Product.objects.get(name=row['Name'])
                setattr(product, f"name_zh_cn", self.translate(row['Name'], 'zh'))
                product.price = Decimal(row['Price'].replace(',', '.'))
                product.save()
                product.tags.set(row['Tags'].split(','))
                product.save()

            for tag in ProductTag.objects.all():
                setattr(tag, f"name_zh_cn", self.translate(tag.name, 'zh'))
                tag.save()

    def translate(self, word, dest):
        translator = Translator(to_lang=dest)
        return translator.translate(word)