from django import template

register = template.Library()


@register.inclusion_tag('super_collections/dashboard/side_nav_inclusion.html',
                        takes_context=True)
def super_collections_side_nav(context):
    return context
