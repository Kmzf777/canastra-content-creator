# Lista única de eventos do Reel 10 (tempos do corte v2, a 30 fps).
# Cada evento: (tempo_s, palavra_ancora, camada, o_que_acontece, som, nivel_db relativo à voz)
# camada: CAM (câmera/layout), TXT (texto), OBJ (objeto/colagem), TRANS (transição de capítulo)
E = [
# ---------------- CAPÍTULO 0 · gancho (fundo real, cor natural) ----------------
(0.00, '(quadro 0)', 'OBJ', 'xícara de vidro com café clarinho (G1) já no quadro, canto inferior esquerdo, girando 2° e subindo devagar; câmera já em push 1,08→1,14', '—', None),
(0.60, 'chamou', 'TXT', 'aspas rabiscadas se desenham ao lado da cabeça (8 q): alguém disse algo', 'rabisco', -20),
(1.10, 'café', 'TXT', 'etiqueta Dymo "CAFÉ" pousa na xícara', 'fita Dymo', -18),
(1.60, 'chafé', 'TXT', '"CHAFÉ?" pintado gigante ATRÁS da cabeça (oclusão, 80% legível) + soco de zoom +6% em 4 q; a etiqueta da xícara vira "CHAFÉ?"', 'carimbo grave', -9),
(2.34, 'errou', 'TXT', 'traço creme risca "CHAFÉ?" (8 q, termina com a palavra)', 'rabisco', -18),
(2.66, 'duas', 'TXT', '"2" carimbado grande à direita', 'pop', -15),
(3.04, 'vezes', 'TXT', '"ERROS" completa "2 ERROS"', 'pop', -15),
(3.50, 'Eu', 'CAM', 'recuo de 1,14 para 1,00 em 10 q: aparecem torrador e sacas; fundo limpo anda 0,96 e o Rafael 1,00 (paralaxe real)', 'whoosh suave', -16),
(3.86, 'Rafael', 'TXT', 'Dymo "RAFAEL" desliza no peito', 'fita Dymo', -18),
(4.36, 'Café', 'OBJ', 'logo Café Canastra (arquivo real) carimba na parede preta, alto à esquerda', 'carimbo leve', -14),
(4.64, 'Canastra', 'OBJ', 'polaroide real da lavoura (base verificada) entra girando 8° e pousa no alto à direita', 'papel', -16),
(5.09, '(corte interno)', 'CAM', 'troca para 1,10 + deriva para a direita, em direção ao torrador; a polaroide sai deslizando', 'slide', -18),
(5.56, 'aqui', 'TXT', 'seta rabiscada começa a se desenhar até o torrador (termina em "torrefação")', 'rabisco', -18),
(6.12, 'torrefação', 'OBJ', 'etiqueta de barbante "TORREFAÇÃO · UBERLÂNDIA" pendurada no torrador, balançando (presa ao fundo, anda com a paralaxe)', 'tick de papel', -18),
(6.88, '(fim do bloco)', 'TRANS', 'folha kraft varre a tela em 7 q e deixa a TELA DIVIDIDA: painel kraft em cima, Rafael embaixo', 'papel rápido (pico 2 q antes)', -12),
# ---------------- CAPÍTULO 1 · erro 1 (tela dividida kraft) ----------------
(7.18, 'primeiro', 'TXT', 'pílula "ERRO 1" fixa no canto do painel (fica até 19,1 s)', '—', None),
(7.48, 'erro', 'TXT', 'carimbo "ERRO 1" grande no centro do painel, encolhe até a pílula em 12 q', 'carimbo', -10),
(7.86, 'achar', 'OBJ', 'xícara de vidro clarinha (G1) sobe para o painel (10 q, assenta)', 'slide', -18),
(8.46, 'clarinho', 'OBJ', 'post-it "CLARINHO" preso com tachinha ao lado da xícara', 'tachinha', -16),
(9.38, 'fraco', 'OBJ', 'post-it "FRACO" entra; um "=" rabiscado liga os dois', 'tachinha', -16),
(9.62, '(pausa)', 'TXT', 'carimbo "≠" em #C8661E (acento da cena) esmaga o "="', 'carimbo', -10),
(9.80, '(fim do bloco)', 'CAM', 'Rafael embaixo passa a 1,15; o painel desliza para a esquerda e entra o quadro seguinte', 'slide', -18),
(10.07, 'torra', 'OBJ', 'recorte de grão torrado entra no painel com Dymo "TORRA"', 'pop', -16),
(10.77, 'intensidade', 'OBJ', 'mostrador de ponteiro "INTENSIDADE" se desenha (traço creme, sem escala de cor)', 'rabisco', -18),
(11.23, 'sim', 'TXT', '✓ rabiscado ao lado de "TORRA → INTENSIDADE"; o ponteiro sobe um degrau', 'tick', -18),
(11.83, 'precisa', 'OBJ', 'marca "PONTO" aparece no mostrador', 'tick', -18),
(12.05, 'passar', 'OBJ', 'ponteiro desliza até a marca', 'slide curto', -18),
(12.55, 'ponto', 'OBJ', 'ponteiro FREIA exatamente na marca (3% de ultrapassagem); carimbo "NO PONTO"', 'carimbo leve', -12),
(13.41, 'intenso', 'TXT', '"INTENSO" grande + soco de zoom no Rafael (+8%, 4 q)', 'pop', -14),
(13.84, '(fim do bloco)', 'TRANS', 'chicote de papel (7 q): tela cheia de kraft, Rafael vira um círculo no canto inferior direito', 'chicote (pico 2 q antes)', -12),
(14.37, 'intensidade', 'OBJ', 'filtro com pó (G5) no centro; mostrador pequeno no canto com o ponteiro tremendo "?"', 'pop', -16),
(15.01, 'Coloca', 'OBJ', 'mão com colher entra pela direita (8 q)', 'slide', -18),
(15.53, 'pouquinho', 'OBJ', 'colher despeja: pó caindo em stop-motion (10 poses/s) + "+1"', 'grãos/pó', -14),
(16.31, 'pó', 'OBJ', 'segunda colherada "+2" + Dymo "PÓ"', 'grãos/pó', -14),
(16.45, '(fim do bloco)', 'TRANS', 'chicote de volta para a tela dividida', 'chicote', -12),
(16.86, 'se', 'OBJ', 'ponteiro do mostrador sobe com o pó (a intensidade vem do pó)', 'tick', -18),
(17.12, 'intensifica', 'TXT', '"INTENSIFICA" engorda de 100% para 120% em 15 q', 'pop', -14),
(18.00, 'sabor', 'OBJ', 'xícara clarinha volta com etiqueta "SABOR"', 'tink de vidro', -18),
(18.48, 'todo', 'TXT', '✓ rabiscado em "SABOR"', 'rabisco', -20),
(19.05, '(fim do bloco)', 'TRANS', 'tela cheia; o fundo limpo escurece para #14100D em 8 q, o Rafael continua aceso (troca de capítulo)', 'grave abafado', -12),
# ---------------- CAPÍTULO 2 · erro 2 (fundo escuro, investigação) ----------------
(19.94, 'segundo', 'TXT', '"2" gigante creme ATRÁS da cabeça', 'pop grave', -12),
(20.34, 'erro', 'TXT', '"ERRO" completa "ERRO 2"; a pílula do canto vira 2', 'carimbo', -10),
(20.78, 'esse', 'CAM', 'push lento 1,00→1,12 em 1,5 s (tensão)', '—', None),
(21.42, 'ninguém', 'TXT', 'Dymo "QUASE NINGUÉM CONTA" desliza', 'fita Dymo', -18),
(21.88, 'conta', 'OBJ', 'lupa entra do canto inferior e para sobre o Dymo', 'slide', -18),
(22.16, '(fim do bloco)', 'CAM', 'tela dividida escura: em cima, cortiça (quadro de investigação); Rafael embaixo a 1,10', 'slide', -16),
(22.48, 'extra', 'OBJ', 'pacote genérico SEM MARCA (desenhado em código) pendurado por tachinha, etiqueta "MUITO EXTRAFORTE"', 'tachinha', -16),
(23.16, 'passa', 'OBJ', 'o mostrador volta na cortiça; o ponteiro anda', 'tick', -18),
(23.68, 'ponto', 'OBJ', 'ponteiro PASSA da marca e continua', 'tick duplo', -16),
(24.24, 'propósito', 'TXT', '"DE PROPÓSITO" pintado em #C8661E, carimbado na diagonal; a imagem congela em P&B na pausa até 24,91', 'carimbo grave', -9),
(24.91, '(fim do bloco)', 'CAM', 'descongela; Rafael em tela cheia a 1,10, fundo escuro', '—', None),
(25.10, 'Isso', 'OBJ', 'lupa grande atravessa rente à lente (primeiro plano, profundidade 1,3)', 'whoosh suave', -16),
(26.18, 'defeito', 'TRANS', 'zoom pelo aro da lupa: tela cheia de cortiça com peneira de classificação; Rafael em círculo; "DEFEITO" em #C8661E', 'whoosh + carimbo', -12),
(26.40, '(rajada)', 'OBJ', 'rajada de 7 defeitos da biblioteca (concha, filme, fungo, imaturo, preto partido, quaker, quebrado), 4 q cada, dentro da lente', 'tick por grão', -20),
(27.13, 'preto', 'OBJ', 'grão preto preso com tachinha + etiqueta "PRETO"', 'tachinha', -15),
(27.76, 'ardido', 'OBJ', 'grão ardido + etiqueta "ARDIDO"', 'tachinha', -15),
(28.36, 'furado', 'OBJ', 'grão brocado + etiqueta "BROCA"', 'tachinha', -15),
(28.92, 'broca', 'CAM', 'lupa passa sobre os furos do brocado (zoom de 1,10 na cena)', '—', None),
(29.41, 'Passando', 'OBJ', 'fita-crepe começa a desenrolar pela esquerda', 'fita puxada', -14),
(30.37, 'tudo', 'OBJ', 'fita cobre o 1º grão', 'fita', -18),
(30.81, 'mesmo', 'OBJ', 'fita cobre o 2º grão', 'fita', -18),
(30.99, 'amargo', 'TXT', '"AMARGO" escrito à mão na fita; ela cobre o 3º grão', 'rabisco', -16),
(31.61, 'defeito', 'OBJ', 'lupa passa sobre a fita e não acha nada; as etiquetas penduradas continuam aparecendo', 'slide', -20),
(31.89, 'some', 'TXT', 'carimbo "ESCONDIDO" (terra/creme)', 'carimbo', -10),
(32.17, '(fim do bloco)', 'TRANS', 'chicote de volta: Rafael em close a 1,15, fundo escuro mais leve (respiro)', 'chicote', -12),
(33.20, 'coloca', 'OBJ', 'colher vazia entra sobre uma xícara de café preto (recorte xícara)', 'slide', -18),
(33.56, 'açúcar', 'OBJ', '1º torrão (G3) cai da colher e quica', 'tink', -18),
(34.38, 'aguentar', 'OBJ', '2º torrão', 'tink', -18),
(34.74, 'tomar', 'OBJ', '3º torrão; o Rafael meio-sorri', 'tink', -18),
(35.23, '(fim do bloco)', 'TRANS', 'o papel escuro RASGA e revela o fundo claro creme (capítulo 3: nada a esconder)', 'rasgo de papel', -10),
# ---------------- CAPÍTULO 3 · o nosso (claro, creme + lavoura real) ----------------
(35.49, 'café', 'OBJ', 'foto real da lavoura presa com fita na parede atrás dele (impressão, não cenário)', 'fita', -18),
(36.13, 'nada', 'OBJ', 'lupa passa pela lavoura e aparece um ✓ limpo', 'rabisco', -18),
(36.63, 'esconder', 'TXT', '"NADA PRA ESCONDER" em terra #3B2A1F atrás da cabeça', 'pop', -14),
(37.41, 'parar', 'CAM', 'tela dividida clara: painel creme em cima, Rafael embaixo', 'slide', -16),
(37.79, 'marrom', 'OBJ', 'packshot REAL do Suave sobe e assenta (sem girar, sem deformar); "MARROM" em #C8661E', 'thump', -12),
(38.12, '(fim do bloco)', 'CAM', 'Rafael embaixo passa a 1,15', '—', None),
(38.81, 'torra', 'OBJ', 'etiqueta de barbante "TORRA MÉDIA" pendurada ao lado do pacote (nunca sobre logo ou selo)', 'tick de papel', -18),
(39.73, 'luz', 'OBJ', 'xícara clarinha (G1) entra ao lado do Suave; sombra de folhas passa pelo painel', 'slide', -18),
(39.89, 'atravessa', 'OBJ', 'varredura de luz creme (não dourada) atravessa a xícara em 12 q', 'brilho', -20),
(40.83, 'xícara', 'OBJ', 'a xícara inclina 2°', 'tink de vidro', -18),
(41.20, '(corte interno)', 'CAM', 'a tela dividida inverte: imagem embaixo, Rafael em cima', 'slide', -16),
(41.51, 'gosto', 'OBJ', 'traço creme sai da xícara e começa uma seta curva', 'golinho', -16),
(42.97, 'chocolate', 'TXT', '"CHOCOLATE" na ponta da seta (só a palavra, sem foto de chocolate)', 'pop', -14),
(43.66, '(corte interno)', 'CAM', 'volta: Rafael embaixo a 1,10', 'slide', -18),
(43.89, 'ainda', 'OBJ', 'a seta continua para a segunda ponta', 'rabisco', -20),
(44.27, 'azedinho', 'TXT', 'Dymo "AZEDINHO"', 'fita Dymo', -18),
(44.97, 'fruta', 'OBJ', 'cereja vermelha (a fruta do próprio café) pousa na ponta da seta', 'pop', -14),
(45.37, 'fim', 'TXT', '✓ rabiscado', 'rabisco', -20),
(45.64, '(fim do bloco)', 'TRANS', 'cartão-receita kraft sobe e ocupa a metade de cima', 'papel', -14),
# ---------------- CAPÍTULO 4 · a receita (cartão kraft) ----------------
(46.47, 'Canastra', 'OBJ', 'logo Café Canastra carimba no topo do cartão (segunda vez, outra posição)', 'carimbo leve', -14),
(47.27, 'conta', 'OBJ', 'balança (G4) entra no cartão', 'slide', -18),
(47.57, '50', 'TXT', 'visor da balança conta de 0 a 50 em 10 q + "50 g" grande em Plex Mono', 'tick + carimbo', -12),
(48.63, 'pó', 'OBJ', 'filtro com pó (G5) pousa na balança', 'grãos/pó', -16),
(49.17, 'meio', 'OBJ', 'jarra medidora (G6) entra', 'tink de vidro', -18),
(49.39, 'litro', 'TXT', '"500 ml" carimbado', 'carimbo', -12),
(49.87, 'água', 'OBJ', 'a água sobe na jarra até a marca', 'água curta', -18),
(50.00, '(fim do bloco)', 'CAM', 'Rafael embaixo passa a 1,15', '—', None),
(50.68, 'intenso', 'OBJ', 'mostrador pequeno: o ponteiro sobe', 'tick', -18),
(51.15, '(corte interno)', 'CAM', 'o cartão sobe e sai (ficou 3,6 s na tela para quem quiser salvar); Rafael em tela cheia a 1,10', 'slide', -16),
(51.59, 'primeiro', 'TXT', 'eco: "ERRO 1" volta igual ao 7,48 por 0,5 s, atrás da cabeça', 'whoosh reverso', -16),
(52.27, 'Coloca', 'OBJ', 'a mão com colher do 15,01 entra rápido', 'slide', -18),
(52.83, 'pouquinho', 'OBJ', 'colherada "+1"', 'grãos/pó', -16),
(53.75, 'pó', 'TXT', '"+ PÓ" (o mesmo cartão do 16,31)', 'pop', -14),
(53.84, '(fim do bloco)', 'TRANS', 'tudo sai num só movimento; volta o fundo real com a cor natural (capítulo final)', 'whoosh', -12),
# ---------------- CAPÍTULO 5 · fecho e loop ----------------
(54.11, 'agora', 'OBJ', 'rajada de recapitulação no lado direito: CHAFÉ? → ERRO 1 → ERRO 2 → Suave, 7 q cada', 'tick por cartão', -20),
(55.07, 'tempo', 'OBJ', 'a rajada termina no Suave, que fica', 'pop', -16),
(55.30, '(corte interno)', 'CAM', 'close a 1,14, o mesmo enquadramento do quadro 0 (prepara o loop)', '—', None),
(55.50, 'manda', 'OBJ', 'aviãozinho de papel rabiscado sai da mão dele e voa para fora do quadro', 'whoosh curto', -14),
(56.10, 'amigo', 'TXT', '"MANDA PRO AMIGO" pequeno em creme', 'pop', -16),
(56.78, 'isso', 'OBJ', 'a xícara clarinha (G1) volta ao canto inferior esquerdo, igual ao quadro 0', 'slide', -18),
(57.26, 'chafé', 'TXT', '"CHAFÉ?" volta atrás da cabeça, igual ao 1,60; o último quadro emenda no primeiro', 'carimbo grave', -9),
]

