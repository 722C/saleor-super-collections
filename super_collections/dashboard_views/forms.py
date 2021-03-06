from django import forms
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.utils.text import slugify
from django.utils.translation import pgettext_lazy

from text_unidecode import unidecode

from saleor.product.models import Collection
from saleor.dashboard.product.forms import RichTextField
from saleor.dashboard.seo.fields import SeoDescriptionField, SeoTitleField
from ..models import SuperCollection


class SuperCollectionForm(forms.ModelForm):

    content = RichTextField()

    class Meta:
        model = SuperCollection
        exclude = ['slug']
        labels = {
            'name': pgettext_lazy('Item name', 'Name'),
            'collections': pgettext_lazy('Collections selection', 'Collections'),
            'background_image': pgettext_lazy(
                'Collections selection',
                'Background Image'),
            'is_published': pgettext_lazy(
                'Collection published toggle',
                'Published')}

    def __init__(self, *args, **kwargs):
        self.parent_pk = kwargs.pop('parent_pk')
        super().__init__(*args, **kwargs)
        self.fields['seo_description'] = SeoDescriptionField()
        self.fields['seo_title'] = SeoTitleField(
            extra_attrs={'data-bind': self['name'].auto_id})

    def save(self, commit=True):
        self.instance.slug = slugify(unidecode(self.instance.name))
        if self.parent_pk:
            self.instance.parent = get_object_or_404(
                SuperCollection, pk=self.parent_pk)
        return super().save(commit=commit)
