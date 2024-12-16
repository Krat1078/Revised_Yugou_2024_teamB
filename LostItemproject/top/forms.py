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
        label="落とした物"
    )
    location_tag = forms.ModelChoiceField(
        queryset=PickedOrDroppedLocationsTag.objects.order_by("picked_or_dropped_location_name"), # 表示する順番をソートする
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False, 
        label="落とした場所"
    )

class DateFilterForm(forms.Form):
    date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date",'class': 'form-date'}),
        label="落とした日（選択した月日以降を表示）"
    )
