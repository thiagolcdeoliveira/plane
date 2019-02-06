# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import *
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import ugettext_lazy as _
from planeapp.forms.produto import ProdutoForm
from planeapp.models.cliente import Cliente
from planeapp.models.produto import Produto


class ProdutoListView(LoginRequiredMixin,ListView):
    '''
     Lista todos os Produtos.
    :URl: http://ip_servidor/produto/listar/
    '''
    model = Produto
    queryset = Produto.objects.all()

class ProdutoDetailViews(LoginRequiredMixin, DetailView):
    '''
     Detalhes do .
    :URl: http://ip_servidor/produto/<id>/
    '''
    model = Produto


class ProdutoCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    '''
     Adiciona um Produto.
    :URl: http://ip_servidor/cliente/cadastrar/
    '''
    model = Produto
    form_class = ProdutoForm
    success_message = "Produto %(name)s adicionado com sucesso!"


    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            name=self.object.nome,
        )


class ProdutoUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    '''
     Atualiza um produto.
    :URl: http://ip_servidor/produto/<id>/alterar
    '''
    model = Produto
    form_class = ProdutoForm
    success_message = _("Produto %(name)s modificado com sucesso!")


    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            name=self.object.nome,
        )


class ProdutoDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    '''
     Deletar um produto.
    :URl: http://ip_servidor/cliente/<id>/excluir
    '''
    success_message = _("Produto deletado com sucesso!")

    queryset = Cliente.objects.all()
    success_url = reverse_lazy('produto-list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.desativado = True
        self.object.save()
        messages.success(self.request, self.success_message)

        return super(ProdutoDeleteView, self).form_valid(form)

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)


