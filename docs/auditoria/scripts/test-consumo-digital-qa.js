// QA del bloque "Test de consumo digital" (Etapa 2): teclado de principio a fin, foco, anuncios,
// equivalencia del cálculo con el script original, axe-core, reflow 320/390, objetivos táctiles,
// modo sin JavaScript y prefers-reduced-motion. Sin red: todo se sirve desde file://.
// Uso: AXE_PATH=/ruta/axe.min.js OUT_DIR=/ruta/salida node docs/auditoria/scripts/test-consumo-digital-qa.js
// Opcionales: ORIGINAL_HTML (por defecto el snapshot docs/auditoria/snapshot-2026-09-26/html/test.html).
const fs = require('fs'), path = require('path');
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const REPO = path.join(__dirname, '../../..');
const BLOCK = path.join(REPO, 'contenido/etapa-2/bloques/test-consumo-digital.html');
const ORIGINAL = process.env.ORIGINAL_HTML || path.join(REPO, 'docs/auditoria/snapshot-2026-09-26/html/test.html');
const AXE = process.env.AXE_PATH || path.join(__dirname, 'node_modules/axe-core/axe.min.js');
const OUT = process.env.OUT_DIR || path.join(require('os').tmpdir(), 'calma-test-qa');
fs.mkdirSync(OUT, { recursive: true });
// Combinaciones: índice de opción elegida (0-3, en el orden en que aparecen) para cada una de las 12 preguntas.
const COMBOS = {
  'A: siempre la primera opción': [0,0,0,0,0,0,0,0,0,0,0,0],
  'B: siempre la de mayor puntaje': [1,3,3,3,3,3,2,3,2,3,3,3],
  'C: 18 pts, borde de redondeo (37,5 % → 38)': [2,2,1,1,1,0,0,0,0,0,0,0],
  'D: mezcla alta': [3,1,2,2,2,2,1,2,3,2,2,2],
  'E: 16 pts, generación "Otra"': [2,2,1,0,0,0,0,0,0,0,0,0]
};
const harness = path.join(OUT, 'harness.html');
fs.writeFileSync(harness, '<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Prueba: test de consumo digital</title>' +
  '<style>body{margin:0;font-family:system-ui,sans-serif;background:#f8fafc}header{padding:12px 20px;background:#fff;border-bottom:1px solid #e2e8f0}main{padding:24px 20px}</style></head>' +
  '<body><header><a href="#inicio">Código Calma (enlace de prueba)</a></header><main id="inicio">' + fs.readFileSync(BLOCK, 'utf8') + '</main></body></html>');
const log = []; let fails = 0;
const ok = (cond, msg) => { log.push((cond ? 'OK   ' : 'FALLA') + ' ' + msg); if (!cond) fails++; };
const AXRUN = async () => { const r = await axe.run(document, { runOnly: { type: 'tag', values: ['wcag2a','wcag2aa','wcag21a','wcag21aa','wcag22aa','best-practice'] } });
  return r.violations.map(v => ({ id: v.id, impact: v.impact, n: v.nodes.length, targets: v.nodes.slice(0, 5).map(n => n.target.join(' ')) })); };
