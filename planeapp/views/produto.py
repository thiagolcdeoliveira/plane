# -*- coding: utf-8 -*-
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import *
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import FormMixin

from planeapp.forms.pedido import PedidoForm
from planeapp.forms.produto import ProdutoForm
from planeapp.models.cliente import Cliente
from planeapp.models.produto import Produto


class ProdutoListView(LoginRequiredMixin,ListView):
    '''
     Lista todos os Produtos.
    :URl: http://ip_servidor/produto/listar/
    '''
    model = Produto
    form_class = PedidoForm
    queryset = Produto.objects.all()


    def get_context_data(self,  object_list=None, **kwargs):
        context = super(ProdutoListView,self).get_context_data(**kwargs)
        # context["form"] = PedidoForm()
        # context["form"] = PedidoForm(id=id)
        # print(context)
        # print(context['form'])
        return context

    # def get_success_url(self):
    #     return reverse('author-detail', kwargs={'pk': self.object.pk})
    #
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['form'] = self.get_form()
    #     return context
    #
    # def post(self, request, *args, **kwargs):
    #     if not request.user.is_authenticated:
    #         return HttpResponseForbidden()
    #     self.object = self.get_object()
    #     form = self.get_form()
    #     if form.is_valid():
    #         return self.form_valid(form)
    #     else:
    #         return self.form_invalid(form)
    #
    # def form_valid(self, form):
    #     # Here, we would record the user's interest using the message
    #     # passed in form.cleaned_data['message']
    #     return super().form_valid(form)

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
            name=self.object.title,
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
            name=self.object.username,
        )


class PageDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    '''
     Deletar um produto.
    :URl: http://ip_servidor/cliente/<id>/excluir
    '''
    success_message = _("Produto %(name)s deletado com sucesso!")

    queryset = Cliente.objects.all()
    success_url = reverse_lazy('produto-list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.desativado = True
        self.object.save()
        return super(PageDeleteView, self).form_valid(form)

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            name=self.object.title,
        )

