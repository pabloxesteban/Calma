const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const AXE = __dirname + '/node_modules/axe-core/axe.min.js';
const pages = ['', 'servicios/', 'contacto/', 'sobre_tatiana/', 'blog/', 'por-que-fallamos-al-intentar-cambiar-conductas/', 'test/', 'testimonios/'];
async function route(ctx){ await ctx.route('**/*', async (route) => {
  const req = route.request();
  if (!/^https?:/.test(req.url())) return route.continue();
  try { const h = { ...req.headers() }; delete h['host'];
    const r = await fetch(req.url(), { method: req.method(), headers: h, body: req.postDataBuffer() || undefined, redirect: 'manual' });
    const body = Buffer.from(await r.arrayBuffer()); const headers = {};
    r.headers.forEach((v, k) => { if (!['content-encoding','content-length','transfer-encoding'].includes(k)) headers[k] = v; });
    await route.fulfill({ status: r.status, headers, body });
  } catch (e) { await route.abort(); } }); }
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args:['--no-proxy-server'] });
  const out = {};
  for (const w of [1280, 390]) {
    const ctx = await b.newContext({ viewport: { width: w, height: 800 }, isMobile: w<1000, hasTouch: w<1000 });
    await route(ctx);
    const p = await ctx.newPage();
    for (const path of pages) {
      const name = path.replace(/\/$/,'') || 'inicio';
      try {
        await p.goto('https://codigocalma.com/' + path, { waitUntil: 'load', timeout: 60000 });
        await p.waitForTimeout(1500);
        await p.addScriptTag({ path: AXE });
        const res = await p.evaluate(async () => { const r = await axe.run(document, { runOnly: { type:'tag', values:['wcag2a','wcag2aa','wcag21a','wcag21aa','wcag22aa','best-practice'] } });
          return r.violations.map(v => ({ id: v.id, impact: v.impact, tags: v.tags.filter(t=>/wcag\d/.test(t)), help: v.help, n: v.nodes.length, nodes: v.nodes.slice(0,6).map(n => ({ t: n.target.join(' '), s: n.failureSummary.slice(0,220), html: n.html.slice(0,160) })) })); });
        const man = await p.evaluate(() => {
          const q = s => [...document.querySelectorAll(s)];
          const vis = e => { const r = e.getBoundingClientRect(); const st = getComputedStyle(e); return r.width>0 && r.height>0 && st.visibility!=='hidden' && st.display!=='none'; };
          return {
            lang: document.documentElement.lang, title: document.title,
            landmarks: { header: q('header,[role=banner]').length, nav: q('nav,[role=navigation]').map(n=>n.getAttribute('aria-label')||'(sin label)'), main: q('main,[role=main]').length, footer: q('footer,[role=contentinfo]').length },
            skip: q('a[href^="#"]').filter(a=>/salt|skip/i.test(a.textContent)).map(a=>a.textContent.trim()+'->'+a.getAttribute('href')),
            headings: q('h1,h2,h3,h4,h5,h6').filter(vis).map(h=>h.tagName+':'+h.textContent.trim().replace(/\s+/g,' ').slice(0,60)),
            imgsNoAlt: q('img').filter(i=>!i.hasAttribute('alt')).map(i=>i.src.split('/').pop()).slice(0,10),
            imgsEmptyAlt: q('img[alt=""]').filter(vis).map(i=>i.src.split('/').pop()).slice(0,10),
            genericLinks: q('a').filter(vis).map(a=>(a.getAttribute('aria-label')||a.textContent).trim().replace(/\s+/g,' ')).filter(t=>/^(leer m[aá]s|continuar|ver m[aá]s|m[aá]s|aqu[ií]|click|saber m[aá]s|read more)\b/i.test(t) || t==='').reduce((m,t)=>(m[t||'(vacío)']=(m[t||'(vacío)']||0)+1,m),{}),
            small24: q('a,button,input,select,textarea,[role=button]').filter(vis).filter(e=>{const r=e.getBoundingClientRect(); return (r.height<24||r.width<24) && !e.closest('p,li')}).map(e=>(e.tagName+':'+(e.getAttribute('aria-label')||e.textContent||e.name||'').trim().slice(0,30)+` ${Math.round(e.getBoundingClientRect().width)}x${Math.round(e.getBoundingClientRect().height)}`)).slice(0,15),
            small44: q('a,button,input,select,textarea,[role=button]').filter(vis).filter(e=>{const r=e.getBoundingClientRect(); return r.height<44||r.width<44}).length,
            overflow: document.documentElement.scrollWidth - innerWidth,
            animated: q('[class*="animat"],[data-aos],[class*="aos"],[class*="wow"]').length,
            reducedMotionCSS: [...document.styleSheets].some(s=>{try{return [...s.cssRules].some(r=>r.media&&/reduced-motion/.test(r.media.mediaText))}catch(e){return false}}),
            clickableDivs: q('[onclick],[data-href],[data-link],[class*="zolo"][class*="link"]').filter(e=>!/^(A|BUTTON)$/.test(e.tagName)).map(e=>e.tagName+'.'+String(e.className).slice(0,60)+' tabindex='+e.getAttribute('tabindex')).slice(0,8),
            forms: q('form').map(f=>({ id:f.id||f.className.slice(0,40), fields: [...f.querySelectorAll('input,textarea,select')].filter(i=>i.type!=='hidden').map(i=>{ const lab = i.labels && i.labels[0] ? i.labels[0].textContent.trim().slice(0,40) : null; return `${i.tagName}[${i.type||''}] name=${i.name} label=${lab} aria=${i.getAttribute('aria-label')} ph=${i.placeholder} req=${i.required||i.getAttribute('aria-required')} ac=${i.autocomplete}`; }) })),
            longParas: q('p').filter(vis).map(p=>p.textContent.trim().split(/\s+/).length).filter(n=>n>80).length,
            paras: q('p').filter(vis).length,
            maxPara: Math.max(0,...q('p').filter(vis).map(p=>p.textContent.trim().split(/\s+/).length)),
            bodyFont: getComputedStyle(document.querySelector('p')||document.body).fontSize + ' / ' + getComputedStyle(document.querySelector('p')||document.body).lineHeight,
            menuToggle: q('button[aria-expanded], .menu-toggle-open, [class*=menu-toggle]').filter(vis).map(e=>e.tagName+' aria-expanded='+e.getAttribute('aria-expanded')+' label='+(e.getAttribute('aria-label')||e.textContent.trim())),
            iframes: q('iframe').map(f=>f.src.slice(0,60)+' title='+f.title),
          };
        });
        // keyboard: tab 25 times, record focus + outline
        const focus = [];
        await p.evaluate(()=>{ document.activeElement && document.activeElement.blur(); window.scrollTo(0,0); });
        for (let i=0;i<25;i++){ await p.keyboard.press('Tab'); focus.push(await p.evaluate(()=>{ const e=document.activeElement; if(!e||e===document.body) return 'BODY'; const s=getComputedStyle(e); const r=e.getBoundingClientRect(); return `${e.tagName}:${(e.getAttribute('aria-label')||e.textContent||'').trim().replace(/\s+/g,' ').slice(0,25)} | outline=${s.outlineStyle} ${s.outlineWidth} ${s.outlineColor} shadow=${s.boxShadow==='none'?'none':'y'} | inView=${r.bottom>0&&r.top<innerHeight}`; })); }
        out[`${name}@${w}`] = { axe: res, man, focus };
        console.error('ok', name, w, res.length);
      } catch(e){ out[`${name}@${w}`] = { error: String(e).slice(0,300) }; console.error('err', name, e.message.slice(0,200)); }
    }
    await ctx.close();
  }
  // reduced motion check on home
  const ctx = await b.newContext({ viewport:{width:1280,height:800}, reducedMotion:'reduce' }); await route(ctx);
  const p = await ctx.newPage(); await p.goto('https://codigocalma.com/', {waitUntil:'load'}); await p.waitForTimeout(300);
  out.reduced = await p.evaluate(()=>[...document.querySelectorAll('*')].filter(e=>{const s=getComputedStyle(e); return (s.animationName!=='none' && parseFloat(s.animationDuration)>0) || (parseFloat(s.transitionDuration)>0.3 && s.transitionProperty!=='all')}).slice(0,15).map(e=>e.tagName+'.'+String(e.className).slice(0,70)+' anim='+getComputedStyle(e).animationName+' '+getComputedStyle(e).animationDuration+' trans='+getComputedStyle(e).transitionDuration));
  await b.close();
  require('fs').writeFileSync(__dirname+'/out.json', JSON.stringify(out,null,1));
})();
