# -*- coding: utf-8 -*-
from django.forms import forms, ModelForm, CharField, HiddenInput, IntegerField, DecimalField

from planeapp.models.pedido import Pedido
from planeapp.models.produto import Produto


class PedidoForm(ModelForm):
    # produto = CharField(widget=HiddenInput())
    quantidade = IntegerField(min_value=1,label="Quantidade", help_text="Você deve colocar a quantidade desse produto que deseja.")
    preco_unit = DecimalField(min_value=0,label="Preço Unitário", help_text="Valor que deseja pagar por unidade.")

    class Meta:
        model = Pedido
        # fields = "__all__"
        fields = ('preco_unit','quantidade',)
    def clean_preco_unit(self):
        valor = self.cleaned_data.get("preco_unit")
        if  valor >= self.produto.preco_unit:
            return valor
        else:
            raise forms.ValidationError("Esse produto deve ser vendido igual ou acima de  R$ %s" % self.produto.preco_unit)

    def clean_quantidade(self):
        quantidade = self.cleaned_data.get("quantidade")
        if quantidade % self.produto.multiplo == 0 :
            return quantidade
        else:
            raise forms.ValidationError("Esse produto só pode ser vendido por multiplos de %s" %self.produto.multiplo)

    def __init__(self, *args, **kwargs):
        produto_id = kwargs.pop('id')
        print(produto_id)
        self.produto = Produto.objects.get(id=produto_id)
        super(PedidoForm, self).__init__(*args, **kwargs)
        # self.fields['produto'].queryset = Produto.objects.filter(id=produto_id)
        self.fields['quantidade'].initial = self.produto.multiplo
        self.fields['preco_unit'].initial = self.produto.preco_unit