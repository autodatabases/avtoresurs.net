from django.views.generic import DetailView, TemplateView
from django.views.generic import ListView
from collections import OrderedDict

from tecdoc.models import Section, CarType
from tecdoc.models.tree import CarTree


class SectionList(ListView):
    model = CarTree
    pk_url_kwarg = 'type_id'
    template_name = 'tecdoc/section_list.html'

    # def get_queryset(self, *args, **kwargs):
        # print(kwargs)
        # car_type_id = kwargs['type_id']
        # print('car_Type_id: %s' % car_type_id)
        # qs = CarTree.objects.all().filter(car_type__id=car_type_id)
        # for ct in qs:
        #     print(ct)
        # return qs


    def get_context_data(self, **kwargs):
        context = super(SectionList, self).get_context_data()

        # sections = context['section_list']
        # for section in sections:
        #     print(section)



        parts = context['cartree_list']
        for part in parts:
            print(part)
        # parts_dict = {part.id: part for part in parts}
        # for part in parts:
        #     if part.parent_id:
        #         parent = parts_dict[part.parent_id]
        #         if hasattr(parent, 'children'):
        #             parent.children.update({part.id: part})
        #             parent.children = OrderedDict(sorted(parent.children.items(), key=lambda part: part[1].title))
        #         else:
        #             parent.children = OrderedDict({part.id: part})
        # parts = [part for part in parts if not part.parent_id]
        # parts = parts[0].children
        # context['parts'] = parts
        #
        # print(parts)

        type_id = self.kwargs['type_id']
        car_type = CarType.objects.get(id=type_id)
        context['car_type'] = car_type

        # todo get tree for current cartype only

        return context
