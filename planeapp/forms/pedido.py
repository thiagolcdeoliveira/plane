# -*- coding: utf-8 -*-
from django.forms import forms, ModelForm, CharField, HiddenInput

from planeapp.models.pedido import Pedido
from planeapp.models.produto import Produto


class PedidoForm(ModelForm):
    # produto = CharField(widget=HiddenInput())

    class Meta:
        model = Pedido
        # fields = "__all__"
        fields = ('preco_unit','quantidade',)

    def __init__(self, *args, **kwargs):
        produto_id = kwargs.pop('id')
        print(produto_id)
        produto = Produto.objects.get(id=produto_id)

        super(PedidoForm, self).__init__(*args, **kwargs)
        # self.fields['produto'].queryset = Produto.objects.filter(id=produto_id)
        self.fields['quantidade'].initial = produto.multiplo
        self.fields['preco_unit'].initial = produto.preco_unit