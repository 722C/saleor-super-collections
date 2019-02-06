from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.utils.translation import pgettext_lazy
from django.views.decorators.http import require_POST

from saleor.core.utils import get_paginator_items
from saleor.dashboard.views import staff_member_required
from .filters import SuperCollectionFilter
from .forms import SuperCollectionForm

from ..models import SuperCollection


@staff_member_required
@permission_required('super_collections.view')
def super_collection_list(request):
    super_collections = SuperCollection.tree.root_nodes().order_by('name')
    super_collection_filter = SuperCollectionFilter(
        request.GET, queryset=super_collections)
    super_collections = get_paginator_items(
        super_collection_filter.qs, settings.DASHBOARD_PAGINATE_BY,
        request.GET.get('page'))
    # Call this so that cleaned_data exists on the filter_set
    super_collection_filter.form.is_valid()
    ctx = {
        'super_collections': super_collections, 'filter_set': super_collection_filter,
        'is_empty': not super_collection_filter.queryset.exists()}
    return TemplateResponse(request, 'super_collections/dashboard/list.html', ctx)


@staff_member_required
@permission_required('super_collections.edit')
def super_collection_create(request, root_pk=None):
    path = None
    super_collection = SuperCollection()
    if root_pk:
        root = get_object_or_404(SuperCollection, pk=root_pk)
        path = root.get_ancestors(include_self=True) if root else []
    form = SuperCollectionForm(
        request.POST or None, request.FILES or None, parent_pk=root_pk)
    if form.is_valid():
        super_collection = form.save()
        messages.success(
            request,
            pgettext_lazy(
                'Dashboard message', 'Added super collection %s') % super_collection)
        if root_pk:
            return redirect('super-collection-dashboard-detail', pk=root_pk)
        return redirect('super-collection-dashboard-list')
    ctx = {'super_collection': super_collection, 'form': form, 'path': path}
    return TemplateResponse(request, 'super_collections/dashboard/form.html', ctx)


@staff_member_required
@permission_required('super_collections.edit')
def super_collection_edit(request, pk=None):
    path = None
    super_collection = get_object_or_404(SuperCollection, pk=pk)
    if pk:
        root = get_object_or_404(SuperCollection, pk=pk)
        path = root.get_ancestors(include_self=True) if root else []
    form = SuperCollectionForm(
        request.POST or None, request.FILES or None, instance=super_collection,
        parent_pk=super_collection.parent_id)
    status = 200
    if form.is_valid():
        super_collection = form.save()
        messages.success(
            request,
            pgettext_lazy(
                'Dashboard message', 'Updated super collection %s') % super_collection)
        if pk:
            return redirect('super-collection-dashboard-detail', pk=pk)
        return redirect('super-collection-dashboard-list')
    elif form.errors:
        status = 400
    ctx = {'super_collection': super_collection,
           'form': form, 'status': status, 'path': path}
    template = 'super_collections/dashboard/form.html'
    return TemplateResponse(request, template, ctx, status=status)


@staff_member_required
@permission_required('super_collections.view')
def super_collection_details(request, pk):
    root = get_object_or_404(SuperCollection, pk=pk)
    path = root.get_ancestors(include_self=True) if root else []
    super_collections = root.get_children().order_by('name')
    super_collections_filter = SuperCollectionFilter(
        request.GET, queryset=super_collections)
    super_collections = get_paginator_items(
        super_collections_filter.qs, settings.DASHBOARD_PAGINATE_BY,
        request.GET.get('page'))
    ctx = {'super_collections': super_collections, 'path': path, 'root': root,
           'filter_set': super_collections_filter,
           'is_empty': not super_collections_filter.queryset.exists()}
    return TemplateResponse(request, 'super_collections/dashboard/detail.html', ctx)


@staff_member_required
@permission_required('super_collections.edit')
def super_collection_delete(request, pk):
    super_collection = get_object_or_404(SuperCollection, pk=pk)
    if request.method == 'POST':
        super_collection.delete()
        messages.success(
            request,
            pgettext_lazy(
                'Dashboard message', 'Removed super collection %s') % super_collection)
        root_pk = None
        if super_collection.parent:
            root_pk = super_collection.parent.pk
        if root_pk:
            if request.is_ajax():
                response = {'redirectUrl': reverse(
                    'super-collection-dashboard-detail', kwargs={'pk': root_pk})}
                return JsonResponse(response)
            return redirect('super-collection-dashboard-detail', pk=root_pk)
        else:
            if request.is_ajax():
                response = {'redirectUrl': reverse(
                    'super-collection-dashboard-list')}
                return JsonResponse(response)
            return redirect('super-collection-dashboard-list')
    ctx = {'super_collection': super_collection,
           'descendants': list(super_collection.get_descendants())}
    return TemplateResponse(
        request, 'super_collections/dashboard/modal/confirm_delete.html', ctx)


@require_POST
@staff_member_required
@permission_required('super_collections.edit')
def super_collection_toggle_is_published(request, pk):
    super_collection = get_object_or_404(SuperCollection, pk=pk)
    super_collection.is_published = not super_collection.is_published
    super_collection.save(update_fields=['is_published'])
    return JsonResponse(
        {'success': True, 'is_published': super_collection.is_published})
