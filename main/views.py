import csv

from django.views.generic import TemplateView
from shop.models.product import Product

# Create your views here.
from tecdoc.models import Part


class MainPageView(TemplateView):
    template_name = 'main_page.html'


class ProductLoader(TemplateView):
    template_name = 'load.html'

    def get(self, request):
        get_data = super(ProductLoader, self).get(request)
        get_data = 0
        path = '/home/auto/avtoresurs_new/avtoresurs_new/NewsAuto.csv'
        pass_first_line = True

        report = []

        with open(path) as f:
            if pass_first_line:
                pass_first_line = False
                pass
            reader = csv.reader(f, delimiter=';')
            for idx, row in enumerate(reader):
                created = ''
                try:
                    # print('sku - %s, brand - %s, title - %s, cross - %s , quantity - %s, active - True, price - %s' %
                    #       (row[0], row[1], row[2], row[3], row[4], row[5]))

                    created = Product.objects.get_or_create(
                        sku=row[0].lower().replace(" ", ""),
                        manufacturer=row[1].lower(),
                        title=row[2].lower(),
                        cross_sku=row[3].lower(),
                        quantity=row[4],
                        # quantity=10,
                        active=True,
                        price=row[5],
                        # price=455.12,
                    )
                    # print(created)
                    part = Part.objects.filter(sku__iexact=created.sku, supplier__title__iexact=created.manufacturer)
                    if not part:
                        error_string = "%s %s %s %s %s" % (
                            idx,
                            created.sku,
                            created.manufacturer,
                            created.title,
                            created.cross_sku
                        )
                        report.append(error_string)
                except:
                    pass

        if report:
            error_file_path = '/home/auto/avtoresurs_new/avtoresurs_new'
            report_log = ''
            for error_line in report:
                error_line += '\n'
                report_log += error_line
            with open(error_file_path, 'w+') as error_file:
                print(report)
                error_file.write(report_log)

        return get_data
