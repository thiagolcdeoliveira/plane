# coding=utf-8
from audioop import reverse

from django.http.response import HttpResponseForbidden, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy


def is_superuser(func):
    """
    Verifica se é admin, caso contário retorna  para home.
    """

    def _decorated(request, *args, **kwargs):
        print(request.user.is_superuser)
        if not request.user.is_superuser:
            return redirect(reverse_lazy('home'))

        return func(request, *args, **kwargs)

    return _decorated