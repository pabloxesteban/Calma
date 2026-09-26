# Test de consumo digital: bloque HTML accesible (Etapa 2)

Archivo: `contenido/etapa-2/bloques/test-consumo-digital.html`, un único bloque autocontenido (CSS bajo `.calma-test`, HTML y JS vanilla en IIFE).
Resuelve: **A11Y-01** (bloqueante), **A11Y-05**, **A11Y-11**, **A11Y-12**, **GEO-14** y las correcciones **E01–E10** de `contenido/etapa-1/correcciones.md`.
QA: `docs/auditoria/scripts/test-consumo-digital-qa.js` (**215 comprobaciones, 0 fallas**).

## 1. Qué reemplazar en el editor

Página **Test** (`/test/`, id 1941). Fila Kadence `kb-row-layout-id1941_a6afa5-34`, columna `kadence-column1941_6d7620-f4`.

1. Selecciona el bloque **HTML personalizado** de esa columna. Hoy contiene `<style data-wp-block-html="css">` con `:root{--blue…}` y `*{margin:0;padding:0}`, el `<script data-wp-block-html="js">` con `QUESTIONS`/`PROFILES` y el marcado `#app` con `#screen-0` a `#screen-3`.
2. En "Editar como HTML", borra **todo** el contenido del bloque y pega el archivo completo, desde `<!--` hasta el último `</div>`.
   - Si la versión de WordPress muestra pestañas separadas de HTML, CSS y JS en el bloque (los atributos `data-wp-block-html` lo sugieren), vacía las pestañas CSS y JS y pega todo en la pestaña HTML. El `<style>` y el `<script>` van dentro de `.calma-test` y funcionan así.
3. **No toques** las filas siguientes: `1941_572bb6-0b`, `1941_40957c-cc` ("Dato que vale la pena saber" / "Tus resultados son tuyos") y `1941_2b6a25-16` (3 info boxes). La Etapa 1 no define correcciones para ellas.
4. Guarda como borrador o en staging, no publiques (regla común 5). Después de guardar, comprueba en la vista previa que el `<script>` sigue sin `<p>` ni `&#8217;` insertados.
   - El archivo no tiene líneas en blanco, usa comillas simples y no tiene `</` dentro del script.
   - En contenido con bloques, WordPress no aplica `wpautop`, y `wptexturize` omite `<script>` y `<style>`.
5. Purga LiteSpeed Cache de `/test/`.

Al quitar el CSS anterior se eliminan también sus efectos globales: `:root` redefinía variables y `*{margin:0;padding:0}` anulaba márgenes en todo el sitio.

## 2. Decisiones

- **Paso a paso (una pregunta por pantalla) sobre formulario completo.** El test original da una respuesta y un "Dato" después de cada pregunta. Mostrar 12 preguntas con 12 datos en una sola página aumenta mucho la carga cognitiva. Una pregunta por pantalla, con el progreso en texto, es más previsible para accesibilidad cognitiva y conserva la experiencia. Sin JS, el mismo HTML se ve como formulario completo.
- **Progressive enhancement.**
  - Sin JS: se ve la intro, "Qué mide" (4 dimensiones y cómo se calcula el puntaje), la generación y las 12 preguntas como `<form>` con `<fieldset>`, `<legend>` y radios nativos, más un aviso de que el cálculo necesita JavaScript.
  - Los datos por pregunta están en el HTML como `<p hidden>` y los puntajes en `value` de cada radio (fuente única: el JS los lee del DOM).
  - Los perfiles siguen en JS.
- **Flujo con JS.**
  - "Empezar" lleva a la generación y luego a P1…P12. Cada pantalla tiene "Anterior" y "Siguiente".
  - El primer "Siguiente" muestra la retroalimentación y el dato en una región `role="status"`. El botón pasa a "Siguiente pregunta" y, en la última, a "Ver mi resultado".
  - Si cambias la respuesta después de ver la retroalimentación, esta se oculta y hay que confirmar de nuevo. Ya no se bloquean las respuestas como en el original.
  - Enter dentro de un radio equivale a "Siguiente": el botón es `type="submit"` y el `submit` se intercepta.
