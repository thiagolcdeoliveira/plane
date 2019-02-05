
from django.conf.urls import url, include

from planeapp.views.pedido import PedidoCreateView, AjaxPedidoCreateView, PedidoAtivoPorUsuarioListView
from planeapp.views.produto import ProdutoListView

urlpatterns=[
    url(r'^$', ProdutoListView.as_view(), name='produto-list'),
    url(r'^$', PedidoCreateView.as_view(), name='pedido-add'),
    url(r'pedido/produto/(?P<id>[\d\-]+)/$', AjaxPedidoCreateView.as_view(), name='pedido-produto-add'),
    url(r'carrinho/$', PedidoAtivoPorUsuarioListView.as_view(), name='carrinho-list'),
]