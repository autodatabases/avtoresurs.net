from django.views.generic import DetailView, TemplateView
from django.views.generic import ListView
from collections import OrderedDict

from tecdoc.models import Section, CarType



class SectionList(ListView):
    model = Section
    pk_url_kwarg = 'type_id'
    template_name = 'tecdoc/section_list.html'

    def get_queryset(self):
        car_type = self.kwargs['type_id']
        qs = Section.objects.filter(car_type=car_type)
        return qs


    def get_context_data(self, **kwargs):
        context = super(SectionList, self).get_context_data()
        parts = context['section_list']
        # for part in parts:
        #     print(part)
        parts_dict = {part.id: part for part in parts}
        for part in parts:
            if part.parent_id:
                parent = parts_dict[part.parent_id]
                if hasattr(parent, 'children'):
                    parent.children.update({part.id: part})
                    parent.children = OrderedDict(sorted(parent.children.items(), key=lambda part: part[1].title))
                else:
                    parent.children = OrderedDict({part.id: part})
        parts = [part for part in parts if not part.parent_id]
        # parts = parts[0].children
        parts = sorted(parts)
        context['parts'] = parts

        # print(parts)

        type_id = self.kwargs['type_id']
        car_type = CarType.objects.get(id=type_id)
        context['car_type'] = car_type

        # todo get tree for current cartype only

        return context
