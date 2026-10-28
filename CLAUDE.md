# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Visão geral

Estoque Qualifica é um sistema de controle de estoque em Django 4.2 (SQLite, pt-BR, fuso `America/Sao_Paulo`), publicado no PythonAnywhere. Código, comentários, nomes e UI estão em português; mantenha esse padrão.

## Comandos

Windows, com o venv da raiz (`venv\Scripts\activate`; no Git Bash use `source venv/Scripts/activate`):

```bash
pip install -r requirements.txt
cp .env.example .env              # SECRET_KEY, DEBUG, OPENAI_API_KEY (opcional)
python manage.py migrate
python manage.py seed_dados       # dados de exemplo: admin/admin123 e funcionario/func123
python manage.py runserver        # http://127.0.0.1:8000
python manage.py collectstatic --noinput
python manage.py check
```

Não há suíte de testes nem linter configurados. Se criar testes, use o runner do Django: `python manage.py test produtos` ou `python manage.py test produtos.tests.NomeDaClasse.test_metodo`. A validação manual/E2E fica em `qa/` (relatório e screenshots feitos com Playwright).

`db.sqlite3.seed_backup` é uma cópia do banco populado; `_backup_redesign_2026-10-28/` guarda templates e estáticos anteriores ao redesign. São só referência, não edite.

## Arquitetura

Apps (cada uma com `urls.py` próprio, montadas em `estoque_qualifica/urls.py` com `app_name` para namespacing, por exemplo `movimentacoes:lista`):

- `accounts`: `Usuario` personalizado (`AUTH_USER_MODEL = 'accounts.Usuario'`) com o campo `perfil` (`admin`/`funcionario`). A autorização é feita à mão nas views com `@login_required` mais `if not request.user.is_admin:` (`is_admin` também é true para superuser). Não existe sistema de permissões do Django em uso.
- `produtos`: `Categoria` e `Produto`. As propriedades `status_estoque`, `esta_abaixo_minimo`, `valor_estoque` e `margem_lucro` concentram a lógica de nível de estoque usada em todas as telas.
- `fornecedores`: CRUD simples, referenciado por `Produto` (`SET_NULL`).
- `movimentacoes`: o coração das regras de negócio. **`Movimentacao.save()` altera `Produto.quantidade`**, mas só na criação (`not self.pk`): `entrada`/`devolucao` somam, `saida`/`perda`/`transferencia` subtraem, `ajuste` define o valor absoluto. Também grava `estoque_anterior`/`estoque_posterior`. Editar uma movimentação existente não recalcula o estoque. A checagem de estoque insuficiente fica na view `registrar_saida`, não no model. Toda mudança de quantidade deve passar por uma `Movimentacao`, nunca por um update direto em `Produto.quantidade`.
- `core`: dashboard, `seed_dados` (management command) e `ia_analise` (POST, retorna JSON). Esta usa a OpenAI (`gpt-3.5-turbo`, SDK `openai==1.3.7`) quando `OPENAI_API_KEY` existe e cai em `gerar_analise_local()` sem chave ou em qualquer erro.
- `relatorios`: agregações por período (semanal/quinzenal/mensal) para gráficos.

Os models de `core` e `relatorios` são vazios: as apps só têm views.

### Front-end

- Templates ficam em `templates/<app>/` (não dentro das apps). `base.html` tem dois layouts: autenticado (`{% block content %}`, sidebar e header com `{% block page_title %}`) e anônimo (`{% block content_anon %}`).
- `templates/components/` traz partials reutilizáveis via `{% include %}` (form_field, mov_form, stat_card, status_badge, confirm_delete, chart_theme etc.). Prefira reaproveitá-los em vez de duplicar markup.
- Tailwind via CDN (`cdn.tailwindcss.com`), com config e classes utilitárias (`@apply`, ex.: `.form-input`, `.field-label`, `.rtable`) definidas inline em `components/head_assets.html`. Não há build de CSS. Os widgets dos forms recebem `class: 'form-input'` no Python.
- `core/templatetags/ui.py` (`{% load ui %}`): `{% icon %}` (SVGs inline), filtros `brl` e `qtd` (formatação pt-BR), `iniciais`, `nivel_estoque` e `status_label`.
- O design é **monocromático** (só preto, branco e cinza), com tema claro/escuro (classe `dark`, persistida em `localStorage.theme`). Status precisam ser distinguíveis sem cor (ícone, borda, padrão). Os gráficos Chart.js são tematizados por `components/chart_theme.html` e recoloridos ao trocar o tema.
- PWA: `static/manifest.json` e `static/sw.js`. O SW é servido na raiz `/sw.js` por uma view em `estoque_qualifica/urls.py`. Ao mudar assets cacheados, incremente `CACHE_NAME` em `sw.js`.

### Configuração e deploy

- `settings.py` lê `.env` via python-dotenv. Estáticos usam WhiteNoise com `CompressedManifestStaticFilesStorage`, então `collectstatic` é obrigatório quando `DEBUG=False` (senão referências `{% static %}` quebram).
- Deploy no PythonAnywhere: `pythonanywhere_wsgi.py` é o modelo do arquivo WSGI (define variáveis de ambiente direto nele). O passo a passo completo está em `GUIA_COMPLETO.md`.

## Agentes do projeto

`.claude/agents/` define subagentes especializados: `estoque-especialista` (regras de movimentação e estoque), `django-reviewer`, `ui-templates` / `frontend-dtl` (templates), `qa-e2e-playwright` e `deploy-pythonanywhere`.
