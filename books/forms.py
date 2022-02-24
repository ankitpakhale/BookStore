from django import forms
from .models import *



class FilterSearchForm(forms.Form):
    category = forms.ChoiceField(
        choices=[
            (category.cat_name)
            for category in Category.objects.all()
        ],
        label='CATEGORY',
        required=False
    )