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
├── index.html      # landing page principal
├── DESIGN.md       # design system "Clinical Editorial"
├── screen.png      # referência visual do mockup original
└── README.md
```

## Placeholders pendentes

Itens marcados com `TODO` no HTML aguardam informação definitiva:

- Link real de inscrição / fluxo de validação de associado CBMEV
- Fotos oficiais dos palestrantes
- Bio curta de cada palestrante
- Horários detalhados por palestra
- Tradução simultânea (sim/não) das palestras internacionais
- Contato oficial no rodapé
- Palestrante do Ambulatório de Loma Linda (a anunciar)
- Confirmação de Beth Frates (Harvard)
- Confirmação do painel "O que há de novo em MOVIMENTO"
