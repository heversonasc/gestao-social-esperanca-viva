# Gestão Social — ONG Esperança Viva

MVP acadêmico para centralizar cadastros de pessoas atendidas e o histórico de atendimentos da ONG Esperança Viva.

## Funcionalidades da primeira versão

- Login obrigatório para acessar as telas administrativas.
- Cadastro e edição de pessoas atendidas.
- Busca por nome ou telefone.
- Registro de atendimentos associados a uma pessoa.
- Consulta do histórico de atendimentos.
- Status do atendimento: realizado, pendente ou cancelado.

## Tecnologias

- Python 3.13
- Django 5.2
- Bootstrap 5.3
- SQLite para execução local inicial; PostgreSQL pode ser habilitado por variáveis de ambiente.

## Executar localmente no macOS

1. Instale Python 3.13.
2. Abra o Terminal e entre na pasta do projeto.
3. Crie e ative o ambiente virtual:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

4. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

5. Copie `.env.example` para `.env` e configure os valores locais. Não publique `.env` no GitHub.
6. Crie as tabelas e um usuário administrador:

   ```bash
   python manage.py makemigrations core
   python manage.py migrate
   python manage.py createsuperuser
   ```

7. Inicie o servidor:

   ```bash
   python manage.py runserver
   ```

8. Acesse http://127.0.0.1:8000/ e entre com o usuário criado no passo 6.

## Ativar PostgreSQL

Configure `DB_ENGINE=postgresql`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST` e `DB_PORT` no ambiente. O pacote `psycopg` já está listado em `requirements.txt`. Depois execute `python manage.py migrate`.

## Testes

```bash
python manage.py test
```

## Publicar no GitHub

Crie no GitHub um repositório público chamado `gestao-social-esperanca-viva`, sem adicionar arquivos iniciais se já utilizar esta pasta. Na pasta do projeto, execute:

```bash
git init
git add .
git commit -m "Estrutura inicial do MVP Gestão Social"
git branch -M main
git remote add origin https://github.com/SEU-USUARIO/gestao-social-esperanca-viva.git
git push -u origin main
```

Substitua `SEU-USUARIO` pelo seu usuário do GitHub. Depois, copie a URL pública do repositório para a plataforma acadêmica.

## Segurança e dados

- Nunca publique senhas, tokens, chaves ou arquivos `.env`.
- Utilize somente dados fictícios durante desenvolvimento e demonstrações.
- A configuração local padrão é destinada a desenvolvimento, não à produção.
- Antes de implantar, configure `DEBUG=False`, `SECRET_KEY` forte, `ALLOWED_HOSTS`, HTTPS, backups e credenciais protegidas.
- O acesso às telas deste MVP é limitado a usuários autenticados. Revise e amplie as permissões por perfil antes de uso institucional real.
