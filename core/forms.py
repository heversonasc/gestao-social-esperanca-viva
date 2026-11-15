from django import forms
from .models import Atendimento, PessoaAtendida

class PessoaAtendidaForm(forms.ModelForm):
    class Meta:
        model = PessoaAtendida
        fields = ["nome", "telefone", "ativo"]
        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control", "autocomplete": "name"}),
            "telefone": forms.TextInput(attrs={"class": "form-control", "autocomplete": "tel", "inputmode": "tel"}),
            "ativo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
        labels = {"nome": "Nome completo", "telefone": "Telefone (opcional)", "ativo": "Cadastro ativo"}

    def clean_nome(self):
        nome = self.cleaned_data["nome"].strip()
        if len(nome) < 2:
            raise forms.ValidationError("Informe um nome com pelo menos dois caracteres.")
        return nome

class AtendimentoForm(forms.ModelForm):
    data_atendimento = forms.DateTimeField(
        input_formats=["%Y-%m-%dT%H:%M"],
        widget=forms.DateTimeInput(format="%Y-%m-%dT%H:%M", attrs={"class": "form-control", "type": "datetime-local"}),
        label="Data e hora",
    )

    class Meta:
        model = Atendimento
        fields = ["pessoa", "data_atendimento", "descricao", "status"]
        widgets = {
            "pessoa": forms.Select(attrs={"class": "form-select"}),
            "descricao": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "status": forms.Select(attrs={"class": "form-select"}),
        }
        labels = {"pessoa": "Pessoa atendida", "descricao": "Descrição do atendimento", "status": "Status"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["pessoa"].queryset = PessoaAtendida.objects.filter(ativo=True).order_by("nome")

    def clean_descricao(self):
        descricao = self.cleaned_data["descricao"].strip()
        if not descricao:
            raise forms.ValidationError("Descreva brevemente o atendimento.")
        return descricao
