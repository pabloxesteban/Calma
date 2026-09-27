# QA · Etapa 7 (organismo digital: fase 1, tarjetas y línea de tiempo)

Incluye la segunda ronda de ajustes:
- la red del hero, más suelta y en todo el sector de la flor, con la onda al pasar sobre ella;
- la bienvenida reorganizada;
- las tarjetas planas y más chicas;
- la línea de tiempo que crece con el scroll.

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
- **WCAG 2.2.2**: la red se detiene sola (≈ 4,2 s de aparición y respiración, después quieta) y cada organismo dura menos de 5 s. La onda de la flor dura 1,5 s y solo sale al pasar sobre ella. No hay bucles.
- **Línea de tiempo**:
  - el movimiento sigue al scroll nativo (no lo controla) y solo se redibuja cuando el scroll cambia;
  - las épocas "en reposo" usan tinta suave (7,6:1), así que se leen igual antes de encenderse;
  - la figura es decorativa (`aria-hidden`) y el texto de cada época es el original, con H3 por época;
  - con movimiento reducido o "Reducir movimiento", todo queda encendido, la línea completa y la figura sin transiciones.
- **Test de consumo digital**: el recorrido de la vieja versión en `a11y-qa-etapa.js` ya no aplica (la Etapa 2 cambió sus ids). Ahora se salta y queda anotado; el recorrido vigente es `test-consumo-digital-qa.js`. El test no cambió en esta etapa.

## Móvil (mobile-qa)
- 360, 390 y 430 px en Inicio y Blog:
  - sin desborde ni texto recortado;
  - objetivos táctiles ≥ 44 px (el único aviso, «Infancias «Figitales»», es un enlace dentro del texto y ya aparecía desde la Etapa 2).
- La red usa hasta 64 nodos en celular (150 en escritorio) y responde al toque sin bloquear el scroll: los eventos son pasivos y no hay `preventDefault`.
- Los seis estados van en una columna compacta y se animan al entrar en pantalla o al tocarlos.
- Línea de tiempo en celular: sin la figura grande; la línea crece y cada época se enciende con su ícono. Reflow a 320 px sin desborde.
- Los títulos de las tarjetas que se marcan como objetivos chicos a 430 px son enlaces dentro del texto (excepción de WCAG 2.5.8).

## Rendimiento
- **CLS 0** en Inicio y Blog: el canvas es absoluto, las figuras tienen tamaño declarado y el lugar ya está reservado.
- **LCP**: sigue siendo el titular o la imagen. La red arranca en `requestIdleCallback`, después del contenido principal. La medición de laboratorio (`rendimiento-etapa-7.json`) sirve solo como comparación cualitativa (ver la nota del script).
- **Peso nuevo**: `calma-organismo.js` 9,5 KB gzip + `calma-etapa7.css` 7,5 KB gzip (dentro del presupuesto de 25 KB de la dirección de arte). Reemplazan a los archivos de la Etapa 6.
- **Regulador**: con cuadros lentos sostenidos, la red se detiene en reposo; a la segunda vez queda quieta. Con ahorro de datos o memoria mínima, empieza quieta. El canvas se pausa fuera de pantalla y con la pestaña oculta. DPR máximo 1,5.

## Capturas
- `docs/auditoria/capturas-despues-etapa-7/` (Inicio y Blog en 4 anchos).
- `docs/diseno/etapa-7-*.png`: hero en reposo y perturbado, cifras, estados, hallazgo abierto, tarjetas, cuadros, móvil y movimiento reducido.

## Tercera y cuarta ronda (tarjetas que giran, accesos animados, figura de conexiones, lecturas en grilla bento)
- **axe-core**: 0 violaciones en 14 páginas × 2 anchos. Reflow a 320 px sin desborde. Nada anima con movimiento reducido.
- **Tarjetas que giran** (probado con teclado):
  - Tab → "Dar vuelta y ver el hallazgo" (`aria-expanded`) → Enter gira la tarjeta y lleva el foco al dorso (región con nombre) → Tab al enlace de la fuente → Tab a "Volver a la pregunta" → Enter vuelve y devuelve el foco al botón. Escape también vuelve.
  - La cara oculta queda `inert` y `aria-hidden`.
  - Sin JS, las dos caras se ven una debajo de la otra.
  - Con movimiento reducido, el giro es instantáneo.
