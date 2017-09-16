from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.core.files.base import ContentFile
from service.parser.parser import get_filename, point_load
from django.core.files.storage import default_storage


class PointView(TemplateView):
    template_name = 'service/point_load.html'

    def post(self, request):
        try:
            file = self.request.FILES['file']
        except KeyError as ke:
            return HttpResponseRedirect('/service/point_load/')

        post_filename = get_filename(self.request.FILES['file'].name)
        filename = default_storage.save(post_filename, ContentFile(file.read()))
        file.close()

        url = point_load(filename)
        return HttpResponseRedirect(url)
