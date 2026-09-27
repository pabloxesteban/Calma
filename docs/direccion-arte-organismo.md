# Dirección de arte · "Tecnología que se comporta como una mente"

Propuesta para evolucionar Código Calma hacia una experiencia editorial e interactiva. **Es un análisis y un plan: todavía no hay código nuevo.** La implementación arranca cuando se apruebe.

Orden de prioridades (del brief): contenido → legibilidad → accesibilidad → rendimiento → interacción → espectáculo. Si un efecto choca con algo que está más arriba en la lista, se descarta.

---

## 1. Diagnóstico: qué tenemos hoy

La home actual (vista previa, Etapa 6) tiene estos bloques, en orden:

| # | Bloque | Cómo está hecho | Estado |
|---|---|---|---|
| 1 | Hero (`.calma-hero`) | HTML propio + halos que siguen al puntero | Sólido de contenido. Visualmente genérico |
| 2 | Bienvenida + cifras "+74 %" y "+6 mil millones" | Kadence info boxes + count-up | La animación de conteo no explica nada. **Al 74 % le falta la fuente** |
| 3 | Últimos artículos | Kadence posts + contenedor ZoloBlocks | Tarjetas correctas, con hover genérico (brillo que sigue al cursor) |
| 4 | Línea de tiempo (`.calma-timeline`) | HTML propio (Etapa 1) | Es la que más potencial narrativo tiene y hoy es una lista estática |
| 5 | "¿Cómo son tus momentos con la tecnología?" | 6 flipboxes ZoloBlocks | Contenido excelente y con fuentes. El giro 3D esconde el texto, no se entiende con teclado y queda raro en celular |
| 6 | Tarjetas CTA (Aprender / Consulta / Recursos) | Kadence info boxes | Funcionan. Es el paso a la conversión |
| 7 | Fila vacía `1204_addcaa-c1` | — | Se elimina |

Movimiento de la Etapa 6 que **choca con el brief nuevo** y se retira:

- Aparición desde abajo en casi todo (`.calma-reveal`): es el cliché "entrada constante desde abajo".
- Brillo que barre los botones y elevación al pasar el mouse.
- Texto con degradado en los títulos.
- Header de vidrio (glassmorphism).
- Conteo de cifras.
- Halos que siguen al puntero como decoración.

Se queda: header compacto al bajar (sin vidrio), barra de progreso de lectura, foco visible, `prefers-reduced-motion`.

---

## 2. Qué evoluciona y qué queda simple

### Evoluciona (6 piezas, todas en la home salvo el mapa)

