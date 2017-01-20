from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.

class PanelMainView (TemplateView):
    template_name = 'panel/base_panel.html'
