from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from .forms import AtendimentoForm, PessoaAtendidaForm
from .models import Atendimento, PessoaAtendida

@login_required
def people_list(request):
    termo = request.GET.get("q", "").strip()
    pessoas = PessoaAtendida.objects.all()
    if termo:
        pessoas = pessoas.filter(Q(nome__icontains=termo) | Q(telefone__icontains=termo))
    return render(request, "core/people_list.html", {"pessoas": pessoas, "termo": termo})

@login_required
def person_create(request):
    form = PessoaAtendidaForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        pessoa = form.save()
        messages.success(request, "Cadastro realizado com sucesso.")
        return redirect("core:person_detail", pk=pessoa.pk)
    return render(request, "core/person_form.html", {"form": form, "titulo": "Cadastrar pessoa"})

@login_required
def person_update(request, pk):
    pessoa = get_object_or_404(PessoaAtendida, pk=pk)
    form = PessoaAtendidaForm(request.POST or None, instance=pessoa)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Cadastro atualizado com sucesso.")
        return redirect("core:person_detail", pk=pessoa.pk)
    return render(request, "core/person_form.html", {"form": form, "titulo": "Editar cadastro", "pessoa": pessoa})

@login_required
def person_detail(request, pk):
    pessoa = get_object_or_404(PessoaAtendida, pk=pk)
    atendimentos = pessoa.atendimentos.all()
    return render(request, "core/person_detail.html", {"pessoa": pessoa, "atendimentos": atendimentos})

@login_required
def attendance_create(request, pk=None):
    initial = {}
    if pk is not None:
        initial["pessoa"] = get_object_or_404(PessoaAtendida, pk=pk, ativo=True)
    form = AtendimentoForm(request.POST or None, initial=initial)
    if request.method == "POST" and form.is_valid():
        atendimento = form.save()
        messages.success(request, "Atendimento registrado com sucesso.")
        return redirect("core:person_detail", pk=atendimento.pessoa_id)
    return render(request, "core/attendance_form.html", {"form": form})
