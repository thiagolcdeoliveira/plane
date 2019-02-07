
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.hashers import make_password
from django.core.urlresolvers import reverse

# Create your tests here.
from django.test import TestCase
from planeapp.models.cliente import Cliente
from planeapp.models.produto import Produto


class TestCliente(TestCase):
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
        response = self.client.post(reverse('cliente-add'),
                                    {'password': '1',
                                     'password_checked': '10',
                                     'username': 'thiago',
                                     'first_name': 'teste',
                                     })
        self.assertContains(response, "This field is required.")

    def test_view_add_cliente(self):
        self.client.login(username='admin', password='teste')
        response = self.client.post(reverse('cliente-add'),
                                    {'password': '100000',
                                     'password_checker': '100000',
                                     'username': 'thiago',
                                     'first_name': 'teste',
                                     'last_name': 'teste',
                                     'email': 'teste@gmail.com',
                                     },follow=True)
        print(response)
        # self.assertContains(response, 'Login')
        # self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('cliente-add'),
                                    {'password': '100000',
                                     'password_checker': '100000',
                                     'username': 'thiago',
                                     'first_name': 'teste',
                                     'last_name': 'teste',

                                     })
        self.assertContains(response, "This field is required.")

        response = self.client.post(reverse('cliente-add'),
                                    {'password': '100000',
                                     'password_checker': '100000',
                                     'username': 'thiago',
                                     'first_name': 'teste',

                                     })
        self.assertContains(response, "This field is required.")

        response = self.client.get(reverse('cliente-add'),
                                    {},follow=True)


        self.assertEqual(response.status_code,200)



