from django import forms
from django.utils.translation import gettext_lazy as _

from dcim.models import Site
from circuits.models import Provider
from utilities.forms.fields import SlugField
from utilities.forms.fields import DynamicModelChoiceField, CommentField
from netbox.forms import NetBoxModelFilterSetForm, NetBoxModelForm, NetBoxModelBulkEditForm

from ..models import *


__all__ = (
    'PhoneDeliveryForm',
    'PhoneDeliveryFilterForm',
    'PhoneDeliveryBulkEditForm',
)


class PhoneDeliveryFilterForm(NetBoxModelFilterSetForm):
    model = PhoneDelivery

    site_id = DynamicModelChoiceField(
        queryset=Site.objects.all(),
        required=False,
        label=_('Site')
    )
    delivery_id = forms.CharField(
        label=_('Delivery Method'),
        required=False
    )
    provider = forms.ModelChoiceField(
        required=False,
        queryset=Provider.objects.all(),
        label=_('Provider')
    )
    status = forms.ChoiceField(
        choices=PhoneDeliveryStatusChoices,
        required=False,
        label=_('Status')
    )


class PhoneDeliveryBulkEditForm(NetBoxModelBulkEditForm):
    model = PhoneDelivery

    site = forms.ModelChoiceField(
        queryset=Site.objects.all(),
        required=False,
        label=_('Site')
    )
    delivery = forms.CharField(
        required=False,
        label=_('Delivery Method'),
        help_text=_('SIP TRUNK, T0, T2, ...')
    )
    provider = forms.ModelChoiceField(
        queryset=Provider.objects.all(),
        required=False,
        label=_('Provider')
    )
    status = forms.ChoiceField(
        choices=PhoneDeliveryStatusChoices,
        required=False,
        label=_('Status')
    )

    class Meta:
        fields = ('site', 'delivery', 'provider', 'status', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'add_tags' in self.fields:
            del self.fields['add_tags']
        if 'remove_tags' in self.fields:
            del self.fields['remove_tags']


class PhoneDeliveryForm(NetBoxModelForm):
    '''
    creates a form for a Phone Delivery object
    '''
    site = forms.ModelChoiceField(
        required=True,
        queryset=Site.objects.all(),
        label=_('Site')
    )
    delivery = forms.CharField(
        required=True,
        label=_('Delivery Method'),
        help_text=_('SIP TRUNK, T0, T2, ...')
    )
    provider = forms.ModelChoiceField(
        required=True,
        queryset=Provider.objects.all(),
        label=_('Provider')
    )
    channel_count = forms.IntegerField(
        required=False,
        label=_('Channel Count'),
        help_text=_('G.711 cidec - 96kbps reserved bandwidth per channel')
    )
    status = forms.ChoiceField(
        choices=PhoneDeliveryStatusChoices,
        required=True,
        label=_('Status'),
    )
    ndi = forms.IntegerField(
        required=False,
        label=_('MBN / NDI'),
        help_text=_("Main Billing Number / Numéro de Désignation d'Installation - E164 format / NUMBER ONLY")
    )
    dto = forms.IntegerField(
        required=False,
        label=_('DTO'),
        help_text=_('E164 format / NUMBER ONLY')
    )
    comments = CommentField()

    class Meta:
        model = PhoneDelivery
        fields = ('site', 'delivery', 'provider', 'channel_count', 'status', 'ndi', 'dto', 'description', 'comments')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'tags' in self.fields:
            del self.fields['tags']
