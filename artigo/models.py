from django.db import models
from django.contrib.auth.models import User
import os
 
# Create your models here.
class Artigo(models.Model):
    titulo = models.CharField(max_length=255)
    autores = models.CharField(max_length=255)
    resumo = models.CharField(max_length=255)
    abstract = models.TextField()
    palavras_chave = models.TextField()
    data = models.DateField(blank=True, null=True)
    revista = models.CharField(max_length=255)
    arquivo = models.FileField(upload_to='arquivos/', null=True, blank=True)
    ultima_modificacao = models.DateTimeField(auto_now=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

class Auditoria(models.Model):
    # Defina os campos do modelo Auditoria
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    acao = models.CharField(max_length=255)
    data = models.DateTimeField(auto_now_add=True)
    data_hora = models.DateTimeField(auto_now_add=True)
    descricao = models.TextField()

    def __str__(self):
        return f"{self.usuario} - {self.acao} em {self.data}"
