const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const pages = ['', 'servicios/', 'contacto/', 'sobre_tatiana/', 'blog/', 'ciberpsicologia/', 'testimonios/', 'por-que-fallamos-al-intentar-cambiar-conductas/'];
const out = process.argv[2];
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args:['--no-proxy-server'] });
  const report = [];
  for (const w of [360, 390, 430, 1280]) {
    const ctx = await b.newContext({ viewport: { width: w, height: 800 }, deviceScaleFactor: 1, isMobile: w < 1000, hasTouch: w < 1000 });
    await ctx.route('**/*', async (route) => {
      const req = route.request();
      if (!/^https?:/.test(req.url())) return route.continue();
      try {
        const h = { ...req.headers() }; delete h['host'];
        const r = await fetch(req.url(), { method: req.method(), headers: h, body: req.postDataBuffer() || undefined, redirect: 'manual' });
        const body = Buffer.from(await r.arrayBuffer());
        const headers = {}; r.headers.forEach((v, k) => { if (!['content-encoding','content-length','transfer-encoding'].includes(k)) headers[k] = v; });
        await route.fulfill({ status: r.status, headers, body });
      } catch (e) { await route.abort(); }
    });
    const p = await ctx.newPage();
    for (const path of pages) {
      const name = (path.replace(/\/$/, '') || 'inicio');
      try {
        await p.goto('https://codigocalma.com/' + path, { waitUntil: 'load', timeout: 60000 });
        await p.waitForTimeout(800);
        const m = await p.evaluate(() => {
          const de = document.documentElement;
          const overflow = de.scrollWidth - window.innerWidth;
          const small = [...document.querySelectorAll('a,button,input,select,textarea,[role=button]')].filter(e => { const r = e.getBoundingClientRect(); const st = getComputedStyle(e); return r.width > 0 && r.height > 0 && st.visibility !== 'hidden' && (r.height < 44 || r.width < 44); }).length;
          const main = document.querySelector('.entry-content, main p, article p') || document.body;
          const pr = document.querySelector('p'); const pl = pr ? pr.getBoundingClientRect().left : null;
          const ctas = [...document.querySelectorAll('a')].filter(a => /Solicitar una consulta/i.test(a.textContent)).map(a => { const s = getComputedStyle(a); return { color: s.color, bg: s.backgroundColor, border: s.borderColor, h: Math.round(a.getBoundingClientRect().height) }; });
          const lcpImgs = document.images.length;
          return { overflow, smallTargets: small, firstParagraphLeft: pl && Math.round(pl), ctas, height: de.scrollHeight, imgs: lcpImgs };
        });
        report.push({ w, page: name, ...m });
        if (w !== 1280 || true) await p.screenshot({ path: `${out}/${name}-${w}.png`, fullPage: true });
      } catch (e) { report.push({ w, page: name, error: String(e).slice(0, 200) }); }
    }
    await ctx.close();
  }
  await b.close();
  require('fs').writeFileSync(`${out}/metricas.json`, JSON.stringify(report, null, 1));
  console.log(JSON.stringify(report));
})();
