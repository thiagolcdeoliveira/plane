# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.urls import reverse_lazy
from planeapp.models.cliente import Cliente
from planeapp.models.produto import Produto


class Pedido(models.Model):
    '''
    :param produto: models.ForeignKey(Produto)
    :param cliente: models.ForeignKey(Cliente)
    :param quantidade: models.PositiveIntegerField(default=1)
    :param desativado: models.BooleanField(blank=True,default=False)
    :param finalizado: models.BooleanField(blank=True,default=False)
    '''
    produto = models.ForeignKey(Produto)
    #c
    cliente = models.ForeignKey(Cliente)
    quantidade = models.PositiveIntegerField(default=1)
    preco_unit = models.DecimalField(decimal_places=2,max_digits=10)
    desativado = models.BooleanField(blank=True,default=False)
    finalizado = models.BooleanField(blank=True,default=False)

    class Meta:
        verbose_name_plural = 'Pedidos'

    def get_absolute_url(self):
        '''
        :return: Define a url de retorno após executar os metodos de Create ou Update
        '''
        return reverse_lazy('pedido-detail', kwargs={'pk': self.pk})

    def __str__(self):
        '''
        :return: Define nome de exibição para o objeto
        '''
        return '%s' % self.pk

    def __unicode__(self):
        '''

        :return: Define nome o unicode de exibição para o objeto
        '''
        return '%s' % self.pk
