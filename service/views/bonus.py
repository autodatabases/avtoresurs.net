from django.core.files.base import ContentFile
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from service.parser.parser import get_filename
from service.parser.bonus import BonusLoader
from django.core.files.storage import default_storage


class BonusView(TemplateView):
    template_name = 'service/bonus_load.html'

    def post(self, request):
        try:
            file = self.request.FILES['file']
        except KeyError as ke:
            return HttpResponseRedirect('/service/bonus_load/')

        post_filename = get_filename(self.request.FILES['file'].name)
        filename = default_storage.save(post_filename, ContentFile(file.read()))
        file.close()

        bonus_loader = BonusLoader(filename)
        bonus_loader.parse_file()
        bonus_loader.load()
        bonus_loader.save_report()
        bonus_loader.send_email()

        return HttpResponseRedirect('/service/bonus_load/')