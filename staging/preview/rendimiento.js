// Rendimiento de laboratorio (mobile): LCP, CLS, peso transferido y peticiones.
// Emula un teléfono de gama media: 390×844, CPU 4× más lenta, red "4G lenta"
// (1,6 Mbps / 150 ms RTT). Mide igual producción (--live) y la vista previa (--preview).
// Uso: NODE_USE_ENV_PROXY=1 node staging/preview/rendimiento.js --live|--preview salida.json [paginas...]
// Nota: los assets se piden a través del proxy de este entorno; los valores sirven
// para comparar antes/después, no como cifra absoluta (usar PageSpeed Insights en producción).
const fs = require('fs'), path = require('path');
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const [, , mode, out, ...only] = process.argv;
const BUILD = path.join(__dirname, 'build');
const PAGES = { inicio: '', servicios: 'servicios/', blog: 'blog/', articulo: 'por-que-fallamos-al-intentar-cambiar-conductas/', contacto: 'contacto/' };
const RUNS = 3;
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--no-proxy-server'] });
  const res = {};
  for (const name of (only.length ? only : Object.keys(PAGES))) {
    const runs = [];
    for (let i = 0; i < RUNS; i++) {
      const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true, deviceScaleFactor: 2 });
      let bytes = 0, reqs = 0, fonts = 0, gfonts = 0;
      await ctx.route('**/*', async (route) => {
        const req = route.request(), u = new URL(req.url());
        if (!/^https?:/.test(req.url())) return route.continue();
        reqs++;
        if (/fonts\.(googleapis|gstatic)\.com/.test(u.hostname)) gfonts++;
        if (req.resourceType() === 'font') fonts++;
        let body, status = 200, headers = {};
        if (mode === '--preview' && u.hostname === 'codigocalma.com' && u.pathname.startsWith('/wp-content/plugins/codigo-calma/')) {
          const f = path.join(__dirname, '../..', decodeURIComponent(u.pathname));
          body = fs.readFileSync(f); headers['content-type'] = f.endsWith('.woff2') ? 'font/woff2' : f.endsWith('.js') ? 'text/javascript' : 'text/css';
        } else if (mode === '--preview' && req.resourceType() === 'document' && u.hostname === 'codigocalma.com') {
          body = fs.readFileSync(path.join(BUILD, (u.pathname.replace(/^\/|\/$/g, '').replace(/\//g, '_') || 'home') + '.html')); headers['content-type'] = 'text/html; charset=utf-8';
        } else {
          try {
            const r = await fetch(req.url(), { method: req.method(), headers: req.headers(), redirect: 'manual' });
            body = Buffer.from(await r.arrayBuffer()); status = r.status;
            r.headers.forEach((v, k) => { if (!['content-encoding', 'content-length', 'transfer-encoding'].includes(k)) headers[k] = v; });
          } catch (e) { return route.abort(); }
        }
        bytes += body.length;
        await route.fulfill({ status, headers, body });
      });
      const p = await ctx.newPage();
      const cdp = await ctx.newCDPSession(p);
      await cdp.send('Network.enable');
      await cdp.send('Network.emulateNetworkConditions', { offline: false, latency: 150, downloadThroughput: 1.6 * 1024 * 1024 / 8, uploadThroughput: 750 * 1024 / 8 });
      await cdp.send('Emulation.setCPUThrottlingRate', { rate: 4 });
      await p.addInitScript(() => {
        window.__lcp = 0; window.__cls = 0; window.__lcpEl = '';
        new PerformanceObserver((l) => { for (const e of l.getEntries()) { window.__lcp = e.startTime; window.__lcpEl = (e.element && (e.element.tagName + '.' + (e.element.className || '').toString().slice(0, 40))) || e.url || ''; } }).observe({ type: 'largest-contentful-paint', buffered: true });
        new PerformanceObserver((l) => { for (const e of l.getEntries()) if (!e.hadRecentInput) window.__cls += e.value; }).observe({ type: 'layout-shift', buffered: true });
      });
      const t0 = Date.now();
      try { await p.goto('https://codigocalma.com/' + PAGES[name], { waitUntil: 'load', timeout: 120000 }); } catch (e) {}
      await p.waitForTimeout(2500);
      const m = await p.evaluate(() => ({ lcp: Math.round(window.__lcp), cls: +window.__cls.toFixed(3), el: window.__lcpEl, title: document.title }));
      runs.push({ ...m, loadMs: Date.now() - t0, kb: Math.round(bytes / 1024), reqs, fonts, gfonts });
      await ctx.close();
    }
    const med = (k) => runs.map(r => r[k]).sort((a, b) => a - b)[Math.floor(RUNS / 2)];
    res[name] = { lcp: med('lcp'), cls: med('cls'), kb: med('kb'), reqs: med('reqs'), fonts: med('fonts'), gfonts: med('gfonts'), lcpEl: runs[0].el, title: runs[0].title };
    console.log(name, JSON.stringify(res[name]));
  }
  await b.close();
  fs.writeFileSync(out, JSON.stringify(res, null, 1));
})();
