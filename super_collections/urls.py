from django.conf.urls import url

from .dashboard_views import views as dashboard_views
from . import storefront_views as storefront_views

urlpatterns = [
    url(r'^super-collection/(?P<slug>[a-z0-9-_/]+?)-(?P<pk>[0-9]+)/$',
        storefront_views.super_collection_index,
        name='super-collection-detail'),

    url(r'^dashboard/super-collections/$',
        dashboard_views.super_collection_list,
        name='super-collection-dashboard-list'),
    url(r'^dashboard/super-collections/(?P<pk>[0-9]+)/$',
        dashboard_views.super_collection_details,
        name='super-collection-dashboard-detail'),
    url(r'^dashboard/super-collections/create/$',
        dashboard_views.super_collection_create,
        name='super-collection-dashboard-create'),
    url(r'^dashboard/super-collections/(?P<root_pk>[0-9]+)/create/$',
        dashboard_views.super_collection_create,
        name='super-collection-dashboard-create'),
    url(r'^dashboard/super-collections/(?P<pk>[0-9]+)/edit/$',
        dashboard_views.super_collection_edit,
        name='super-collection-dashboard-edit'),
    url(r'^dashboard/super-collections/(?P<pk>[0-9]+)/delete/$',
        dashboard_views.super_collection_delete,
        name='super-collection-dashboard-delete'),
    url(r'^dashboard/super-collections/(?P<pk>[0-9]+)/publish/$',
        dashboard_views.super_collection_toggle_is_published,
        name='super-collection-dashboard-publish'),
]
