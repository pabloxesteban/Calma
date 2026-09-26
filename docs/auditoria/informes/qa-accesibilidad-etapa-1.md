# QA de accesibilidad: Etapa 1 (antes de aplicarla en WordPress)

**Fecha:** 2026-09-26 · **Revisor:** subagente `accessibility-qa` · **Línea base:** `informes/accesibilidad.md`
**Qué se revisó:** plugin `wp-content/plugins/codigo-calma/` (tokens, `calma-etapa1.css`, PHP), bloques de `contenido/etapa-1/bloques/`, `correcciones.md` y la guía `docs/implementacion/etapa-1.md`.

## Método
- **Antes:** producción en vivo. **Después:** vista previa `staging/preview/build/*.html` (HTML de producción con la Etapa 1 aplicada). El documento principal se sirvió en local y el resto se pidió a producción con `fetch` de Node, con TLS verificado.
- **Script:** `docs/auditoria/scripts/a11y-qa-etapa.js` (`--live` o `--preview`). Hace lo siguiente:
  - axe-core 4.x con las etiquetas wcag2a/aa, wcag21a/aa, wcag22aa y best-practice, a 1280 y 390 px, en 11 páginas.
  - Revisa encabezados visibles, 20 pasos de Tab y reflow a 320 px.
  - Prueba el menú mobile con teclado, el test en sus 4 pantallas y `prefers-reduced-motion`.
- **Revisión complementaria:** estilos de foco por CDP (reglas que ganan en la cascada), capturas del foco después de las transiciones, y muestreo de píxeles para el texto sobre degradé, que axe no puede evaluar.
- **Límites:**
  - `/blog/` en vivo volvió a responder "Bot Verification" en la segunda pasada (A11Y-17 sigue abierto). Para ese "antes" se usa la primera pasada del día.
  - El formulario de la vista previa emula el Kadence Advanced Form. Los mensajes de error reales solo se pueden verificar en el sitio.

## Antes / después por página (axe: violaciones · nodos; valores a 1280 / 390 px)
CC = `color-contrast`, H1 = `page-has-heading-one`, HO = `heading-order`, TS = `target-size`.

| Página | Antes (vivo) | Después (vista previa) | H1 visibles antes → después |
|---|---|---|---|
| inicio | CC 18/17 · HO 1/1 · TS 1/– | HO 1/1 · TS 1/– | 2 (al final) → **1** «Te damos la bienvenida…» |
| servicios | CC 2/1 · H1 · TS 1/– | TS 1/– | 0 → **1** |
| contacto | CC 2/1 · H1 · TS 1/– | TS 1/– | 0 → **1** |
| sobre_tatiana | CC 2/1 · link-name 1/1 · TS 1/– | link-name 1/1 · TS 1/– | 1 → 1 |
| blog | CC 13/13 · H1 | TS 1/– | 0 → **1** «Blog» |
| artículo *por-que-fallamos…* | CC 1/1 · TS 1/– | TS 1/– | 1 → 1 |
| test (pantalla 0) | CC 2/5 · HO 3/3 · TS 1/– | CC 2/2 · HO 3/3 · TS 1/– | 1 → 1 |
| test (pantallas 1, 2 y 3) | CC 7 · 2 · 2 | CC 7 · 1 · 2 | — |
| testimonios | CC 14/14 · H1 | TS 1/– | 0 → **1** |
| herramientas | CC 5/4 · button-name 3/3 · HO 3/3 · TS 4/3 · scrollable-region 0/1 | CC 3/3 · button-name 3/3 · HO 3/3 · TS 4/3 · scrollable-region 0/1 | 1 → 1 |
| bienestar-digital | HO 2/2 | HO 1/1 | 3 → **1** |
| descargas-2 | CC 8/8 · H1 | HO 1/1 · TS 1/– | 0 → **1** |
| **Total de nodos CC a 1280** | **67** | **5** (test 2 y herramientas 3) | Todas las páginas con un H1 único |

El TS restante es siempre el mismo: `button.dropdown-nav-special-toggle` de 16×53 px (ver Q-08).

