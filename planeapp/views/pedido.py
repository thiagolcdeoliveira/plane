# -*- coding: utf-8 -*-
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import *
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import ugettext_lazy as _

from planeapp.models.cliente import Cliente
from planeapp.models.pedido import Pedido


class PedidoListView(LoginRequiredMixin, ListView):
    '''
     Lista todos os Pedido.
    :URl: http://ip_servidor/pedidos/listar/
    '''
    queryset = Pedido.objects.all()


class PedidoDetailViews(LoginRequiredMixin, DetailView):
    '''
     Detalhes do Pedido.
    :URl: http://ip_servidor/pedido/<id>/
    '''
    model = Pedido


class PedidoCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    '''
     Adiciona um pedido.
    :URl: http://ip_servidor/pedido/cadastrar/
    '''
    model = Pedido
    form_class = PedidoForm
    success_message = "Pedido %(name)s adicionado com sucesso!"


    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            name=self.object.title,
        )


class PedidoUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    '''
     Atualiza um Cliente.
    :URl: http://ip_servidor/pedido/listar/
    '''
    model = Pedido
    form_class = PedidoForm
    success_message = _("Pedido %(name)s modificado com sucesso!")


    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            name=self.object.username,
        )


class PedidoDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    '''
     Deletar uma página.
    :URl: http://ip_servidor/pedido/<pk>/excluir
    '''
    success_message = _("Pedido %(name)s deletado com sucesso!")

    queryset = Cliente.objects.all()
    success_url = reverse_lazy('pedido-list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.desativado = True
        self.object.save()
        return super(PedidoDeleteView, self).form_valid(form)

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            name=self.object.title,
        )

