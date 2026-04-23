# Simpósio MEV — Instituto Adapta

Landing page para o **1º Simpósio Internacional de Medicina do Estilo de Vida do Instituto Adapta**.

- **Datas:** 26, 27 e 28 de abril
- **Formato:** 100% online
- **Acesso:** gratuito, edição exclusiva para membros associados do CBMEV (Colégio Brasileiro de Medicina do Estilo de Vida)

Evento de 3 dias reunindo referências nacionais e internacionais em Medicina do Estilo de Vida (MEV).

## Stack

- HTML estático
- Tailwind CSS (via CDN)
- Plus Jakarta Sans (Google Fonts)
- Material Symbols (Google Fonts)

Sem build step — basta abrir `index.html` no navegador ou servir com qualquer servidor estático.

## Rodar localmente

```bash
# opção 1: abrir direto
open index.html

# opção 2: servidor estático simples
python3 -m http.server 8000
# depois: http://localhost:8000
```

## Estrutura

```
simposiomev/
├── index.html            # landing page do simpósio
├── posgraduacao.html    # página de vendas da Pós MEV
├── obrigado.html         # página de confirmação de inscrição
├── DESIGN.md             # design system "Clinical Editorial"
├── screen.png            # referência visual do mockup original
└── README.md
```

## Páginas

- **`index.html`** — Landing do 1º Simpósio Internacional de MEV.
- **`posgraduacao.html`** — Página de vendas da pós-graduação em Medicina do Estilo de Vida e Mudança de Comportamento (oferta baseada na LP oficial em `lp.institutoadapta.com/pos-medicina-estilo-de-vida-web`).
- **`obrigado.html`** — Página de confirmação pós-inscrição no simpósio.

## Placeholders pendentes

Itens marcados com `TODO` no HTML aguardam informação definitiva:

**Simpósio (`index.html`):**
- Link real de inscrição / fluxo de validação de associado CBMEV
- Fotos oficiais dos palestrantes
- Bio curta de cada palestrante
- Horários detalhados por palestra
- Tradução simultânea (sim/não) das palestras internacionais
- Contato oficial no rodapé
- Palestrante do Ambulatório de Loma Linda (a anunciar)
- Confirmação de Beth Frates (Harvard)
- Confirmação do painel "O que há de novo em MOVIMENTO"

**Pós-graduação (`posgraduacao.html`):**
- URL final: `eventos.institutoadapta.com/simposiomev/posgraduacao`
- Link real de checkout das duas ofertas (padrão e exclusiva)
- Data de início da próxima turma
- Data limite real dos bônus (atualmente o countdown é client-side, 7 dias a partir do primeiro acesso)
- Demais docentes do corpo docente (além da coordenadora)
- WhatsApp oficial da pós no rodapé
- CNPJ e contato institucional no rodapé
