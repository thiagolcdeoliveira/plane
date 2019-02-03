# -*- coding: utf-8 -*-
from django.forms import forms

from planeapp.models.pedido import Pedido


class ClienteForm(forms.Form):

    class Meta:
        model = Pedido
        fields="__all__"
