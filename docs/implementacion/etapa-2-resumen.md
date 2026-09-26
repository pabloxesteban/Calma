# Etapa 2 — Resumen de cierre

Estado: **lista para aplicar** (nada publicado). Guía: `docs/implementacion/etapa-2.md`. QA: `docs/auditoria/informes/qa-etapa-2.md` (aprueba).

## Cambios realizados
| Área | Qué | Dónde |
|---|---|---|
| Tipografía | Lora (títulos) + Inter (texto) alojadas en el sitio; fuera Google Fonts, Jost, Sora y Playfair; escala única; cuerpo 17–18 px | plugin `codigo-calma` 1.1.0 (`assets/fonts`, `calma-fonts.css`) |
| Header | Blanco con borde, logo 48 px (descarga la variante de 150 px, no la de 512), estado activo, botón "Solicitar una consulta" en escritorio y en el menú mobile | plugin + Personalizador |
| Menú mobile | Plano: Blog, Test, Descargas y Herramientas ya no quedan escondidos en un submenú | Menús |
| Componentes | Botones píldora 48 px, tarjetas de artículos (16:9, badge por categoría, resumen de 4 líneas), metadatos con "Publicado/Actualizado", lectura a 68ch, Info Box y tarjetas giratorias sin cortes de palabra, paginación 44 px | `calma-etapa2.css` |
| Pie | 4 columnas (marca + CTA, Explorar, Recursos, Contacto) y fila legal con aviso de urgencias | `contenido/etapa-2/footer/pie-widget.html` |
| Herramientas | Carrusel horizontal → grilla de 3 tarjetas, sin JS ni Google Fonts, tuteo | `contenido/etapa-2/bloques/herramientas-habitos.html` |
| **Test accesible (adelantado)** | Radios nativos, paso a paso con foco y anuncios, preguntas en el HTML (GEO-14), "Otra / prefiero no decirlo", CTA de consulta, aviso orientativo y de urgencias; mismo cálculo que el original | `contenido/etapa-2/bloques/test-consumo-digital.html` |

## Antes / después (producción → vista previa Etapas 1+2)
| Métrica | Antes | Después |
|---|---|---|
| Violaciones axe (11 páginas, 2 anchos) | 67 solo de contraste | 0 de cualquier tipo |
| Test con teclado (A11Y-01) | Imposible pasar del paso 1 | Completo de principio a fin |
| Familias tipográficas / peticiones a Google Fonts | 6 / 2–3 por página | 2 / 0 |
| Objetivos táctiles < 44 px (390 px, por página) | 3–17 | 0–2 (los que quedan cumplen 2.5.8) |
| Menú mobile | Negro, con submenú | Blanco, plano, con botón de consulta |
| Pie | 2 íconos y © | 4 columnas + aviso de urgencias |

Capturas: `docs/auditoria/capturas-despues-etapa-2/` (comparar con `capturas-antes/` y `capturas-despues-etapa-1/`).

## Decisiones pendientes
- **Cálculo del test:** el original compara umbrales con el porcentaje (3 perfiles nunca salen). Se conservó igual; corregirlo cambia los resultados → decide Tatiana.
- **Nombres de las 4 dimensiones del test** (placeholder visible con propuesta).
- URL de la política de privacidad y enlace a líneas de ayuda (aparecen en el pie, el formulario y el test).