- **Foco y anuncios (A11Y-11).**
  - En cada cambio de pantalla, el foco va al H2 de la pantalla (`tabindex="-1"`, con `scroll-margin-top:120px` por el header fijo).
  - Una región `aria-live="polite"` anuncia "Pregunta N de 12". En el resultado, el foco va a su H2 y se anuncia "Tu resultado está listo".
  - La barra de progreso es decorativa (`aria-hidden`). El progreso real es texto visible, y el número de pregunta también está en cada `<legend>` (oculto visualmente con JS).
- **Generación (A11Y-01).**
  - Las tarjetas son radios nativos con `<label>`, y se agrega **"Otra / prefiero no decirlo"**.
  - "Continuar" nunca se desactiva. Sin elección, muestra "Elige una opción para continuar." (asociado con `aria-describedby`), lo anuncia y lleva el foco a la primera opción.
  - **Contexto neutro:** en el script original la generación **no cambia nada** (`QUESTIONS.x` y `QUESTIONS.z` son copias de `QUESTIONS.millennial` y el resultado no la menciona). Todas las opciones, incluida "Otra", dan las mismas preguntas y el mismo cálculo.
- **Encabezados (A11Y-12).** El H1 "Test de consumo digital" queda **dentro del bloque**, porque hoy es el único H1 de la página. Está comentado en el archivo: si se activa el título de Kadence, hay que cambiarlo a `<p>`. Debajo van solo H2 (intro, generación, cada pregunta, resultado) y un H3 ("Un paso concreto"). Sin JS: H1 → 16 × H2, sin saltos.
- **Estilo.** Tokens `var(--calma-*, fallback)`, radios de 16 px, botones pill de 48 px, foco de 2 px #1d5f94 con offset de 2 px, sin fuentes externas (antes: Roboto) y sin `:root` ni `*`. Todas las transiciones están dentro de `prefers-reduced-motion: no-preference`. El scroll es `smooth` solo sin `reduce`.
- **Eliminado.** El botón "↺" del encabezado (sin nombre accesible; lo reemplaza "Repetir el test"), el pie "Código Calma" de la intro (2,27:1), los emojis como contenido (quedan `aria-hidden`) y todos los `onclick` inline.
- **Resultado.**
  - Muestra emoji, título, subtítulo, "Tu puntaje: N de 48 puntos", el análisis y "Un paso concreto" (texto original en tuteo, correo como `mailto:`).
  - Agrega la línea "Este resultado es orientativo: no es un diagnóstico ni reemplaza una evaluación profesional." y el aviso de urgencias con **`[COMPLETAR: enlace a líneas de ayuda]`** visible.
  - CTA: "Solicitar una consulta →" (primario, `/contacto/?area=habitos`) y "Repetir el test" (botón secundario, vuelve a la generación con el formulario vacío).

## 3. Verificación (Playwright + Chromium, sin red)

Comando:
```
AXE_PATH=<scratchpad>/a11y/node_modules/axe-core/axe.min.js OUT_DIR=<salida> node docs/auditoria/scripts/test-consumo-digital-qa.js
```
El script envuelve el bloque en una página mínima (`lang="es"`, un enlace de header antes del bloque). Conduce todo **solo con teclado** (Tab, Shift+Tab, flechas, Espacio y Enter) con `reducedMotion: 'reduce'`. Para comparar, ejecuta el script **original** del snapshot (`docs/auditoria/snapshot-2026-09-26/html/test.html`, funciones `selectGen`/`confirmGen`/`nextQuestion`/`showResult` sin modificar) con las mismas respuestas.

