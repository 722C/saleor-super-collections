from django.http import HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from .models import SuperCollection


def super_collections_visible_to_user(user):
    if user.is_authenticated and user.is_active and user.is_staff:
        return SuperCollection.objects.all()
    return SuperCollection.objects.public()


def super_collection_index(request, slug, pk):
    super_collections = super_collections_visible_to_user(request.user)
    super_collection = get_object_or_404(super_collections, id=pk)
    if super_collection.slug != slug:
        return HttpResponsePermanentRedirect(super_collection.get_absolute_url())
    ctx = {}
    ctx.update({'super_collection': super_collection})
    return TemplateResponse(request, 'super_collections/super_collection.html', ctx)
