---
name: mobile-qa
description: Pruebas mobile reproducibles para codigocalma.com en 360, 390 y 430 px de ancho (más 1280 de control) — sin scroll horizontal, contenido no recortado, márgenes laterales, áreas táctiles ≥ 44 px, legibilidad y capturas antes/después. Úsala al cierre de cada etapa y ante cualquier cambio de CSS o plantilla.
---

# Mobile QA — Código Calma

## Herramienta
Playwright + Chromium preinstalados (`/opt/node22/lib/node_modules/playwright`, `/opt/pw-browsers/chromium`). Scripts en `docs/auditoria/scripts/capturas.js` (capturas + métricas) y `docs/auditoria/scripts/traza-recorte.js` (cadena de ancestros de un elemento recortado).
En este entorno el navegador no confía en el CA del proxy: los scripts enrutan las peticiones por `fetch` de Node (que sí valida TLS). Ejecutar con `NODE_USE_ENV_PROXY=1 node docs/auditoria/scripts/capturas.js <carpeta-salida>`.
Para probar la rama local (no producción) servir el HTML/tema en un WordPress local o staging y cambiar la URL base.

## Páginas mínimas
Inicio, Servicios, Contacto, Sobre (equipo), Blog, un artículo largo, una categoría, Test, Descargas, 404.

## Anchos
360 (Android chico), 390 (iPhone 12–15), 430 (iPhone Pro Max), 1280 (desktop de control). Alto de viewport 844.

## Checks automáticos (por página y ancho)
```js
const r = await page.evaluate(() => {
  const vw = innerWidth;
  return {
    overflowX: document.documentElement.scrollWidth - vw,                  // debe ser 0
    clipped: [...document.querySelectorAll('h1,h2,h3,p,li,a,button,img')]
      .filter(e => { const b = e.getBoundingClientRect(); return b.width && (b.left < 0 || b.right > vw + 1); })
      .map(e => e.tagName + ': ' + e.textContent.trim().slice(0, 40)),        // debe estar vacío
    smallTargets: [...document.querySelectorAll('a,button,input,select,textarea,[role=button]')]
      .filter(e => { const b = e.getBoundingClientRect(); return b.width && b.height && (b.height < 44 || b.width < 44)
        && !e.closest('p,li'); })                                            // enlaces en línea dentro de texto se excluyen
      .map(e => (e.textContent || e.getAttribute('aria-label') || e.tagName).trim().slice(0, 30)),
    minGutter: Math.min(...[...document.querySelectorAll('main p, main h1, main h2')]
      .map(e => e.getBoundingClientRect()).filter(b => b.width).map(b => Math.min(b.left, vw - b.right))), // ≥ 16 (objetivo 20)
    bodyFont: parseFloat(getComputedStyle(document.querySelector('main p') || document.body).fontSize),  // ≥ 16
  };
});
```
Además: esperar el fin de animaciones de entrada (o emular `prefers-reduced-motion: reduce`) antes de medir, porque hoy hay columnas con `transform: translateX(-74px)` que dejan texto fuera de pantalla.

## Checks manuales
- [ ] Menú mobile: abre/cierra, foco atrapado dentro, cierra con Esc, ítems ≥ 44 px.
- [ ] CTA "Solicitar una consulta" visible en la primera pantalla de Servicios e Inicio.
- [ ] Formularios: teclado correcto (`type="email"`), el zoom no se dispara (inputs ≥ 16 px).
- [ ] Tarjetas: padding ≥ 20 px, números/íconos dentro.
- [ ] Sin franjas vacías arriba del contenido ni antes del footer.
- [ ] Imágenes sin deformación, con dimensiones (sin saltos de layout al cargar).
- [ ] Orientación horizontal (844×390) sin cortes.
- [ ] Zoom de texto 200 % sin superposición.

## Criterio de aprobación
`overflowX = 0`, `clipped = []`, `minGutter ≥ 16`, cero áreas táctiles < 44 px fuera de texto corrido, en los 3 anchos y en todas las páginas mínimas.

## Informe
`docs/auditoria/informes/mobile-qa-etapa-N.md`: tabla página × ancho con cada métrica ✅/❌ y capturas `capturas-antes/` vs `capturas-despues-etapa-N/` con el mismo nombre de archivo.

## Línea base (26-09-2026, producción)
- Inicio 390 px: el H2 "Bienvenidos a Código Calma" y su párrafo empiezan en x = −49 px (columna con `transform: translateX(-74px)` de animación) y los títulos de las tarjetas del blog aparecen recortados por el contenedor `.wp-site-blocks` (overflow: clip) con 40 px de margen a cada lado.
- Servicios 390 px: tarjetas de pasos sin padding interno; el círculo del número queda sobre el borde.
- Botón "Solicitar una consulta": en inicio blanco sobre `#64b2e5` = 2,32:1 ❌.
- Footer: solo íconos y ©; franja blanca vacía antes del footer.
