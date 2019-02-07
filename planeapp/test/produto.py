
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.hashers import make_password
from django.core.urlresolvers import reverse

# Create your tests here.
from django.test import TestCase
from planeapp.models.cliente import Cliente
from planeapp.models.produto import Produto


class TestProduto(TestCase):
    def setUp(self):
        # activate('pt-br')
        self.user = Cliente(
            username='admin', password=make_password('teste')
        )
        self.user.save()

        self.produto = Produto(
            nome='Milenium', preco_unit='100', multiplo='3',
        )
        self.produto.save()
        pass


    def test_error_add_produto(self):
        self.client.login(username='admin', password='teste')
        response = self.client.post(reverse('produto-add'),
                                    {})
        self.assertContains(response, "This field is required.")

    def test_view_add_produto(self):
        self.client.login(username='admin', password='teste')
        response = self.client.post(reverse('produto-add'),
                                    {'nome': 'milenium',
                                     'preco_unit': '10',
                                     }, follow=True)
        # print(response)
        self.assertContains(response,  "This field is required.")
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('produto-add'),
                                {'nome': '3',
                                 'preco_unit': '10',
                                 'multiplo': '10',
                                 }, follow=True)

        self.assertContains(response, 'Produto 3 adicionado com sucesso')
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('produto-add'),
                                    {'nome': 'milenium',
                                     'preco_unit': '100',
                                     }, follow=True)
        self.assertContains(response, "This field is required.")
        self.assertEqual(response.status_code, 200)



