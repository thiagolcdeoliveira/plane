# -*- coding: utf-8 -*-
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.views.generic import *
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import ugettext_lazy as _
from planeapp.forms.pedido import PedidoForm
from planeapp.models.cliente import Cliente
from planeapp.models.pedido import Pedido
from planeapp.models.produto import Produto


class PedidoListView(LoginRequiredMixin, ListView):
    '''
     Lista todos os Pedido.
    :URl: http://ip_servidor/pedidos/listar/
    '''
    queryset = Pedido.objects.all()

class PedidoAtivoPorUsuarioListView(LoginRequiredMixin, ListView):
    '''
    Lista todos os Pedido ativos.
    :URl: http://ip_servidor/pedidos/listar/
    '''
    queryset = Pedido.objects.filter()
    def get_queryset(self):
        user =  self.request.user
        self.queryset =self.queryset.filter(desativado=False,finalizado=False,cliente__username='root1234')
        return self.queryset.filter(desativado=False,finalizado=False,cliente__username='root1234')

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

    def get(self, request,id,**kwargs):
        context = {}
        data = {}
        form = PedidoForm(id=id)
        context['form'] =  form
        context['titulo'] =  get_object_or_404(Produto,pk=self.kwargs.get("id"))
        context['url'] = reverse('pedido-produto-add',kwargs={"id":id})

        data['html_form'] = render_to_string(self.template_name_json, context, request=request)
        return JsonResponse(data)

    def post(self, request,id):
        print("oi")
        form = PedidoForm(request.POST, request.FILES, id=id)
        print(form)
        if form.is_valid():
            form = form.save(commit=False)
            form.cliente = Cliente.objects.get(username='root1234')
            form.produto = Produto.objects.get(id=id)
            return self.form_valid(form)
        else:
            print(form.errors)
            return self.form_invalid(form)

    def form_valid(self, form):
        data = dict()
        form.save()
        data['form_is_valid'] = True
        return JsonResponse(data)

    def form_invalid(self, form):
        context = {}
        data = dict()
        data['form_is_valid'] = False
        context['form'] = form
        context['classe_css'] = 'pedido_add'
        context['titulo'] =  get_object_or_404(Produto, pk=self.kwargs.get("id"))
        context["url"] = reverse("pedido-produto-add", kwargs={"id":self.kwargs.get("id")})
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


class PedidoDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    '''
     Deleta um pedido do carrinho.
    :URl: http://ip_servidor/pedido/<pk>/excluir
    '''
    success_message = _("Pedido %(name)s deletado com sucesso!")

    queryset = Pedido.objects.all()
    success_url = reverse_lazy('carrinho-list')

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


class PedidoFinalizarView(LoginRequiredMixin, SuccessMessageMixin, View):
    '''
     Finaliza  o carrinho  do usuário.
    :URl: http://ip_servidor/carrinho/finalizar
    '''
    success_message = "Pedido finalizado com sucesso!"
    queryset = Pedido.objects.all()
    success_url = reverse_lazy('produto-list')
    def get(self,request, *args, **kwargs):
        pedidos = Pedido.objects.filter(desativado=False,finalizado=False,cliente__username="root1234")
        for object in pedidos:
            object.finalizado = True
            object.save()
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
        pedidos = Pedido.objects.filter(desativado=False,finalizado=False,cliente__username="root1234")
        for object in pedidos:
            object.desativado = True
            object.save()
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
        return redirect(reverse('carrinho-list'))
