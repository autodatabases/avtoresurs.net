from django.views.generic import DetailView
from django.views.generic import ListView
from collections import OrderedDict

from tecdoc.models import Section, CarType


class SectionList(ListView):
    model = Section

    def get_context_data(self, **kwargs):
        context = super(SectionList, self).get_context_data()

        # sections = context['section_list']
        # for section in sections:
        #     print(section)

        parts = context['section_list']
        parts_dict = {part.id: part for part in parts}
        for part in parts:
            if part.parent_id:
                parent = parts_dict[part.parent_id]
                if hasattr(parent, 'children'):
                    parent.children.update({part.id: part})
                    parent.children = OrderedDict(sorted(parent.children.items(), key=lambda part: part[1].designation))
                else:
                    parent.children = OrderedDict({part.id: part})
        parts = [part for part in parts if not part.parent_id]
        parts = parts[0].children
        context['parts'] = parts

        type_id = self.kwargs['type_id']
        car_type = CarType.objects.get(id=type_id)
        context['car_type'] = car_type

        # todo get tree for current cartype only

        return context
