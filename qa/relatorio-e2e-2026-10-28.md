# Relatório E2E: Estoque Qualifica (pós-redesign monocromático)

## 1. Resumo

- **Data:** 28/10/2026
- **Ambiente:** local, http://127.0.0.1:8000 (servidor já em execução; não foi iniciado nem parado pelo QA). Chromium headless via MCP Playwright.
- **Perfis usados:** `admin` (administrador), `funcionario` (funcionário) e dois usuários temporários `[E2E]` (`e2e_user`, `e2e_func`), já excluídos.
- **Telas cobertas:** login; dashboard; produtos (lista, filtros e busca, detalhe, criar, editar, categorias, confirmação de exclusão de produto e de categoria); fornecedores (lista, detalhe, criar, editar, exclusão); movimentações (lista, detalhe, entrada, saída, ajuste); relatórios (semanal, quinzenal e mensal); usuários (lista, cadastro, edição, exclusão, perfil); páginas 404; `manifest.json` e `sw.js`.
- **Viewports:** 1366×768, 768×1024 e 360×800, sempre nos temas **escuro e claro**. Cada tela foi varrida por script `playwright_evaluate`, que verifica rolagem horizontal, cores com croma > 26/255 em color, background, border, outline, fill, stroke, box-shadow, background-image, caret e accent, contraste WCAG de todo nó de texto visível, inputs sem label, botões só com ícone sem `aria-label`, imagens sem `alt`, emojis sem `grayscale`, recursos com status ≥ 400 e pixels coloridos nos `<canvas>`.
- **Fluxos:** CRUD completo com prefixo `[E2E]`; entrada, saída e ajuste, inclusive casos-limite (0, negativo, decimal, saída maior que o estoque, acentos e caracteres especiais, HTML no nome, texto longo, envio duplo); transições de status (zerado → crítico → normal → crítico → alerta → zerado); permissões (UI e URL direta); login, logout e `?next=`.

**Totais de bugs:** 1 Crítica · 4 Alta · 9 Média · 12 Baixa (**26**)

---

## 2. Conformidade com o redesign

