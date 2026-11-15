from django.contrib import admin
from .models import Atendimento, PessoaAtendida

@admin.register(PessoaAtendida)
class PessoaAtendidaAdmin(admin.ModelAdmin):
    list_display = ("nome", "telefone", "ativo", "data_cadastro")
    search_fields = ("nome", "telefone")
    list_filter = ("ativo",)

@admin.register(Atendimento)
class AtendimentoAdmin(admin.ModelAdmin):
    list_display = ("pessoa", "data_atendimento", "status")
    search_fields = ("pessoa__nome", "descricao")
    list_filter = ("status",)
