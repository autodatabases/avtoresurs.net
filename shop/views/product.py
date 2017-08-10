import os
from collections import Set
from django.views.generic import DetailView

from profile.models import Profile
from shop.models.product import Product, clean_number, get_part_analogs
from tecdoc.models import PartAnalog, Part, PartCriteria, CarType, PartGroup, Image, Supplier, PartApplicability, \
    PartAttribute, Q


def get_product_analogs(supplier, part_number, user):
    raw = "SELECT DISTINCT a.datasupplierarticlenumber, s.description supplier_name, c.PartsDataSupplierArticleNumber part_number FROM article_oe a JOIN manufacturers m ON m.id=a.manufacturerId JOIN article_cross c ON c.OENbr=a.OENbr JOIN suppliers s ON s.id=c.SupplierId WHERE a.datasupplierarticlenumber='%s' AND a.supplierid='%s'" % (
        part_number, supplier.id)
    part_analogs = PartAnalog.objects.raw(raw)
    data = []
    for part in part_analogs:
        data.append(part)

    sku = []
    for part in data:
        sku.append(part.part_number)
        sku.append(clean_number(part.part_number))
        part.price = -1
        part.product_id = ''
        part.qty = ''
    products = Product.objects.filter(sku__in=sku)

    for part in data:
        pg = PartGroup.objects.filter(supplier=supplier).filter(Q(part_number=part_number) | Q(part_number=clean_number(part_number))).first()
        if pg:
            part.title = pg.part.title
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

    return data


