import sys

from shop.models.product import Product, clean_number
from tecdoc.models import Supplier, Part, PartCross, PartAnalog, Manufacturer


def get_title(oe_number):
    part_cross = PartCross.objects.filter(oenbr=oe_number).first()
    part = Part.objects.filter(supplier=part_cross.supplier, part_number=part_cross.part_number)
    title = part.title
    return title


def create_part_analogs(supplier, sku, row):
    manufacturer = Manufacturer.objects.get(id=16)
    try:
        part_analog = PartAnalog(supplier=supplier, part_number=sku, oenbr=row[6], manufacturer=manufacturer)
        part_analog.save()
        print(row[6])
    except Exception as exp:
        print('PA1: /n %s' % exp)
    try:
        part_analog = PartAnalog(supplier=supplier, part_number=sku, oenbr=row[7], manufacturer=manufacturer)
        part_analog.save()
        print(row[7])
    except Exception as exp:
        print('PA2: /n %s' % exp)
    try:
        part_analog = PartAnalog(supplier=supplier, part_number=sku, oenbr=row[8], manufacturer=manufacturer)
        part_analog.save()
        print(row[8])
    except Exception as exp:
        print('PA3: /n %s' % exp)


def create_part_crosses(supplier, sku, row):
    manufacturer = Manufacturer.objects.get(id=16)
    try:
        part_cross = PartCross(supplier=supplier, part_number=sku, oenbr=row[6], manufacturer=manufacturer)
        part_cross.save()
    except:
        pass
    try:
        part_cross = PartCross(supplier=supplier, part_number=sku, oenbr=row[7], manufacturer=manufacturer)
        part_cross.save()
    except:
        pass
    try:
        part_cross = PartCross(supplier=supplier, part_number=sku, oenbr=row[8], manufacturer=manufacturer)
        part_cross.save()
    except:
        pass


class CustomCross:
    def __init__(self, filename):
        self.filename = filename
        self.data = None
        self.brands = None

    def parse_file(self):
        with open(self.filename, 'r') as file_custom_cross:
            data = file_custom_cross.read().splitlines(True)
        file_custom_cross.close()
        self.data = data

    def make_suppliers(self):
        brands = list()
        row = self.data[0].split(',')
        for brand in row[:4]:
            supplier, created = Supplier.objects.get_or_create(dataversion='custom', title=brand.upper(),
                                                               matchcode=brand.upper(), nbrofarticles='false',
                                                               hasnewversionarticles='false')
            supplier.save()
            brands.append(brand)
        self.brands = brands
        print(self.brands)

    def make_products(self):
        for row in self.data[1:]:
            row = row.split(',')
            i = 0
            try:
                for brand in self.brands:
                    # print(row)*
                    sku = row[i]
                    clean_sku = clean_number(sku)
                    print('sku: %s, clean_sku: %s' % (sku, clean_sku))
                    product, created = Product.objects.get_or_create(brand=brand, sku=clean_sku)
                    product.save()
                    print('Product %s %s SAVE()' % (product.brand, product.sku))
                    supplier = Supplier.objects.get(title=brand.upper())
                    title = 'Деталь глушителя'
                    # try:
                    #     title = get_title(row[6])
                    # except:
                    #     title = 'Нет названия'
                    part, created = Part.objects.get_or_create(supplier=supplier, part_number=sku,
                                                               clean_part_number=clean_sku, title=title)
                    if created:
                        part.save()
                    print('Part %s saved' % part.part_number)

                    create_part_analogs(supplier, sku, row)
                    print('part_analogs SAVED()')

                    create_part_crosses(supplier, sku, row)
                    print('part_crosses SAVED()')

                    i = i + 1
                    print('%s %s %s added' % (title, supplier.title, sku))
            except Exception as e:
                print(e)

