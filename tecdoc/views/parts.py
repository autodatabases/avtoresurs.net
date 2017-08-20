from django.views.generic import ListView, DetailView

from shop.models.product import Product, get_part_analogs, clean_number
from tecdoc.models import Part, PartTypeGroupSupplier, CarType, Section, PartCross, Supplier, PartSection


# SET @TYP_ID = 3822; /* ALFA ROMEO 145 (930) 1.4 i.e. [1994/07-1996/12] */
# SET @STR_ID = 10630; /* Поршень в сборе; Можете использовать NULL для вывода ВСЕХ запчастей к автомобилю */
#
# SELECT	LA_ART_ID
# FROM LINK_GA_STR
# INNER JOIN LINK_LA_TYP ON LAT_TYP_ID = @TYP_ID AND	LAT_GA_ID = LGS_GA_ID
# INNER JOIN LINK_ART ON LA_ID = LAT_LA_ID
# WHERE LGS_STR_ID <=> @STR_ID
# ORDER BY LA_ART_ID
# LIMIT	100;


def get_price(parts, user):
    data = []
    for part in parts:
        data.append(part)

    sku = []
    for part in data:
        sku.append(clean_number(part.part_number))
        sku.append(part.part_number)
        part.price = -1
        part.product_id = ''
        part.qty = ''
    products = Product.objects.filter(sku__in=sku)

    for part in data:
        brand_name = part.supplier_name
        sku = clean_number(part.part_number)
        for product in products:
            if sku == clean_number(product.sku) and brand_name == product.brand:
                part.price = product.get_price(user=user)
                part.product_id = product.id
                part.qty = product.get_quantity()

        if not hasattr(part, 'price'):
            part.price = -1

    data = sorted(data, key=lambda x: x.price, reverse=True)
    # for part in new_data:
    #     print("%s %s %s" % (part.product_id, part.price, part.qty))
    return data


class PartGroupList(ListView):
    template_name = 'tecdoc/part_list.html'

    def get_queryset(self):
        car_type = self.kwargs['type_id']
        section = self.kwargs['section_id']

        raw = "SELECT al.supplierid, al.datasupplierarticlenumber part_number, s.description supplier_name, prd.description product_name FROM article_links al JOIN passanger_car_pds pds ON al.supplierid = pds.supplierid JOIN suppliers s ON s.id = al.supplierid JOIN passanger_car_prd prd ON prd.id = al.productid WHERE al.productid = pds.productid AND al.linkageid = pds.passangercarid AND al.linkageid = %s AND pds.nodeid = %s AND al.linkagetypeid = 2 ORDER BY s.description , al.datasupplierarticlenumber" % (
            car_type,
            section
        )

        qs = PartSection.objects.raw(raw)

        return qs

    def get_context_data(self, **kwargs):
        context = super(PartGroupList, self).get_context_data()
        parts = context['object_list']
        context['parts'] = get_price(parts, user=self.request.user)

        type_id = self.kwargs['type_id']
        car_type = CarType.objects.get(id=type_id)
        context['car_type'] = car_type
        context['section'] = Section.objects.get(id=self.kwargs['section_id'], car_type=car_type)

        return context
