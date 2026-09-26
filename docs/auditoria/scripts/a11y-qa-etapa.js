// QA de accesibilidad por etapa: axe-core + encabezados + foco + reflow 320 + menú mobile + test + reduced motion.
// Uso: NODE_USE_ENV_PROXY=1 AXE_PATH=/ruta/axe.min.js node docs/auditoria/scripts/a11y-qa-etapa.js --preview|--live salida.json
// --preview sirve el documento principal desde staging/preview/build/<slug>.html; el resto se pide a producción con fetch de Node (TLS verificado).
const fs=require('fs'), path=require('path');
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const AXE = process.env.AXE_PATH || __dirname + '/node_modules/axe-core/axe.min.js';
const BUILD=path.join(__dirname, '../../../staging/preview/build');
const [, , mode, outFile] = process.argv;
const PAGES = { inicio:'', servicios:'servicios/', contacto:'contacto/', sobre_tatiana:'sobre_tatiana/', blog:'blog/',
  'por-que-fallamos':'por-que-fallamos-al-intentar-cambiar-conductas/', test:'test/', testimonios:'testimonios/',
  herramientas:'herramientas/', 'bienestar-digital':'bienestar-digital/', 'descargas-2':'descargas-2/' };
const fileFor = (p) => path.join(BUILD, (p.replace(/\/$/, '').replace(/\//g, '_') || 'home') + '.html');
async function route(ctx){ await ctx.route('**/*', async (route) => {
  const req = route.request(); const url=req.url(); if (!/^https?:/.test(url)) return route.continue();
  const u=new URL(url);
  if (mode==='--preview' && u.hostname==='codigocalma.com' && u.pathname.startsWith('/wp-content/plugins/codigo-calma/')) {
    const f=path.join(__dirname,'../../..',decodeURIComponent(u.pathname)); if (fs.existsSync(f)) return route.fulfill({status:200, body:fs.readFileSync(f), contentType:f.endsWith('.woff2')?'font/woff2':'text/css', headers:{'access-control-allow-origin':'*'}}); }
  if (mode==='--preview' && req.resourceType()==='document' && u.hostname==='codigocalma.com') {
    const f=fileFor(u.pathname.replace(/^\//,'')); if (fs.existsSync(f)) return route.fulfill({status:200, contentType:'text/html; charset=utf-8', body:fs.readFileSync(f)}); }
  try { const h = { ...req.headers() }; delete h['host'];
    const r = await fetch(url, { method: req.method(), headers: h, body: req.postDataBuffer() || undefined, redirect: 'manual' });
    const body = Buffer.from(await r.arrayBuffer()); const headers = {};
    r.headers.forEach((v, k) => { if (!['content-encoding','content-length','transfer-encoding'].includes(k)) headers[k] = v; });
    await route.fulfill({ status: r.status, headers, body }); } catch (e) { await route.abort(); } }); }
const AXRUN = async () => { const r = await axe.run(document, { runOnly: { type:'tag', values:['wcag2a','wcag2aa','wcag21a','wcag21aa','wcag22aa','best-practice'] } });
  return r.violations.map(v => ({ id: v.id, impact: v.impact, n: v.nodes.length, nodes: v.nodes.slice(0,8).map(n => ({ t: n.target.join(' ').slice(0,120), s: (n.failureSummary.match(/contrast of [\d.]+ \(foreground color: #\w+, background color: #\w+, font size: [\d.]+pt \([\d.]+px\), font weight: \w+\)/)||[n.failureSummary.slice(0,160)])[0], html: n.html.slice(0,140) })) })); };
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args:['--no-proxy-server'] });
  const out = {};
  for (const w of [1280, 390]) {
    const ctx = await b.newContext({ viewport: { width: w, height: 844 }, isMobile: w<1000, hasTouch: w<1000 });
    await route(ctx); const p = await ctx.newPage();
    for (const [name, pth] of Object.entries(PAGES)) {
      try {
        await p.goto('https://codigocalma.com/' + pth, { waitUntil: 'load', timeout: 90000 });
        await p.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 600) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 50)); } window.scrollTo(0, 0); });
        await p.waitForTimeout(1200);
        await p.addScriptTag({ path: AXE });
        const res = await p.evaluate(AXRUN);
        const man = await p.evaluate(() => {
          const q = s => [...document.querySelectorAll(s)];
          const vis = e => { const r = e.getBoundingClientRect(); const st = getComputedStyle(e); return r.width>0 && r.height>0 && st.visibility!=='hidden' && st.display!=='none' && parseFloat(st.opacity)>0.05; };
          const hs = q('h1,h2,h3,h4,h5,h6').filter(vis);
          let jumps=[]; for(let i=1;i<hs.length;i++){ const a=+hs[i-1].tagName[1], c=+hs[i].tagName[1]; if(c>a+1) jumps.push(hs[i-1].tagName+'>'+hs[i].tagName+':'+hs[i].textContent.trim().slice(0,30)); }
          const main=document.querySelector('main,#main')||document.body;
          const firstH = hs[0] ? hs[0].tagName+':'+hs[0].textContent.trim().slice(0,40) : null;
          const hidden = [...main.querySelectorAll('h1,h2,h3,p,li')].filter(e => { const s = getComputedStyle(e); return e.textContent.trim() && (s.visibility === 'hidden' || parseFloat(s.opacity) < 0.05) && !e.closest('[hidden], .screen-reader-text, [aria-hidden="true"], .zolo-flip-box_back, .popup-drawer, .screen:not(.active), .hidden'); }).map(e=>e.tagName+':'+e.textContent.trim().slice(0,30));
          const offscreen = [...main.querySelectorAll('h1,h2,h3,p')].filter(e=>{const r=e.getBoundingClientRect(); return vis(e) && (r.left< -1 || r.right>innerWidth+1) && !e.closest('[class*="slider"],[class*="carousel"],.splide,[style*="overflow-x"]');}).map(e=>e.tagName+':'+e.textContent.trim().slice(0,30));
          return { title: document.title, h1: q('h1').filter(vis).map(h=>h.textContent.trim().replace(/\s+/g,' ').slice(0,60)), h1All: q('h1').length, firstH, jumps, headings: hs.map(h=>h.tagName+':'+h.textContent.trim().replace(/\s+/g,' ').slice(0,40)).slice(0,40), hidden: hidden.slice(0,10), offscreen: offscreen.slice(0,10), overflow: document.documentElement.scrollWidth - innerWidth,
            forms: q('form').filter(f=>!f.closest('#search-drawer')&&!f.classList.contains('search-form')).map(f=>[...f.querySelectorAll('input,textarea,select')].filter(i=>i.type!=='hidden').map(i=>({type:i.type, label: i.labels&&i.labels[0]?i.labels[0].textContent.trim().slice(0,60):null, labelVisible: i.labels&&i.labels[0]?vis(i.labels[0]):false, ac:i.getAttribute('autocomplete'), req:i.required, desc:i.getAttribute('aria-describedby'), h: Math.round(i.getBoundingClientRect().height)}))) };
        });
        // Tab 20 pasos, estilo de foco
        await p.evaluate(()=>{ document.activeElement && document.activeElement.blur(); window.scrollTo(0,0); });
        const focus=[]; for (let i=0;i<20;i++){ await p.keyboard.press('Tab'); await p.waitForTimeout(260); /* el tema anima outline en 0,2 s */ focus.push(await p.evaluate(()=>{ const e=document.activeElement; if(!e||e===document.body) return 'BODY'; const s=getComputedStyle(e); const r=e.getBoundingClientRect(); return `${e.tagName}:${(e.getAttribute('aria-label')||e.textContent||'').trim().replace(/\s+/g,' ').slice(0,22)}|o=${s.outlineStyle} ${s.outlineWidth} ${s.outlineColor}|sh=${s.boxShadow==='none'?0:1}|vis=${r.width>0&&r.bottom>0&&r.top<innerHeight}`; })); }
        out[`${name}@${w}`] = { axe: res, man, focus };
        console.error('ok', name, w, res.map(v=>v.id+'('+v.n+')').join(' '));
      } catch(e){ out[`${name}@${w}`] = { error: String(e).slice(0,300) }; console.error('err', name, w, e.message.slice(0,200)); }
    }
    await ctx.close();
  }
  fs.writeFileSync(outFile, JSON.stringify(out,null,1));
  // Reflow 320
  { const ctx = await b.newContext({ viewport:{width:320,height:700}, isMobile:true, hasTouch:true }); await route(ctx); const p=await ctx.newPage(); out.reflow320={};
    for (const [name, pth] of Object.entries(PAGES)) { try { await p.goto('https://codigocalma.com/'+pth,{waitUntil:'load',timeout:90000}); await p.waitForTimeout(800);
      out.reflow320[name]=await p.evaluate(()=>{ const vw=innerWidth; const off=[...document.querySelectorAll('main *')].filter(e=>{const r=e.getBoundingClientRect(); const s=getComputedStyle(e); return r.width>0&&r.height>0&&s.visibility!=='hidden'&&(r.right>vw+1)&&!e.closest('[class*="slider"],[class*="carousel"],.splide,[style*="overflow"],pre,table,.zolo-flip-box_back')&&e.children.length===0;}).slice(0,6).map(e=>e.tagName+'.'+String(e.className).slice(0,40)+':'+(e.textContent||'').trim().slice(0,25)+' r='+Math.round(e.getBoundingClientRect().right)); return { overflow: document.documentElement.scrollWidth-vw, off }; }); } catch(e){ out.reflow320[name]={error:String(e).slice(0,100)}; } }
    await ctx.close(); }
  // Menú mobile
  { const ctx = await b.newContext({ viewport:{width:390,height:844}, isMobile:true, hasTouch:true }); await route(ctx); const p=await ctx.newPage();
    await p.goto('https://codigocalma.com/servicios/',{waitUntil:'load',timeout:90000}); await p.waitForTimeout(800);
    const t = await p.$('#mobile-toggle'); const R={};
    R.toggle = await p.evaluate(()=>{const e=document.querySelector('#mobile-toggle'); const r=e.getBoundingClientRect(); return {label:e.getAttribute('aria-label'), exp:e.getAttribute('aria-expanded'), w:Math.round(r.width), h:Math.round(r.height)};});
    await t.focus(); await p.keyboard.press('Enter'); await p.waitForTimeout(700);
    await p.addScriptTag({ path: AXE });
    R.open = await p.evaluate(()=>{ const d=document.querySelector('#mobile-drawer .drawer-inner'); const s=getComputedStyle(d); const links=[...document.querySelectorAll('#mobile-drawer a, #mobile-drawer button')].filter(e=>e.getBoundingClientRect().height>0).map(e=>{const cs=getComputedStyle(e); const r=e.getBoundingClientRect(); return (e.getAttribute('aria-label')||e.textContent).trim().slice(0,25)+' c='+cs.color+' h='+Math.round(r.height)+' w='+Math.round(r.width)}); return { bg:s.backgroundColor, exp: document.querySelector('#mobile-toggle').getAttribute('aria-expanded'), active: document.activeElement.className+':'+(document.activeElement.getAttribute('aria-label')||document.activeElement.textContent.trim().slice(0,20)), links }; });
    R.axeDrawer = await p.evaluate(async()=> (await axe.run('#mobile-drawer',{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag22aa']}})).violations.map(v=>v.id+'('+v.nodes.length+') '+v.nodes.slice(0,3).map(n=>n.html.slice(0,60)+' '+(n.failureSummary.match(/contrast of [\d.]+[^)]*\)/)||[''])[0]).join(' | ')));
    const seq=[]; for(let i=0;i<12;i++){ await p.keyboard.press('Tab'); seq.push(await p.evaluate(()=>{const e=document.activeElement; const s=getComputedStyle(e); return (e.getAttribute('aria-label')||e.textContent).trim().replace(/\s+/g,' ').slice(0,22)+' o='+s.outlineStyle+' '+s.outlineColor+' inDrawer='+!!e.closest('#mobile-drawer');})); }
    R.tabSeq=seq;
    await p.screenshot({path: path.join(path.dirname(outFile), (mode==='--preview'?'after':'before')+'-menu390.png')});
    // focus a link and screenshot
    await p.keyboard.press('Escape'); await p.waitForTimeout(400);
    R.afterEsc = await p.evaluate(()=>({exp: document.querySelector('#mobile-toggle').getAttribute('aria-expanded'), active: document.activeElement.id||document.activeElement.className}));
    out.menu=R; await ctx.close(); }
  fs.writeFileSync(outFile, JSON.stringify(out,null,1));
  // Test teclado
  { const ctx = await b.newContext({ viewport:{width:1280,height:844} }); await route(ctx); const p=await ctx.newPage();
    await p.goto('https://codigocalma.com/test/',{waitUntil:'load',timeout:90000}); await p.waitForTimeout(800);
    const R={};
    await p.focus('#screen-0 button.btn-primary').catch(e=>R.err=String(e)); await p.keyboard.press('Enter'); await p.waitForTimeout(600);
    const seq=[]; for(let i=0;i<6;i++){ await p.keyboard.press('Tab'); seq.push(await p.evaluate(()=>{const e=document.activeElement; return e.tagName+'#'+e.id+':'+(e.textContent||'').trim().slice(0,25)})); }
    R.seq=seq; R.cards = await p.evaluate(()=>[...document.querySelectorAll('.gen-card')].map(c=>c.tagName+' tab='+c.tabIndex+' role='+c.getAttribute('role')));
    R.h = await p.evaluate(()=>[...document.querySelectorAll('h1,h2,h3,h4,h5,h6')].map(h=>h.tagName+':'+h.textContent.trim().slice(0,30)));
    await p.addScriptTag({ path: AXE });
    const ax = async()=> p.evaluate(async()=> (await axe.run('#main',{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag22aa']}})).violations.map(v=>v.id+'('+v.nodes.length+') '+v.nodes.slice(0,5).map(n=>n.html.slice(0,60)+' '+(n.failureSummary.match(/contrast of [\d.]+ \(foreground color: #\w+, background color: #\w+/)||[''])[0]).join(' | ')));
    R.S1 = await ax();
    await p.click('#gen-millennial'); R.S1sel = await ax(); await p.click('#btn-continue-gen'); await p.waitForTimeout(500); R.S2 = await ax();
    const n = await p.evaluate(()=>state.questions.length);
    for(let i=0;i<n;i++){ await p.click('.answer-btn',{timeout:3000}).catch(()=>{}); await p.waitForTimeout(150); if(i==0) R.S2fb = await ax(); await p.click('#btn-next',{timeout:3000}).catch(()=>{}); await p.waitForTimeout(150); await p.click('#btn-next',{timeout:1500}).catch(()=>{}); await p.waitForTimeout(150); }
    R.final = await p.evaluate(()=>document.querySelector('.screen.active')?.id);
    await p.waitForTimeout(600); R.S3 = await ax();
    out.test=R; fs.writeFileSync(outFile, JSON.stringify(out,null,1)); await ctx.close(); }
  // Reduced motion
  { const ctx = await b.newContext({ viewport:{width:1280,height:800}, reducedMotion:'reduce' }); await route(ctx); const p=await ctx.newPage(); await p.goto('https://codigocalma.com/',{waitUntil:'load',timeout:90000}); await p.waitForTimeout(400);
    out.reduced = await p.evaluate(()=>[...document.querySelectorAll('*')].filter(e=>{const s=getComputedStyle(e); return (s.animationName!=='none' && parseFloat(s.animationDuration)>0.02) || (parseFloat(s.transitionDuration)>0.3)}).slice(0,10).map(e=>e.tagName+'.'+String(e.className).slice(0,60)+' anim='+getComputedStyle(e).animationName+' trans='+getComputedStyle(e).transitionDuration));
    await ctx.close(); }
  await b.close();
  fs.writeFileSync(outFile, JSON.stringify(out,null,1));
})();
