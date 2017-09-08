from shop.models.product import Product, ProductPrice
from shop.models.storage import Storage, ProductStoragePrice

product_prices = ProductPrice.objects.all()

for product_price in product_prices:
    product = product_price.product
    storage = Storage.objects.get(id=1)
    psp = ProductStoragePrice(product=product, storage=storage, product_price=product)
    psp.save()
