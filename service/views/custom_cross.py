from django.contrib.admin.views.decorators import staff_member_required
from django.core.files.base import ContentFile
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.core.files.storage import default_storage
from service.parser.custom_cross import CustomCross
from service.parser.parser import get_filename


@method_decorator(staff_member_required, name='dispatch')
class CustomCrossView(TemplateView):
    template_name = 'service/custom_cross.html'

    def post(self, request):
        try:
            file = self.request.FILES['file']
        except KeyError as ke:
            return HttpResponseRedirect('/service/custom_cross/')

        post_filename = get_filename(self.request.FILES['file'].name)
        filename = default_storage.save(post_filename, ContentFile(file.read()))
        file.close()

        cc = CustomCross(filename)
        cc.parse_file()
        cc.make_suppliers()
        cc.make_products()
        return HttpResponseRedirect('/service/custom_cross/')
