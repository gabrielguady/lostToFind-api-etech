from django_filters import filterset
from django.db.models import Q
from django_filters import rest_framework as filters

from core import models

LIKE = 'unaccent__icontains'
ICONTAINS = 'icontains'
EQUALS = 'exact'
STARTS_WITH = 'startswith'
GT = 'gt'
GTE = 'gte'

class LostItemFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr=ICONTAINS)
    last_seen_details = filters.CharFilter(lookup_expr=ICONTAINS)
    city = filters.CharFilter(lookup_expr=ICONTAINS)
    category_name = filters.CharFilter(field_name='category__name',lookup_expr=ICONTAINS)

    class Meta:
        model = models.LostItem
        fields = ['last_seen_details', 'title', 'category_name', 'city']


class FoundItemFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr=ICONTAINS)
    description = filters.CharFilter(lookup_expr=ICONTAINS)
    category_name = filters.CharFilter(field_name='category__name', lookup_expr=ICONTAINS)
    city = filters.CharFilter(lookup_expr=ICONTAINS)
    id_user = filters.NumberFilter(lookup_expr=EQUALS)

    class Meta:
        model = models.FoundItem
        fields = ['title', 'description', 'category_name', 'city', 'id_user']

class ItemCategoryFilter(filters.FilterSet):
    items = filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = models.Category
        fields = ['items']

