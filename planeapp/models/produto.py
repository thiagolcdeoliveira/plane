# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from _decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse_lazy
from django.contrib.auth.models import User

class Produto(models.Model):
    '''
    :param nome: models.CharField(max_length=100)
    :param preco_unit: models.FloatField(validators={MinValueValidator(Decimal('0.01'))})
    :param multiplo: models.PositiveIntegerField(default=1)
    '''

    nome = models.CharField(max_length=100)
    preco_unit = models.FloatField(validators={MinValueValidator(Decimal('0.01'))})
    multiplo = models.PositiveIntegerField(default=1,blank=True)

    class Meta:
        verbose_name_plural = 'Produtos'

    def get_absolute_url(self):
        '''
        :return: Define a url de retorno após executar os metodos de Create ou Update
        '''
        return reverse_lazy('produtos-detail', kwargs={'pk': self.pk})

    def __str__(self):
        '''
        :return: Define nome de exibição para o objeto
        '''
        return '%s' % self.nome

    def __unicode__(self):
        '''
        
        :return: Define nome o unicode de exibição para o objeto
        '''
        return self.nome
