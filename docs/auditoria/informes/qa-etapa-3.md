# QA mobile y accesibilidad — Etapa 3

Fecha: 26-09-2026 · Vista previa acumulada (Etapas 1 + 2 + 3) · 15 páginas (incluye `/equipo/` y dos páginas de persona) × 360/390/430/1280 px.

## Mobile (390 px; 360 y 430 dan lo mismo)

| Página | Recortados | Texto oculto | Margen mín. | Objetivos < 44 px | H1 |
|---|---|---|---|---|---|
| inicio | 0 | 0 | 20 | 0 | 1 |
| servicios | 0 | 0 | 20 | 0 | 1 |
| contacto | 0 | 0 | 24 | 6 | 1 |
| sobre_tatiana | 0 | 0 | 20 | 0 | 1 |
| blog | 0 | 0 | 20 | 1 | 1 |
| ciberpsicologia | 0 | 0 | 24 | 0 | 1 |
| testimonios | 0 | 0 | 24 | 0 | 1 |
| test | 0 | 0 | 24 | 0 | 1 |
| herramientas | 0 | 0 | 24 | 0 | 1 |
| descargas-2 | 0 | 0 | 24 | 0 | 1 |
| bienestar-digital | 0 | 0 | 24 | 0 | 1 |
| por-que-fallamos-al-intentar-cambiar-conductas | 0 | 0 | 19 | 0 | 1 |
| equipo | 0 | 0 | 20 | 0 | 1 |
| equipo-tatiana | 0 | 0 | 20 | 0 | 1 |
| equipo-francisca | 0 | 0 | 20 | 0 | 1 |

Objetivos < 44 px restantes: en Contacto, los 4 radios del área y la casilla de privacidad (24 px, con la fila/etiqueta completa clicable de 44 px) y el enlace "política de privacidad" dentro de la etiqueta; en el blog, un título corto (enlace de texto). Cumplen WCAG 2.5.8.

## Conversión (comprobaciones funcionales)

| Comprobación | Resultado |
|---|---|
| CTA "Solicitar una consulta" visible sin scroll a 390 px en Inicio y Servicios | ✅ (≈ 520 px del borde superior) |
| `/contacto/?area=habitos\|accesibilidad\|proyectos\|no-se` preselecciona la opción | ✅ 4/4; valores inválidos no marcan nada |
| Evento `generate_lead` al recibir `kb-advanced-form-success` | ✅ `dataLayer` recibe `{event, form_id, area}` |
| Caja de consulta al final de las 15 entradas (PHP real del plugin) | ✅ Tatiana en 13, Emanuel en "¿Por qué fallamos…", equipo en ILOVEYOU (sin aviso de urgencias) |
| Preguntas frecuentes operables con teclado (details/summary) | ✅ |

## Accesibilidad (axe-core, 14 páginas × 1280/390 px)

| Criterio | Etapa 2 | Etapa 3 |
|---|---|---|
| Violaciones axe | 0 | 0 (tras agrandar los radios del área: la primera pasada dio `target-size` ×4 en Contacto, corregido y re-verificado) |
| Elementos sin foco visible | 0 | 0 |
| Un H1 por página | ✅ | ✅ (15/15) |

## Veredicto
**Aprueba** Etapa 3. Pendiente fuera de QA: revisión humana del copy y los placeholders de datos (honorarios, duración de sesiones, confidencialidad, fotos, formación de Francisca y Emanuel, líneas de ayuda).
