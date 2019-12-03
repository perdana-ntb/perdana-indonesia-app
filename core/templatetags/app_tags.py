from django import template

register = template.Library()


@register.simple_tag
def equals(arg, comparator):
    return arg == comparator


@register.filter
def qs_to_list(queryset, field):
    return queryset.values_list(field, flat=True)
