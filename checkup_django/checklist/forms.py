# checklist/forms.py

from django import forms
from django.forms import inlineformset_factory
from .models import Checklist, CheckItem

class CheckItemForm(forms.ModelForm):
    class Meta:
        model = CheckItem
        fields = ['id', 'nom', 'statut', 'commentaire']
        widgets = {
            'id': forms.HiddenInput(),
            'nom': forms.HiddenInput(),
            'statut': forms.Select(attrs={
                'class': 'form-select statut-select',
                'data-field': 'statut'
            }),
            'commentaire': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2
            }),
        }
        labels = {
            'statut': 'Statut',
            'commentaire': 'Commentaire',
        }

CheckItemFormSet = inlineformset_factory(
    parent_model=Checklist,
    model=CheckItem,
    form=CheckItemForm,
    extra=0,
    can_delete=False,
)
