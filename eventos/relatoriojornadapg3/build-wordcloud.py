"""
Gerador de wordcloud SVG com cores por cluster semantico.

Roda uma vez para produzir o trecho SVG inline para o relatorio.
Output: stdout (cole o conteudo no index.html no lugar da imagem base64)
"""
import math
import random

# (texto, frequencia, cluster)
WORDS = [
    ('conteúdo', 23, 'eval'),
    ('conhecimento', 18, 'core'),
    ('exercícios', 14, 'core'),
    ('aprender', 13, 'emo'),
    ('alunos', 13, 'audience'),
    ('trabalhar', 12, 'emo'),
    ('grupos especiais', 12, 'core'),
    ('interessante', 10, 'eval'),
    ('importante', 10, 'eval'),
    ('trabalho', 10, 'eval'),
    ('profissional', 9, 'eval'),
    ('curso', 9, 'eval'),
    ('idosos', 9, 'audience'),
    ('excelente', 9, 'eval'),
    ('gostei', 8, 'eval'),
    ('ótimo', 8, 'eval'),
    ('preciso', 7, 'emo'),
    ('prescrever', 7, 'core'),
    ('ansiosa', 7, 'emo'),
    ('prescrição', 6, 'core'),
    ('segurança', 6, 'emo'),
    ('sinto', 6, 'emo'),
    ('hipertensos', 5, 'audience'),
    ('mercado', 5, 'eval'),
    ('diabéticos', 4, 'audience'),
    ('pressão', 4, 'audience'),
    ('quero', 4, 'emo'),
    ('aprendendo', 4, 'emo'),
    ('atendimento', 4, 'core'),
    ('aplicar', 4, 'core'),
    ('cardíacos', 3, 'audience'),
    ('referência', 3, 'emo'),
    ('especialização', 3, 'core'),
    ('reabilitação', 3, 'core'),
    ('oncológicos', 3, 'audience'),
    ('confiante', 2, 'emo'),
    ('insegura', 2, 'emo'),
    ('capaz', 2, 'emo'),
    ('medo', 2, 'emo'),
    ('preparado', 2, 'emo'),
    ('clínico', 2, 'core'),
    ('protocolo', 2, 'core'),
    ('musculação', 2, 'core'),
    ('didática', 2, 'eval'),
    ('material', 2, 'eval'),
    ('comorbidades', 2, 'audience'),
    ('avaliação', 2, 'core'),
    ('saúde', 2, 'eval'),
    ('crescimento', 2, 'eval'),
    ('aplicação', 2, 'core'),
]

COLORS = {
    'core':     '#116BF8',  # brand blue (clinico/nucleo)
    'audience': '#0848B8',  # deep blue (publico)
    'emo':      '#00B36C',  # green (emocional) - tom mais escuro para legibilidade
    'eval':     '#3F4856',  # ink-soft (avaliacao neutra)
}

WEIGHTS = {
    'core':     700,
    'audience': 600,
    'emo':      700,
    'eval':     500,
}

W, H = 1180, 580
CENTER = (W / 2, H / 2)

# Tamanho da fonte: range generoso
MAX_FREQ = max(f for _, f, _ in WORDS)
MIN_FREQ = min(f for _, f, _ in WORDS)
SIZE_MIN, SIZE_MAX = 14, 72

def font_size(freq):
    # mapeamento nao-linear para dar mais drama no topo
    t = (freq - MIN_FREQ) / (MAX_FREQ - MIN_FREQ)
    t = t ** 0.65
    return SIZE_MIN + (SIZE_MAX - SIZE_MIN) * t

def text_bbox(text, size):
    # estimativa de largura/altura — Jakarta Sans tende a ter avg ~0.55em
    avg_char = 0.56 * size
    return (len(text) * avg_char, size * 1.05)

random.seed(42)

placed = []  # list of (x, y, w, h)

def fits(x, y, w, h, pad=4):
    # dentro do canvas
    if x < 6 or y < 6 or x + w > W - 6 or y + h > H - 6:
        return False
    for px, py, pw, ph in placed:
        if not (x + w + pad < px or px + pw + pad < x or y + h + pad < py or py + ph + pad < y):
            return False
    return True

def place(text, size):
    w, h = text_bbox(text, size)
    cx, cy = CENTER
    # comeca no centro e espirala para fora
    step_r = 4
    step_theta = 0.35
    for i in range(0, 8000):
        r = step_r * (i ** 0.5)
        theta = step_theta * i
        x = cx + r * math.cos(theta) - w / 2
        y = cy + r * math.sin(theta) - h / 2
        if fits(x, y, w, h):
            placed.append((x, y, w, h))
            return (x + w / 2, y + h * 0.78)  # baseline y aproximada
    return None

# Ordena por frequencia (maior primeiro)
ordered = sorted(WORDS, key=lambda w: -w[1])

svg_elements = []
svg_elements.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid meet" font-family="\'Plus Jakarta Sans\', sans-serif" aria-label="Nuvem de palavras com cores por cluster semantico">')
svg_elements.append('<rect width="100%" height="100%" fill="transparent"/>')

# legenda? deixa pra fora do SVG, na pagina

for text, freq, cluster in ordered:
    size = font_size(freq)
    pos = place(text, size)
    if pos is None:
        continue
    x, y = pos
    color = COLORS[cluster]
    weight = WEIGHTS[cluster]
    # encode entities
    safe = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    svg_elements.append(
        f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size:.1f}" font-weight="{weight}" '
        f'fill="{color}" text-anchor="middle" letter-spacing="-0.01em">{safe}</text>'
    )

svg_elements.append('</svg>')
print('\n'.join(svg_elements))
