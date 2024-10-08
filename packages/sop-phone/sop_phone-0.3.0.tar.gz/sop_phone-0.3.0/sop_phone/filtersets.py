import django_filters
from django.db.models import Q
from django.utils.translation import gettext_lazy as _ 

from netbox.filtersets import NetBoxModelFilterSet
from dcim.models import Site

from .models import *
from .validators import number_quicksearch


__all__ = (
    'PhoneDeliveryFilterSet',
    'PhoneInfoFilterSet',
    'PhoneMaintainerFilterSet',
    'PhoneDIDFilterSet',
)


#_________________________
# Phone Delivery Filters

class PhoneDeliveryFilterSet(NetBoxModelFilterSet):
    status = django_filters.MultipleChoiceFilter(
        choices=PhoneDeliveryStatusChoices,
        null_value=None
    )
    site_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Site.objects.all(),
        field_name='site',
        label=_('Site (ID)')
    )
    site_name = django_filters.CharFilter(
        field_name='site__name',
        label=_('Site (name)')
    )
    maintainer_id = django_filters.ModelMultipleChoiceFilter(
        queryset=PhoneMaintainer.objects.all(),
        method='search_maintainer_id',
        label=_('Maintainer (ID)')
    )
    maintainer_name = django_filters.CharFilter(
        method='search_maintainer_name',
        label=_('Maintainer (name')
    )

    class Meta:
        model = PhoneDelivery
        fields = ('id', 'delivery', 'provider', 'status', 'channel_count', 'ndi', 'dto')

    def search_maintainer_id(self, queryset, name, value):
        if not value:
            return queryset
        try:
            site_ids = PhoneInfo.objects.filter(maintainer__in=value).values_list('site__id', flat=True )
            return queryset.filter(site__id__in=site_ids)
        except:return queryset

    def search_maintainer_name(self, queryset, name, value):
        if not value:
            return queryset
        try:
            maintainer_ids = PhoneMaintainer.objects.filter(name=value).values_list('id', flat=True)
            site_ids = PhoneInfo.objects.filter(maintainer__in=maintainer_ids).values_list('site__id', flat=True)
            return queryset.filter(site__id__in=site_ids)
        except:return queryset

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(delivery__icontains=value) |
            Q(provider__name__icontains=value) |
            Q(dto__icontains=value) |
            Q(ndi__icontains=value)
        )


#_________________________
# Informations filters

class PhoneInfoFilterSet(NetBoxModelFilterSet):

    site_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Site.objects.all(),
        field_name='site__id',
        method='search_site_id',
        label=_('Site (ID)')
    )
    site_name = django_filters.CharFilter(
        field_name='site__name',
        label=_('Site (name)')
    )
    maintainer_id = django_filters.ModelMultipleChoiceFilter(
        queryset=PhoneMaintainer.objects.all(),
        field_name='maintainer',
        label=_('Maintainer (ID)')
    )
    maintainer_name = django_filters.CharFilter(
        field_name='maintainer__name',
        label=_('Maintainer (name)')
    )

    class Meta:
        model = PhoneInfo
        fields = ('id', 'site', 'site_id', 'site_name', 'maintainer',)

    def search_site_id(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(site__in=value)


#_________________________
# Maintainers filter

class PhoneMaintainerFilterSet(NetBoxModelFilterSet):
    status = django_filters.MultipleChoiceFilter(
        choices=PhoneMaintainerStatusChoice,
        null_value=None
    )
    site_name = django_filters.CharFilter(
        method='search_site_name',
        label=_('Site (name)')
    )
    site_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Site.objects.all(),
        method='search_site_id',
        label=_('Site (ID)')
    )

    class Meta:
        model = PhoneMaintainer
        fields = ('id', 'name', 'status')

    def search_site_name(self, queryset, name, value):
        if not value:
            return queryset
        try:
            maintainer_id = PhoneInfo.objects.filter(site__in=Site.objects.filter(name=value)).values_list('maintainer_id', flat=True)
            return queryset.filter(pk__in=maintainer_id)
        except:return queryset

    def search_site_id(self, queryset, name, value):
        if not value:
            return queryset
        try:
            maintainer_id = PhoneInfo.objects.filter(site__in=value).values_list('maintainer_id', flat=True)
            return queryset.filter(pk__in=maintainer_id)
        except:return queryset

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value)
        )


#_________________________
# DID filters (DIDs)

class PhoneDIDFilterSet(NetBoxModelFilterSet):
    site_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Site.objects.all(),
        field_name='site',
        label=_('Site (ID)')
    )
    site_name = django_filters.CharFilter(
        field_name='site__name',
        label=_('Site (name)')
    )
    maintainer_id = django_filters.ModelMultipleChoiceFilter(
        queryset=PhoneMaintainer.objects.all(),
        field_name='site',
        method='did_maintainer_filter',
        label=_('Maintainer (ID)')
    )
    maintainer_name = django_filters.CharFilter(
        method='did_maintainer_name_filter',
        label=_('Maintainer (name)')
    )
    delivery_id = django_filters.ModelMultipleChoiceFilter(
        queryset=PhoneDelivery.objects.all(),
        field_name='delivery',
        label=_('Delivery (ID)')
    )
    partial_number = django_filters.NumberFilter(
        label=_('Partial number'),
        method='search_partial_number'
    )

    class Meta:
        model = PhoneDID
        fields = ('id', 'start', 'end', 'site', 'delivery_id')

    def search_partial_number(self, queryset, name, value):
        if not value:
            return queryset

        valid_ids: list[int] = []

        for rng in queryset:
            if number_quicksearch(rng.start, rng.end, str(value)):
                valid_ids.append(rng.id)

        return queryset.filter(id__in=valid_ids)

    def did_maintainer_name_filter(self, queryset, name, value):
        if not value:
            return queryset
        try:
            site_ids = PhoneInfo.objects.filter(maintainer__name=value).values_list('site_id', flat=True)
            return queryset.filter(site_id__in=site_ids)
        except:return queryset

    def did_maintainer_filter(self, queryset, name, value):
        if not value:
            return queryset
        try:
            site_ids = PhoneInfo.objects.filter(maintainer__in=value).values_list('site_id', flat=True)
            return queryset.filter(site_id__in=site_ids)
        except:return queryset

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(start__icontains=value) |
            Q(end__icontains=value) |
            Q(site__name__icontains=value) |
            Q(delivery__delivery__icontains=value) |
            Q(delivery__provider__name__icontains=value)
        )
