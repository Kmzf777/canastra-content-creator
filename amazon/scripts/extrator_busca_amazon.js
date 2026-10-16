// Extrator de resultados da busca da Amazon Brasil (amazon.com.br/s?k=...), medido em 14/10/2026.
// A busca renderiza mesmo com a janela do Chrome oculta. Uso: navigate -> wait 4 -> javascript_tool
// com este arquivo. Acumula em localStorage.__amz (uma linha TSV por ASIN e termo).
// Colunas: termo, pagina, pos, asin, patrocinado, selo (Escolha da Amazon / Mais vendido), titulo,
//          nota, avaliacoes, compras_mes, preco, preco_lista, prime, entrega, cupom
(()=>{const q=new URLSearchParams(location.search);const termo=q.get('k');const pag=q.get('page')||'1';
const num=s=>{if(!s)return '';const m=s.replace(/\./g,'').match(/(\d+(?:,\d+)?)\s*(mil)?/);if(!m)return '';return String(Math.round(parseFloat(m[1].replace(',','.'))*(m[2]?1000:1)))};
const L=[];let pos=0;
for(const c of document.querySelectorAll('[data-component-type="s-search-result"]')){const asin=c.getAttribute('data-asin');if(!asin)continue;pos++;
const t=c.innerText;const tit=(c.querySelector('h2')?.innerText||'').replace(/\s+/g,' ').trim();
const pat=/Patrocinado/.test(t)?'PAT':'';const selo=/Escolha da Amazon/.test(t)?'ESCOLHA':/Mais vendido/.test(t)?'MAISVENDIDO':'';
const nota=(t.match(/(\d,\d) de 5 estrelas/)||[,''])[1];const aval=num((c.querySelector('[aria-label*="classificações"], a[href*="customerReviews"] span')?.innerText||(t.match(/\(([\d.,]+ ?mil|[\d.]+)\)/)||[,''])[1]));
const compras=num((t.match(/Mais de ([\d.,]+ ?(?:mil)?) compras? no mês passado/)||[,''])[1]);
const preco=(c.querySelector('.a-price:not(.a-text-price) .a-offscreen')?.textContent||'').replace(/[^\d,]/g,'');
const lista=(c.querySelector('.a-price.a-text-price .a-offscreen')?.textContent||'').replace(/[^\d,]/g,'');
const prime=c.querySelector('i.a-icon-prime, [aria-label*="Prime"]')?'PRIME':'';
const ent=(t.match(/Entrega[^\n|]*/)||[''])[0].slice(0,80);const cup=(t.match(/(Economize[^\n]*cupom[^\n]*|R\$ ?[\d,]+ off|\d+% off)/i)||[''])[0].slice(0,40);
L.push([termo,pag,pos,asin,pat,selo,tit.slice(0,160),nota,aval,compras,preco,lista,prime,ent,cup].join('\t'))}
localStorage.__amz=(localStorage.__amz||'')+L.join('\n')+'\n';return L.length+' acc='+localStorage.__amz.split('\n').length})()
