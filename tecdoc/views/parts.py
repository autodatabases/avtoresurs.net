from django.views.generic import ListView, DetailView

from shop.models.product import Product
from tecdoc.models import Part, PartTypeGroupSupplier, CarType, Section


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


class PartTypeGroupSupplierList(ListView):
    model = PartTypeGroupSupplier
    template_name = 'tecdoc/part_list.html'

    def get_queryset(self, *args, **kwargs):
        car_type_id = self.kwargs['type_id']
        car_type = CarType.objects.get(id=car_type_id)
        section_id = self.kwargs['section_id']
        section = Section.objects.get(id=section_id)
        qs = super(PartTypeGroupSupplierList, self).\
            get_queryset().\
            filter(car_type=car_type, group__section=section)
        return qs

    def get_context_data(self, **kwargs):
        context = super(PartTypeGroupSupplierList, self).get_context_data(**kwargs)

        sku = []
        brand = []
        for part in context['parttypegroupsupplier_list']:
            sku.append(part.part_group.part.sku)
        products = Product.objects.filter(sku__in=sku)

        # adding price data into parttypegroupsupplier_list
        parts_with_price = []
        parts_without_price = []
        for part in context['parttypegroupsupplier_list']:
            brand_name_small = part.part_group.part.supplier.title.lower()
            sku_small = part.part_group.part.sku.lower()
            for product in products:
                if sku_small == product.sku and brand_name_small == product.manufacturer:
                    # print(product)
                    part.part_group.part.price = product.get_price()
                    part.part_group.part.product_id = product.id
                    part.part_group.part.quantity = product.get_quantity()
            if not hasattr(part.part_group.part, 'price'):
                part.part_group.part.price = -1
        context['parttypegroupsupplier_list'] = sorted(context['parttypegroupsupplier_list'],
                                                       key=lambda x: x.part_group.part.price, reverse=True)

        type_id = self.kwargs['type_id']
        car_type = CarType.objects.get(id=type_id)
        context['car_type'] = car_type
        context['section'] = Section.objects.get(id=self.kwargs['section_id'])

        return context
