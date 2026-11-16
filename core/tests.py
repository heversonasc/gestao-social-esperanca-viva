
from datetime import timedelta

from django.contrib.auth.models import User
from django.db.models.deletion import ProtectedError
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Atendimento, PessoaAtendida


class GestaoSocialTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="teste",
            password="SenhaSegura123!x"
        )
        self.pessoa = PessoaAtendida.objects.create(
            nome="Maria Oliveira",
            telefone="(71) 99999-0000"
        )

    def login(self):
        self.client.login(
            username="teste",
            password="SenhaSegura123!x"
        )

    def test_lista_exige_login(self):
        response = self.client.get(reverse("core:people_list"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("accounts/login", response.url)

    def test_usuario_autenticado_visualiza_lista(self):
        self.login()
        response = self.client.get(reverse("core:people_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Maria Oliveira")

    def test_busca_por_nome(self):
        PessoaAtendida.objects.create(nome="João Santos")
        self.login()

        response = self.client.get(
            reverse("core:people_list"),
            {"q": "Maria"}
        )

        self.assertContains(response, "Maria Oliveira")
        self.assertNotContains(response, "João Santos")

    def test_cadastro_de_pessoa(self):
        self.login()

        response = self.client.post(
            reverse("core:person_create"),
            {
                "nome": "Ana Souza",
                "telefone": "",
                "ativo": "on",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            PessoaAtendida.objects.filter(nome="Ana Souza").exists()
        )

    def test_nome_vazio_nao_e_aceito(self):
        self.login()

        response = self.client.post(
            reverse("core:person_create"),
            {"nome": "   ", "telefone": ""}
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            PessoaAtendida.objects.filter(nome="").exists()
        )

    def test_atendimento_fica_vinculado_a_pessoa(self):
        Atendimento.objects.create(
            pessoa=self.pessoa,
            data_atendimento=timezone.now() + timedelta(minutes=1),
            descricao="Orientação social",
            status=Atendimento.Status.REALIZADO,
        )

        self.assertEqual(self.pessoa.atendimentos.count(), 1)

    def test_criar_atendimento_pela_interface(self):
        self.login()

        data = timezone.localtime(timezone.now()).strftime("%Y-%m-%dT%H:%M")

        response = self.client.post(
            reverse("core:attendance_create"),
            {
                "pessoa": str(self.pessoa.pk),
                "data_atendimento": data,
                "descricao": "Orientação social",
                "status": Atendimento.Status.REALIZADO,
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            self.pessoa.atendimentos.filter(
                descricao="Orientação social"
            ).exists()
        )

    def test_nao_permite_apagar_pessoa_com_historico(self):
        Atendimento.objects.create(
            pessoa=self.pessoa,
            data_atendimento=timezone.now(),
            descricao="Registro de teste",
        )

        with self.assertRaises(ProtectedError):
            self.pessoa.delete()

    def test_edicao_de_pessoa_atualiza_nome_e_telefone(self):
        self.login()

        response = self.client.post(
            reverse("core:person_update", args=[self.pessoa.pk]),
            {
                "nome": "Maria Oliveira Atualizada",
                "telefone": "(71) 98888-1111",
                "ativo": "on",
            },
        )

        self.assertEqual(response.status_code, 302)

        self.pessoa.refresh_from_db()

        self.assertEqual(
            self.pessoa.nome,
            "Maria Oliveira Atualizada"
        )
        self.assertEqual(
            self.pessoa.telefone,
            "(71) 98888-1111"
        )

    def test_busca_por_telefone(self):
        PessoaAtendida.objects.create(
            nome="João Santos",
            telefone="(71) 98888-1111"
        )
        self.login()

        response = self.client.get(
            reverse("core:people_list"),
            {"q": "99999"}
        )

        self.assertContains(response, "Maria Oliveira")
        self.assertNotContains(response, "João Santos")

    def test_lista_exibe_cadastros_ativos_e_inativos(self):
        self.pessoa.ativo = False
        self.pessoa.save(update_fields=["ativo"])

        PessoaAtendida.objects.create(
            nome="Ana Souza",
            telefone="(71) 97777-2222"
        )

        self.login()

        response = self.client.get(reverse("core:people_list"))

        self.assertContains(response, "Maria Oliveira")
        self.assertContains(response, "Ana Souza")
        self.assertContains(response, "Inativo")
        self.assertContains(response, "Ativo")

    def test_historico_mostra_apenas_atendimentos_da_pessoa_selecionada(self):
        outra_pessoa = PessoaAtendida.objects.create(
            nome="João Santos"
        )

        Atendimento.objects.create(
            pessoa=self.pessoa,
            data_atendimento=timezone.now(),
            descricao="Orientação social de Maria",
            status=Atendimento.Status.REALIZADO,
        )

        Atendimento.objects.create(
            pessoa=outra_pessoa,
            data_atendimento=timezone.now(),
            descricao="Entrega de cesta básica de João",
            status=Atendimento.Status.PENDENTE,
        )

        self.login()

        response = self.client.get(
            reverse("core:person_detail", args=[self.pessoa.pk])
        )

        self.assertContains(response, "Orientação social de Maria")
        self.assertNotContains(response, "Entrega de cesta básica de João")

    def test_atendimento_nao_pode_ser_vinculado_a_pessoa_inativa(self):
        self.pessoa.ativo = False
        self.pessoa.save(update_fields=["ativo"])

        self.login()

        data = timezone.localtime(timezone.now()).strftime("%Y-%m-%dT%H:%M")

        response = self.client.post(
            reverse("core:attendance_create"),
            {
                "pessoa": str(self.pessoa.pk),
                "data_atendimento": data,
                "descricao": "Tentativa de atendimento",
                "status": Atendimento.Status.REALIZADO,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.pessoa.atendimentos.exists())

    def test_edicao_exige_login(self):
        response = self.client.get(
            reverse("core:person_update", args=[self.pessoa.pk])
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn("accounts/login", response.url)

    def test_novo_atendimento_exige_login(self):
        response = self.client.get(
            reverse("core:attendance_create")
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn("accounts/login", response.url)
