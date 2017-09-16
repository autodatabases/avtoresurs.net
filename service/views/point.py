from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.core.files.base import ContentFile
from service.parser.parser import get_filename
from django.core.files.storage import default_storage

from service.parser.point import PointLoader


class PointView(TemplateView):
    template_name = 'service/point_load.html'
    url = '/service/point_load/'

    def post(self, request):
        try:
            file = self.request.FILES['file']
        except KeyError as ke:
            return HttpResponseRedirect(self.url)

        post_filename = get_filename(self.request.FILES['file'].name)
        filename = default_storage.save(post_filename, ContentFile(file.read()))
        file.close()

        point_loader = PointLoader(filename)
        point_loader.parse_file()
        point_loader.load()
        point_loader.save_report()
        point_loader.send_email()

        return HttpResponseRedirect(self.url)
