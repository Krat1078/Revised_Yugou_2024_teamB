from django import forms
from .models import ItemsNameTag, PickedOrDroppedLocationsTag

class TagFilterForm(forms.Form):
    itemname_tag = forms.ModelChoiceField(queryset=ItemsNameTag.objects.all(), required=False)
    location_tag = forms.ModelChoiceField(queryset=PickedOrDroppedLocationsTag.objects.all(), required=False)
