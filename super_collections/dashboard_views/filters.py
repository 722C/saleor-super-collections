from django import forms
from django.utils.translation import npgettext, pgettext_lazy
from django_filters import (CharFilter, OrderingFilter, ChoiceFilter)

from saleor.core.filters import SortedFilterSet

from ..models import SuperCollection

SORT_BY_FIELDS = {
    'name': pgettext_lazy('SuperCollection list sorting option', 'name')}

PUBLISHED_CHOICES = (
    ('1', pgettext_lazy('Is publish filter choice', 'Published')),
    ('0', pgettext_lazy('Is publish filter choice', 'Not published')))


class SuperCollectionFilter(SortedFilterSet):
    name = CharFilter(
        label=pgettext_lazy('SuperCollection list name filter label', 'Name'),
        lookup_expr='icontains')
    is_published = ChoiceFilter(
        label=pgettext_lazy(
            'SuperCollection list filter label', 'Is published'),
        choices=PUBLISHED_CHOICES,
        empty_label=pgettext_lazy('Filter empty choice label', 'All'),
        widget=forms.Select)
    sort_by = OrderingFilter(
        label=pgettext_lazy(
            'SuperCollection list sorting filter label', 'Sort by'),
        fields=SORT_BY_FIELDS.keys(),
        field_labels=SORT_BY_FIELDS)

    class Meta:
        model = SuperCollection
        fields = []

    def get_summary_message(self):
        counter = self.qs.count()
        return npgettext(
            'Number of matching records in the dashboard super collections list',
            'Found %(counter)d matching super collection',
            'Found %(counter)d matching super collections',
            number=counter) % {'counter': counter}
