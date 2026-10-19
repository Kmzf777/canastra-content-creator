// Extrator de cards da busca do ML (lista.mercadolivre.com.br), medido em 08/10/2026.
// Uso: grave em localStorage.__ext2 UMA vez numa aba de lista.mercadolivre.com.br
// (localStorage é por origem: www. e vendedores. NÃO enxergam), e em cada busca:
//   navigate -> wait 3 -> screenshot (força o render se a janela estiver oculta) -> wait 3
//   -> javascript_tool: eval(localStorage.__ext2)
// Acumula em localStorage.__acc. No fim, baixe de uma ABA NOVA na mesma origem
// (o Chrome só libera o primeiro download automático de cada aba — lição 52).
// Colunas: termo, pos, titulo, preco_vitrine (Pix), riscado, outros_meios, vendidos, nota, tags, url
// tags: PAT patrocinado · FULL · FG frete grátis · MV mais vendido · LOJA oficial · SUPER Full Super · PIX
(()=>{const amt=e=>{if(!e)return '';const f=e.querySelector('.andes-money-amount__fraction')?.textContent.replace(/\./g,'')||'';const ct=e.querySelector('.andes-money-amount__cents')?.textContent||'0';return f?(+f+ +ct/100).toFixed(2):''};
const cs=[...document.querySelectorAll('[class*="poly-card"]')].filter(c=>!c.parentElement.closest('[class*="poly-card"]'));
const seen=new Set();const L=[];let pos=0;
const total=(document.querySelector('.ui-search-search-result__quantity-results')?.textContent||'').trim();
for(const c of cs){const t=(c.querySelector('.poly-component__title')?.textContent||'').trim();if(!t)continue;
const cur=amt(c.querySelector('.poly-price__current .andes-money-amount'));const prev=amt(c.querySelector('s.andes-money-amount, .andes-money-amount--previous'));
const rest=c.innerText.replace(/\n+/g,' ¦ ');
const al=[...c.querySelectorAll('[aria-label]')].map(e=>e.getAttribute('aria-label'));
const monies=[...c.querySelectorAll('.andes-money-amount[aria-label]')].map(e=>e.getAttribute('aria-label')).filter(x=>!/^Antes/.test(x));
const p=s=>{const m=(s||'').match(/([\d\.]+) reais?(?: com (\d+) centavos?)?/);return m?(+m[1].replace(/\./g,'')+(m[2]?+m[2]/100:0)).toFixed(2):''};
const outros=/em outros meios/.test(rest)?p(monies[1]):'';
const hid=[...c.querySelectorAll('.andes-visually-hidden')].map(e=>e.textContent).join(' ');
const rat=(hid.match(/Classificação ([\d.]+)/)||[,''])[1];const vend=(hid.match(/Mais de ([\d\.]+ ?(mil)?) produtos? vendidos?/)||rest.match(/\+(\d[\d\.]* ?(mil)?) vendid/)||[,''])[1];
const full=al.some(x=>/^Full/i.test(x)||x==='FULL')||/\bFULL\b/.test(rest);const loja=al.includes('Loja oficial');
const tags=[/Patrocinado/.test(rest)?'PAT':'',full?'FULL':'',/Frete grátis/i.test(rest)?'FG':'',/MAIS VENDIDO/.test(rest)?'MV':'',/OFERTA DO DIA/.test(rest)?'OD':'',loja?'LOJA':'',al.includes('Full Super')?'SUPER':'',/no Pix/.test(rest)?'PIX':''].filter(Boolean).join(',');
const href=[...c.querySelectorAll('a')].map(a=>a.href).find(h=>/\/p\/MLB|MLB-?\d/.test(h))||'';
const k=t+cur;if(seen.has(k))continue;seen.add(k);pos++;L.push([decodeURIComponent(location.pathname.slice(1))+' ('+total+')',pos,t,cur,prev,outros,vend,rat,tags,href.split('#')[0].split('?')[0]].join('\t'))}
localStorage.__acc=(localStorage.__acc||'')+L.join('\n')+'\n';return total+' / '+L.length+' acc='+localStorage.__acc.split('\n').length})()