| Pieza | Concepto que comunica | Propuesta | En celular |
|---|---|---|---|
| **Hero: campo vivo** | Presencia → perturbación → regulación | Campo de partículas en Canvas 2D: una red orgánica muy lenta, con ruido procedural. El cursor (o el toque) la perturba y vuelve sola al equilibrio en ~2 s. No hay bucle permanente: se asienta y queda quieto. El texto va arriba, sobre fondo limpio | ~150 nodos, se perturba con el toque. Si el equipo es de gama baja: SVG estático de la red en equilibrio |
| **Datos como organismos** | Sobrecarga, conexión | 27 % (teléfono con la pareja, PMC 2024) como anillo con un sector que se "desprende". 6 mil millones como nodos contra la población mundial. Cada figura tiene su número y su fuente en texto: la visualización acompaña al dato, no lo reemplaza. Nada de contadores | Figuras SVG estáticas; una sola transición corta al entrar en pantalla |
| **Línea de tiempo que se transforma** | Transformación, adaptación | Un único glifo SVG que muta al avanzar con el scroll nativo: objeto (1975–85) → red (1990–2000) → dispositivo (2000–10) → plataforma (2010–20) → inteligencia (2020–hoy). Glifo sticky a un costado y texto que sigue su curso. El scroll se lee, nunca se secuestra. Con CSS scroll-driven animations y fallback a IntersectionObserver | Lista vertical con un glifo chico por época. La transformación sucede cuando cada época entra en pantalla |
| **Estados mentales** (reemplaza a los 6 flipboxes) | Uno por tarjeta | Tarjetas con el texto siempre visible y un "micro-organismo" SVG que se activa con hover, foco o al entrar en pantalla, y se calma solo: **disponibilidad permanente** → pulsación; **validación métrica** → partículas que se agrupan; **presencia fragmentada** → un campo que se divide en dos; **scroll sin horizonte** → flujo que no llega a destino; **ruido constante** → interferencia; **pantalla hasta dormir** → baja frecuencia y oscurecimiento. La fuente de cada hallazgo se ve directamente, sin girar la tarjeta | Carrusel horizontal con scroll-snap nativo, o apiladas; animación solo al tocar |
| **Tarjetas de artículos** | Curiosidad | Solo CSS: la tarjeta gana un poco de profundidad (sombra, no escala), la imagen se desplaza unos 4 px y aparecen categoría y tiempo de lectura. Una textura de grano se mueve apenas | Sin hover: la metadata queda siempre visible |
| **Mapa de conocimiento** | Conexión, memoria | Seis dominios (Psicología, Ciberpsicología, IA, Neurociencia, Bienestar digital, Tecnología) como grafo SVG. La base es una lista de enlaces accesible y el grafo es una mejora progresiva: al pasar por un dominio se iluminan sus vecinos y los artículos relacionados. Va en la página pilar y como sección de la home. **No reemplaza al menú principal** | Chips en filas, sin grafo |

### Queda simple (a propósito)

| Pieza | Por qué |
|---|---|
| Header y menú | La navegación tiene que ser predecible. Fondo sólido "papel" con una línea fina. Sin vidrio |
| Servicios | La página de conversión va sin distracciones. A lo sumo, una línea fina que conecta los pasos |
| Contacto y formulario | Cero movimiento. Es el momento de más carga cognitiva |
| Test de consumo digital | Ya pasa la revisión de accesibilidad; el foco tiene que estar en las preguntas |
| Lectura de artículos | Tipografía, "En resumen", fuentes y barra de progreso. Nada más |
| Equipo, herramientas, descargas, testimonios, footer | Solo reciben los tokens visuales nuevos, sin interacción propia |

---

## 3. Sistema visual

- **Papel cálido.** El fondo pasa de blanco a un marfil muy leve (≈ `#faf8f4`) y el texto, de negro a tinta azulada (≈ `#1b2233`). Se mantiene el azul de marca `#1d5f94` para enlaces y acciones. Se suma un **verde azulado profundo** para las visualizaciones y un acento cálido escaso (arcilla) solo en datos. Todas las combinaciones de texto se verifican en ≥ 4,5:1. **El violeta queda solo como sello de categoría**, para alejarnos del "violeta IA".
- **Tipografía editorial.** Lora para los titulares grandes, con itálica como acento (reemplaza al degradado). Inter para el cuerpo. Rótulos científicos chicos en `ui-monospace`, por ejemplo «Fig. 03 — Presencia fragmentada · PMC·NIH 2024».
- **Estructura.** Líneas finas de 1 px, una retícula visible solo en los separadores, mucho espacio negativo y grano sutil (SVG noise de ~1 KB en CSS). Sin sombras duras ni glow.
- **Formas.** Redes orgánicas, ondas y campos, en líneas finas. Nada de neón, glitch, esferas 3D ni cerebros literales.

## 4. Gramática de movimiento

Cuatro verbos, y nada fuera de ellos:

1. **Perturbar → asentar.** Una interacción mueve y el sistema vuelve solo al equilibrio (presencia, regulación). Es el verbo central.
2. **Conectar.** Una línea se dibuja entre dos cosas relacionadas (conexión, memoria).
3. **Transformar.** Una forma muta en otra y nunca desaparece de golpe (transformación, adaptación).
4. **Atenuar.** Baja la frecuencia o la luz (descanso, sueño, calma).

