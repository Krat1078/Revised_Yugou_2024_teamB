from django import forms
from .models import ItemsNameTag, PickedOrDroppedLocationsTag

# class TagFilterForm(forms.Form):
#     itemname_tag = forms.ModelChoiceField(
#         queryset=ItemsNameTag.objects.all(), 
#         widget=forms.Select(attrs={'class': 'form-select'}),
#         required=False,
#         label="落としたもの",
#     )
#     location_tag = forms.ModelChoiceField(
#         queryset=PickedOrDroppedLocationsTag.objects.all(), 
#         required=False,
#         label="落とした場所"
#     )

class TagFilterForm(forms.Form):
    itemname_tag = forms.ModelChoiceField(
        queryset=ItemsNameTag.objects.all(), 
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False,
        label="落としたもの"
    )
    location_tag = forms.ModelChoiceField(
        queryset=PickedOrDroppedLocationsTag.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False, 
    )

class DateFilterForm(forms.Form):
    date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
        label="落とした日"
    )