- **Accesos**:
  - los dibujos son decorativos (`aria-hidden`) y el nombre accesible es el del botón;
  - con movimiento reducido o sin JS se ven en su pose final (`--p: 1`);
  - el recorrido depende solo de la posición de scroll y los gestos al llegar duran menos de 2 s.
- **Lecturas (grilla bento)**:
  - la tarjeta entera es clicable (el enlace del título la cubre) y la categoría y "Leer más" siguen siendo enlaces propios;
  - los tonos de fondo por categoría mantienen el contraste del texto (tinta sobre tonos muy claros);
  - el número de índice es decorativo.
- **Figura de la línea de tiempo**:
  - es un canvas decorativo (`aria-hidden`) con la aclaración visible "Figura ilustrativa: cada punto es una persona";
  - solo se redibuja cuando cambia el scroll;
  - con movimiento reducido pasa de una época a otra sin transición.
- **Móvil**: sin desborde ni texto recortado a 360/390/430. En celular, la grilla bento pasa a una columna y los personajes llegan a su pose al entrar cada tarjeta.

## Quinta ronda (sin rótulos grises, botón "Ver más", flor que gira, red en circuito)
- **axe-core**: 0 violaciones en 14 páginas × 2 anchos. Reflow a 320 px sin desborde. Con movimiento reducido no anima nada: la flor no gira y el circuito se dibuja completo, sin señales.
- **Tarjetas que giran** (probado con teclado):
  - Tab → "Ver más: hallazgo sobre …" (nombre accesible completo, aunque en pantalla solo se vea el ícono) → Enter gira y lleva el foco al dorso → Tab a la fuente → Tab a "Volver a la pregunta" → Enter vuelve.
  - Escape también vuelve.
  - Con el mouse el foco no se mueve.
- **Hero**:
  - el circuito es decorativo (`aria-hidden`);
  - las señales duran unos 4 s al cargar y ≈ 1,5 s por interacción, y después el dibujo se detiene (WCAG 2.2.2);
  - la red no cambia de forma, así que no hay movimiento de fondo que distraiga la lectura;
  - la rotación de la flor depende solo de la posición del scroll.

## Sexta ronda (flor más lenta, una tarjeta girada por vez, accesos con título)
- **axe-core**: 0 violaciones en 14 páginas × 2 anchos. Reflow a 320 px sin desborde. Nada anima con movimiento reducido.
- **Accesos**:
  - cada tarjeta es un único enlace con título (H3), descripción y botón visual, así que el nombre accesible dice adónde lleva;
  - los personajes son decorativos (`aria-hidden`);
  - el texto de "Recursos gratuitos" sale de lo que hoy dice la página de Descargas (no se inventan contenidos).
- **Tarjetas que giran**: probado que al girar una, la anterior vuelve. El teclado funciona igual que antes.

## Mapa de temas
- **axe-core**: 0 violaciones en 14 páginas × 2 anchos. Reflow a 320 px sin desborde. Con movimiento reducido no anima nada: la entrada del panel y las señales quedan desactivadas y las uniones se ven dibujadas.
- **Teclado**: Tab recorre los seis temas (botones con `aria-pressed` y `aria-controls`); Enter elige y muestra solo ese panel; el Tab siguiente entra a los enlaces del panel. Los paneles están en una región `aria-live="polite"`.
- **Estructura**: el grafo (líneas y señales) es decorativo (`aria-hidden`); el contenido está en los paneles, cada uno con H3. Sin JS se ven todos los paneles.
- **Móvil**: los temas pasan a fichas de 44 px de alto; sin desborde a 360/390/430.
- **Datos**: los artículos y las uniones salen de la taxonomía de la Etapa 5; no se agregan temas ni artículos inventados.
