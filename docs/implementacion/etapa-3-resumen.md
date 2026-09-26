# Etapa 3 — Resumen de cierre

Estado: **lista para aplicar tras la revisión humana del copy** (nada publicado). Guía: `docs/implementacion/etapa-3.md`. QA: `docs/auditoria/informes/qa-etapa-3.md` (aprueba).

## Cambios realizados
| Área | Antes | Después |
|---|---|---|
| Servicios | H1 sin resultado ni público; único CTA a ~3.400 px; sin FAQ ni prueba social | Hero con CTA en la primera pantalla, "¿Es para ti?" y "cuándo no", 3 pasos con "te llevas", equipo con CTA por área, formación declarada, 3 reseñas reales de Google enlazadas, 6 preguntas frecuentes, cierre y aviso de urgencias |
| Inicio | Hero sin propuesta de valor; CTA al final de ~14.000 px | H1 "Entiende cómo te afecta la tecnología y decide cómo quieres usarla" + CTA sin scroll |
| Contacto | Tres viñetas tipo "deberes"; no decía qué pasa después | Intro breve, 3 pasos de "qué pasa después", campo de área preseleccionable |
| Equipo | Solo "Sobre Tatiana"; Francisca y Emanuel sin página | `/equipo/` + una página por persona (bio, temas, formación declarada, CTA). `/sobre_tatiana/` → 301 |
| Artículos | Ningún CTA | Caja "¿Te identificas con esto?" según el tema + aviso de urgencias en salud mental |
| Medición | Nada | `generate_lead` en dataLayer/gtag (listo para la analítica de la Etapa 4) |
| Newsletter | No existía | Bloque y shortcode listos; se activan al configurar el proveedor (no se muestra un formulario que no envía) |

## Recorrido hasta la consulta (clics desde la entrada)
| Desde | Antes | Después |
|---|---|---|
| Inicio | Scroll hasta el final o menú → Contacto | 1 clic (hero) |
| Un artículo | Menú → Servicios/Contacto (2–3 toques) | 1 clic (caja al final, área preseleccionada) |
| Servicios | Scroll de ~3.400 px | 1 clic (hero) |
| Cualquier página | Menú | 1 clic (botón del header, Etapa 2) |

## Pendiente antes de publicar
1. **Revisión humana** de `contenido/etapa-3/copy.md` (Tatiana, Francisca, Emanuel).
2. Datos: honorarios o cómo mostrarlos, duración/frecuencia de sesiones, plataforma, confidencialidad, fotos, formación de Francisca y Emanuel, URL de líneas de ayuda y de privacidad.
3. Consentimiento para reutilizar las reseñas y verificar los enlaces de Hugo B. y Caro C.
4. Aclarar si las reseñas hablan de terapia o de mentoría (afecta a la FAQ "¿Es psicoterapia?").
5. Elegir proveedor de newsletter.
