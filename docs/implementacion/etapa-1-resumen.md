# Etapa 1 — Resumen de cierre

Estado: **lista para aplicar** (nada publicado). Guía: `docs/implementacion/etapa-1.md`.

## Cambios realizados
| Área | Qué | Dónde |
|---|---|---|
| Acceso de IA | robots.txt con grupos explícitos por bot; pasos y ticket para el firewall de Hostinger (429 a GPTBot, reCAPTCHA de LiteSpeed) | `contenido/etapa-1/rank-math/robots.txt`, guía paso 1 |
| Maquetación mobile | Fin del recorte de 40 px y del texto fuera de pantalla en el inicio (documento HTML pegado + animaciones); tarjetas de pasos con padding; sin franjas vacías; margen lateral ≥ 19 px; títulos mobile | plugin `codigo-calma`, bloques de inicio y Servicios |
| Estilo unificado (base) | Tokens `calma-*`; paleta de Kadence con contraste AA (`#1d5f94`); menú mobile claro; botones de 48 px; foco visible | `wp-content/plugins/codigo-calma/` |
| Texto | 77 correcciones: 6M+ → +6 mil millones, autoría, «día a día», voseo → tuteo, títulos, puntuación, H1 únicos, nombres accesibles | `contenido/etapa-1/correcciones.md` |
| Formulario | Etiquetas en español y visibles, nombre obligatorio, autocomplete, privacidad, aviso de urgencias, qué pasa después | `contenido/etapa-1/bloques/formulario-contacto.md` |
| SEO rápido | Rank Math (redirecciones + robots), `/entradas/` → `/blog/`, firma de la autora sin 404, Contact Form 7 deja de cargarse | guía paso 8 |

## Antes / después (vista previa, 360–430 px)
| Métrica | Antes | Después |
|---|---|---|
| Contenido recortado | Inicio: 3 elementos (bienvenida en x = −49 px) | 0 en 12 páginas |
| Margen lateral mínimo | 0 px (inicio) | 19–27 px |
| Páginas con un único H1 | 5 de 12 | 12 de 12 |
| Violaciones de contraste (axe, 1280 px) | 67 | 0 |
| Contraste del CTA "Solicitar una consulta" | 2,32:1 | 6,7:1 |
| Menú mobile | Negro | Blanco, ítems ≥ 48 px |

Capturas: `docs/auditoria/capturas-antes/` vs `docs/auditoria/capturas-despues-etapa-1/` (mismo nombre de archivo; detalle en `detalle/`).
QA: `docs/auditoria/informes/qa-mobile-etapa-1.md` (aprueba) y `qa-accesibilidad-etapa-1.md` (aprueba; A11Y-01 pendiente).

## Pendiente para el cliente antes/después de aplicar
- Revisar el firewall en hPanel o abrir el ticket (paso 1).
- URL de la política de privacidad para el formulario.
- Decidir sobre CCBot/Bytespider en robots.txt.
- Consultas a la autora: «no buscamos entendernos», «Libros» vs. «Guías», talleres, testimonios de Luis R. y Ana M.

## Recomendación para la Etapa 2
Adelantar el **test de consumo digital accesible por teclado** (A11Y-01, único bloqueante WCAG) y resolver los objetivos táctiles de metadatos y del carrusel de Herramientas junto con los componentes del design system.
