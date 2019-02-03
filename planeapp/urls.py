
from django.conf.urls import url, include

from planeapp.views.produto import ProdutoListView

urlpatterns=[
    url(r'^$', ProdutoListView.as_view(), name='produto-list'),
]