## Criterios de aceptación de la Etapa 1
| Criterio | Resultado | Evidencia |
|---|---|---|
| 0 violaciones de contraste en axe | **Cumple con salvedades** | Las 9 páginas de contenido quedan en 0. Siguen el test (A11Y-05, Q-04) y herramientas (Q-05), con CSS propio fuera del plugin. Además hay un fallo que axe no ve, porque el texto está sobre un degradé: Q-02 en el hero del inicio. |
| Un H1 único, sin saltos graves | **Cumple** | 11 de 11 páginas tienen un solo H1 y es el primer encabezado visible. Los saltos que quedan son leves (H1→H3 y H2→H5); ver Q-06. |
| Menú mobile claro y operable | **Cumple** | Botón de 48×48 (antes 37×31). Fondo #fff y enlaces #0f172a (17:1). Ítem actual en #1d5f94 (6,7:1) con `aria-current`. Filas de 50 px, foco de 2 px sólido, foco atrapado en el menú, Esc lo cierra y devuelve el foco al botón. axe da 0 dentro del drawer. |
| Foco visible | **No cumple en los campos** | Enlaces y botones tienen contorno de 2 px #1d5f94 (verificado tras la transición de 0,3 s de Kadence). **Los campos de texto del formulario y del buscador no muestran ningún cambio al recibir el foco** (Q-01). |
| Formulario: etiquetas visibles en español, autocomplete y privacidad | **Cumple, con dos pendientes** | Etiquetas encima del campo, en español y asociadas con `for`. `autocomplete` name y email, ayudas con `aria-describedby`, campos de 48 px, casilla de privacidad obligatoria de 24 px y aviso de urgencias. Pendientes: el asterisco no se explica, y el enlace de privacidad es `href="#"` con `[COMPLETAR]` (Q-07). |
| Contenido no oculto por animaciones | **Cumple, salvo el texto escrito del hero** | 0 textos ocultos o fuera de pantalla. Con `reduce` no queda ninguna transición (las flip-boxes pasan de 0,6 s a 0). El texto animado del hero sigue escribiéndose y borrándose en bucle (Q-02). |
| Reflow a 320 px | **Cumple** | Desborde de 0 px en las 11 páginas. El texto escrito del hero, que antes se salía del contenedor, ya no se sale. |

## A11Y-01 (test con teclado): confirmado sin cambios
La secuencia de Tab es idéntica antes y después:
1. «Empezar».
2. «Continuar →», que sigue bloqueado con `pointer-events:none` y opacidad 0,4.
3. De ahí el foco salta al pie.

Las tarjetas `.gen-card` siguen siendo `<div>` con `tabindex=-1` y sin rol. **La Etapa 1 no empeora la operación con teclado.** Hay dos efectos menores:
- El contraste de `--gray-3` pasa de 3,11 a **2,97:1**, porque ahora se ve el fondo #f8fafc: el plugin deja transparente `.content-bg`.
- El foco global `:where(...)` no le gana a `.answer-btn:focus{outline:none}` del CSS del test.

**Recomendación:** adelantar A11Y-01 (esfuerzo S) y, mientras tanto, incluir ya el CSS de Q-04.

