from collections import Set
from django.views.generic import DetailView

from profile.models import Profile
from shop.models.product import Product, get_price
from tecdoc.models import PartAnalog, get_part_analogs, clean_number, Part, PartCriteria


class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        product = context['product']
        product.price = get_price(product=product, user=self.request.user)
        product.default_price = get_price(product)

        part = Part.objects.get(sku__iexact=product.sku, supplier__title=product.brand)

        images = list()
        for image in part.images.all():
            images.append(image.absolute_url())
        product.images = images

        raw_sql = 'select ACR_ART_ID, des_texts.tex_text as text1, ifnull(des_texts2.tex_text, acr_value) as text2 from article_criteria left join designations as designations2 on designations2.des_id = acr_kv_des_id left join des_texts as des_texts2 on des_texts2.tex_id = designations2.des_tex_id left join criteria on cri_id = acr_cri_id left join designations on designations.des_id = cri_des_id left join des_texts on des_texts.tex_id = designations.des_tex_id where	acr_art_id = %s and (designations.des_lng_id is null or designations.des_lng_id = 16) and (designations2.des_lng_id is null or designations2.des_lng_id = 16);'
        part_criteria = PartCriteria.objects.raw(raw_sql, [part.pk])
        if len(list(part_criteria)) == 0:
            part_criteria = None
        product.part_criteria = part_criteria

        part_analogs = PartAnalog.objects.filter(search_number=clean_number(product.sku))
        product.title = Part.objects.filter(sku=product.sku, supplier__title=product.brand)[0].designation
        parts = set()
        sku = []
        for pa in part_analogs:
            parts.add(pa.part)
            sku.append(pa.part.sku)
        products = Product.objects.filter(sku__in=sku)

        for part in parts:
            brand_name = part.supplier.title
            for prod in products:
                if clean_number(part.sku) == clean_number(prod.sku) and brand_name == prod.brand:
                    part.price = get_price(product=prod, user=self.request.user)
                    part.product_id = prod.id
                    part.quantity = prod.get_quantity()
            if not hasattr(part, 'price'):
                part.price = -1

        parts = sorted(parts, key=lambda part: part.price, reverse=True)
        context['part_analogs'] = parts
        return context
