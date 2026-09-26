// Capturas + métricas mobile (skill mobile-qa) de producción o de la vista previa.
// Uso:
//   NODE_USE_ENV_PROXY=1 node staging/preview/capturas.js --preview <carpeta-salida> [paginas...]
//   NODE_USE_ENV_PROXY=1 node staging/preview/capturas.js --live    <carpeta-salida> [paginas...]
// En modo --preview, el documento principal se sirve desde staging/preview/build/<slug>.html
// y el resto (CSS, JS, imágenes, fuentes) se pide a producción.
// Chromium no confía en el CA del proxy de este entorno: todas las peticiones se
// rehacen con fetch de Node, que sí valida TLS. Nunca se desactiva la verificación.
const fs = require('fs');
const path = require('path');
const { chromium } = require('/opt/node22/lib/node_modules/playwright');

const [, , mode, out, ...only] = process.argv;
const BUILD = path.join(__dirname, 'build');
const PAGES = {
  inicio: '', servicios: 'servicios/', contacto: 'contacto/', sobre_tatiana: 'sobre_tatiana/',
  blog: 'blog/', ciberpsicologia: 'ciberpsicologia/', testimonios: 'testimonios/', test: 'test/',
  herramientas: 'herramientas/', 'descargas-2': 'descargas-2/', 'bienestar-digital': 'bienestar-digital/',
  'por-que-fallamos-al-intentar-cambiar-conductas': 'por-que-fallamos-al-intentar-cambiar-conductas/',
  equipo: 'equipo/', 'equipo-tatiana': 'equipo/tatiana-x-stacul/', 'equipo-francisca': 'equipo/francisca-cortes-santoro/',
};
const WIDTHS = [360, 390, 430, 1280];
const fileFor = (p) => path.join(BUILD, (p.replace(/\/$/, '').replace(/\//g, '_') || 'home') + '.html');

(async () => {
  fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--no-proxy-server'] });
  const report = [];
  const names = only.length ? only : Object.keys(PAGES);
  for (const w of WIDTHS) {
    const ctx = await b.newContext({ viewport: { width: w, height: 844 }, isMobile: w < 1000, hasTouch: w < 1000, reducedMotion: 'no-preference' });
    await ctx.route('**/*', async (route) => {
      const req = route.request();
      const url = req.url();
      if (!/^https?:/.test(url)) return route.continue();
      const u = new URL(url);
      if (mode === '--preview' && u.hostname === 'codigocalma.com' && u.pathname.startsWith('/wp-content/plugins/codigo-calma/')) {
        const f = path.join(__dirname, '../..', decodeURIComponent(u.pathname));
        if (fs.existsSync(f)) return route.fulfill({ status: 200, body: fs.readFileSync(f), contentType: f.endsWith('.woff2') ? 'font/woff2' : f.endsWith('.css') ? 'text/css' : f.endsWith('.js') ? 'text/javascript' : 'application/octet-stream', headers: { 'access-control-allow-origin': '*' } });
      }
      if (mode === '--preview' && req.resourceType() === 'document' && u.hostname === 'codigocalma.com') {
        const f = fileFor(u.pathname.replace(/^\//, ''));
        if (fs.existsSync(f)) return route.fulfill({ status: 200, contentType: 'text/html; charset=utf-8', body: fs.readFileSync(f) });
      }
      try {
        const h = { ...req.headers() };
        const r = await fetch(url, { method: req.method(), headers: h, body: req.postDataBuffer() || undefined, redirect: 'manual' });
        const body = Buffer.from(await r.arrayBuffer());
        const headers = {};
        r.headers.forEach((v, k) => { if (!['content-encoding', 'content-length', 'transfer-encoding'].includes(k)) headers[k] = v; });
        await route.fulfill({ status: r.status, headers, body });
      } catch (e) { await route.abort(); }
    });
    const p = await ctx.newPage();
    for (const name of names) {
      try {
        await p.goto('https://codigocalma.com/' + PAGES[name], { waitUntil: 'load', timeout: 90000 });
        // Recorre la página para disparar lazy-load y observadores de scroll.
        await p.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 600) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 60)); } window.scrollTo(0, 0); });
        await p.waitForTimeout(1200);
        const m = await p.evaluate(() => {
          const vw = innerWidth;
          const vis = (e) => { const s = getComputedStyle(e); const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none' && parseFloat(s.opacity) > 0.05; };
          const main = document.querySelector('#main, main') || document.body;
          const clipped = [...main.querySelectorAll('h1,h2,h3,p,li,a,button,img')].filter(e => { const r = e.getBoundingClientRect(); return vis(e) && (r.left < -1 || r.right > vw + 1) && !e.closest('.splide, .kb-splide, [class*="slider"], [class*="carousel"], .cc-slider, .cc-track, [style*="overflow-x"]'); })
            .map(e => e.tagName + ':' + (e.textContent || e.alt || '').trim().slice(0, 40));
          const hidden = [...main.querySelectorAll('h1,h2,h3,p')].filter(e => { const s = getComputedStyle(e); return e.textContent.trim() && (s.visibility === 'hidden' || parseFloat(s.opacity) < 0.05) && !e.closest('[hidden], .screen-reader-text, [aria-hidden="true"], .zolo-flip-box_back, .popup-drawer'); }).length;
          const small = [...document.querySelectorAll('a,button,input,select,textarea,[role=button]')].filter(e => { const r = e.getBoundingClientRect(); return vis(e) && (r.height < 44 || r.width < 44) && !e.closest('p, li p, .entry-content li, .entry-summary, .comment-content, .skip-link') && e.type !== 'hidden'; })
            .map(e => (e.getAttribute('aria-label') || e.textContent || e.tagName).trim().replace(/\s+/g, ' ').slice(0, 30));
          const texts = [...main.querySelectorAll('p, h1, h2, h3, li')].filter(e => vis(e) && e.textContent.trim().length > 20).map(e => e.getBoundingClientRect());
          const gut = texts.length ? Math.round(Math.min(...texts.map(r => Math.min(r.left, vw - r.right)))) : null;
          const h1 = [...document.querySelectorAll('h1')].filter(vis).map(e => e.textContent.trim().slice(0, 50));
          const ctas = [...document.querySelectorAll('a, button')].filter(a => /Solicitar una consulta|Enviar/i.test(a.textContent) && vis(a)).map(a => { const s = getComputedStyle(a); return { t: a.textContent.trim().slice(0, 30), color: s.color, bg: s.backgroundColor, h: Math.round(a.getBoundingClientRect().height) }; });
          return { overflowX: document.documentElement.scrollWidth - vw, clipped, hiddenText: hidden, smallTargets: small.length, smallSample: small.slice(0, 6), minGutter: gut, h1, ctas, height: document.documentElement.scrollHeight };
        });
        report.push({ w, page: name, ...m });
        await p.screenshot({ path: path.join(out, `${name}-${w}.png`), fullPage: true });
      } catch (e) { report.push({ w, page: name, error: String(e).slice(0, 200) }); }
    }
    await ctx.close();
  }
  await b.close();
  fs.writeFileSync(path.join(out, 'metricas.json'), JSON.stringify(report, null, 1));
  console.log(JSON.stringify(report));
})();
