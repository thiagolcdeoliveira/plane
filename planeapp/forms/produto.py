# -*- coding: utf-8 -*-
from django.forms import forms

from planeapp.models.produto import Produto


class ClienteForm(forms.Form):
    
    class Meta:
        model = Produto
        fields="__all__"
