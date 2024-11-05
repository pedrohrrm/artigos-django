# artigos/forms.py
from django import forms
from .models import Artigo
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re

class ArtigoForm(forms.ModelForm):
    class Meta:
        model = Artigo
        fields = "__all__"

class ConfirmacaoExclusaoForm(forms.Form):
    confirmar = forms.BooleanField(label='Confirmar exclusão?')
    
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, min_length=8)
    confirm_password = forms.CharField(widget=forms.PasswordInput, min_length=8)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        # Verifica se as senhas coincidem
        if password != confirm_password:
            raise ValidationError("As senhas não coincidem.")

        # Verifica se a senha atende aos critérios
        if not re.search(r'[A-Z]', password):
            raise ValidationError("A senha deve conter pelo menos uma letra maiúscula.")
        if not re.search(r'[a-z]', password):
            raise ValidationError("A senha deve conter pelo menos uma letra minúscula.")
        if not re.search(r'[0-9]', password):
            raise ValidationError("A senha deve conter pelo menos um dígito.")
        if not re.search(r'[\W_]', password):
            raise ValidationError("A senha deve conter pelo menos um caractere especial.")

        return cleaned_data
    
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, min_length=8, label="Senha")
    confirm_password = forms.CharField(widget=forms.PasswordInput, min_length=8, label="Confirme a Senha")

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        # Verifica se as senhas coincidem
        if password != confirm_password:
            raise ValidationError("As senhas não coincidem.")

        # Verifica critérios de segurança
        if not re.search(r'[A-Z]', password):
            raise ValidationError("A senha deve conter pelo menos uma letra maiúscula.")
        if not re.search(r'[a-z]', password):
            raise ValidationError("A senha deve conter pelo menos uma letra minúscula.")
        if not re.search(r'[0-9]', password):
            raise ValidationError("A senha deve conter pelo menos um dígito.")
        if not re.search(r'[\W_]', password):
            raise ValidationError("A senha deve conter pelo menos um caractere especial.")

        return cleaned_data

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])  # Criptografa a senha
        if commit:
            user.save()
        return user