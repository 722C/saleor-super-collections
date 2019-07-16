from django.core.management.base import BaseCommand
from django.db import transaction
import importlib

SuperCollection = importlib.import_module('saleor-super-collections.super_collections.models').SuperCollection

class Command(BaseCommand):
    help = 'Rebuilds the mptt tree for super collections'
    def handle(self, **options):
        with transaction.atomic():
            SuperCollection.tree.rebuild()

        self.stdout.write(self.style.SUCCESS('Successfully rebuilt tree'))