| Comprobación | Resultado |
|---|---|
| Teclado de principio a fin, 5 recorridos (390 px ×3, 320 px ×2) | ✅ Tab → "Empezar" → Enter → foco en H2 de generación → radios (flechas/Espacio) → "Continuar" → 12 preguntas → "Ver mi resultado" → foco en H2 del resultado |
| Foco al cambiar de pantalla | ✅ en el H2 de cada una de las 12 preguntas, de la generación y del resultado; tras "Repetir el test", en el H2 de generación |
| Anuncio `aria-live` | ✅ "Pregunta N de 12" en cada paso; "Tu resultado está listo" |
| Retroalimentación y dato | ✅ en `role="status"`; el foco se queda en el botón ("Siguiente pregunta" / "Ver mi resultado") |
| "Continuar" sin elegir | ✅ error visible y foco en la primera opción (antes: botón inalcanzable) |
| "Anterior" (Shift+Tab) | ✅ vuelve a P2 con foco en su H2 y la respuesta conservada; al volver a P3, Tab va a la opción ya marcada |
| Cálculo igual al original | ✅ A (todas la 1.ª opción): **Navegante con marea**, 13 pts = original · B (máximo): **Arquitecto digital**, 46 = original · C (18 pts, borde de redondeo 37,5 % → 38): **Arquitecto digital** = original · D: **Arquitecto digital**, 35 = original · E (16 pts, generación "Otra"): **Consumo consciente** = original |
| axe-core (wcag2a/aa, 21a/aa, 22aa, best-practice) | ✅ **0 violaciones de cualquier severidad** en inicio, pregunta 6 con retroalimentación y resultado, a 390 y 320 px |
| Reflow 320 / 390 px | ✅ sin scroll horizontal en inicio, pregunta y resultado |
| Objetivos táctiles | ✅ opciones ≥ 48 px de alto (label completa); botones y CTA ≥ 48 px; el enlace de correo en línea está exento (2.5.8) |
| Foco visible | ✅ `solid 2px rgb(29, 95, 148)` con offset de 2 px (medido en "Repetir el test"); opciones con contorno vía `:has(:focus-visible)` |
| `prefers-reduced-motion: reduce` | ✅ `transition-duration: 0s` |
| Sin JavaScript (320 px) | ✅ 13 fieldsets (generación + 12) y 52 radios visibles, aviso sin JS, sección de dimensiones, encabezados H1 → H2 sin saltos |
| Errores de JS | ✅ 0 en los 5 recorridos |

Contraste de texto (WCAG 2.x):

| Texto / fondo | Contraste |
|---|---|
| H1, enlaces y botón secundario #1d5f94 / #fff | 6,74:1 |
| Botón primario #fff / #1d5f94 | 6,74:1 (hover 8,86:1) |
| Texto secundario #475569 / #fff | 7,58:1 (sobre opción marcada #eef4fa: 6,84:1) |
| Progreso y eyebrow #5b3fb8 / #fff | 7,37:1 (sobre #f1eefc: 6,45:1) |
| Retroalimentación, placeholder y urgencias #0f172a / fondos claros | ≥ 15,6:1 |
| Error #b42318 / #fff | 6,57:1 |

Antes (A11Y-05): 3,11:1, 2,12:1, 2,71:1, 2,79:1, 4,31:1 y 2,27:1.

Evidencias, en el scratchpad de la sesión (fuera del repo), carpeta `qa-test/`:
- `qa-resultado.json`: log completo y salida de axe.
- `log.txt`
- Capturas: `inicio-390.png`, `pregunta6-390.png`, `resultado-390.png`, `inicio-320.png`, `pregunta6-320.png`, `resultado-320.png`, `sin-js-320.png`.

Se regeneran con el comando de arriba. Pendiente manual (criterio de la Etapa 2): escuchar el recorrido con NVDA o VoiceOver.

## 4. Textos cambiados (antes → después)

La lista completa también está en el comentario inicial del archivo. Preguntas, opciones, puntajes, datos, perfiles y umbrales: **sin cambios de fondo**.

| Dónde | Antes | Después |
|---|---|---|
| H1 (E10) | Test de Consumo Digital | Test de consumo digital |
| Bajada (E01) | Descubrí cómo es tu relación… | Descubre cómo es tu relación… |
| Pasos (E02–E04) | Elegís / Respondés / Obtenés | Eliges / Respondes / Obtienes |
| Generación (E05–E06) | ¿De qué generación sos? / Elegí la que mejor te representa | ¿De qué generación eres? / Elige la que mejor te representa |
| Años | 1981 — 1996 (y demás) | 1981–1996 |
| CTA (E07–E08) | Contactanos → / Volver a jugar → | Solicitar una consulta → / Repetir el test |
| Un paso concreto | Escribinos a… | Escríbenos a… |
| Puntaje | / 48 pts | Tu puntaje: N de 48 puntos |
| Retroalimentación | ✓ Buen manejo Tu respuesta… | ✓ Buen manejo. Tu respuesta… (punto añadido; ícono oculto a lectores de pantalla) |
| Dato | (sin etiqueta) | "Dato: " + texto original |
| P1 | Son las 11pm… ¿Qué hacés… | Son las 11 p. m.… ¿Qué haces… |
| P2 (E09) | te quedás… ¿cómo te sentís? / Un poco incómodo pero me adapto | te quedas… ¿cómo te sientes? / Un poco incómodo, pero me adapto |
| P3 | abrís | abres |
| P4, P7 | ¿Podés… | ¿Puedes… |
| P5 | en vos | en ti |
| P6 | Subís | Subes |
| P7 | Sí pero requiere práctica / Sí lo disfruto | Sí, pero requiere práctica / Sí, lo disfruto |
| P8 | ¿Sabés… pasás…? | ¿Sabes… pasas…? |
| P12 | ¿Checkeás… | ¿Chequeas… |
| Dato P8 | lo que pasás… lo que elegiría | lo que pasas… lo que elegirías |
| Dato P10 | decidís | decides |
| Títulos de perfil | Arquitecto Digital, Consumo Consciente, Navegante con Marea, En Modo Automático, Corriente Abajo, Atrapado en el Sistema | Mayúscula solo inicial (como E10) |
| Perfiles | elegís / Sabés… Tomás / hacés… sabés / Avanzás / de vos | eliges / Sabes… Tomas / haces… sabes / Avanzas / de ti |

