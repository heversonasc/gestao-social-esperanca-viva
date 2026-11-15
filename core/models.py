from django.db import models
from django.core.validators import MinLengthValidator

class PessoaAtendida(models.Model):
    nome = models.CharField(max_length=120, validators=[MinLengthValidator(2)])
    telefone = models.CharField(max_length=20, blank=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        ordering = ["nome"]
        verbose_name = "Pessoa atendida"
        verbose_name_plural = "Pessoas atendidas"

    def __str__(self):
        return self.nome

class Atendimento(models.Model):
    class Status(models.TextChoices):
        REALIZADO = "realizado", "Realizado"
        PENDENTE = "pendente", "Pendente"
        CANCELADO = "cancelado", "Cancelado"

    pessoa = models.ForeignKey(PessoaAtendida, on_delete=models.PROTECT, related_name="atendimentos")
    data_atendimento = models.DateTimeField()
    descricao = models.TextField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.REALIZADO)
    data_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-data_atendimento", "-id"]
        verbose_name = "Atendimento"
        verbose_name_plural = "Atendimentos"

    def __str__(self):
        return f"{self.pessoa.nome} — {self.get_status_display()}"
