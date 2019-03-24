from django import template
register=template.Library()

@register.filter
def add_filter(value,arg):
    return "{}_{}".format(value,arg)