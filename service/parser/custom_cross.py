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
    print("PA sku: %s" % sku)
    try:
        oenbr = row[6].strip()
        if oenbr:
            part_analog, created = PartAnalog.objects.get_or_create(supplier=supplier, part_number=sku, oenbr=oenbr,
                                                                    manufacturer=manufacturer)
            if created:
                part_analog.save()
            print(oenbr)
    except Exception as exp:
        print('PA1: /n %s' % exp)
    try:
        oenbr = row[7].strip()
        if oenbr:
            part_analog, created = PartAnalog.objects.get_or_create(supplier=supplier, part_number=sku, oenbr=oenbr,
                                                                    manufacturer=manufacturer)
            if created:
                part_analog.save()
            print(oenbr)
    except Exception as exp:
        print('PA2: /n %s' % exp)
    try:
        oenbr = row[8].strip()
        if oenbr:
            part_analog, created = PartAnalog.objects.get_or_create(supplier=supplier, part_number=sku, oenbr=oenbr,
                                                                    manufacturer=manufacturer)
            if created:
                part_analog.save()
            print(oenbr)
    except Exception as exp:
        print('PA3: /n %s' % exp)


def create_part_crosses(supplier, sku, row):
    manufacturer = Manufacturer.objects.get(id=16)
    try:
        oenbr = row[6].strip()
        if oenbr:
            part_cross, created = PartCross.objects.get_or_create(supplier=supplier, part_number=sku, oenbr=oenbr,
                                                                  manufacturer=manufacturer)
            if created:
                part_cross.save()
    except:
        pass
    try:
        oenbr = row[7].strip()
        if oenbr:
            part_cross, created = PartCross.objects.get_or_create(supplier=supplier, part_number=sku, oenbr=oenbr,
                                                                  manufacturer=manufacturer)
            if created:
                part_cross.save()
    except:
        pass
    try:
        oenbr = row[8].strip()
        if oenbr:
            part_cross, created = PartCross.objects.get_or_create(supplier=supplier, part_number=sku, oenbr=oenbr,
                                                                  manufacturer=manufacturer)
            if created:
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
            supplier, created = Supplier.objects.get_or_create(title=brand.strip().upper())
            # if created:
            #     supplier.matchcode = supplier.title
            #     supplier.dataversion = 'custom'
            #     supplier.nbrofarticles = 'false'
            #     supplier.hasnewversionarticles = 'false'
            #     supplier.save()
            brands.append(brand.strip().upper())
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
                    i = i + 1
                    if sku == '-':
                        continue
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
                    print('%s %s %s added' % (title, supplier.title, sku))
            except Exception as e:
                print(e)