const active = (p) => p.evaluate(() => { const a = document.activeElement; return { tag: a.tagName, text: (a.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 90), type: a.type || '', name: a.name || '', value: a.value || '', checked: !!a.checked }; });
const noHScroll = (p) => p.evaluate(() => document.documentElement.scrollWidth <= document.documentElement.clientWidth);
async function axeCheck(p, label, store) {
  await p.addScriptTag({ path: AXE });
  const v = await p.evaluate(AXRUN);
  store[label] = v;
  const serious = v.filter(x => x.impact === 'serious' || x.impact === 'critical');
  ok(serious.length === 0, `axe [${label}]: ${serious.length} violaciones serias/críticas (${v.length} en total: ${v.map(x => x.id + '/' + x.impact).join(', ') || 'ninguna'})`);
}
async function tabTo(p, pred, max = 12) { for (let i = 0; i < max; i++) { await p.keyboard.press('Tab'); const a = await active(p); if (pred(a)) return a; } return null; }
async function originalProfile(browser, combo) {
  const ctx = await browser.newContext();
  await ctx.route('**/*', r => /^file:/.test(r.request().url()) ? r.continue() : r.abort());
  const p = await ctx.newPage();
  await p.goto('file://' + ORIGINAL, { waitUntil: 'domcontentloaded' });
  const res = await p.evaluate((combo) => {
    // Lógica original sin tocar: selectGen/confirmGen/selectAnswer/nextQuestion (dos clics) y showResult.
    selectGen('millennial'); confirmGen();
    combo.forEach((idx) => { document.querySelectorAll('.answer-btn')[idx].click(); nextQuestion(); nextQuestion(); });
    return { title: document.getElementById('result-title').textContent, score: state.score };
  }, combo);
  await ctx.close();
  return res;
}
async function keyboardRun(browser, width, name, combo, extras, axeStore) {
  const ctx = await browser.newContext({ viewport: { width, height: 800 }, reducedMotion: 'reduce' });
  await ctx.route('**/*', r => /^file:/.test(r.request().url()) ? r.continue() : r.abort());
  const p = await ctx.newPage();
  const errors = []; p.on('pageerror', e => errors.push(e.message));
  await p.goto('file://' + harness);
  const tag = `[${width}px ${name}]`;
  if (extras.axe) await axeCheck(p, `${width}px inicial`, axeStore);
  if (extras.shots) await p.screenshot({ path: path.join(OUT, `inicio-${width}.png`), fullPage: true });
  ok(await noHScroll(p), `${tag} sin scroll horizontal en la pantalla inicial`);
  const start = await tabTo(p, a => a.tag === 'BUTTON' && /Empezar/.test(a.text));
  ok(!!start, `${tag} Tab llega a "Empezar"`);
  await p.keyboard.press('Enter');
  let a = await active(p);
  ok(a.tag === 'H2' && /generación/.test(a.text), `${tag} tras Empezar el foco está en el H2 "${a.text}"`);
  if (extras.errorPath) {
    await tabTo(p, x => x.tag === 'BUTTON' && /Continuar/.test(x.text));
    await p.keyboard.press('Enter');
    a = await active(p);
    const errVisible = await p.evaluate(() => !document.querySelector('[data-calma-error]').hidden);
    ok(errVisible && a.type === 'radio', `${tag} Continuar sin elegir: mensaje de error visible y foco en la primera opción (${a.name}=${a.value})`);
    await p.evaluate(() => document.querySelector('[data-calma-step="gen"] h2').focus());
  }
  // Generación: primera opción con Tab; flechas para moverse; Espacio para marcar.
  a = await tabTo(p, x => x.type === 'radio', 3);
  ok(a && a.name === 'generacion', `${tag} Tab entra al grupo de generación`);
  for (let i = 0; i < (extras.gen || 0); i++) await p.keyboard.press('ArrowDown');
  await p.keyboard.press('Space');
  a = await active(p);
  ok(a.checked, `${tag} generación elegida con teclado: ${a.value}`);
  await tabTo(p, x => x.tag === 'BUTTON' && /Continuar/.test(x.text), 3);
  await p.keyboard.press('Enter');
  for (let qi = 0; qi < 12; qi++) {
    a = await active(p);
    const live = await p.evaluate(() => new Promise(r => setTimeout(() => r(document.querySelector('[data-calma-live]').textContent), 120)));
    const prog = await p.textContent('[data-calma-progress-text]');
    ok(a.tag === 'H2' && prog === `Pregunta ${qi + 1} de 12` && live === prog, `${tag} P${qi + 1}: foco en H2 "${a.text.slice(0, 50)}", progreso "${prog}", anuncio "${live}"`);
    if (qi === 5 && extras.shots) await p.screenshot({ path: path.join(OUT, `pregunta6-${width}.png`), fullPage: true });
    a = await tabTo(p, x => x.type === 'radio', 3);
    ok(a && a.name === 'q' + (qi + 1), `${tag} P${qi + 1}: Tab entra al grupo de radios`);
    const idx = combo[qi];
    if (idx === 0) await p.keyboard.press('Space'); else for (let i = 0; i < idx; i++) await p.keyboard.press('ArrowDown');
    a = await active(p);
    if (!(a.checked)) ok(false, `${tag} P${qi + 1}: la opción ${idx} no quedó marcada`);
    await tabTo(p, x => x.tag === 'BUTTON' && /^Siguiente|Ver mi resultado/.test(x.text), 3);
    await p.keyboard.press('Enter');
    const fb = await p.evaluate(() => document.querySelector('[data-calma-feedback]').textContent.trim());
    a = await active(p);
    if (qi === 0 || qi === 11) ok(/Buen manejo|Patrón común|Comportamiento frecuente/.test(fb) && /Dato:/.test(fb) && a.tag === 'BUTTON', `${tag} P${qi + 1}: retroalimentación y dato en región role=status; foco sigue en "${a.text}"`);
    if (qi === 5 && extras.axe) { await axeCheck(p, `${width}px pregunta 6 con retroalimentación`, axeStore); ok(await noHScroll(p), `${tag} P6 sin scroll horizontal`); }
    if (qi === 2 && extras.back) {
      await p.keyboard.down('Shift'); await p.keyboard.press('Tab'); await p.keyboard.up('Shift');
      a = await active(p);
      ok(a.tag === 'BUTTON' && a.text === 'Anterior', `${tag} Shift+Tab llega a "Anterior"`);
      await p.keyboard.press('Enter');
      a = await active(p);
      const kept = await p.evaluate(() => !!document.querySelector('input[name="q2"]:checked'));
      ok(a.tag === 'H2' && /batería/.test(a.text) && kept, `${tag} Anterior vuelve a P2 con foco en su H2 y conserva la respuesta`);
      await tabTo(p, x => x.type === 'radio', 3);
      await tabTo(p, x => x.tag === 'BUTTON' && x.text === 'Siguiente', 3);
      await p.keyboard.press('Enter'); await p.keyboard.press('Enter');
      a = await tabTo(p, x => x.type === 'radio', 3);
      a = await active(p);
      ok(a.checked && a.name === 'q3', `${tag} de vuelta en P3: Tab va a la opción ya marcada`);
      await tabTo(p, x => x.tag === 'BUTTON' && x.text === 'Siguiente', 3);
      await p.keyboard.press('Enter');
    }
    a = await active(p);
    const expected = qi === 11 ? 'Ver mi resultado' : 'Siguiente pregunta';
    if (a.text !== expected) ok(false, `${tag} P${qi + 1}: el botón dice "${a.text}", se esperaba "${expected}"`);
    await p.keyboard.press('Enter');
  }
  a = await active(p);
  const res = await p.evaluate(() => ({ profile: document.getElementById('calma-test').getAttribute('data-calma-profile'), score: +document.getElementById('calma-test').getAttribute('data-calma-score'),
    resultVisible: !document.querySelector('[data-calma-result]').hidden, live: document.querySelector('[data-calma-live]').textContent }));
  await p.waitForTimeout(150);
  res.live = await p.textContent('[data-calma-live]');
  ok(res.resultVisible && a.tag === 'H2' && a.text === res.profile, `${tag} resultado visible, foco en su H2 "${a.text}", anuncio "${res.live}"`);
  const orig = await originalProfile(browser, combo);
  ok(orig.title.toLowerCase() === res.profile.toLowerCase() && orig.score === res.score, `${tag} cálculo = original: nuevo "${res.profile}" ${res.score} pts · original "${orig.title}" ${orig.score} pts`);
  const cta = await p.evaluate(() => [...document.querySelectorAll('[data-calma-result] .calma-test__actions > *')].map(e => ({ t: e.textContent.trim(), href: e.getAttribute('href'), tag: e.tagName })));
  ok(cta[0].t === 'Solicitar una consulta →' && cta[0].href === '/contacto/?area=habitos' && cta[1].t === 'Repetir el test' && cta[1].tag === 'BUTTON', `${tag} CTA: ${JSON.stringify(cta)}`);
  ok(await noHScroll(p), `${tag} resultado sin scroll horizontal`);
  if (extras.axe) await axeCheck(p, `${width}px resultado`, axeStore);
  if (extras.shots) await p.screenshot({ path: path.join(OUT, `resultado-${width}.png`), fullPage: true });
  // Objetivos táctiles y foco visible en el resultado.
  const sizes = await p.evaluate(() => [...document.querySelectorAll('#calma-test a, #calma-test button, #calma-test label')].filter(e => e.offsetParent).map(e => { const r = e.getBoundingClientRect(); return { t: e.textContent.trim().slice(0, 30), h: Math.round(r.height), w: Math.round(r.width), inline: getComputedStyle(e).display === 'inline' }; }));
  const small = sizes.filter(s => !s.inline && (s.h < 44 || s.w < 44));
  ok(small.length === 0, `${tag} objetivos visibles ≥ 44 px en el resultado (${sizes.length} medidos; enlace de correo en línea exento por 2.5.8)`);
  const restart = await tabTo(p, x => x.tag === 'BUTTON' && x.text === 'Repetir el test', 8);
  const outline = await p.evaluate(() => { const s = getComputedStyle(document.activeElement); return s.outlineStyle + ' ' + s.outlineWidth + ' ' + s.outlineColor + ' offset ' + s.outlineOffset; });
  ok(!!restart && /solid 2px rgb\(29, 95, 148\) offset 2px/.test(outline), `${tag} foco visible en "Repetir el test": ${outline}`);
  await p.keyboard.press('Enter');
  a = await active(p);
  const reset = await p.evaluate(() => document.querySelectorAll('#calma-test input:checked').length);
  ok(a.tag === 'H2' && /generación/.test(a.text) && reset === 0, `${tag} Repetir el test vuelve a la generación con el formulario vacío y foco en su H2`);
  const trans = await p.evaluate(() => getComputedStyle(document.querySelector('[data-calma-bar]')).transitionDuration);
  ok(trans === '0s', `${tag} prefers-reduced-motion: reduce → sin transición (${trans})`);
  ok(errors.length === 0, `${tag} sin errores de JavaScript (${errors.join(' | ') || '0'})`);
  await ctx.close();
}
async function noJsCheck(browser, axeStore) {
  const ctx = await browser.newContext({ viewport: { width: 320, height: 800 }, javaScriptEnabled: false });
  const p = await ctx.newPage();
  await p.goto('file://' + harness);
  const info = await p.evaluate(() => ({
    fieldsets: document.querySelectorAll('#calma-test fieldset').length,
    visibleFieldsets: [...document.querySelectorAll('#calma-test fieldset')].filter(f => f.offsetParent).length,
    radios: [...document.querySelectorAll('#calma-test input[type=radio]')].filter(r => r.offsetParent).length,
    legends: [...document.querySelectorAll('#calma-test fieldset legend h2')].map(h => h.textContent),
    headings: [...document.querySelectorAll('#calma-test h1, #calma-test h2, #calma-test h3')].filter(h => h.offsetParent).map(h => h.tagName),
    nojs: !!document.querySelector('[data-calma-nojs]').offsetParent,
    dims: /4 dimensiones/.test(document.body.textContent), scroll: document.documentElement.scrollWidth <= document.documentElement.clientWidth }));
  ok(info.visibleFieldsets === 13 && info.radios === 52, `[sin JS 320px] formulario completo visible: ${info.visibleFieldsets} fieldsets (generación + 12), ${info.radios} radios`);
  ok(info.nojs && info.dims && info.scroll, `[sin JS 320px] aviso sin JavaScript visible, sección de dimensiones presente, sin scroll horizontal`);
  let jumps = 0; for (let i = 1; i < info.headings.length; i++) if (+info.headings[i][1] - +info.headings[i - 1][1] > 1) jumps++;
  ok(jumps === 0, `[sin JS 320px] encabezados sin saltos: ${info.headings.join(' ')}`);
  await p.screenshot({ path: path.join(OUT, 'sin-js-320.png'), fullPage: true });
  await ctx.close();
}
(async () => {
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--no-proxy-server'] });
  const axeStore = {};
  const names = Object.keys(COMBOS);
  await keyboardRun(browser, 390, names[0], COMBOS[names[0]], { axe: true, shots: true, errorPath: true, back: true, gen: 0 }, axeStore);
  await keyboardRun(browser, 320, names[1], COMBOS[names[1]], { axe: true, shots: true, gen: 3 }, axeStore);
  await keyboardRun(browser, 390, names[2], COMBOS[names[2]], { gen: 1 }, axeStore);
  await keyboardRun(browser, 320, names[3], COMBOS[names[3]], { gen: 2 }, axeStore);
  await keyboardRun(browser, 390, names[4], COMBOS[names[4]], { gen: 3 }, axeStore);
  await noJsCheck(browser, axeStore);
  await browser.close();
  fs.writeFileSync(path.join(OUT, 'qa-resultado.json'), JSON.stringify({ log, axe: axeStore }, null, 2));
  console.log(log.join('\n'));
  console.log(`\n${fails} fallas · evidencias en ${OUT}`);
  process.exit(fails ? 1 : 0);
})();
