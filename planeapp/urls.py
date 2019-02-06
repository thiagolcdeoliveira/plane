
from django.conf.urls import url, include

from planeapp.views.cliente import ClienteCreateView, ClienteDetailView
from planeapp.views.pedido import PedidoCreateView, AjaxPedidoCreateView, PedidoAtivoPorUsuarioListView, \
    PedidoDeleteView, PedidoFinalizarView, PedidoLimparView, PedidoComprarView, AjaxPedidoUpdateView, PedidoListView
from planeapp.views.produto import ProdutoListView

urlpatterns=[
    url(r'^$', ProdutoListView.as_view(), name='home'),
    url(r'produto/listar$', ProdutoListView.as_view(), name='produto-list'),
    # url(r'^$', PedidoCreateView.as_view(), name='pedido-add'),
    url(r'pedido/produto/(?P<id>[\d\-]+)/$', AjaxPedidoCreateView.as_view(), name='pedido-produto-add'),
    url(r'pedido/(?P<id>[\d\-]+)/editar$', AjaxPedidoUpdateView.as_view(), name='pedido-editar'),
    url(r'carrinho/$', PedidoAtivoPorUsuarioListView.as_view(), name='carrinho-list'),
    url(r'carrinho/produto/(?P<pk>[\d\-]+)/excluir$', PedidoDeleteView.as_view(), name='carrinho-produto-excluir'),
    url(r'carrinho/finalizar/$', PedidoFinalizarView.as_view(), name='carrinho-finalizar'),
    url(r'carrinho/limpar/$', PedidoLimparView.as_view(), name='carrinho-limpar'),
    url(r'produto/(?P<id>[\d\-]+)/comprar/$', PedidoComprarView.as_view(), name='produto-comprar'),
    url(r'usuario/cadastrar/$', ClienteCreateView.as_view(), name='cliente-add'),
    url(r'usuario/detail/$', ClienteDetailView.as_view(), name='cliente-detail'),
    url(r'pedido/listar/$', PedidoListView.as_view(), name='pedido-list'),
]