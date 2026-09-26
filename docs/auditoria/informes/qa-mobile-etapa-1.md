# QA mobile — Etapa 1

Fecha: 26-09-2026 · Skill `mobile-qa` · Script: `staging/preview/capturas.js` (mismas métricas en producción y en la vista previa).

- **Antes** = producción (`capturas-antes/metricas-v2.json`). **Después** = vista previa de la Etapa 1 (`capturas-despues-etapa-1/`).
- Las métricas se toman después de recorrer la página (así las animaciones ya se dispararon). Por eso "texto oculto" da 0 también antes: el problema de la animación aparece con scroll rápido o al llegar por un ancla, y se ve en las capturas de detalle.
- En producción, `/blog/` devolvió la pantalla «Bot Verification» (reCAPTCHA de LiteSpeed): la fila "antes" del blog no es válida. Es el mismo bloqueo de GEO-02.

| Página | Ancho | Recortados antes → después | Margen lateral mín. (px) | Objetivos < 44 px | H1 |
|---|---|---|---|---|---|
| inicio | 360 | 3 → 0 | 0 → 20 | 3 → 0 | 2 → 1 |
| servicios | 360 | 0 → 0 | 20 → 20 | 3 → 0 | 0 → 1 |
| contacto | 360 | 0 → 0 | 24 → 24 | 3 → 2 | 0 → 1 |
| sobre_tatiana | 360 | 0 → 0 | 20 → 20 | 4 → 0 | 1 → 1 |
| blog | 360 | — → 0 | — → 20 | — → 24 | — → 1 |
| ciberpsicologia | 360 | 0 → 0 | 24 → 24 | 3 → 0 | 1 → 1 |
| testimonios | 360 | 0 → 0 | 24 → 24 | 17 → 0 | 0 → 1 |
| test | 360 | 0 → 0 | 32 → 24 | 3 → 0 | 1 → 1 |
| herramientas | 360 | 0 → 0 | slider* → slider* | 6 → 3 | 1 → 1 |
| descargas-2 | 360 | 0 → 0 | 30 → 24 | 3 → 0 | 0 → 1 |
| bienestar-digital | 360 | 0 → 0 | 32 → 24 | 3 → 0 | 3 → 1 |
| por-que-fallamos-al-intentar-cambiar-conductas | 360 | 0 → 0 | 23 → 19 | 12 → 9 | 1 → 1 |
| inicio | 390 | 3 → 0 | 0 → 20 | 3 → 0 | 2 → 1 |
| servicios | 390 | 0 → 0 | 20 → 20 | 3 → 0 | 0 → 1 |
| contacto | 390 | 0 → 0 | 24 → 24 | 3 → 2 | 0 → 1 |
| sobre_tatiana | 390 | 0 → 0 | 20 → 20 | 4 → 0 | 1 → 1 |
| blog | 390 | — → 0 | — → 20 | — → 24 | — → 1 |
| ciberpsicologia | 390 | 0 → 0 | 24 → 24 | 3 → 0 | 1 → 1 |
| testimonios | 390 | 0 → 0 | 24 → 24 | 17 → 0 | 0 → 1 |
| test | 390 | 0 → 0 | 32 → 24 | 3 → 0 | 1 → 1 |
| herramientas | 390 | 0 → 0 | slider* → slider* | 6 → 3 | 1 → 1 |
| descargas-2 | 390 | 0 → 0 | 30 → 24 | 3 → 0 | 0 → 1 |
| bienestar-digital | 390 | 0 → 0 | 32 → 24 | 3 → 0 | 3 → 1 |
| por-que-fallamos-al-intentar-cambiar-conductas | 390 | 0 → 0 | 23 → 19 | 12 → 9 | 1 → 1 |
| inicio | 430 | 3 → 0 | 0 → 22 | 3 → 0 | 2 → 1 |
| servicios | 430 | 0 → 0 | 20 → 20 | 3 → 0 | 0 → 1 |
| contacto | 430 | 0 → 0 | 24 → 24 | 3 → 2 | 0 → 1 |
| sobre_tatiana | 430 | 0 → 0 | 20 → 20 | 4 → 0 | 1 → 1 |
| blog | 430 | — → 0 | — → 22 | — → 24 | — → 1 |
| ciberpsicologia | 430 | 0 → 0 | 24 → 24 | 3 → 0 | 1 → 1 |
| testimonios | 430 | 0 → 0 | 24 → 24 | 17 → 0 | 0 → 1 |
| test | 430 | 0 → 0 | 32 → 27 | 3 → 0 | 1 → 1 |
| herramientas | 430 | 0 → 0 | slider* → slider* | 6 → 3 | 1 → 1 |
| descargas-2 | 430 | 0 → 0 | 30 → 27 | 3 → 0 | 0 → 1 |
| bienestar-digital | 430 | 0 → 0 | 32 → 27 | 3 → 0 | 3 → 1 |
| por-que-fallamos-al-intentar-cambiar-conductas | 430 | 0 → 0 | 23 → 21 | 12 → 9 | 1 → 1 |

\* Herramientas: el carrusel horizontal de tarjetas es intencional (se desplaza con el dedo); se rehace en la Etapa 2.

## Resultado por criterio (360 / 390 / 430 px)

| Criterio | Antes | Después | Estado |
|---|---|---|---|
| Sin scroll horizontal | 0 px (pero con contenido recortado por `overflow: clip`) | 0 px | ✅ |
| Contenido recortado | Inicio: título de bienvenida en x = −49 px y tarjetas de artículos cortadas | 0 en todas las páginas | ✅ |
| Margen lateral ≥ 16 px (objetivo 20) | Inicio 0 px; tarjetas pegadas al borde | ≥ 19 px en todas (artículo: 19 px) | ✅ |
| Tarjetas con padding, números dentro | Servicios: sin padding, número sobre el borde | 26 px; número dentro | ✅ (ver `servicios-390.png`) |
| Franjas vacías arriba / antes del pie | ≈ 56 px en páginas boxed | Eliminadas en páginas; en entradas, margen medido de 24/40 px | ✅ |
| Un H1 por página | 6 páginas sin H1, inicio con 2, bienestar con 3 | 1 en todas | ✅ |
| Menú mobile | Negro `#090c10` | Blanco, ítems ≥ 48 px | ✅ (`detalle/menu-mobile-390.png`) |
| Objetivos táctiles < 44 px fuera de texto | 3–17 por página | 0 en la mayoría; quedan enlaces de metadatos (categoría, autora) en blog y artículos, casilla nativa del formulario y botones del carrusel de Herramientas | ⚠️ pendiente Etapa 2 (componentes de tarjeta y meta) |
| CTA "Solicitar una consulta" | Blanco sobre `#64b2e5` (2,32:1) | Blanco sobre `#1d5f94` (6,7:1), 48–68 px de alto | ✅ |

## Pendientes para la Etapa 2
- Enlaces de metadatos (categoría y autora) en tarjetas del blog y cabecera de artículos: 24 y 9 objetivos < 44 px. Se resuelven con el componente de tarjeta y meta del design system.
- Carrusel de Herramientas: botones < 44 px y desplazamiento horizontal; se rehace la página.
- El texto del hero del inicio se sigue escribiendo letra a letra (animación "typing" de Blocks Animation) mientras el plugin esté activo: desaparece al desactivarlo (paso 3 de la guía).

## Veredicto
**Aprueba** los criterios mobile de la Etapa 1. Los pendientes no son bloqueantes y tienen etapa asignada.