## Hallazgos nuevos o pendientes
| ID | WCAG | Sev. | Evidencia | Corrección propuesta |
|---|---|---|---|---|
| Q-01 | 2.4.7 | **Alta** | Contacto: `input[type=text/email]` y `textarea` tienen `outline:0` y el mismo borde #64748b con foco y sin foco. Lo imponen `.kb-form-basic-style input[type=text]:focus` (especificidad 0,3,1) y `input[type=text]:focus` de Kadence, que le ganan a `:where()` (0,1,0). A11Y-20 se daba por resuelto y no lo está. | Añadir a `calma-etapa1.css` §7 el bloque **CSS-1** (abajo). |
| Q-02 | 1.4.3, 2.2.2 | **Alta** | Hero del inicio (`.kt-adv-heading1204_179e11-cf`). El texto «Comprendiendo el comportamiento humano…» es #f8fafc sobre un degradé lavanda (muestreado entre #acb7d0 y #ccd0e8): **1,5–1,9:1**, a 17 px en mobile y 32 px en escritorio. Además se escribe y se borra en bucle sin control para pausarlo. «PORTAL DE CIBERPSICOLOGÍA» (#174d78) queda entre 4,4 y 5,8:1. axe no lo detecta (fondo con degradé). | Editor: Advanced Heading → color del texto: paleta 3. En «Texto escrito», desactivar el bucle o dejar la frase estática (recomendado por accesibilidad cognitiva). Mientras tanto, en el plugin, el bloque **CSS-2**. |
| Q-03 | 1.4.11, 2.4.7 | Media | Test: `.answer-btn:focus{outline:none}` y los botones `.btn-primary` no tienen contorno de foco. | Incluido en el bloque **CSS-3**. |
| Q-04 | 1.4.3 | Alta (sigue abierto A11Y-05) | Test: `--gray-3` #8a92a6 tiene entre 2,97 y 3,11:1 en 7 nodos de la pantalla 1 y 2 del resultado. El % de progreso #7a9fd4 tiene 2,59:1. El degradé de `.btn-primary` empieza en #5b86c5 (3,6:1 con blanco). `.footer-brand` tiene opacidad 0,5. | El bloque **CSS-3** (limitado a `page-id-1941`) lo resuelve sin tocar el HTML del test. Se puede aplicar ya, sin esperar a la Etapa 5. |
| Q-05 | 1.4.3, 4.1.2, 2.5.8 | Media | Herramientas: `.cc-eyebrow` y `.cc-titulo em` en #4ecdc4 (1,93:1). `.cc-nota` en #b0b8c4 (2:1). Los puntos `.cc-dot` son `<button>` sin nombre y miden 7×7 px. `#ccSlider` no se puede enfocar. | Contraste: bloque **CSS-4**. Marcado (Etapa 2): `<button class="cc-dot" data-cc="0" aria-label="Grupo 1 de 3">` y `min-width/height:24px`. |
| Q-06 | 1.3.1 | Baja | Saltos de encabezado que quedan: inicio, cifras en H3 bajo el H1 (A11Y-07 a medias). Descargas: H1→H3 en las 4 guías. Bienestar: H2→H5 «Cómo comenzar…». Herramientas: 3 H6. Test: H3→H6 y H2→H5. | Agregar a `correcciones.json`: cifras de inicio (Info Box) de H3 a P. Guías de Descargas de H3 a H2. Bienestar de H5 a H3. Herramientas de H6 a P/H3. |
| Q-07 | 3.3.2 | Baja (bloquea la publicación del formulario) | La casilla de privacidad enlaza a `href="#"` (placeholder). El asterisco no se explica. La validación y los errores son los nativos de Kadence y no se pueden ver en la vista previa. | Antes de publicar, completar la URL de privacidad. Añadir sobre el formulario: «Todos los campos son obligatorios.». Tras aplicar la etapa, verificar con envío vacío que el error aparece bajo cada campo y se anuncia (paso 4 de `formulario-contacto.md`; A11Y-10, Etapa 2). |
| Q-08 | 2.5.8 | Baja (excepción justificada) | axe marca `button.dropdown-nav-special-toggle` (16×53) en todas las páginas a 1280. En dispositivos con puntero tiene `pointer-events:none`: es un control solo de teclado. Con pantalla táctil (`hover:none`) ocupa todo el ítem. La regla del plugin `.header-navigation .dropdown-nav-toggle{min-width:24px}` apunta al chevron decorativo y no tiene efecto. | Quitar esa regla o dejarla, sin impacto. Se registra como excepción documentada. |
| Q-09 | 3.1 (lectura fácil) | Baja | Descargas: los títulos de las guías 1 y 2 son nombres de archivo («Ansiedad-Funcional-vs-Ansiedad-Desbordada», «Guia de Ciberseguridad para Psicologos»). D01 y D02 corrigen solo el `alt`. | Agregar D06 y D07: «Ansiedad funcional vs. ansiedad desbordada» y «Guía de ciberseguridad para psicólogos». |

