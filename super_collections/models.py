from django.db import models
from django.urls import reverse
from django.utils.translation import pgettext_lazy

from mptt.managers import TreeManager
from mptt.models import MPTTModel

from versatileimagefield.fields import VersatileImageField

from saleor.core.permissions import MODELS_PERMISSIONS
from saleor.seo.models import SeoModel


# Add in the permissions specific to our models.
MODELS_PERMISSIONS += [
    'super_collections.view',
    'super_collections.edit'
]


class SuperCollectionQuerySet(models.QuerySet):
    def public(self):
        return self.filter(is_published=True)

    def public_roots(self):
        return self.filter(is_published=True, parent__isnull=True)


class SuperCollection(MPTTModel, SeoModel):
    parent = models.ForeignKey(
        'self', null=True, blank=True, related_name='children',
        on_delete=models.CASCADE)
    collections = models.ManyToManyField(
        'product.Collection',
        related_name='super_collections', blank=True)
    name = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(max_length=128)

    background_image = VersatileImageField(
        upload_to='super-collection-backgrounds', blank=True, null=True)
    is_published = models.BooleanField(default=False)

    alternative_name = models.CharField(max_length=255, blank=True)
    content = models.TextField(help_text=pgettext_lazy(
        'Collection extension', 'CMS-able content.'), blank=True)
    added = models.DateTimeField(auto_now_add=True)

    objects = SuperCollectionQuerySet.as_manager()
    tree = TreeManager()

    class Meta:
        app_label = 'super_collections'
        ordering = ['pk']

        permissions = (
            ('view', pgettext_lazy('Permission description',
                                   'Can view super collections')
             ),
            ('edit', pgettext_lazy('Permission description',
                                   'Can edit super collections')))

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            'super-collection-detail',
            kwargs={'pk': self.id, 'slug': self.slug})

    def get_full_path(self, ancestors=None):
        if not self.parent_id:
            return self.slug
        if not ancestors:
            ancestors = self.get_ancestors()
        nodes = [node for node in ancestors] + [self]
        return '/'.join([node.slug for node in nodes])

    def published_children(self):
        return self.children.filter(is_published=True)

    def published_collections(self):
        return self.collections.filter(is_published=True)
