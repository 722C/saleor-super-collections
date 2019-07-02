import json

from django.http import HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.db.models import Q

from saleor.core.utils import build_absolute_uri
from saleor.product.utils import products_with_availability

from .models import SuperCollection


def super_collections_visible_to_user(user):
    if user.is_authenticated and user.is_active and user.is_staff:
        return SuperCollection.objects.all()
    return SuperCollection.objects.public()


def super_collection_breadcrumb_json_ld_list(super_collection):
    lists = []
    list_elements = []
    for ancestor in super_collection.get_ancestors():
        list_elements.append({
            '@type': 'ListItem',
            'position': len(list_elements) + 1,
            'name': ancestor.name,
            'item': build_absolute_uri(
                location=ancestor.get_absolute_url())
        })
    if list_elements:
        lists.append({
            '@context': 'http://schema.org',
            '@type': 'BreadcrumbList',
            'itemListElement': list_elements
        })
    return lists


def super_collection_index(request, slug, pk):
    super_collections = super_collections_visible_to_user(request.user)
    super_collection = get_object_or_404(super_collections, id=pk)
    if super_collection.slug != slug:
        return HttpResponsePermanentRedirect(
            super_collection.get_absolute_url())
    ctx = {}
    products = filter(lambda product: product, [
        super_collection.best_seller_1,
        super_collection.best_seller_2,
        super_collection.best_seller_3,
        super_collection.best_seller_4,
        super_collection.best_seller_5,
        super_collection.best_seller_6,
    ])
    products_and_availability = list(products_with_availability(
        products, request.discounts, request.taxes,
        request.currency))
    json_ld_breadcrumbs = super_collection_breadcrumb_json_ld_list(
        super_collection)
    ctx.update({
        'super_collection': super_collection,
        'super_collections': SuperCollection.objects.public_roots_for_list(),
        'products': products_and_availability,
        'json_ld_breadcrumbs': list(map(json.dumps, json_ld_breadcrumbs))
    })
    return TemplateResponse(request, 'super_collections/super_collection.html',
                            ctx)


def super_collection_redirect(request, slug, pk):
    super_collections = super_collections_visible_to_user(request.user)
    super_collection = get_object_or_404(super_collections, id=pk)
    if not super_collection.custom_slug:
        return super_collection_index(request, slug, pk)
    else:
        return HttpResponsePermanentRedirect(
            super_collection.get_absolute_url())
