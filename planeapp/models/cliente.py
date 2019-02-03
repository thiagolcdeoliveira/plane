# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.urls import reverse_lazy
from django.contrib.auth.models import User

class Cliente(User):
    '''

    '''


    class Meta:
        verbose_name_plural = 'Clientes'

    def get_absolute_url(self):
        '''
        :return: Define a url de retorno após executar  os metodos de Create ou Update
        '''
        return reverse_lazy('cliente-detail', kwargs={'pk': self.pk})

    def __str__(self):
        '''
        :return: Define nome de exibição para o objeto
        '''
        return '%s' % self.username

    def __unicode__(self):
        '''

        :return: Define nome o unicode de exibição para o objeto
        '''
        return self.username
