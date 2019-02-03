
from django.conf.urls import url, include

urlpatterns=[
    url(r'^/$', ProdutoListViews.as_view(), name='produto-list'),
]