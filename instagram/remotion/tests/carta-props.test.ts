import {expect, test} from 'vitest';
import {
  MOLDES_ESTATICO,
  areaImagem,
  areaSegura,
  faixaDeTexto,
  validarProps,
} from '../src/estatico/moldes';

test('o molde cartao-produto declara os mesmos campos que o catalogo Python', () => {
  // Se esta lista divergir de MOLDES["cartao-produto"].campos em
  // instagram/estaticos/catalogo.py, a costura quebra em silencio.
  expect(MOLDES_ESTATICO['cartao-produto'].campos).toEqual([
    'preco',
    'altitude',
    'local',
  ]);
});

test('cartao-produto e 1080x1350, que e 4:5 com os dois lados pares', () => {
  const m = MOLDES_ESTATICO['cartao-produto'];
  expect(m.largura).toBe(1080);
  expect(m.altura).toBe(1350);
  // h264 exige lado par; a licao 26 registra 360x639 descendo para 638 em
  // silencio, com exit 0, e a peca saindo 0,3% esticada.
  expect(m.largura % 2).toBe(0);
  expect(m.altura % 2).toBe(0);
  expect(m.largura * 5).toBe(m.altura * 4);
});

test('a area segura respeita a margem title-safe de 5 a 8% nos dois eixos', () => {
  const m = MOLDES_ESTATICO['cartao-produto'];
  const s = areaSegura(m);
  expect(s.x).toBeGreaterThanOrEqual(Math.round(m.largura * 0.05));
  expect(s.x).toBeLessThanOrEqual(Math.round(m.largura * 0.08));
  expect(s.y).toBeGreaterThanOrEqual(Math.round(m.altura * 0.05));
  expect(s.y).toBeLessThanOrEqual(Math.round(m.altura * 0.08));
});

test('a area segura fecha com as dimensoes do molde', () => {
  const m = MOLDES_ESTATICO['cartao-produto'];
  const s = areaSegura(m);
  expect(s.x + s.largura + s.x).toBe(m.largura);
  expect(s.y + s.altura + s.y).toBe(m.altura);
});

test('a margem do estatico NAO herda a base de 16% do reel', () => {
  // O layout de reel usa base 16% para liberar a interface do Reels. Num 4:5
  // de feed essa interface nao existe por cima, entao herdar seria perder um
  // sexto do quadro por um motivo que nao se aplica.
  const m = MOLDES_ESTATICO['cartao-produto'];
  const s = areaSegura(m);
  const margemDeBaixo = (m.altura - s.y - s.altura) / m.altura;
  expect(margemDeBaixo).toBeLessThan(0.1);
});

test('props sem um campo do molde e recusado', () => {
  expect(() =>
    validarProps('cartao-produto', {preco: 'R$ 31,70', altitude: '1.250 m'}),
  ).toThrow(/local/);
});

test('props com campo extra e recusado', () => {
  expect(() =>
    validarProps('cartao-produto', {
      preco: 'R$ 31,70',
      altitude: '1.250 m',
      local: 'Medeiros, MG',
      intruso: 'x',
    }),
  ).toThrow(/intruso/);
});

test('props com campo vazio e recusado', () => {
  expect(() =>
    validarProps('cartao-produto', {
      preco: '   ',
      altitude: '1.250 m',
      local: 'Medeiros, MG',
    }),
  ).toThrow(/vazios/);
});

test('molde desconhecido e recusado e lista os validos', () => {
  expect(() => validarProps('inventado', {})).toThrow(/cartao-produto/);
});

test('props completo passa e devolve o texto na ordem do molde', () => {
  const r = validarProps('cartao-produto', {
    // de proposito fora de ordem: a ordem de saida e a do MOLDE, nao a do objeto
    local: 'Medeiros, MG',
    preco: 'R$ 31,70',
    altitude: '1.250 m',
  });
  expect(r).toEqual(['R$ 31,70', '1.250 m', 'Medeiros, MG']);
});

test('a faixa de texto fica no rodape e nao invade a area da imagem', () => {
  const m = MOLDES_ESTATICO['cartao-produto'];
  const f = faixaDeTexto(m);
  const img = areaImagem(m);

  // encostadas, sem sobreposicao e sem buraco
  expect(img.y + img.altura).toBe(f.y);
  expect(f.y + f.altura).toBe(m.altura);
  expect(f.largura).toBe(m.largura);
});

test('a faixa nao come mais de um terco do quadro', () => {
  const m = MOLDES_ESTATICO['cartao-produto'];
  expect(faixaDeTexto(m).altura / m.altura).toBeLessThan(1 / 3);
});

test('creme sobre terra passa o piso WCAG de 4,5:1 com folga', () => {
  // E a razao de a faixa existir: sobreposto ao packshot o creme media 1,09:1
  // na terceira linha. Aqui o contraste e constante do molde, nao loteria da foto.
  const lum = (hex: string) => {
    const n = parseInt(hex.slice(1), 16);
    const canais = [(n >> 16) & 255, (n >> 8) & 255, n & 255].map((v) => {
      const c = v / 255;
      return c <= 0.03928 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4;
    });
    return 0.2126 * canais[0] + 0.7152 * canais[1] + 0.0722 * canais[2];
  };
  const a = lum('#F1ECE0');
  const b = lum('#3B2A1F');
  const razao = (Math.max(a, b) + 0.05) / (Math.min(a, b) + 0.05);
  expect(razao).toBeGreaterThan(4.5);
});
