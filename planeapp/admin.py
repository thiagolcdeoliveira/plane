# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from planeapp.models.cliente import Cliente
from planeapp.models.pedido import Pedido
from planeapp.models.produto import Produto

admin.site.register(Cliente)
admin.site.register(Produto)
admin.site.register(Pedido)