**Pendientes de la línea base que no son de esta etapa (sin regresión):**
- A11Y-08: LinkedIn sin nombre en sobre_tatiana.
- A11Y-10 y A11Y-11.
- A11Y-14: los 14 «Ver testimonio completo» ya miden 44 px, pero siguen sin nombre distintivo.
- A11Y-15: las flip-boxes ya respetan `reduce`, pero siguen el `<a href="">` y el clic sobre un `div`.
- A11Y-16: alt de la foto de Tatiana.
- A11Y-17: reCAPTCHA en `/blog/`. Se reprodujo hoy; lo cubre el paso 1 de la guía.
- A11Y-18 y A11Y-21: «Copy Link» sigue en inglés en el recorrido de foco.

## CSS propuesto (añadir al final de `calma-etapa1.css`)
```css
/* CSS-1 · Q-01: foco visible en campos (gana a Kadence 0,3,1 sin !important) */
html body :is(input:not([type="checkbox"]):not([type="radio"]):not([type="submit"]), textarea, select):focus-visible {
	outline: 2px solid var(--calma-focus);
	outline-offset: 2px;
	border-color: var(--calma-focus);
}
/* CSS-2 · Q-02: texto del hero legible (provisional hasta el cambio en el editor / Etapa 3) */
.kt-adv-heading1204_179e11-cf.has-text-color,
.kt-adv-heading1204_179e11-cf .has-theme-palette-8-color { color: var(--calma-text) !important; }   /* 8,9–11,7:1 */
.kt-adv-heading1204_179e11-cf .has-theme-palette-2-color { color: var(--calma-navy) !important; }
/* CSS-3 · Q-03/Q-04: test de consumo digital (page-id-1941) */
body.page-id-1941 { --gray-3: #4a5068; --blue-dk: #1d5f94; }   /* 7,96:1 sobre #fff; 5,43:1 sobre tarjeta activa #c5d6f7 */
body.page-id-1941 .btn-primary { background: var(--calma-primary); }
body.page-id-1941 .footer-brand { opacity: 1; }
body.page-id-1941 .answer-btn:focus-visible,
body.page-id-1941 .btn-primary:focus-visible { outline: 2px solid var(--calma-focus); outline-offset: 3px; }
/* CSS-4 · Q-05: herramientas (page-id-1618) */
.page-id-1618 .cc-eyebrow,
.page-id-1618 .cc-titulo em { color: #0f766e; }   /* 5,47:1 */
.page-id-1618 .cc-eyebrow { font-size: var(--calma-fs-xs); }
.page-id-1618 .cc-nota { color: var(--calma-text-muted); }   /* 7,58:1 */
```
Aclaraciones:
- «Repetir el test» mantiene su fondo transparente, porque lo define en un estilo en línea.
- «Continuar» desactivado queda exento por ser un control inactivo.
- Tras aplicar el CSS, volver a correr el script con `--preview` y comprobar CC = 0 en las 4 pantallas del test y en herramientas, y que los campos del formulario muestran el contorno.

## Veredicto: **aprueba con condiciones**
La Etapa 1 resuelve A11Y-02, 03, 04, 06, 07 (casi entero), 19 y el menú mobile. Baja los nodos de contraste de 67 a 5 y no introduce regresiones relevantes: la única es la baja de 3,11 a 2,97 en el test, que CSS-3 corrige.

**Condiciones para aplicarla:**
1. Añadir CSS-1, CSS-2 y CSS-3 al plugin. CSS-4 es recomendado.
2. En el editor, desactivar el bucle del texto escrito del hero (Q-02).
3. Completar la URL de privacidad antes de publicar el formulario (Q-07).

**Sin estas condiciones no aprueba**, por Q-01 y Q-02, que son altos. A nivel de sitio, **A11Y-01 sigue siendo bloqueante**: se recomienda adelantarlo desde la Etapa 5 a la 2.
