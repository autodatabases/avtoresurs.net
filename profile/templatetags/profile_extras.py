from django.template.defaultfilters import register
# from django import template


@register.simple_tag()
def multiply(unit_price, qty, *args, **kwargs):
    # you would need to do any localization of the result here
    return unit_price * qty


# register = template.Library()
