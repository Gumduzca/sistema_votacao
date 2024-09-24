# votacao/models.py
from django.db import models
from django.contrib.auth.models import User

class Mesario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Eleitor(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11, unique=True)
    ja_votou = models.BooleanField(default=False)

    def __str__(self):
        return self.nome

class Candidato(models.Model):
    nome = models.CharField(max_length=100)
    numero = models.IntegerField(unique=True)
    votos = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.nome} - {self.numero}"

class Voto(models.Model):
    eleitor = models.ForeignKey(Eleitor, on_delete=models.CASCADE)
    candidato = models.ForeignKey(Candidato, on_delete=models.CASCADE)
    data_hora = models.DateTimeField(auto_now_add=True)
