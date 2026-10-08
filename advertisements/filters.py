from django_filters import rest_framework as filters

from advertisements.models import Advertisement


class AdvertisementFilter(filters.FilterSet):
    created_at = filters.DateFromToRangeFilter()
    status = filters.ChoiceFilter(choices=Advertisement.STATUS_CHOICES)

    class Meta:
        model = Advertisement
        fields = ['status', 'created_at']