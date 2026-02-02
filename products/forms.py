from django import forms
from .models import Product, Store


class ProductForms(forms.ModelForm):
    class Meta:
        model = Product

        fields = ['name', 'url', 'store', 'target_price']
        widgets = {
            "name": forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Например: IPone 17'}),
            'url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Например: https://...'}),
            'store': forms.Select(attrs={'class': 'form-control'}),
            'target_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder':' Например: желаемая цена'})

        }

