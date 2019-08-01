from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import Case, When, Value, Q
from django.urls import reverse, get_script_prefix
from django.utils.encoding import iri_to_uri
from django.utils.translation import pgettext_lazy

from mptt.managers import TreeManager
from mptt.models import MPTTModel

from versatileimagefield.fields import VersatileImageField

from saleor.core.permissions import MODELS_PERMISSIONS
from saleor.core.models import SortableModel
from saleor.product.models import Collection
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

    def public_roots_for_list(self):
        return self.filter(is_published=True, parent__isnull=True,
                           show_in_root_list=True)


class SuperCollection(MPTTModel, SeoModel, SortableModel):
    parent = models.ForeignKey(
        'self', null=True, blank=True, related_name='children',
        on_delete=models.CASCADE)
    appears_in = models.ManyToManyField(
        'self', blank=True, related_name='step_children', symmetrical=False)
    collections = models.ManyToManyField(
        'product.Collection',
        related_name='super_collections', blank=True)
    collection_ordering = ArrayField(
        models.PositiveIntegerField(), blank=True, default=list)
    name = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(max_length=128)
    sort_order = models.PositiveIntegerField(default=100)

    background_image = VersatileImageField(
        upload_to='super-collection-backgrounds', blank=True, null=True)
    is_published = models.BooleanField(default=False)
    show_in_root_list = models.BooleanField(default=False)
    show_children_in_side_nav = models.BooleanField(default=False)

    hide_sidebar = models.BooleanField(default=False)

    show_collections = models.BooleanField(default=False)

    alternative_name = models.CharField(max_length=255, blank=True)
    subheader = models.CharField(max_length=255, blank=True)
    content = models.TextField(help_text=pgettext_lazy(
        'Collection extension', 'CMS-able content.'), blank=True)
    added = models.DateTimeField(auto_now_add=True)

    objects = SuperCollectionQuerySet.as_manager()
    tree = TreeManager()

    custom_slug = models.SlugField(max_length=128, unique=True, null=True)

    main_picture_1 = models.ImageField(blank=True, null=True)
    main_picture_2 = models.ImageField(blank=True, null=True)
    main_picture_3 = models.ImageField(blank=True, null=True)

    main_picture_1_to_3_box_header_picture = models.ImageField(
        blank=True, null=True)
    main_picture_1_to_3_box_header_text = models.CharField(
        max_length=200, blank=True)
    main_picture_1_to_3_box_subheader_text = models.CharField(
        max_length=200, blank=True)
    main_picture_1_to_3_box_text = models.CharField(max_length=200, blank=True)
    main_picture_1_to_3_box_button_text = models.CharField(
        max_length=200, blank=True)
    main_picture_1_to_3_link = models.CharField(max_length=200, blank=True)

    popular_collection_1 = models.ImageField(blank=True, null=True)
    popular_collection_1_text = models.CharField(max_length=200, blank=True)
    popular_collection_1_link = models.CharField(max_length=200, blank=True)

    popular_collection_2 = models.ImageField(blank=True, null=True)
    popular_collection_2_text = models.CharField(max_length=200, blank=True)
    popular_collection_2_link = models.CharField(max_length=200, blank=True)

    popular_collection_3 = models.ImageField(blank=True, null=True)
    popular_collection_3_text = models.CharField(max_length=200, blank=True)
    popular_collection_3_link = models.CharField(max_length=200, blank=True)

    popular_collection_4 = models.ImageField(blank=True, null=True)
    popular_collection_4_text = models.CharField(max_length=200, blank=True)
    popular_collection_4_link = models.CharField(max_length=200, blank=True)

    popular_collection_5 = models.ImageField(blank=True, null=True)
    popular_collection_5_text = models.CharField(max_length=200, blank=True)
    popular_collection_5_link = models.CharField(max_length=200, blank=True)

    main_picture_4 = models.ImageField(blank=True, null=True)

    main_picture_4_box_header_picture = models.ImageField(
        blank=True, null=True)
    main_picture_4_box_header_text = models.CharField(
        max_length=200, blank=True)
    main_picture_4_box_text = models.CharField(max_length=200, blank=True)
    main_picture_4_box_button_text = models.CharField(
        max_length=200, blank=True)
    main_picture_4_link = models.CharField(max_length=200, blank=True)

    best_seller_1 = models.ForeignKey(
        'product.Product', blank=True, null=True, on_delete=models.SET_NULL,
        related_name='+')
    best_seller_2 = models.ForeignKey(
        'product.Product', blank=True, null=True, on_delete=models.SET_NULL,
        related_name='+')
    best_seller_3 = models.ForeignKey(
        'product.Product', blank=True, null=True, on_delete=models.SET_NULL,
        related_name='+')
    best_seller_4 = models.ForeignKey(
        'product.Product', blank=True, null=True, on_delete=models.SET_NULL,
        related_name='+')
    best_seller_5 = models.ForeignKey(
        'product.Product', blank=True, null=True, on_delete=models.SET_NULL,
        related_name='+')
    best_seller_6 = models.ForeignKey(
        'product.Product', blank=True, null=True, on_delete=models.SET_NULL,
        related_name='+')

    previous_picture = models.ImageField(blank=True, null=True)
    previous_picture_text = models.CharField(max_length=200, blank=True)
    previous_picture_link = models.CharField(max_length=200, blank=True)

    next_picture = models.ImageField(blank=True, null=True)
    next_picture_text = models.CharField(max_length=200, blank=True)
    next_picture_link = models.CharField(max_length=200, blank=True)

    class Meta:
        app_label = 'super_collections'
        ordering = ['sort_order']

        permissions = (
            ('view', pgettext_lazy('Permission description',
                                   'Can view super collections')
             ),
            ('edit', pgettext_lazy('Permission description',
                                   'Can edit super collections')))

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        if not self.custom_slug:
            return reverse(
                'super-collection-detail',
                kwargs={'pk': self.id, 'slug': self.slug})
        else:
            # Handle script prefix manually because we bypass reverse()
            return iri_to_uri(get_script_prefix() +
                              self.custom_slug)

    def get_full_path(self, ancestors=None):
        if not self.parent_id:
            return self.slug
        if not ancestors:
            ancestors = self.get_ancestors()
        nodes = [node for node in ancestors] + [self]
        return '/'.join([node.slug for node in nodes])

    def published_children(self):
        if not self.pk:
            return SuperCollection.objects.none()
        return SuperCollection.objects.filter(Q(parent=self) | Q(appears_in=self), is_published=True).distinct()

    def published_collections(self):
        return self.sorted_collections.filter(is_published=True)

    def get_ordering_queryset(self):
        return self.published_children()

    @property
    def menu_item(self):
        from saleor.menu.models import MenuItem
        return MenuItem.objects.filter(Q(supercollection=self) | Q(url__icontains=self.get_absolute_url())).first()

    @property
    def preserved_order(self):
        return Case(
            When(pk=0, then=0),
            *[When(pk=pk, then=pos) for pos, pk in enumerate(
                self.collection_ordering)],
            default=Value(0),
            output_field=models.PositiveIntegerField()
        )

    @property
    def sorted_collections(self):
        if not self.pk:
            return Collection.objects.none()
        return self.collections.annotate(
            preserved=self.preserved_order).order_by('preserved', 'pk')
