# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.forms import forms, ModelForm, CharField, PasswordInput, EmailField, EmailInput

from planeapp.models.cliente import Cliente


class ClienteForm(ModelForm):
    password = CharField(label="Senha", help_text="Digite uma senha com mais de cinco digitos ", widget=PasswordInput())
    password_checker = CharField(required=True, help_text="Digite outra vez a senha", label='Confirmar Senha', widget=PasswordInput)
    username = CharField(required=True, label='Username', help_text="Deve ser preenchido com seu usuário")
    email = CharField(required=True, label='Email', help_text="Deve seu email",widget=EmailInput())
    first_name = CharField(required=True, label='Primeiro  Nome', help_text="Deve seu primeiro nome")
    last_name = CharField(required=True, label='Último Nome', help_text="Deve seu ultimo nome")

    class Meta:
        model = Cliente
        fields = ("username","email","password","password_checker","first_name","last_name")


    def clean_username(self):
        username = self.cleaned_data['username']
        usuarios = User.objects.all()
        if username not in usuarios:
            return username
        else:
            raise forms.ValidationError('Esse usuário já existe!')

    def clean_password_checker(self):
        if 'password' in self.cleaned_data:
            password = self.cleaned_data['password']
            password_checker = self.cleaned_data['password_checker']
            if password == password_checker and len(password) > 5:
                return password_checker
            else:
                raise forms.ValidationError('Senhas diferentes ou possui menos de cinco digitos')
        else:
            raise forms.ValidationError('Senhas diferentes  ou possui menos de cinco digitos!')

    def save(self, commit=True):
        pessoa = super(ClienteForm, self).save(commit=False)
        pessoa.set_password(self.cleaned_data['password'])
        if commit:
            pessoa.save()
        return pessoa
