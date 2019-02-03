# -*- coding: utf-8 -*-
from django.forms import forms

from planeapp.models.cliente import Cliente


class ClienteForm(forms.Form):

    class Meta:
        model = Cliente
        fields = "__all__"
