# QA — Etapa 5 (GEO y blog)

Fecha: 27-09-2026 · Vista previa acumulada (Etapas 1–5) · 15 páginas × 360/390/430/1280 px (`capturas-despues-etapa-5/`) + WordPress 7 local.

## Mobile y accesibilidad
| Criterio | Resultado |
|---|---|
| Contenido recortado u oculto | 0 en las 15 páginas y 3 anchos |
| Margen lateral mínimo | ≥ 19 px |
| Un H1 por página | 15/15 (incluida la pilar) |
| Violaciones axe (WCAG 2.2 AA + best practices, 1280 y 390 px) | **0** |
| Elementos sin foco visible | 0 |
| Objetivos < 44 px | Solo Contacto (radios/casilla de 24 px con fila de 44 px, enlace dentro de etiqueta) y un título corto del blog; cumplen WCAG 2.5.8 |

## Funcional (WordPress real)
| Comprobación | Resultado |
|---|---|
| `wp calma geo-import` | Resumen y definición cargados; H2 subidos por texto exacto (h3 y h5), con revisión; solo fuentes "verificada" publicadas |
| Entrada con fuentes | Sección "Fuentes" con DOI; JSON-LD `abstract` + `citation` |
| `/llms.txt` | 200, `text/markdown`, `X-Robots-Tag: noindex`; equipo, servicios, guías, temas y artículos con su resumen; se regenera al guardar |
| `wp calma taxonomia` | 6 categorías, 15 etiquetas, 15 entradas con una categoría, limpieza y 16 × 301 creadas en Rank Math; segunda ejecución sin duplicados; si Rank Math no guarda una 301, la tabla dice ERROR |
| Redirecciones | `category/psicologia` → `category/habitos-y-conducta`, `tag/salud_mental` → `tag/salud-mental`, `category/ciberpsicologia` → `/ciberpsicologia/` (301) |
| Caja de consulta con la taxonomía nueva | Usa el `area_cta` de cada categoría (`calma_cta_mapa`); el campo `calma_cta_area` de cada entrada tiene prioridad |
| Página pilar | Article + FAQPage (3 preguntas; la que tiene placeholder se omite) |
| `debug.log` | Sin avisos del plugin (los anteriores eran de la tabla de Rank Math ausente en el entorno SQLite, ya creada) |

## Pendiente de producción
validator.schema.org, prueba de resultados enriquecidos, pruebas de citación en motores de IA (tras abrir el firewall).

## Veredicto
**Aprueba.**