| # | Requisito | Resultado | Evidência / motivo |
|---|---|---|---|
| 1 | Tema monocromático (só preto, branco e cinza) | **REPROVADO** (parcial) | A interface das páginas passou: a varredura de `getComputedStyle` em todos os elementos visíveis de todas as telas, nos dois temas e nos três tamanhos, encontrou **0** cores saturadas. Os gráficos têm 0 pixels coloridos. Os emojis de categoria recebem `grayscale`. Seleção de texto, foco, badges, mensagens e `accent-color` usam tokens cinza. **Falhas:** (a) o favicon, os `apple-touch-icon` e os ícones do PWA (`static/icons/*.png`) são **verdes**; (b) na tela **Categorias**, o campo "Ícone (emoji)" mostra o emoji colorido (📦), e o campo "Cor (hex)" é um `input type=color` que exibe uma amostra colorida (padrão `#6b7280`, levemente azulado) e aceita qualquer cor (testado com `#ff0000`). |
| 2 | Escuro = preto com branco; claro = branco com preto; alternância no header e no login; persistência; sem flash | **APROVADO** | Escuro: body `rgb(0,0,0)` com texto `rgb(250,250,250)`. Claro: `#fafafa` com `#0a0a0a`. Os botões do header e do login alternam o tema, gravam `localStorage.theme` e atualizam `aria-pressed` e `meta theme-color`. Depois do reload o tema persiste, e a classe `dark` já está correta com `document.readyState === 'loading'` (script síncrono no `<head>`, mais `color-scheme`). Sem preferência salva, o tema segue `prefers-color-scheme`. Observação: o Tailwind via CDN gera o CSS em tempo de execução, então um FOUC de estilos é possível. Não foi possível medi-lo quadro a quadro, e ele é mitigado por `color-scheme`. |
| 3 | Status de estoque, tipos de movimentação e mensagens distinguíveis sem cor | **APROVADO** | Estoque: *Normal* tem contorno e ícone de check; *Atenção* (alerta) tem fundo cinza médio; *Crítico* é invertido, com ícone de alerta e "mín: X"; *Zerado* é tracejado e listrado, com ícone de proibido. Movimentação: *Entrada* com contorno sólido e ícone de download, *Saída* com fundo cinza e ícone de upload, *Ajuste* tracejado com ícone de ajustes. Mensagens: ícone, prefixo textual ("Sucesso:", "Erro:", "Atenção:", "Aviso:") e estilo próprio (borda esquerda grossa, invertido, cinza, tracejado), com `role=status/alert`. |
| 4 | Gráficos Chart.js em cinza e recolorindo ao trocar o tema | **APROVADO** | Os 4 gráficos (`chartLinha`, `chartRosca`, `chartLinhaRelatorio`, `chartCategorias`) têm 0 pixels com croma acima de 26 nos dois temas. Ao alternar o tema, as cores dos datasets e eixos mudam na hora (ex.: Entradas `rgba(10,10,10)` vira `rgba(250,250,250)`; rosca de `[10,64,112,160]` para `[250,205,160,120]`). |
| 5 | Responsividade em 360, 768 e 1366 | **APROVADO** (com ressalvas) | `scrollWidth === innerWidth` em **todas** as telas, nos três tamanhos e dois temas. O menu mobile abre, leva o foco ao primeiro link, fecha com Esc, overlay ou X, devolve o foco ao botão, bloqueia a rolagem do body e deixa a sidebar `inert` quando fechada. As tabelas viram cards abaixo de 768px e rolam dentro do container acima disso. Ressalvas (melhorias): em 768px as ações da lista de produtos empilham em 3 linhas e os botões de ícone medem 36px; em 1366px o KPI "Valor entrado" aparece truncado ("R$ 11…"); em 360px o rótulo "FORNECEDORES" encosta no ícone do card. |
| 6 | Sem erro de console, sem 404 de recurso, sem 500 ou TemplateSyntaxError | **APROVADO** | Nenhum erro de console da aplicação e nenhum recurso com status ≥ 400 (`performance.getEntriesByType('resource')`) em todas as telas. Nenhum 500 ou TemplateSyntaxError. `manifest.json` e `sw.js` respondem 200, e `sw.js` com o MIME correto. Única mensagem: o *warning* "cdn.tailwindcss.com should not be used in production". Os erros 404, 405 e X-Frame-Options que aparecem no log foram provocados pelos testes do próprio QA. |
| 7 | Contraste WCAG AA nos dois temas e foco visível | **APROVADO** (com ressalvas) | O verificador automático encontrou 0 textos abaixo de 4,5:1 (3:1 para texto grande) nas duas paletas. Exemplos: `subtle` escuro (140) sobre preto ≈ 7,4:1; `subtle` claro (102) sobre `#fafafa` ≈ 5,6:1. O foco é visível em toda a navegação por Tab (outline de 2px na cor `fg`, com offset). Os inputs mostram borda `fg` e halo. Ressalvas: placeholders no tema claro ficam em ~4:1 (opacidade .85); campos com erro não mudam de estilo nem recebem `aria-invalid`/`aria-describedby`; toasts de **erro** somem sozinhos em 6 s. |

### Pontos reportados pelo desenvolvedor do front

| Ponto | Procede? | Detalhe |
|---|---|---|
| (a) `Produto.status_estoque` levanta TypeError Decimal*float | **Sim** | Reproduzido no `manage.py shell` (somente leitura): para um produto com 9.00 e mínimo 3.00, a chamada levanta `TypeError: unsupported operand type(s) for *: 'decimal.Decimal' and 'float'` em `produtos/models.py:171` (`self.estoque_minimo * 1.5`). O filtro `nivel_estoque` (`core/templatetags/ui.py:159-177`) contorna o erro no template. Bug **M7**. |
| (b) `produtos_alerta_count` inexistente; sino só no dashboard | **Sim** | `settings.py:68-73` não tem nenhum context processor próprio. `base.html:65` depende de `produtos_alerta_count`, que nunca existe, e `base.html:129` usa `produtos_alerta`, que só é enviado por `core/views.py:100`. Confirmado: em /produtos/ e nas demais telas o header mostra apenas o botão de tema. Bug **B9**. |
| (c) N+1 | **Parcial** | **Categorias:** `templates/produtos/categorias.html:33` chama `cat.produto_set.count` 2× por categoria, ou seja, 2N consultas. **Fornecedores (não citado):** `templates/fornecedores/lista.html:58` chama `f.total_produtos` 2× por card (`fornecedores/models.py:74-76` faz `count()`), também 2N. **Lista de produtos:** *não* há N+1 (`select_related('categoria','fornecedor')` em `produtos/views.py:20`). **Entrada/Saída:** não é N+1, mas o queryset de produtos é avaliado 2× (uma vez pelo widget `<select>` e outra pelo loop em `components/mov_stock_js.html:9`). |
| (d) JSON pré-serializado para os gráficos | **Sim** | `core/views.py:107-111` e `relatorios/views.py:136-140` usam `json.dumps`, e os templates fazem `JSON.parse('{{ x|escapejs }}')` (`dashboard.html:190-194`, `relatorios.html:162-166`). Funciona e é seguro graças ao `escapejs`. Recomenda-se passar listas e usar `{{ dados|json_script:"id" }}`. Melhoria, não bug. |