**Textos nuevos:**
- La opción "Otra / prefiero no decirlo".
- La sección "Qué mide": "Las 12 preguntas recorren 4 dimensiones…" más "Cada respuesta suma de 1 a 4 puntos, con un máximo de 48. Tu perfil se calcula a partir del puntaje total.", un dato tomado del script.
- El aviso sin JS, la línea de resultado orientativo y el aviso de urgencias.

## 5. Placeholders y recomendaciones (no aplicadas)

1. **`[COMPLETAR: nombres de las 4 dimensiones que mide el test]`.** El test original dice "4 dimensiones" pero no las nombra en ningún sitio: ni en el HTML, ni en el script, ni en el snapshot, ni en `llms.txt`. No se inventaron.
   - Propuesta para que valide Tatiana X. Stacul, agrupando las preguntas existentes: hábitos y sueño (P1, P12), atención y foco (P3, P4, P7, P10), emociones y vínculos (P2, P5, P6, P9) y conciencia de uso y herramientas (P8, P11).
   - Hay que registrar este placeholder y el de líneas de ayuda en `docs/placeholders.md` (no se tocó por alcance).
2. **`[COMPLETAR: enlace a líneas de ayuda]`** en el resultado: se necesita la fuente oficial por país.
3. **Posible error de cálculo en el original (se conservó idéntico).**
   - Los umbrales de `PROFILES` (38, 32, 24, 16, 8, 0) se comparan con el **porcentaje** (`score/48*100`). Como el puntaje mínimo posible es 12 (25 %), "En modo automático", "Corriente abajo" y "Atrapado en el sistema" son **inalcanzables**.
   - Cualquier puntaje ≥ 18 (38 %) da "Arquitecto digital": responder 2 puntos en todo (24 pts) da el perfil más alto.
   - Parece que los umbrales se pensaron en puntos sobre 48. Si el equipo lo confirma, basta con cambiar en el JS `pct >= PROFILES[j].min` por `score >= PROFILES[j].min`. Es un cambio de fondo y se propone, no se aplica.
4. **"Eliges tu generación para personalizar el contexto"** promete una personalización que no existe (la generación no cambia preguntas ni resultado). Se propone reformular o quitar el paso. Se mantuvo por la regla de no cambiar contenido.
5. **Jerarquía de los bloques Kadence siguientes.**
   - "Dato que vale la pena saber" es H6 y va antes del H2 "Tus resultados son tuyos". Los 3 info boxes son H5 (Contexto colapsado, Datos de comportamiento, El valor está en la reflexión). Tras los H2 del test quedan saltos H2 → H6 y H2 → H5 (axe `heading-order`).
   - Recomendación: pasar el H6 a párrafo con estilo de eyebrow (`.calma-badge`) y los H5 de los info boxes a H3.
   - Además, la fila `1941_2b6a25-16` usa `animated fadeInUp` (Blocks Animation): verificar que respete `prefers-reduced-motion`.
6. **Otros textos no corregidos (no son voseo):**
   - "Scrolleo", "likes" y "¿Cómo es tu relación con notificaciones?" (falta "las"). Revisión de estilo opcional con Francisca Cortés Santoro.
   - Las comillas simples de 'aburrimiento' se mantienen; la unificación a « » queda para la Etapa 5 (CRO #64).
