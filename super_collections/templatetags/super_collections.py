from django import template

from ..models import SuperCollection

register = template.Library()


@register.inclusion_tag('super_collections/dashboard/side_nav_inclusion.html',
                        takes_context=True)
def super_collections_side_nav(context):
    return context


@register.inclusion_tag('super_collections/_list.html', takes_context=True)
def super_collections(context):
    context['super_collections'] = SuperCollection.objects.public_roots_for_list()
    return context
