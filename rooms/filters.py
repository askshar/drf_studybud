import django_filters

from .models import Room


class RoomFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    topic = django_filters.CharFilter(field_name='topic__name', lookup_expr='icontains')
    host = django_filters.CharFilter(field_name='host__username', lookup_expr='icontains')

    class Meta:
        model = Room
        fields = ('name', 'topic', 'host')