Reglas:

- Easing largo y suave (`cubic-bezier(.2,.7,.2,1)`), de 400 a 900 ms. Sin rebote. Desplazamientos de 4 a 8 px como máximo.
- Nada se mueve más de 5 s sin que la persona lo pida (WCAG 2.2.2). Sin bucles infinitos.
- El scroll es siempre nativo: el progreso se lee, nunca se controla.
- Con `prefers-reduced-motion`, cada pieza muestra su estado final (el equilibrio, el glifo de la época, el organismo en reposo), con el mismo contenido. Además se suma un control visible **"Reducir movimiento"** en el footer, para quien no configuró su sistema.

## 5. Técnica, rendimiento y accesibilidad

- **Sin Three.js ni WebGL por ahora.** Canvas 2D solo en el hero; el resto es SVG + CSS. WebGL/WebGPU solo se justifica si más adelante hay un fluido real que Canvas no pueda sostener, y siempre detrás del mismo fallback.
- **Presupuesto:** JS de movimiento ≤ 25 KB gzip en total. Se carga después del LCP (`requestIdleCallback`). El LCP sigue siendo el titular de texto, así que el objetivo de LCP < 2,5 s y CLS < 0,1 no cambia: los canvas tienen tamaño reservado.
- **Gama baja:** se detecta con `hardwareConcurrency ≤ 4`, `deviceMemory ≤ 4`, `saveData` y un regulador de FPS. Si baja de ~45 fps, reduce partículas; si sigue mal, congela en el estado de equilibrio. DPR máximo 1,5. El canvas se pausa fuera de pantalla y con la pestaña oculta.
- **Accesibilidad:** canvas y SVG decorativos con `aria-hidden`. Cada visualización tiene su equivalente en texto (el dato, la fuente, la época). Las tarjetas son elementos reales (enlaces o `details`) con foco visible, y la perturbación del hero también responde al foco. Ninguna información depende solo del movimiento o del color. Axe con 0 violaciones en cada fase.
- **Celular:** no es "el escritorio en chico". Hay menos elementos, todo se activa con toque o al entrar en pantalla, el contenido va primero y ningún efecto pone en riesgo el rendimiento.

## 6. Plan por fases

Cada fase se publica en la vista previa de GitHub Pages y se revisa antes de seguir. Todas pasan por accessibility-qa, mobile-qa (360/390/430) y una medición de rendimiento.

| Fase | Contenido | Para decidir |
|---|---|---|
| **F1 · Base + hero** | Tokens nuevos (papel, tinta, verde azulado, rótulos mono, grano). Se retiran los clichés de la Etapa 6. Hero con campo vivo y fallbacks | El "tacto" general: ¿es la dirección? |
| **F2 · Estados y datos** | Los 6 estados mentales reemplazan a los flipboxes. Visualizaciones del 27 % y los 6 mil millones | |
| **F3 · Línea de tiempo** | Glifo que se transforma con el scroll | |
| **F4 · Mapa de conocimiento** | Grafo accesible en la pilar y la home | |
| **F5 · Artículos** | Microinteracciones de tarjetas y pulido general | |

Los cambios quedan en el plugin `codigo-calma`, como un reemplazo de `calma-etapa6.css` y `calma-motion.js`, más bloques HTML nuevos para la home. Cambiar los flipboxes por los estados mentales implica editar la home en WordPress; la guía de aplicación se escribe en `docs/implementacion/`.

## 7. Datos que faltan

- **74 %:** no tiene fuente verificada. No se visualiza hasta tenerla; mientras tanto, `[COMPLETAR: fuente del 74 %]`.
- **6 mil millones:** confirmar la fuente (¿usuarios de internet o de smartphones? ¿de qué año?) antes de dibujarlo contra la población mundial. Ya figura en `docs/placeholders.md` (fila 61).
- **27 %:** fuente PMC·NIH 2024, ya citada en la tarjeta de presencia fragmentada.
