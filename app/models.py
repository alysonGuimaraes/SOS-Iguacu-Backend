from django.db import models

class Voluntario(models.Model):
    id = models.AutoField(primary_key=True)
    nome_completo = models.CharField(max_length=255)
    cpf = models.CharField(max_length=11, unique=True)
    data_nascimento = models.DateField()
    disponibilidade = models.TextField(help_text="Descreva os dias/horários disponíveis")

    def __str__(self):
        return self.nome_completo
class Doacao(models.Model):
    produto = models.CharField(max_length=100)
    quantidade = models.IntegerField()
    # Link com o id do voluntário que doou
    voluntario = models.ForeignKey(Voluntario, on_delete=models.SET_NULL, null=True, related_name='doacoes')

    def Doacao(self):
        return f"{self.produto} 
        ({self.quantidade}) 
        - Doado por: 
        {self.voluntario.nome_completo 
         if self.voluntario 
         else 'Não informado'}"