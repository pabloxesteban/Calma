const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const fs=require('fs'); const src=fs.readFileSync(__dirname+'/run.js','utf8');
async function route(ctx){ await ctx.route('**/*', async (route) => {
  const req = route.request(); if (!/^https?:/.test(req.url())) return route.continue();
  try { const h = { ...req.headers() }; delete h['host'];
    const r = await fetch(req.url(), { method: req.method(), headers: h, body: req.postDataBuffer() || undefined, redirect: 'manual' });
    const body = Buffer.from(await r.arrayBuffer()); const headers = {};
    r.headers.forEach((v, k) => { if (!['content-encoding','content-length','transfer-encoding'].includes(k)) headers[k] = v; });
    await route.fulfill({ status: r.status, headers, body }); } catch (e) { await route.abort(); } }); }
const S=__dirname+'/shots/'; fs.mkdirSync(S,{recursive:true});
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args:['--no-proxy-server'] });
  const R={};
  let ctx = await b.newContext({ viewport:{width:1280,height:800} }); await route(ctx); let p = await ctx.newPage();
  // focus visibility screenshots
  await p.goto('https://codigocalma.com/servicios/',{waitUntil:'load'}); await p.waitForTimeout(800);
  for (let i=1;i<=10;i++){ await p.keyboard.press('Tab'); if([3,6,10].includes(i)){ const el=await p.evaluateHandle(()=>document.activeElement); const bb=await el.boundingBox(); await p.screenshot({path:S+`focus-serv-${i}.png`, clip:{x:Math.max(0,bb.x-20),y:Math.max(0,bb.y-20),width:bb.width+40,height:bb.height+40}}); } }
  // test page keyboard
  await p.goto('https://codigocalma.com/test/',{waitUntil:'load'}); await p.waitForTimeout(800);
  await p.focus('button.btn-primary'); await p.keyboard.press('Enter'); await p.waitForTimeout(600);
  const seq=[]; for(let i=0;i<8;i++){ await p.keyboard.press('Tab'); seq.push(await p.evaluate(()=>{const e=document.activeElement; return e.tagName+'#'+e.id+':'+(e.textContent||'').trim().slice(0,30)})); }
  R.testAfterStart = { active: await p.evaluate(()=>document.querySelector('.screen.active')?.id), tabSeq: seq, genCards: await p.evaluate(()=>[...document.querySelectorAll('.gen-card')].map(c=>({tab:c.tabIndex, role:c.getAttribute('role'), txt:c.textContent.trim().replace(/\s+/g,' ').slice(0,60)}))) };
  await p.screenshot({path:S+'test-screen1.png'});
  // continue with mouse to see answers
  await p.click('#gen-millennial'); await p.click('#btn-continue-gen'); await p.waitForTimeout(500);
  R.testQ = await p.evaluate(()=>({ focus: document.activeElement.tagName+':'+document.activeElement.textContent.trim().slice(0,20), live: document.querySelectorAll('[aria-live],[role=status],[role=alert]').length, answers:[...document.querySelectorAll('.answer-btn')].map(b=>b.textContent.slice(0,40)+' pressed='+b.getAttribute('aria-pressed')), progress: document.getElementById('progress-fill')?.getAttribute('role'), q: document.getElementById('question-text')?.tagName }));
  await p.keyboard.press('Tab'); await p.keyboard.press('Tab');
  await p.focus('.answer-btn'); await p.keyboard.press('Enter'); await p.waitForTimeout(200);
  R.testAnswerKb = await p.evaluate(()=>({ sel: document.querySelectorAll('.answer-btn.selected').length, nextVisible: !document.getElementById('btn-next').classList.contains('hidden') }));
  await p.keyboard.press('Tab'); R.afterAnsTab = await p.evaluate(()=>document.activeElement.id||document.activeElement.textContent.slice(0,20));
  await p.screenshot({path:S+'test-q1.png', fullPage:false});
  // contact form empty submit
  await p.goto('https://codigocalma.com/contacto/',{waitUntil:'load'}); await p.waitForTimeout(800);
  R.formHtml = await p.evaluate(()=>{const f=document.querySelector('form.kb-form, form[id^=kb]'); return f? f.outerHTML.replace(/\s+/g,' ').slice(0,2500):null});
  await p.click('form[id^=kb] button[type=submit], form[id^=kb] .kb-submit-field button').catch(e=>R.clickErr=String(e).slice(0,100)); await p.waitForTimeout(1500);
  R.formAfter = await p.evaluate(()=>({ msgs:[...document.querySelectorAll('.kb-adv-form-message, .kb-form-error-msg, [role=alert], .kb-adv-form-infield-error, [class*=error]')].map(e=>e.className+': '+e.textContent.trim().slice(0,100)).slice(0,8), invalid:[...document.querySelectorAll('[aria-invalid=true]')].length, desc:[...document.querySelectorAll('input,textarea')].map(i=>i.getAttribute('aria-describedby')), validity:[...document.querySelectorAll('form[id^=kb] input:not([type=hidden]),form[id^=kb] textarea')].map(i=>i.validationMessage) }));
  await p.screenshot({path:S+'contact-err.png', fullPage:true});
  // home flip boxes & cards & leer mas
  await p.goto('https://codigocalma.com/',{waitUntil:'load'}); await p.waitForTimeout(1500);
  R.home = await p.evaluate(()=>({
    flip: [...document.querySelectorAll('.zolo-flip-box, [class*=zolo-flip-box_inner-item]')].slice(0,4).map(e=>({cls:String(e.className).slice(0,60), tab:e.tabIndex, a:e.querySelectorAll('a,button').length, back:(e.querySelector('[class*=back]')||{}).textContent?.trim().replace(/\s+/g,' ').slice(0,80)})),
    flipCount: document.querySelectorAll('.zolo-flip-box').length,
    zolo: [...new Set([...document.querySelectorAll('[class*=zolo]')].map(e=>String(e.className).split(' ').find(c=>c.startsWith('zolo'))))].slice(0,20),
    readmore: [...document.querySelectorAll('a')].filter(a=>/Leer m/.test(a.textContent)).slice(0,2).map(a=>a.outerHTML.replace(/\s+/g,' ').slice(0,300)),
    infobox: [...document.querySelectorAll('.kt-blocks-info-box-link-wrap')].slice(0,3).map(e=>e.tagName+' href='+e.getAttribute('href')+' txt='+e.textContent.trim().replace(/\s+/g,' ').slice(0,80)),
    h1: [...document.querySelectorAll('h1')].map(h=>h.outerHTML.slice(0,200)),
    anims: [...document.querySelectorAll('[class*=animated],[class*=animation],[data-animation]')].slice(0,5).map(e=>String(e.className).slice(0,90)),
    rmRules: [...document.styleSheets].flatMap(s=>{try{return [...s.cssRules].filter(r=>r.media&&/reduced-motion/.test(r.media.mediaText)).map(r=>(s.href||'inline').split('/').pop()+': '+r.cssText.slice(0,120))}catch(e){return []}}).slice(0,12)
  }));
  await ctx.close();
  // hover/focus flip keyboard: tab through home and record if focus lands in flip
  // mobile menu
  ctx = await b.newContext({ viewport:{width:390,height:800}, isMobile:true, hasTouch:true }); await route(ctx); p = await ctx.newPage();
  await p.goto('https://codigocalma.com/',{waitUntil:'load'}); await p.waitForTimeout(800);
  await p.focus('button[aria-label="Abrir menú"]'); await p.keyboard.press('Enter'); await p.waitForTimeout(700);
  const ms=[]; for(let i=0;i<14;i++){ await p.keyboard.press('Tab'); ms.push(await p.evaluate(()=>{const e=document.activeElement; const r=e.getBoundingClientRect(); return e.tagName+':'+(e.getAttribute('aria-label')||e.textContent).trim().replace(/\s+/g,' ').slice(0,30)+' '+Math.round(r.width)+'x'+Math.round(r.height)+' exp='+e.getAttribute('aria-expanded')})); }
  R.mobileMenu = { dialog: await p.evaluate(()=>{const d=document.querySelector('#mobile-drawer'); return d? {role:d.getAttribute('role'), modal:d.getAttribute('aria-modal'), hidden:d.getAttribute('aria-hidden'), cls:d.className}:null}), tabs: ms };
  await p.keyboard.press('Escape'); await p.waitForTimeout(400);
  R.mobileMenu.afterEsc = await p.evaluate(()=>({open: document.body.className.includes('showing-popup-drawer'), focus: document.activeElement.getAttribute('aria-label')||document.activeElement.tagName}));
  await p.screenshot({path:S+'mobile-menu.png'});
  // 320 reflow + text spacing on article
  await p.setViewportSize({width:320,height:700});
  for (const u of ['', 'servicios/','contacto/','test/','por-que-fallamos-al-intentar-cambiar-conductas/','testimonios/','sobre_tatiana/']) { await p.goto('https://codigocalma.com/'+u,{waitUntil:'load'}); await p.waitForTimeout(500);
    const ov = await p.evaluate(()=>document.documentElement.scrollWidth-innerWidth);
    await p.addStyleTag({content:'*{line-height:1.5!important;letter-spacing:.12em!important;word-spacing:.16em!important} p{margin-bottom:2em!important}'});
    const ov2 = await p.evaluate(()=>document.documentElement.scrollWidth-innerWidth);
    (R.reflow=R.reflow||{})[u||'inicio']={ov320:ov, ovSpacing:ov2}; }
  await b.close(); fs.writeFileSync(__dirname+'/out2.json', JSON.stringify(R,null,1)); console.log(JSON.stringify(R,null,1).slice(0,12000));
})();
