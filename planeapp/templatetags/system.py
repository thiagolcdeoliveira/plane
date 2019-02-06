from django import template
from planeapp.models.pedido import Pedido

register = template.Library()

@register.filter(name='multiplica')
def multiplica(valor_unit,multiplo):
    return valor_unit * multiplo

@register.filter(name='carrinho')
def carrinho(user):
   return Pedido.objects.filter(desativado=False,finalizado=False,cliente__username=user).count()

@register.filter(name='valorizacao')
def valorizacao(id):
    pedido = Pedido.objects.get(id=id)
    return pedido.preco_unit > pedido.produto.preco_unit