CORTES = [5.09, 6.95, 9.80, 13.90, 16.51, 19.11, 22.16, 24.91, 26.71, 27.55, 28.28, 29.31,
          32.23, 35.29, 38.12, 41.20, 43.66, 45.70, 50.00, 51.15, 53.90, 55.30]
FIM = 57.66

if __name__ == '__main__':
    import json, sys
    import numpy as np
    t = np.array([e[0] for e in E])
    assert all(np.diff(t) >= 0), 'eventos fora de ordem'
    gaps = np.diff(np.concatenate([[0], t, [FIM]]))
    ini = np.concatenate([[0], t])
    print('eventos', len(E), '| por 10 s', round(len(E) / FIM * 10, 1),
          '| intervalo mediano', round(float(np.median(gaps)), 2),
          '| maior intervalo', round(float(gaps.max()), 2), 's a partir de', round(float(ini[gaps.argmax()]), 2))
    top = sorted(zip(gaps, ini), reverse=True)[:5]
    print('5 maiores intervalos:', [(round(float(g), 2), round(float(i), 2)) for g, i in top])
    sem = [s for s in range(int(np.ceil(FIM))) if not any(s <= x < s + 1 for x in t)]
    print('segundos sem evento novo:', sem)
    por_s = [sum(1 for x in t if s <= x < s + 1) for s in range(int(np.ceil(FIM)))]
    print('máx eventos num segundo:', max(por_s), 'no segundo', por_s.index(max(por_s)))
    q = [round(x * 30) for x in t]
    print('quadros com 2 eventos:', sorted(x for x in set(q) if q.count(x) > 1))
    desc = [c for c in CORTES
            if not any(abs(c - e[0]) <= 0.12 and e[2] in ('CAM', 'TRANS') for e in E)
            and not (26.18 <= c <= 32.17)]
    print('cortes do corte seco sem troca de enquadramento ou transição (±0,12 s):', desc)
    json.dump([dict(t=e[0], quadro=round(e[0] * 30), palavra=e[1], camada=e[2], acao=e[3], som=e[4], db=e[5]) for e in E],
              open(sys.argv[1], 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
