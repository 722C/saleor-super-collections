from django.http import HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from saleor.product.utils import products_with_availability

from .models import SuperCollection


def super_collections_visible_to_user(user):
    if user.is_authenticated and user.is_active and user.is_staff:
        return SuperCollection.objects.all()
    return SuperCollection.objects.public()


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
    ctx.update({'super_collection': super_collection,
                'super_collections': SuperCollection.objects.public_roots(),
                'products': products_and_availability})
    return TemplateResponse(request, 'super_collections/super_collection.html',
                            ctx)
