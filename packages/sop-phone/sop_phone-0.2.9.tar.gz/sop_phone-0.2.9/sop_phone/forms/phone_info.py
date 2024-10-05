from django import forms
from django.utils.translation import gettext_lazy as _

from netbox.forms import NetBoxModelBulkEditForm, NetBoxModelForm, NetBoxModelFilterSetForm
from utilities.forms.fields import DynamicModelChoiceField
from dcim.models import Site

from ..models import PhoneInfo, PhoneMaintainer


__all__ = (
    'PhoneInfoForm',
    'PhoneInfoFilterForm',
    'PhoneInfoBulkEditForm',
)


class PhoneInfoFilterForm(NetBoxModelFilterSetForm):
    model = PhoneInfo
    site_id = DynamicModelChoiceField(
        queryset=Site.objects.all(),
        required=False,
        label=_('Site')
    )
    maintainer_id = DynamicModelChoiceField(
        queryset=PhoneMaintainer.objects.all(),
        required=False,
        label=_('Maintainer'),
    )


class PhoneInfoForm(NetBoxModelForm):

    site = forms.ModelChoiceField(
        queryset=Site.objects.all(),
        required=False,
        label=_('Site')
    )
    maintainer = forms.ModelChoiceField(
        queryset=PhoneMaintainer.objects.all(),
        required=False,
        label=_('Maintainer')
    )

    class Meta:
        model = PhoneInfo
        fields = ('site', 'maintainer', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if 'tags' in self.fields:
            del self.fields['tags']


class PhoneInfoBulkEditForm(NetBoxModelBulkEditForm):
    model = PhoneInfo
    maintainer = forms.ModelChoiceField(
        queryset=PhoneMaintainer.objects.all(),
        required=False,
        label=_('Maintainer')
    )

    class Meta:
        fields = ('maintainer', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'add_tags' in self.fields:
            del self.fields['add_tags']
        if 'remove_tags' in self.fields:
            del self.fields['remove_tags']
