# -*- coding: utf-8 -*-
import json

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import *
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import ugettext_lazy as _
from planeapp.forms.pedido import PedidoForm
from planeapp.models.cliente import Cliente
from planeapp.models.pedido import Pedido
from planeapp.models.produto import Produto
from planeapp.permission.decorator import is_superuser


@method_decorator(is_superuser,name='dispatch')
class PedidoListView(LoginRequiredMixin, ListView):
    '''
     Lista todos os Pedido.
    :URl: http://ip_servidor/pedido/listar/
    '''
    queryset = Pedido.objects.all()
    template_name = "pedido_list_admin.html"
    template_name_suffix = "_list_admin"
    paginate_by = 20

class PedidoAtivoPorUsuarioListView(LoginRequiredMixin, ListView):
    '''
    Lista todos os Pedido ativos.
    :URl: http://ip_servidor/carrinho/listar/
    '''
    queryset = Pedido.objects.filter()

    def get_queryset(self):
        user =  self.request.user
        self.queryset =self.queryset.filter(desativado=False,finalizado=False,cliente__username=self.request.user)
        return self.queryset.filter(desativado=False,finalizado=False,cliente__username=self.request.user)

    def get_context_data(self, object_list=None, **kwargs):
        context = super(PedidoAtivoPorUsuarioListView,self).get_context_data(**kwargs)
        pedidos = self.queryset
        context["valor_total"] = sum(valor for valor in [pedido.quantidade * pedido.preco_unit for pedido in pedidos ])
        return context

class PedidoDetailViews(LoginRequiredMixin, DetailView):
    '''
     Detalhes do Pedido.
    :URl: http://ip_servidor/pedido/<id>/
    '''
    model = Pedido

#Não Implementado
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

class AjaxPedidoCreateView(View):
    '''
    Adiciona um pedido via AJAX.
   :URl: http://ip_servidor/pedido/cadastrar/
    '''
    template_name_json = 'includes/form_json.html'
    template_mensagem = 'includes/mensagem_json.html'

    def get(self, request,id,**kwargs):
        '''
        :param request:
        :param id:
        :param kwargs: id do produto
        :return: HTML do modal
        '''
        context = {}
        data = {}
        form = PedidoForm(id=id)
        context['form'] =  form
        context['titulo'] =  get_object_or_404(Produto,pk=self.kwargs.get("id"))
        context['url'] = reverse('pedido-produto-add',kwargs={"id":id})

        data['html_form'] = render_to_string(self.template_name_json, context, request=request)
        return JsonResponse(data)

    def post(self, request,id):
        '''
        :param self:
        :param request:
        :param id: id do produto
        :return: sucesso ou não do cadstro
        '''
        form = PedidoForm(request.POST, request.FILES, id=id)
        if form.is_valid():
            form = form.save(commit=False)
            form.cliente = Cliente.objects.get(username=request.user)
            form.produto = Produto.objects.get(id=id)
            return self.form_valid(form)
        else:
            print(form.errors)
            return self.form_invalid(form)

    def form_valid(self, form):
        '''
        :param self:
        :param form: de cadastro do pedido
        :return: um JSON com as informações sobre o cadstro
        '''
        data = dict()
        context = {}
        form.save()
        data['form_is_valid'] = True
        data["carrinho"] = Pedido.objects.filter(desativado=False,finalizado=False,cliente__username=self.request.user).count()
        data['html_mensagem'] = render_to_string(self.template_mensagem, context, request=self.request)
        return JsonResponse(data)

    def form_invalid(self, form):
        '''

        :param self:
        :param form: erro no form
        :return: retorna o erro no cadastro
        '''
        context = {}
        data = dict()
        data['form_is_valid'] = False
        context['form'] = form
        context['classe_css'] = 'pedido_add'
        context['titulo'] =  get_object_or_404(Produto, pk=self.kwargs.get("id"))
        context["url"] = reverse("pedido-produto-add", kwargs={"id":self.kwargs.get("id")})
        data['html_form'] = render_to_string(self.template_name_json, context, request=self.request)
        return JsonResponse(data)

class AjaxPedidoUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    '''
     Atualiza um pedido.
    :URl: http://ip_servidor/pedido/<id>/atualizar
    '''
    template_name_json = 'includes/form_json.html'
    template_mensagem = 'includes/mensagem_json.html'

    def get(self, request, id, **kwargs):
        '''

        :param request:
        :param id: id do pedido
        :param kwargs:
        :return: o cadastro de uma atualização
        '''
        context = {}
        data = {}
        pedido= Pedido.objects.get(id=id)
        form = PedidoForm(id=pedido.produto.id,instance=pedido)
        context['form'] = form
        context['titulo'] = get_object_or_404(Pedido, pk=self.kwargs.get("id"))
        context['editado'] = True
        context['url'] = reverse('pedido-editar', kwargs={"id": id})
        data['html_form'] = render_to_string(self.template_name_json, context, request=request)
        return JsonResponse(data)

    def post(self, request, id):
        '''

        :param request:
        :param id: do pedido
        :return: retorna o sucesso ou não
        '''
        pedido= Pedido.objects.get(id=id)
        form = PedidoForm(request.POST, request.FILES,id=pedido.produto.id,instance=pedido)
        if form.is_valid():
            form = form.save(commit=False)
            return self.form_valid(form)
        else:
            print(form.errors)
            return self.form_invalid(form)

    def form_valid(self, form):
        '''

        :param form:
        :return: retorna retorna o sucesso do cadastro
        '''
        data = dict()
        context = {}
        form.save()
        data['form_is_valid'] = True
        data['editado'] = True
        context['editado'] = True
        pedido = Pedido.objects.get(id=self.kwargs.get("id"))
        data['pedido'] = pedido.id
        data['quantidade'] = pedido.quantidade
        data['preco'] = pedido.preco_unit
        pedidos = Pedido.objects.filter(desativado=False,finalizado=False,cliente__username=self.request.user)
        data['total'] =  sum(valor for valor in [pedido.quantidade * pedido.preco_unit for pedido in pedidos ])
        data['html_mensagem'] = render_to_string(self.template_mensagem, context, request=self.request)
        return JsonResponse(data)

    def form_invalid(self, form):
        '''

        :param form:
        :return: retorna o erro no cadastro da atualização
        '''
        context = {}
        data = dict()
        data['form_is_valid'] = False
        context['form'] = form
        context['classe_css'] = 'pedido_editar'
        context['titulo'] = get_object_or_404(Pedido, pk=self.kwargs.get("id"))
        context["url"] = reverse("pedido-editar", kwargs={"id": self.kwargs.get("id")})
        data['html_form'] = render_to_string(self.template_name_json, context, request=self.request)
        return JsonResponse(data)


# Não Implentado
class PedidoUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    '''
     Atualiza um pedido.
    :URl: http://ip_servidor/pedido/<id>/atualizar
    '''
    model = Pedido
    form_class = PedidoForm
    success_message = _("Pedido %(name)s modificado com sucesso!")


    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            name=self.object.username,
        )


class PedidoDeleteView(SuccessMessageMixin,LoginRequiredMixin, DeleteView):
    '''
     Deleta um pedido do carrinho.
    :URl: http://ip_servidor/pedido/<pk>/excluir
    '''

    success_message = _("Pedido  deletado com sucesso!")
    queryset = Pedido.objects.all()
    success_url = reverse_lazy('carrinho-list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.desativado = True
        self.object.save()
        messages.success(self.request, self.success_message)
        return super(PedidoDeleteView, self).form_valid(form)

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            name=self.object.title,
        )


class PedidoFinalizarView(LoginRequiredMixin, SuccessMessageMixin, View):
    '''
     Finaliza  o carrinho  do usuário.
    :URl: http://ip_servidor/carrinho/finalizar
    '''
    success_message = "Pedido finalizado com sucesso!"
    queryset = Pedido.objects.all()
    success_url = reverse_lazy('produto-list')
    def get(self,request, *args, **kwargs):
        pedidos = Pedido.objects.filter(desativado=False,finalizado=False,cliente__username=self.request.user)
        for object in pedidos:
            object.finalizado = True
            object.save()
        messages.success(self.request, self.success_message)
        return redirect(reverse('produto-list'))

class PedidoLimparView(LoginRequiredMixin, SuccessMessageMixin, View):
    '''
     Limpa o carrinho do usuário logado.
    :URl: http://ip_servidor/carrinho/limpar
    '''
    success_message = "Carrinho limpo com sucesso!"
    queryset = Pedido.objects.all()
    success_url = reverse_lazy('produto-list')
    def get(self,request, *args, **kwargs):
        pedidos = Pedido.objects.filter(desativado=False,finalizado=False,cliente__username=request.user)
        for object in pedidos:
            object.desativado = True
            object.save()
        messages.success(self.request, self.success_message)
        return redirect(reverse('produto-list'))

class PedidoComprarView(LoginRequiredMixin, SuccessMessageMixin, View):
    '''
     Comprar item isolado de um carrinho.
    :URl: http://ip_servidor/produto/<id>/comprar
    '''
    success_message = "Produto Comprado com sucesso!"
    def get(self,request,id, *args, **kwargs):
        object = Pedido.objects.get(pk=id)
        object.finalizado = True
        object.save()
        messages.success(self.request, self.success_message)
        return redirect(reverse('carrinho-list'))


