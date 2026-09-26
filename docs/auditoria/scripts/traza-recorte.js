const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const [,, url, w, out, ...ys] = process.argv;
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args:['--no-proxy-server'] });
  const ctx = await b.newContext({ viewport: { width: +w, height: 844 }, isMobile: false });
  await ctx.route('**/*', async (route) => { const req = route.request(); if (!/^https?:/.test(req.url())) return route.continue();
    try { const h = { ...req.headers() }; const r = await fetch(req.url(), { method: req.method(), headers: h, body: req.postDataBuffer() || undefined, redirect: 'manual' });
      const body = Buffer.from(await r.arrayBuffer()); const headers = {}; r.headers.forEach((v, k) => { if (!['content-encoding','content-length','transfer-encoding'].includes(k)) headers[k] = v; });
      await route.fulfill({ status: r.status, headers, body }); } catch (e) { await route.abort(); } });
  const p = await ctx.newPage(); await p.goto(url, { waitUntil: 'load', timeout: 60000 }); await p.waitForTimeout(1000);
  const chain = await p.evaluate(() => { const h=[...document.querySelectorAll('article h2, .entry-title')].find(e=>e.getBoundingClientRect().left<0); const out=[]; let e=h; while(e&&e!==document.body){const r=e.getBoundingClientRect(),s=getComputedStyle(e); out.push(`${e.tagName}.${[...e.classList].slice(0,3).join('.')} L${Math.round(r.left)} W${Math.round(r.width)} ov:${s.overflow} ml:${s.marginLeft} pl:${s.paddingLeft} tr:${s.transform} zoom:${s.zoom} maxw:${s.maxWidth}`); e=e.parentElement;} return out; }); console.log(chain.join('\n'));
  const info = await p.evaluate(() => ({ bodyOX: getComputedStyle(document.body).overflowX, htmlOX: getComputedStyle(document.documentElement).overflowX, wide: [...document.querySelectorAll('h1,h2,h3,p')].filter(e=>{const r=e.getBoundingClientRect();return r.left<0||r.right>innerWidth+1}).slice(0,8).map(e=>e.tagName+':'+e.textContent.trim().slice(0,40)+' L'+Math.round(e.getBoundingClientRect().left)+' R'+Math.round(e.getBoundingClientRect().right)) }));
  console.log(JSON.stringify(info));
  for (const y of ys) { await p.evaluate(y => window.scrollTo(0, +y), y); await p.waitForTimeout(400); await p.screenshot({ path: `${out}-${y}.png` }); }
  await b.close();
})();
