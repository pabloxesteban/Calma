const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const AXE = __dirname + '/node_modules/axe-core/axe.min.js';
async function route(ctx){ await ctx.route('**/*', async (route) => {
  const req = route.request(); if (!/^https?:/.test(req.url())) return route.continue();
  try { const h = { ...req.headers() }; delete h['host'];
    const r = await fetch(req.url(), { method: req.method(), headers: h, body: req.postDataBuffer() || undefined, redirect: 'manual' });
    const body = Buffer.from(await r.arrayBuffer()); const headers = {};
    r.headers.forEach((v, k) => { if (!['content-encoding','content-length','transfer-encoding'].includes(k)) headers[k] = v; });
    await route.fulfill({ status: r.status, headers, body }); } catch (e) { await route.abort(); } }); }
const ax = p => p.evaluate(async()=> (await axe.run('#main',{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag22aa']}})).violations.map(v=>v.id+' n='+v.nodes.length+' :: '+v.nodes.slice(0,4).map(n=>n.html.slice(0,70)+' ['+(n.failureSummary.match(/contrast of [\d.]+ \(foreground color: #\w+, background color: #\w+/)||[''])[0]+']').join(' | ')));
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args:['--no-proxy-server'] });
  const ctx = await b.newContext({ viewport:{width:1280,height:800} }); await route(ctx); const p = await ctx.newPage();
  await p.goto('https://codigocalma.com/test/',{waitUntil:'load'}); await p.waitForTimeout(800); await p.addScriptTag({path:AXE});
  await p.click('#screen-0 button.btn-primary'); await p.waitForTimeout(500); console.log('S1', await ax(p));
  await p.click('#gen-millennial'); await p.click('#btn-continue-gen'); await p.waitForTimeout(500); console.log('S2', await ax(p));
  const n = await p.evaluate(()=>state.questions.length);
  for(let i=0;i<n;i++){ await p.click('.answer-btn'); await p.click('#btn-next'); await p.waitForTimeout(150); if(i==0) {console.log('S2fb', await ax(p)); console.log('FB', await p.evaluate(()=>document.querySelector('#screen-2').innerText.slice(0,600)));} await p.click('#btn-next').catch(()=>{}); await p.waitForTimeout(150); }
  await p.waitForTimeout(500); console.log('S3', await ax(p)); console.log('RES', await p.evaluate(()=>document.querySelector('#screen-3').innerText.slice(0,900)));
  // home flip focus
  await p.goto('https://codigocalma.com/',{waitUntil:'load'}); await p.waitForTimeout(1200);
  const info = await p.evaluate(()=>{ const it=document.querySelector('.zolo-flip-box_item'); const a=it.querySelector('a'); return {a: a? a.outerHTML.slice(0,200):null, itemHtml: it.outerHTML.replace(/\s+/g,' ').slice(0,700)}; });
  console.log('FLIP', JSON.stringify(info));
  const a = await p.$('.zolo-flip-box_item a'); if(a){ await a.focus(); await p.waitForTimeout(700); const bb=await (await p.$('.zolo-flip-box_item')).boundingBox(); await p.screenshot({path:__dirname+'/shots/flip-focus.png',clip:bb}); console.log('flipTransform', await p.evaluate(()=>getComputedStyle(document.querySelector('.zolo-flip-box_inner-item')).transform)); }
  await b.close();
})();
