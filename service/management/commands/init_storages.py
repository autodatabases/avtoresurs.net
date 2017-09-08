from django.core.management import BaseCommand

from shop.models.product import Product, ProductPrice
from shop.models.storage import Storage, ProductStoragePrice



class Command(BaseCommand):
    help = 'initial create ProductStoragePrice'

    def handle(self, *args, **options):
        product_prices = ProductPrice.objects.all()
        for product_price in product_prices:
            product = product_price.product
            storage = Storage.objects.get(id=1)
            psp = ProductStoragePrice(product=product, storage=storage, price=product_price)
            psp.save()
