# models.py (no seu app Django)
from django.db import models

class Voluntario(models.Model):
    id = models.AutoField(primary_key=True)
    nome_completo = models.CharField(max_length=255)
    cpf = models.CharField(max_length=11, unique=True)
    data_nascimento = models.DateField()
    disponibilidade = models.TextField(help_text="Descreva os dias/horários disponíveis")

    def __str__(self):
        return self.nome_completo