---

## 3. Bugs

| # | Severidade | Tela/URL | Descrição | Passos para reproduzir | Esperado × Obtido | Causa provável (arquivo:linha) |
|---|---|---|---|---|---|---|
| C1 | **Crítica** | /accounts/perfil/ | **Escalada de privilégio:** qualquer funcionário vira administrador editando o próprio perfil. | 1. Logar como funcionário (testado com o usuário temporário `[E2E] e2e_func`). 2. Ir em Meu Perfil. 3. Trocar "Perfil" para Administrador e salvar. 4. Acessar /accounts/usuarios/. | Esperado: o campo não aparece para o funcionário, ou é ignorado. Obtido: o perfil vira "Administrador" e o menu Administração e a gestão de usuários ficam liberados. Reproduzido. | `accounts/forms.py:110` (`EdicaoUsuarioForm.fields` inclui `perfil`) usado sem restrição em `accounts/views.py:138-149` |
| A1 | Alta | /movimentacoes/saida/, /entrada/, /ajuste/ | Quantidade **negativa** é aceita pelo servidor. Uma saída de -5 **aumenta** o estoque e passa pela checagem "estoque insuficiente". Entrada negativa reduz o estoque; ajuste negativo deixa o estoque negativo. Qualquer funcionário consegue fazer isso. | 1. Abrir a saída do produto E2E-001 (estoque 0). 2. Remover o `min` via DevTools (ou enviar POST direto) e informar -5. 3. Confirmar. | Esperado: erro de validação. Obtido: "Saída registrada: -5", estoque 0 → 5 (mov. #10, anterior 0,00, posterior 5,00). A lista mostra "−-5". | `movimentacoes/models.py:57-60` (sem `MinValueValidator`), `movimentacoes/forms.py` (sem `clean_quantidade`), `movimentacoes/views.py:99` (`-5 > estoque` é falso) |
| A2 | Alta | /produtos/novo/ e /produtos/<id>/editar/ | O produto aceita **quantidade e preços negativos** (o limite está só no atributo HTML `min`). | Remover `min` e `required`, criar com quantidade -3 e preço de venda -5. | Esperado: erro. Obtido: "[E2E] Produto negativo" salvo com -3 Unidade e R$ -5,00 (classificado como "Zerado"). | `produtos/models.py` e `produtos/forms.py` sem validadores ≥ 0 |
| A3 | Alta | /produtos/<id>/editar/ | A edição do produto permite alterar `quantidade` diretamente, **sem gerar movimentação**, o que quebra a trilha de auditoria e os relatórios. | Editar um produto e mudar "Quantidade em Estoque" de -3 para 0. Salvar. | Esperado: quantidade somente leitura na edição (alterações só via ajuste). Obtido: estoque alterado sem nenhum registro em Movimentações. | `produtos/forms.py` (`ProdutoForm` inclui `quantidade`), `produtos/views.py:105` |
| A4 | Alta | /accounts/login/ | As credenciais padrão (admin/admin123, funcionario/func123) aparecem **sempre** na tela de login, sem nenhuma condição de DEBUG. Em produção, isso dá acesso de admin a qualquer visitante, se o seed tiver sido rodado. | Abrir /accounts/login/. | Esperado: bloco visível só com `DEBUG=True` (ou removido). Obtido: sempre visível. | `templates/registration/login.html:70-75` |
| M1 | Média | /accounts/login/?next=… | O login ignora `?next=` e sempre redireciona para o dashboard. | Acessar /produtos/ deslogado (redireciona para `login?next=/produtos/`) e logar. | Esperado: /produtos/. Obtido: /dashboard/. Reproduzido 2×. | `accounts/views.py:36` (`redirect('core:dashboard')` fixo) |
| M2 | Média | /accounts/login/ → /dashboard/ | `login.html` não inclui `components/messages.html`. Mensagens de logout ("Você saiu do sistema.") e erros de login via `messages` só aparecem **depois**, no dashboard, já desatualizadas. | Sair e logar novamente. | Esperado: a mensagem de logout aparece na tela de login. Obtido: no dashboard aparecem "Aviso: Você saiu do sistema." e "Bem-vindo". | `templates/registration/login.html` (sem include); `accounts/views.py:38,50` |
| M3 | Média | /produtos/?busca= | Busca acentuada sem distinguir maiúsculas falha: "álcool" não encontra "Álcool 70% 1 litro" (só "Álcool" encontra). | `/produtos/?busca=álcool` | Esperado: 1 resultado. Obtido: 0 ("Nenhum produto encontrado"). | `produtos/views.py:22-28` (`icontains` no SQLite só ignora maiúsculas em ASCII). Usar coluna normalizada ou `unaccent`/`Lower` em produção. |
| M4 | Média | /movimentacoes/ | A tela de **detalhe da movimentação** (/movimentacoes/<id>/) é inalcançável pela interface: as linhas da lista só levam ao produto, e nenhuma outra tela aponta para lá. | Abrir a lista e procurar um link de detalhe. | Esperado: link "Ver" por linha. Obtido: 0 links para /movimentacoes/<id>/. | `templates/movimentacoes/lista.html` |
| M5 | Média | /dashboard/ (funcionário) | O funcionário vê o botão "Novo Produto", ação exclusiva de admin. Ao clicar, é redirecionado com erro. | Logar como funcionario e olhar o hero do dashboard. | Esperado: botão oculto para não-admin. Obtido: botão visível. | `templates/core/dashboard.html:28` (sem `{% if user.is_admin %}`) |
| M6 | Média | /accounts/usuarios/cadastrar/ | O perfil padrão do novo usuário é **Administrador** (primeira opção do select). Um descuido cria admins. | Abrir o cadastro de usuário e observar "Perfil". | Esperado: padrão "Funcionário". Obtido: "admin" selecionado. | `accounts/forms.py:78-82` (sem `initial`) |
| M7 | Média | (model) | `Produto.status_estoque` levanta TypeError para todo produto acima do mínimo (ponto a). Hoje está oculto pelo filtro, mas quebra admin, IA, scripts ou qualquer código novo que use a property. | `manage.py shell`: `p.status_estoque` em produto com 9 de 3. | Esperado: 'normal'. Obtido: TypeError. | `produtos/models.py:171` (`* 1.5` → `* Decimal('1.5')`) |
| M8 | Média | /movimentacoes/, /relatorios/ | Os totalizadores somam valores inválidos: "Saídas: 5" no período (= -5 + 10). "Top produtos" soma o valor do **ajuste** (valor absoluto, não delta) e as quantidades negativas: o [E2E] aparece com 32 (= 0 - 5 + 12,5 + 10 + 14 = 31,5, arredondado). O KPI "Entradas 258" arredonda 258,5. | Ver as listas após os testes de A1. | Esperado: somas coerentes (ajuste por delta, sem negativos). Obtido: números distorcidos. | `movimentacoes/views.py:42-45`, `relatorios/views.py:110-120` (agregação de `quantidade` sem considerar tipo e sinal) |
| M9 | Média | /movimentacoes/entrada/ e /saida/ | Quantidade **0** é aceita pelo servidor (o `min=0.01` existe só no HTML) e cria movimentação sem efeito. | Remover `min` e enviar entrada com 0. | Esperado: erro. Obtido: "Entrada registrada: 0 Unidade" (mov. #9). | Mesmo local de A1 |
| B1 | Baixa | favicon / PWA | Favicon, `apple-touch-icon` e ícones do manifest são **verdes** (viola o requisito 1). | Ver a aba do navegador ou `static/icons/icon-192.png`. | Esperado: ícone preto e branco. Obtido: verde. | `static/icons/*.png` |
| B2 | Baixa | /produtos/categorias/ | O formulário de categoria exibe cores: emoji colorido no input "Ícone" e amostra colorida no `input type=color` "Cor (hex)", que aceita qualquer cor (a cor nem é usada na interface). | Abrir Categorias. | Esperado: monocromático. Obtido: 📦 colorido e amostra `#6b7280`/`#ff0000`. | `produtos/forms.py` (`CategoriaForm`: widgets `icone`/`cor`), `templates/produtos/categorias.html` |
| B3 | Baixa | /relatorios/ @1366 | O KPI "Valor entrado" aparece truncado ("R$ 11…"). | Abrir Relatórios em 1366×768. | Esperado: valor completo. Obtido: reticências. | `templates/components/stat_card.html:7` (`truncate`) com 6 colunas |
| B4 | Baixa | /movimentacoes/ | O motivo aparece como código cru ("compra", "venda"), e não como rótulo ("Compra", "Venda"). | Ver a lista. | Esperado: rótulo. Obtido: código. | O campo `motivo` não tem `choices` no model (`movimentacoes/models.py:54`). O template precisa mapear para MOTIVO_ENTRADA/SAIDA. |
| B5 | Baixa | mensagens de movimentação | Números sem localização nas mensagens ("12.5 Unidade", "Disponível: 17.50"), enquanto a interface usa "12,5". Sinal duplicado "−-5" na lista. | Registrar entrada de 12,5; tentar saída de 100. | Esperado: formato pt-BR. Obtido: ponto decimal. | `movimentacoes/views.py:71,102,109` (f-string com Decimal) |
| B6 | Baixa | várias | `<title>` inconsistente: sem o sufixo " — Estoque Qualifica" em Registrar Entrada/Saída, Ajuste, Movimentações, Movimentação #n, Categorias, Usuários, Cadastrar/Editar/Excluir Usuário, Meu Perfil, Excluir Produto/Fornecedor/Categoria e no detalhe do produto (só o nome). | Comparar abas. | Padrão único. | blocos `title` dos templates citados |
| B7 | Baixa | dashboard, produtos | Falta pluralização da unidade: "0 Unidade", "4 Unidade", "40 Unidade". | Ver Estoque Crítico ou a lista. | "4 unidades". | `get_unidade_display` sem plural |
| B8 | Baixa | /movimentacoes/99999/ | 404 e 500 usam a página padrão do Django (com DEBUG, mostra dados de debug). Não há `404.html`/`500.html` no novo design. | Acessar um id inexistente. | Página 404 no tema. | `templates/` (faltam 404.html e 500.html) |
| B9 | Baixa | todas exceto dashboard | O contador de alertas do menu nunca aparece e o sino só existe no dashboard (ponto b). | Abrir /produtos/. | Badge e sino em todas as páginas. | `base.html:65,129` sem context processor |
| B10 | Baixa | /accounts/logout/ | Logout via GET (link), sujeito a logout por CSRF ou prefetch. | — | POST com CSRF. | `accounts/views.py:47`, `base.html:113` |
| B11 | Baixa | /fornecedores/novo/ | CNPJ inválido "00.000.000/0001-00" é aceito. | Cadastrar fornecedor com esse documento. | Validação de dígitos. | `fornecedores/forms.py` |
| B12 | Baixa | /accounts/usuarios/ @1366 | O nome do admin aparece truncado ("Administra…") sem `title`/tooltip. As ações da lista de produtos quebram em 2 linhas quando há nome longo. | Ver a lista. | Nome legível. | `templates/accounts/lista_usuarios.html:19`; `produtos/lista.html` (coluna de ações sem `whitespace-nowrap`) |

Também verificado e **OK:** envio duplo bloqueado (dois cliques geram uma só movimentação, e o botão fica `is-loading`); saída maior que o estoque é bloqueada com mensagem e o formulário mantém os valores; não é possível excluir produto com movimentações, categoria com produtos ou a própria conta; HTML no nome do produto é escapado; acentos e caracteres especiais são preservados; o funcionário não vê editar, excluir, nova categoria, ajuste nem usuários, e o acesso direto a 12 URLs de admin redireciona com erro; /admin/ exige login; a confirmação de exclusão existe para produto, categoria, fornecedor e usuário.

---

## 4. Melhorias de UI/UX

### Responsividade
1. **Ações da lista de produtos em tablet (768px).** Os 5 botões de ícone empilham em uma grade de 3 linhas e deixam cada linha alta. Impacto: leitura e toque ruins. Sugestão: em `md`/`lg`, juntar Editar e Excluir num menu "⋯" (`<details>`) ou usar `flex-nowrap gap-1` com `whitespace-nowrap`. Esforço P. Screenshot: `produtos-lista-768-*.png`.
2. **Alvos de toque em tablet.** `.btn-icon` usa `md:h-9 md:w-9` (36px) em telas de toque de 768px. Sugestão: manter 44px até `lg` (`lg:h-9 lg:w-9`). Esforço P.
3. **KPIs de Relatórios.** Seis colunas em 1366px truncam valores monetários. Sugestão: `xl:grid-cols-6` só a partir de 1536px (ou 3 colunas), `text-xl` para valores e `title="{{ value }}"`. Esforço P. Screenshot: `relatorios-desktop-semanal-*.png`.
4. **Rótulo e ícone do stat card em 360px.** "FORNECEDORES" encosta no ícone. Sugestão: `min-w-0 truncate` no rótulo e `gap-2`. Esforço P. Screenshot: `relatorios-360-*.png`.
5. **Labels longos no formulário de produto.** "Quantidade em Estoque *" e "Estoque Mínimo (alerta) *" quebram linha e desalinham os inputs da grade de 4 colunas. Sugestão: `sm:grid-cols-2 lg:grid-cols-4` com labels curtos ("Qtd. atual", "Mínimo") e texto de ajuda. Esforço P. Screenshot: `produto-form-desktop-escuro-*.png`.

### Consistência visual
6. Cor e emoji em Categorias (B2): remover o campo `cor` do formulário (ou trocar por `type=hidden`) e aplicar `grayscale` ao input de emoji, ou trocar por uma lista de ícones SVG. Esforço P.
7. Ícones PWA e favicon em preto e branco (B1), coerentes com o logo "EQ". Esforço P.
8. Padronizar `<title>` (B6) com um bloco base `{% block title %}{{ page }} — Estoque Qualifica{% endblock %}`. Esforço P.
9. O botão "Excluir" das confirmações usa o mesmo visual do primário. Sugestão: usar `.btn-danger` (tracejado, que inverte no hover), como nas listas, para diferenciar a ação destrutiva. Esforço P.
10. Formato numérico pt-BR nas mensagens (B5) e pluralização de unidades (B7). Esforço P.

### Usabilidade
11. **Detalhe da movimentação inacessível (M4):** adicionar um link "Ver" por linha (`td.cell-actions`). Esforço P.
12. **Ajuste sem estoque atual:** a tela de ajuste não mostra o estoque atual nem a diferença. Sugestão: reutilizar `mov_stock_js` e exibir "Atual: X → Novo: Y (Δ)". Esforço P. Screenshot: `mov-ajuste-desktop-*.png`.
13. **Saída acima do estoque:** só é avisada após o envio. Sugestão: definir `max` no input pelo JS de `mov_stock_js` e mostrar aviso inline em tempo real. Esforço P. Screenshot: `mov-saida-excede-estoque-*.png`.
14. **Preço unitário:** vem 0 em entrada e saída. Pré-preencher com o preço de custo (entrada) ou de venda (saída) do produto selecionado. Esforço P.
15. **Erros duplicados:** um toast "Erro ao cadastrar…" mais um alerta inline dizem a mesma coisa. Manter só o inline nos formulários. Esforço P.
16. **Paginação:** as listas de produtos, movimentações e fornecedores não têm paginação. Esforço M.
17. **Unidade "Unidade" aceita decimais (12,5).** Sugestão: `step=1` quando a unidade for contável. Esforço M.
18. **Teclado no celular:** telefone, celular e CEP usam `type=text`. Sugestão: `type="tel"`/`inputmode="numeric"`, `autocomplete="tel"`, `postal-code`, `email`. Esforço P.
19. Esconder no dashboard as ações exclusivas de admin (M5), seguindo o padrão já aplicado em Produtos. Esforço P.

### Acessibilidade
20. **Campos com erro:** adicionar `aria-invalid="true"` e `aria-describedby` apontando para `.field-error`, além de um estilo visual de erro (ex.: `border-fg border-2` ou borda tracejada) no `components/form_field.html`. Esforço P. Screenshot: `produto-form-erros-escuro-*.png`.
21. **Toasts de erro somem em 6 s** (`base.html:197-201`): manter `alert-error`/`alert-warning` até serem fechados (WCAG 2.2.1). Esforço P.
22. **Placeholders no tema claro:** opacidade .85 dá ~4:1. Usar `opacity: 1` com `--c-subtle`. Esforço P.
23. **Tabelas:** a `<caption>` existe, mas está oculta ("Lista de produtos"); conferir `scope="col"` nos `th`. Esforço P.

### Desempenho
24. N+1 em Categorias e Fornecedores: `annotate(n=Count('produto'))` nas views e uso de `cat.n`/`f.n` no template. Esforço P.
25. Avaliar o queryset de produtos uma vez só em Entrada/Saída (passar a lista ao contexto ou usar `{{ dados|json_script }}`). Esforço P.
26. Trocar o **Tailwind CDN** por build (CLI/PostCSS): remove o warning do console, o FOUC e cerca de 300 KB de JS em runtime. Esforço M.
27. Dados dos gráficos com `json_script` em vez de `json.dumps` mais `JSON.parse('…|escapejs')` (ponto d). Esforço P.

---

## 5. Lista priorizada

- [ ] **C1** Remover `perfil` do formulário de "Meu Perfil" (formulário próprio, sem perfil) e travar a alteração de perfil fora da gestão de usuários. Agente: `django-reviewer`.
- [ ] **A4** Exibir as credenciais de demonstração só com `DEBUG` (ou removê-las). Agente: `frontend-dtl`.
- [ ] **A1/M9** Validar `quantidade > 0` (model e form) e transformar o save da movimentação em operação atômica (`transaction.atomic` + `select_for_update`). Agente: `estoque-especialista`.
- [ ] **A2** Adicionar `MinValueValidator(0)` em preços, quantidade, mínimo e máximo do produto. Agente: `estoque-especialista`.
- [ ] **A3** Tornar `quantidade` somente leitura na edição (alteração só via ajuste). Agente: `estoque-especialista`.
- [ ] **M7** `status_estoque`: usar `Decimal('1.5')` e depois remover o fallback do filtro. Agente: `estoque-especialista`.
- [ ] **M6** Perfil padrão "funcionario" no cadastro. Agente: `django-reviewer`.
- [ ] **M5** Ocultar "Novo Produto" do dashboard para não-admin. Agente: `frontend-dtl`.
- [ ] **M1/M2** Respeitar `next` (com `url_has_allowed_host_and_scheme`) e incluir `messages.html` no login. Agentes: `django-reviewer` e `frontend-dtl`.
- [ ] **B1/B2** Ícones PWA e favicon em preto e branco; remover a cor e o emoji colorido do formulário de categoria. Agente: `frontend-dtl`.
- [ ] **M4** Link para o detalhe da movimentação na lista. Agente: `frontend-dtl`.
- [ ] **A11y** `aria-invalid`/`aria-describedby` e estilo de erro; toasts de erro persistentes; placeholder opaco. Agente: `frontend-dtl`.
- [ ] **B9** Context processor `produtos_alerta` (badge no menu e sino global). Agente: `frontend-dtl`.
- [ ] **M8** Corrigir os totalizadores (ajuste por delta; filtrar por tipo). Agente: `estoque-especialista`.
- [ ] **M3** Busca sem acento e sem distinção de maiúsculas. Agente: `django-reviewer`.
- [ ] **Desempenho** `annotate(Count)` em Categorias e Fornecedores; queryset único em Entrada/Saída; `json_script`. Agente: `django-reviewer`.
- [ ] **Responsividade** Ações da lista em tablet; `btn-icon` com 44px até `lg`; KPIs de relatório; labels do formulário de produto. Agente: `frontend-dtl`.
- [ ] **UX de movimentação** Estoque atual no ajuste; `max` e aviso em tempo real na saída; preço pré-preenchido; `step` por unidade. Agente: `frontend-dtl` (com `estoque-especialista` para as regras).
- [ ] **Polimento** Títulos, pluralização, formato pt-BR, motivo legível, botão de exclusão com `.btn-danger`, páginas 404 e 500, logout via POST, validação de CNPJ, paginação. Agentes: `frontend-dtl` e `django-reviewer`.
- [ ] **Build** Tailwind compilado no lugar do CDN. Agente: `frontend-dtl`.

---

## 6. Não testado / limitações

- **Análise por IA ("Analisar Agora", /api/ia-analise/):** não acionada, porque chama a API externa da OpenAI (custo e dependência de chave). Só foi confirmado que o endpoint recusa GET (405).
- **Sessão expirada:** não simulada, porque os cookies HttpOnly não podem ser apagados pelas ferramentas disponíveis. Acesso deslogado a URL protegida e o redirecionamento para o login foram testados.
- **Flash de tema e FOUC do Tailwind CDN:** verificado só o estado da classe `dark` durante `readyState=loading`; sem captura quadro a quadro.
- **Upload de imagem** (produto e foto de perfil) não testado.
- **Contraste:** o verificador aproxima fundos com gradiente (usa a pior cor do gradiente) e não cobre placeholders nem estados de hover. A inspeção visual complementou.
- Em 360 e 768px, os formulários de edição de produto e fornecedor e as confirmações de exclusão de categoria e produto foram cobertos por amostragem: compartilham templates com as telas testadas, sem rolagem horizontal.
- O banco é SQLite local. O comportamento de M3 pode variar em MySQL/Postgres.

### Registros `[E2E]` deixados no banco
- **Produto** `E2E-001`, "[E2E] Açúcar Refinado "Ç" & <b>teste</b>" (pk 17, categoria Alimentação, estoque 0). Não pode ser excluído pela interface porque tem movimentações (`on_delete=PROTECT`).
- **Movimentações** desse produto: #9 (entrada 0), #10 (saída -5), #11 (entrada 12,5), #12 (saída 10), #13 (ajuste para 14) e #14 (saída 14, feita pelo usuário `funcionario`). Observações com "[E2E]" em #10 a #14.
- **Excluídos durante os testes:** produto "[E2E] Produto para excluir" (pk 16), categoria "[E2E] Categoria teste" (pk 9), fornecedor "[E2E] Forn" (pk 6) e usuários `e2e_user` (pk 3) e `e2e_func` (pk 4, usado para provar C1).
- Nenhum registro de terceiros foi editado. As mensagens de erro geradas pelos testes de URL direta com o usuário `funcionario` foram consumidas na própria sessão.

### Screenshots
Pasta `qa/screenshots/` (28 arquivos), entre eles: `login-desktop-claro-*`, `login-360-*`, `dashboard-desktop-escuro-*`, `dashboard-chartlinha-escuro-*`, `dashboard-360-escuro-*`, `menu-mobile-aberto-360-*`, `produtos-lista-desktop-claro-*` (capturado no tema escuro), `produtos-lista-360-*`, `produtos-lista-768-*`, `produto-form-desktop-escuro-*`, `produto-form-erros-escuro-*`, `produto-confirmar-exclusao-*`, `categorias-desktop-*`, `fornecedores-lista-desktop-*`, `fornecedor-detalhe-desktop-*`, `mov-entrada-desktop-*`, `mov-saida-excede-estoque-*`, `mov-ajuste-desktop-*`, `mov-lista-desktop-*`, `mov-lista-360-*`, `relatorios-desktop-semanal-*`, `relatorios-360-*`, `usuarios-lista-desktop-*`, `perfil-desktop-*`, `foco-teclado-sidebar-escuro-*`.
