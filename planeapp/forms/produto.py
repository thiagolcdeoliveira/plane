# -*- coding: utf-8 -*-
from django.forms import forms, ModelForm

from planeapp.models.produto import Produto


class ProdutoForm(ModelForm):
    
    class Meta:
        model = Produto
        fields="__all__"

    def clean_multiplo(self):
        if self.cleaned_data["multiplo"] >=1:
            return self.cleaned_data["multiplo"]
        else:
            raise forms.ValidationError("O multiplo deve ser maior que 0")
