# Masterclass CBMEV — MEV e Obesidade na Era do GLP-1

Landing page da **Masterclass CBMEV: MEV e Obesidade na Era do GLP-1** — evento exclusivo do **CBMEV** (Colégio Brasileiro de Medicina do Estilo de Vida).

- **Data:** 30 de maio de 2026
- **Local:** Kurotel — Gramado/RS
- **Formato:** presencial (imersão)
- **Público:** médicos, nutricionistas e profissionais de saúde (aberto ao público geral da área)
- **Palestrantes:** Dra. Tassiane Alvarenga (endocrinologista, USP) e Dra. Carol Pimentel (nutricionista, doutora USP)
- **Inscrições:** via Sympla — [link oficial](https://www.sympla.com.br/evento/masterclass-mev-e-obesidade-na-era-dos-analogos-do-glp1/3386092)

## Identidade visual

Baseada na **Proposta de IDV Masterclass Obesidade na Era do GLP-1** enviada pelo cliente. Conceito:

- "O" íntegro = obesidade como condição fisiológica e social
- "G/Q" partido = intervenção farmacológica (GLP-1) como marcador de inflexão
- Paleta: coral/rosa (primária), roxo, verde, azul, creme
- Tipografia: **Boldonse** (títulos) + **MuseoModerno** (corpo), ambas via Google Fonts

## Stack

- HTML estático
- Tailwind CSS (via CDN)
- Google Fonts (Boldonse + MuseoModerno + Material Symbols)
- SVGs inline para o logotipo "OG"

Sem build step — basta abrir `index.html` ou servir com qualquer servidor estático.

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
masterclassglp1/
├── index.html          # landing page principal
├── favicon.ico
├── images/
│   └── brand/          # logo CBMEV + favicons
└── README.md
```

## Deploy

Roteamento configurado em `../vercel.json` — a raiz do domínio redireciona para `/masterclassglp1/`.

## Pendências / TODO

- `og-image.png` específica da Masterclass (atualmente sem OG image)
- Horário de início/término do evento (não informado no briefing)
- Valor da inscrição (controlado via Sympla)
- Confirmar se haverá certificação / carga horária oficial