class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        product = context['product']
        product.price = product.get_price(user=self.request.user)
        product.default_price = product.get_price()

        # product.title =



        supplier = Supplier.objects.get(title=product.brand)
        part_number = product.sku

        pg = PartGroup.objects.filter(supplier=supplier, part_number=part_number).first()
        if pg:
            title = pg.part.title
            product.title = title

        tecdoc_image_path = '/static/main/images/tecdoc/'
        image = Image.objects.filter(supplier=supplier, part_number=part_number).first()
        try:
            base, ext = os.path.splitext(image.picture)
            if ext == '.BMP':
                ext = ext.replace('BMP', 'jpg')
            product.image = '%s%s%s' % (tecdoc_image_path, base, ext.lower())
        except Exception as exc:
            product.image = '/static/main/images/no-image.png'
        part_applicability = PartApplicability.objects.filter(supplier=supplier,
                                                              part_number=part_number).select_related(
            'car_type', 'car_type__model', 'car_type__model__manufacturer'
        )
        product.part_applicability = part_applicability

        part_attributes = PartAttribute.objects.filter(supplier=supplier, part_number=part_number)
        product.part_attributes = part_attributes

        context['part_analogs'] = get_product_analogs(supplier, part_number, user=self.request.user)

        # images = list()
        # for image in part.images.all():
        #     images.append(image.absolute_url())
        # product.images = images
        #
        # lng_id = 16;
        # raw_sql = 'select ACR_ART_ID, des_texts.tex_text as text1, ifnull(des_texts2.tex_text, acr_value) as text2 from article_criteria left join designations as designations2 on designations2.des_id = acr_kv_des_id left join des_texts as des_texts2 on des_texts2.tex_id = designations2.des_tex_id left join criteria on cri_id = acr_cri_id left join designations on designations.des_id = cri_des_id left join des_texts on des_texts.tex_id = designations.des_tex_id where	acr_art_id = %s and (designations.des_lng_id is null or designations.des_lng_id = %s) and (designations2.des_lng_id is null or designations2.des_lng_id = %s);'
        # part_criteria = PartCriteria.objects.raw(raw_sql, [part.pk, lng_id, lng_id])
        # if len(list(part_criteria)) == 0:
        #     part_criteria = None
        # product.part_criteria = part_criteria
        #
        # # print(part.pk)
        #
        # raw_sql_applicability = 'select	la_id, typ_id,	mfa_brand,	des_texts7.tex_text as mod_cds_text,	des_texts.tex_text as typ_cds_text,	typ_pcon_start,	typ_pcon_end, typ_ccm,	typ_kw_from,	typ_kw_upto,	typ_hp_from,	typ_hp_upto,	typ_cylinders,	engines.eng_code,	des_texts2.tex_text as typ_engine_des_text, des_texts3.tex_text as typ_fuel_des_text, ifnull(des_texts4.tex_text, des_texts5.tex_text) as typ_body_des_text, des_texts6.tex_text as typ_axle_des_text, typ_max_weight from link_art inner join link_la_typ on lat_la_id = la_id inner join types on typ_id = lat_typ_id inner join country_designations on country_designations.cds_id = typ_cds_id inner join des_texts on des_texts.tex_id = country_designations.cds_tex_id inner join models on mod_id = typ_mod_id inner join manufacturers on mfa_id = mod_mfa_id inner join country_designations as country_designations2 on country_designations2.cds_id = mod_cds_id inner join des_texts as des_texts7 on des_texts7.tex_id = country_designations2.cds_tex_id left join designations on designations.des_id = typ_kv_engine_des_id left join des_texts as des_texts2 on des_texts2.tex_id = designations.des_tex_id left join designations as designations2 on designations2.des_id = typ_kv_fuel_des_id left join des_texts as des_texts3 on des_texts3.tex_id = designations2.des_tex_id left join link_typ_eng on lte_typ_id = typ_id left join engines on eng_id = lte_eng_id left join designations as designations3 on designations3.des_id = typ_kv_body_des_id  left join des_texts as des_texts4 on des_texts4.tex_id = designations3.des_tex_id left join designations as designations4 on designations4.des_id = typ_kv_model_des_id left join des_texts as des_texts5 on des_texts5.tex_id = designations4.des_tex_id left join designations as designations5 on designations5.des_id = typ_kv_axle_des_id left join des_texts as des_texts6 on des_texts6.tex_id = designations5.des_tex_id where	la_art_id = %s and	country_designations.cds_lng_id = %s and	country_designations2.cds_lng_id = %s and (designations.des_lng_id is null or designations.des_lng_id = %s) and (designations2.des_lng_id is null or designations2.des_lng_id = %s) and (designations3.des_lng_id is null or designations3.des_lng_id = %s) and (designations4.des_lng_id is null or designations4.des_lng_id = %s) and (designations5.des_lng_id is null or designations5.des_lng_id = %s) order by	mfa_brand,	mod_cds_text,	typ_cds_text,	typ_pcon_start,	typ_ccm;'
        # car_types = PartGroup.objects.raw(raw_sql_applicability,
        #                                   [part.pk, lng_id, lng_id, lng_id, lng_id, lng_id, lng_id, lng_id, ])
        # if len(list(car_types)) == 0:
        #     car_types = None
        # product.car_types = car_types

        # for car in car_types:
        #     print("%s %s %s" % (car.mfa_brand, car.mod_cds_text, car.typ_cds_text))


        # part_analogs = PartAnalog.objects.filter(search_number=clean_number(product.sku))
        # product.title = Part.objects.filter(sku=product.sku, supplier__title=product.brand)[0].designation
        # sku = set()
        # parts = set()
        # group = part_analogs[0].part.group.all()
        # for pa in part_analogs:
        #     parts.add(pa.part)
        #     sku.add(pa.part.sku)

        # additional block to search the the second level tree cross
        # clean_sku = set()
        # for sku_num in sku:
        #     clean_sku.add(clean_number(sku_num))
        # part_analogs = PartAnalog.objects.filter(search_number__in=clean_sku, part__group__in=group)
        # parts = set()
        # sku = set()
        # for pa in part_analogs:
        #     parts.add(pa.part)
        #     sku.add(pa.part.sku)

        # products = Product.objects.filter(sku__in=sku)
        #
        # for part in parts:
        #     brand_name = part.supplier.title
        #     for prod in products:
        #         if clean_number(part.sku) == clean_number(prod.sku) and brand_name == prod.brand:
        #             part.price = prod.get_price(user=self.request.user)
        #             part.product_id = prod.id
        #             part.quantity = prod.get_quantity()
        #     if not hasattr(part, 'price'):
        #         part.price = -1
        #
        # parts = sorted(parts, key=lambda part: part.price, reverse=True)
        # context['part_analogs'] = parts
        return context
