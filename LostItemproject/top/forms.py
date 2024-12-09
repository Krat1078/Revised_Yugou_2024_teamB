from django import forms
from .models import ItemsNameTag, PickedOrDroppedLocationsTag

class TagFilterForm(forms.Form):
    itemname_tag = forms.ModelChoiceField(
        queryset=ItemsNameTag.objects.all(), 
        required=False,
        label="落とした物"
    )
    location_tag = forms.ModelChoiceField(
        queryset=PickedOrDroppedLocationsTag.objects.all(), 
        required=False,
        label="落とした場所"
    )

class DateFilterForm(forms.Form):
    date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
        label="落とした日（選択した月日以降を表示）"
    )
