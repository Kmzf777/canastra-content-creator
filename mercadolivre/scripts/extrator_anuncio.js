// Leitor de página de anúncio do ML (www.mercadolivre.com.br/.../p/ ou /up/), medido em 08/10/2026.
// Grave em localStorage.__pdpx numa aba de www.mercadolivre.com.br e rode eval(localStorage.__pdpx)
// em cada anúncio (navigate -> wait 5; página de produto renderiza mesmo com a janela oculta).
// Acumula em localStorage.__pdp (JSON). Baixe de uma aba nova em www. (um download por aba).
// Ficha vem das linhas .andes-table__row (o bloco visível mostra só as principais).
// Fotos = .ui-pdp-thumbnail (inclui a miniatura do vídeo quando há).
(()=>{const q=s=>document.querySelector(s);const tx=(s,n=4000)=>{const e=q(s);return e?e.innerText.replace(/\n{2,}/g,'\n').trim().slice(0,n):''};
const g=q('.ui-pdp-gallery');const thumbs=g?g.querySelectorAll('.ui-pdp-thumbnail').length:0;
const video=!!(g&&g.querySelector('[class*="clip"],[class*="video"],video,[aria-label*="ídeo"]'))||!!q('[class*="clips"]');
const o={url:location.href.split('?')[0],titulo:tx('.ui-pdp-title',300),sub:tx('.ui-pdp-subtitle',200),header:tx('.ui-pdp-header',500),preco:tx('.ui-pdp-price',400),fotos:thumbs,video,
variacoes:tx('.ui-pdp-variations',800),destaques:tx('.ui-vpp-highlighted-specs',1500),ficha:[...document.querySelectorAll('.andes-table__row, tr')].map(r=>r.innerText.replace(/\s+/g,' ').trim()).join(' ; ').slice(0,3000),descricao:tx('.ui-pdp-description',3500),
estoque:tx('.ui-pdp-stock-and-full',300)+' '+tx('.ui-pdp-stock-information',200),vendedor:tx('.ui-pdp-seller',600)||tx('.ui-pdp-seller-summary',600),outros:tx('.ui-pdp-other-sellers',600),
perguntas:tx('.ui-pdp-questions',600),opinioes:tx('[class*="ui-review-capability"]',2500)||tx('[class*="reviews"]',2000),niveis:(document.body.innerText.match(/\d+ unidades\s*\n?R\$[^\n]*\n?[^\n]*/g)||[]).slice(0,6).join(' / ')};
const arr=JSON.parse(localStorage.__pdp||'[]').filter(x=>x.url!==o.url);arr.push(o);localStorage.__pdp=JSON.stringify(arr);
return arr.length+' | '+o.titulo+' | fotos '+o.fotos+' video '+video})()
