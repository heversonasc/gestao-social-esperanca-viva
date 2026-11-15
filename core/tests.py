from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from .models import Atendimento, PessoaAtendida

class GestaoSocialTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="teste", password="SenhaSegura123!")
        self.pessoa = PessoaAtendida.objects.create(nome="Maria Oliveira")

    def test_lista_exige_login(self):
        response = self.client.get(reverse("core:people_list"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("accounts/login", response.url)

    def test_usuario_autenticado_visualiza_lista(self):
        self.client.login(username="teste", password="SenhaSegura123!")
        response = self.client.get(reverse("core:people_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Maria Oliveira")

    def test_busca_por_nome(self):
        PessoaAtendida.objects.create(nome="João Santos")
        self.client.login(username="teste", password="SenhaSegura123!")
        response = self.client.get(reverse("core:people_list"), {"q": "Maria"})
        self.assertContains(response, "Maria Oliveira")
        self.assertNotContains(response, "João Santos")

    def test_atendimento_fica_vinculado_a_pessoa(self):
        atendimento = Atendimento.objects.create(
            pessoa=self.pessoa,
            data_atendimento=timezone.now() + timedelta(minutes=1),
            descricao="Orientação social",
            status=Atendimento.Status.REALIZADO,
        )
        self.assertEqual(atendimento.pessoa, self.pessoa)
        self.assertEqual(self.pessoa.atendimentos.count(), 1)
