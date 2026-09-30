import {registerRoot} from 'remotion';

// Import de EFEITO COLATERAL, e por isso vem antes da raiz: este modulo carrega
// Archivo Black, Inter e IBM Plex Mono de arquivo local e abre um `delayRender`
// que segura o primeiro frame ate as tres estarem aplicadas. Sem ele o Chrome
// headless desenha Times New Roman e nao reclama -- foi o que aconteceu com
// todos os renders anteriores a 30/09/2026. Ver `identidade/tipografia.ts`.
//
// Esta aqui, no entrypoint, para valer para QUALQUER composicao registrada, e
// nao so para as que hoje tem texto.
import './identidade/tipografia';

import {Raiz} from './motor/Raiz';

registerRoot(Raiz);
