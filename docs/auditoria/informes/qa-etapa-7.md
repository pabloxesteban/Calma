# QA · Etapa 7 (organismo digital: fase 1 + tarjetas)

Vista previa: `staging/preview/build.py etapa-7` sobre el snapshot de producción. Fecha: 2026-09-27.

## Accesibilidad (accessibility-qa)
- **axe-core** (WCAG 2.0/2.1/2.2 A y AA): **0 violaciones** en 14 páginas × 2 anchos (1280 y 390). Resultado en `qa-accesibilidad-etapa-7.json`.
  - La primera pasada encontró 4 textos grises de Kadence (`--global-palette6`, #64748b) con 4,48:1 sobre el papel nuevo. Se corrigió a #566173 (6,0:1).
- **Reflow a 320 px**: sin desborde horizontal en ninguna página.
- **Menú móvil**: foco atrapado en el panel, Escape cierra y devuelve el foco, fondo papel y contraste correcto.
- **Seis estados**:
  - el botón tiene `aria-expanded` y `aria-controls`, y cambia de texto ("Ver" / "Ocultar el hallazgo");
  - el panel cerrado queda con `visibility: hidden`, así que no se lee ni recibe foco; abierto, el Tab siguiente llega al enlace de la fuente;
  - el foco es visible;
  - sin JavaScript, todos los hallazgos se ven abiertos y el botón no aparece.
- **Figuras** (canvas y SVG): `aria-hidden`. El dato, la fuente y el rótulo están en texto y no dependen del color ni del movimiento.
- **Movimiento reducido** (`prefers-reduced-motion: reduce`):
  - ningún elemento anima ni tiene transiciones de más de 0,3 s;
  - la red se dibuja quieta en su equilibrio y cada organismo muestra su estado final.
- **"Reducir movimiento"**: `aria-pressed`, se aplica al instante (pausa la red) y se recuerda al recargar.
- **WCAG 2.2.2**: la red se detiene sola (unos 3 s de crecimiento y respiración, después quieta) y cada organismo dura menos de 5 s. No hay bucles.
- **Test de consumo digital**: el recorrido de la vieja versión en `a11y-qa-etapa.js` ya no aplica (la Etapa 2 cambió sus ids). Ahora se salta y queda anotado; el recorrido vigente es `test-consumo-digital-qa.js`. El test no cambió en esta etapa.

## Móvil (mobile-qa)
- 360, 390 y 430 px en Inicio y Blog:
  - sin desborde ni texto recortado;
  - objetivos táctiles ≥ 44 px (el único aviso, «Infancias «Figitales»», es un enlace dentro del texto y ya aparecía desde la Etapa 2).
- La red usa 46 nodos en celular (110 en escritorio) y responde al toque sin bloquear el scroll: los eventos son pasivos y no hay `preventDefault`.
- Los seis estados van en una columna compacta y se animan al entrar en pantalla o al tocarlos.

## Rendimiento
- **CLS 0** en Inicio y Blog: el canvas es absoluto, las figuras tienen tamaño declarado y el lugar ya está reservado.
- **LCP**: sigue siendo el titular o la imagen. La red arranca en `requestIdleCallback`, después del contenido principal. La medición de laboratorio (`rendimiento-etapa-7.json`) sirve solo como comparación cualitativa (ver la nota del script).
- **Peso nuevo**: `calma-organismo.js` 6,4 KB gzip + `calma-etapa7.css` 5,9 KB gzip. Reemplazan a los archivos de la Etapa 6.
- **Regulador**: con cuadros lentos sostenidos, la red se detiene en reposo; a la segunda vez queda quieta. Con ahorro de datos o memoria mínima, empieza quieta. El canvas se pausa fuera de pantalla y con la pestaña oculta. DPR máximo 1,5.

## Capturas
- `docs/auditoria/capturas-despues-etapa-7/` (Inicio y Blog en 4 anchos).
- `docs/diseno/etapa-7-*.png`: hero en reposo y perturbado, cifras, estados, hallazgo abierto, tarjetas, cuadros, móvil y movimiento reducido.
