# -*- coding: utf-8 -*-
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import *
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import ugettext_lazy as _

from planeapp.models.cliente import Cliente


class ClienteListView(LoginRequiredMixin, ListView):
    '''
     Lista todos os Clientes.
    :URl: http://ip_servidor/clientes/listar/
    '''
    queryset = Cliente.objects.all()


class PageDetailViews(LoginRequiredMixin, DetailView):
    '''
     Detalhes do Cliente.
    :URl: http://ip_servidor/cliente/<id>/
    '''
    model = Cliente


class ClienteCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    '''
     Adiciona um Cliente.
    :URl: http://ip_servidor/cliente/cadastrar/
    '''
    model = Cliente
    form_class = ClienteForm
    success_message = "Cliente %(name)s adicionado com sucesso!"


    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            name=self.object.title,
        )


class ClienteUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    '''
     Atualiza um Cliente.
    :URl: http://ip_servidor/category/listar/
    '''
    model = Cliente
    form_class = ClienteForm
    success_message = _("Cliente %(name)s modificado com sucesso!")


    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            name=self.object.username,
        )


class PageDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    '''
     Deletar uma página.
    :URl: http://ip_servidor/cliente/<pk>/excluir
    '''
    success_message = _("Cliente %(name)s deletado com sucesso!")

    queryset = Cliente.objects.all()
    success_url = reverse_lazy('client-list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.is_active = False
        self.object.save()
        return super(PageDeleteView, self).form_valid(form)

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            name=self.object.title,
        )

