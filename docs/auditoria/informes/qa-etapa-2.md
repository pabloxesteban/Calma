# QA mobile y accesibilidad — Etapa 2

Fecha: 26-09-2026 · Skills `mobile-qa` + agente `accessibility-qa` · Vista previa acumulada (Etapas 1 + 2).
Datos: `capturas-despues-etapa-2/metricas.json`, `qa-accesibilidad-etapa-2.json`. "Antes" = producción (`capturas-antes/metricas-v2.json`; el blog de producción devolvió la pantalla antibots).

## Mobile (360 / 390 / 430 px)

| Página | Recortados | Margen mín. (px) antes → después | Objetivos < 44 px antes → después | H1 |
|---|---|---|---|---|
| inicio | 0 | 0 → 20 | 3 → 0 | 1 |
| servicios | 0 | 20 → 20 | 3 → 0 | 1 |
| contacto | 0 | 24 → 24 | 3 → 2 | 1 |
| sobre_tatiana | 0 | 20 → 20 | 4 → 0 | 1 |
| blog | 0 | — → 20 | — → 1 | 1 |
| ciberpsicologia | 0 | 24 → 24 | 3 → 0 | 1 |
| testimonios | 0 | 24 → 24 | 17 → 0 | 1 |
| test | 0 | 32 → 24 | 3 → 0 | 1 |
| herramientas | 0 | slider → 24 | 6 → 0 | 1 |
| descargas-2 | 0 | 30 → 24 | 3 → 0 | 1 |
| bienestar-digital | 0 | 32 → 24 | 3 → 0 | 1 |
| por-que-fallamos-al-intentar-cambiar-conductas | 0 | 23 → 19 | 12 → 0 | 1 |

(Tabla a 390 px; 360 y 430 px dan los mismos resultados, ver `metricas.json`.)

Objetivos < 44 px que quedan, todos admitidos por WCAG 2.5.8 (≥ 24 px o enlace dentro de texto):
- Contacto: casilla de privacidad (24 px, con la etiqueta completa clicable) y el enlace "política de privacidad" dentro de esa etiqueta.
- Blog: título corto de una tarjeta ("Infancias «Figitales»"), enlace de texto dentro del título.
- Escritorio (1280): botón de submenú (24 px de ancho) y lupa del buscador.

## Accesibilidad (axe-core WCAG 2.2 AA + best practices, 11 páginas × 1280/390 px)

| Criterio | Etapa 1 (re-verificación) | Etapa 2 |
|---|---|---|
| Violaciones axe (todas las severidades) | 18 (heading-order 12, target-size 6) | **0** |
| Contraste | 0 | 0 |
| Elementos sin foco visible (20 Tab por página) | 0 | 0 |
| Reflow 320 px | 0 desbordes | 0 desbordes |
| Menú mobile | Blanco, 48×48, Esc | Igual + menú plano y botón de consulta |
| **A11Y-01 · Test operable con teclado** | ❌ bloqueante | ✅ resuelto: radios nativos, foco al H2 de cada pantalla, aria-live, 0 violaciones en inicio/pregunta/resultado (`contenido/etapa-2/bloques/test-consumo-digital.md`) |

Pendiente manual: escuchar el recorrido del test con NVDA o VoiceOver.

## Veredicto
**Aprueba** Etapa 2 (mobile y accesibilidad). Sin bloqueantes WCAG en las páginas revisadas.
