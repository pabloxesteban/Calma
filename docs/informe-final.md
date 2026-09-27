# Informe final — Rediseño de codigocalma.com

Rama: `claude/focused-babbage-403shx` · Fecha: 27-09-2026 · Estado: **todo listo para aplicar en WordPress; nada publicado ni desplegado.**

---

## 1. Resumen

- **El sitio es un WordPress sin código versionado.** Vive en Hostinger, con Kadence, Kadence Blocks, ZoloBlocks y LiteSpeed Cache.
- **Cómo se entrega el rediseño:**
  - un plugin propio, `codigo-calma` (1.4.0);
  - bloques de contenido listos para pegar;
  - archivos de datos que el plugin importa con un clic;
  - una guía paso a paso por etapa para quien tenga acceso a wp-admin y hPanel.
- **Por qué un plugin y no un tema hijo:** un tema hijo haría perder los ajustes del Personalizador de Kadence.
- **Cómo se verificó:**
  - una vista previa reproducible sobre el HTML real de producción (`staging/preview/`), con capturas a 360, 390, 430 y 1280 px, métricas mobile y axe-core en cada etapa;
  - un WordPress 7 local con Kadence, Kadence Blocks y Rank Math para todo el PHP del plugin.
- **El bloqueo de las IA no estaba en robots.txt, sino en el firewall de Hostinger.** GPTBot recibía 429 y cualquier visitante recibía a veces un reCAPTCHA. Se resuelve en hPanel (guía de la Etapa 1, paso 1).

## 2. Cómo aplicar

Aplicar las etapas en orden, siguiendo cada guía. Tiempo total estimado: **9–11 horas** de trabajo en wp-admin, más la revisión del equipo.

| Etapa | Guía | Resumen | QA |
|---|---|---|---|
| 1 · Arreglos críticos | `docs/implementacion/etapa-1.md` | `etapa-1-resumen.md` | aprueba |
| 2 · Design system + test accesible | `etapa-2.md` | `etapa-2-resumen.md` | aprueba |
| 3 · Servicios y flujo de consulta | `etapa-3.md` | `etapa-3-resumen.md` | aprueba |
| 4 · SEO técnico y schema | `etapa-4.md` | `etapa-4-resumen.md` | aprueba |
| 5 · GEO y blog | `etapa-5.md` | este informe | aprueba |

**Antes de publicar las Etapas 3 y 5**, Tatiana, Francisca y Emanuel revisan los textos nuevos (`contenido/etapa-3/copy.md`, `contenido/etapa-5/*`).

## 3. Cambios realizados

### Etapa 1 — Arreglos críticos
- robots.txt con permiso explícito a GPTBot, OAI-SearchBot, ChatGPT-User, ClaudeBot, Claude-SearchBot, Claude-User, PerplexityBot, Perplexity-User, Google-Extended, Applebot-Extended y Bingbot. Incluye un ticket listo para el firewall de Hostinger.
- **77 correcciones de texto y encabezados.** Entre ellas:
  - 6M+ → +6 mil millones, «autoría», «día a día»;
  - voseo → tuteo, títulos, puntuación;
  - un H1 por página y nombres accesibles.
- Fin del recorte en mobile:
  - el documento HTML pegado en el inicio se reemplazó;
  - se quitó el CSS que anulaba el padding en Servicios;
  - se neutralizaron las animaciones.
- Sin franjas vacías, margen lateral de 20 px, menú mobile claro (fin del "menú negro").
- Contraste AA en todo el sitio: el azul principal pasa de `#64b2e5` (2,3:1) a `#1d5f94` (6,7:1).
- Formulario de contacto: etiquetas en español, privacidad y aviso de urgencias.

### Etapa 2 — Design system unificado
- Tokens `calma-*`.
- Lora e Inter alojadas en el sitio: de 6 familias tipográficas a 2 y 0 peticiones a Google Fonts.
- Header con CTA, menú mobile plano y pie en 4 columnas con aviso de urgencias.
- Componentes (botones, tarjetas, badges por categoría, metadatos con "Publicado/Actualizado", lectura a 68ch).
- Herramientas pasa de carrusel a grilla.
- **Test de consumo digital accesible**, que era el único bloqueante WCAG. Ahora se completa con teclado y las preguntas están en el HTML.

### Etapa 3 — Servicios y flujo de consulta
- **Servicios:**
  - hero con CTA y "¿Es para ti?";
  - proceso con "Te llevas", equipo con "Consultar con…" y el área preseleccionada;
  - formación declarada y reseñas reales enlazadas a Google, FAQ y aviso de urgencias.
- **Inicio:** hero con propuesta de valor.
- **Contacto:** "qué pasa después" y campo de área.
- **`/equipo/`** y una página por profesional.
- **Caja de consulta al final de cada artículo** según el tema, y evento `generate_lead`.
- **Newsletter** listo para conectar a un proveedor.

### Etapa 4 — SEO técnico, schema y rendimiento
- Títulos y descripciones de 34 URLs importables con un clic.
- Open Graph con imagen por defecto de 1200×630.
- **JSON-LD en un único `@graph`** por página: Organization, WebSite, Person ×3, ProfilePage, ProfessionalService, FAQPage, BlogPosting y BreadcrumbList.
- Sitemap de Rank Math y archivos finos sin indexar.
- Redirecciones 301: `/descargas/`, autor y www.
- Usuaria autora real.
- LCP = H1 y hero, y CLS del inicio 0.

### Etapa 5 — GEO y blog
- `/llms.txt` automático.
- **"En resumen"** (54–60 palabras) en los 15 artículos y 13 definiciones citables.
- **10 fuentes verificadas** con DOI, EUR-Lex u Open Library, que alimentan `citation`.
- H2 de sección en los 7 artículos que no tenían.
- Taxonomía nueva: 6 categorías, 15 etiquetas y 16 redirecciones.
- Página pilar **"¿Qué es la ciberpsicología?"** con Article + FAQPage y fuentes verificadas.
- Apertura de Bienestar digital con definición.
- Calendario editorial de octubre a diciembre.

## 4. Resultados medidos (vista previa sobre producción)

| Métrica | Antes | Después |
|---|---|---|
| Violaciones de accesibilidad (axe, 11–15 páginas × 2 anchos) | 67 de contraste + 1 bloqueante (test) | **0** |
| Contenido recortado en mobile (inicio) | Título a −49 px, tarjetas cortadas | 0 en todas las páginas |
| Margen lateral mínimo (390 px) | 0 px | 19–27 px |
| Páginas con un único H1 | 5 de 12 | 15 de 15 |
| Contraste del CTA "Solicitar una consulta" | 2,32:1 | 6,7:1 |
| CLS del inicio | 0,262 | 0 |
| Peticiones a Google Fonts por página | 3–5 | 0 |
| URLs con meta description / Open Graph / JSON-LD | 0 / 0 / 0 de 28 | 34 / todas / todas |
| Artículos con resumen inicial / fuentes enlazadas | 0 / 0 de 15 | 15 / 10 con fuentes verificadas |
| Clics desde un artículo hasta la consulta | 2–3 toques de menú | 1 (con el área preseleccionada) |

Lo que solo se puede medir en producción:
- **LCP real:** con PageSpeed Insights. La vista previa no aplica la simulación de red.
- **Resultados enriquecidos:** con validator.schema.org y Search Console.
- **Citas en motores de IA:** después de abrir el firewall.

## 5. Mejoras esperadas

No incluyo cifras de tráfico ni de conversión: no hay línea base, porque el sitio no tiene analítica.

- **SEO (Google):**
  - cada URL pasa a tener título y descripción propios, canonical, Open Graph y datos estructurados válidos;
  - sin duplicados (`/entradas/`, `/descargas-2/`, etiquetas finas) y con enlazado pilar ↔ artículos ↔ servicios;
  - autoría verificable (E-E-A-T);
  - Core Web Vitals en verde tras activar WebP;
  - se puede esperar más cobertura de indexación y mejor CTR en 8–12 semanas, medible en Search Console.
- **GEO (ChatGPT, Perplexity, Gemini, Claude):**
  - con el firewall abierto, los bots de IA reciben 200;
  - encuentran `llms.txt`, una definición en la primera oración de la pilar, respuestas directas al inicio de cada artículo, fuentes enlazadas y entidades consistentes (organización y profesionales).
  - Son las condiciones para que citen el sitio. El seguimiento mensual está en la guía de la Etapa 5, paso 8.
- **Conversión:**
  - la consulta queda a un clic desde cualquier página, con un formulario más corto y en español;
  - dice qué pasa después, con reaseguros de privacidad y urgencias, y con la persona adecuada según el tema;
  - el newsletter crea un canal propio;
  - todo se mide con `generate_lead` cuando se instale la analítica.

## 6. Placeholders pendientes (`docs/placeholders.md`: 63 filas)

Los más urgentes:
1. **Fotos del equipo** y **bios validadas** (Tatiana, Francisca, Emanuel), formación declarada de Francisca y Emanuel.
2. **Matrícula o colegiación** de Tatiana (si corresponde) y **modalidades** (mentoría o psicoterapia) con su habilitación. Los testimonios hablan de "terapia".
3. **Honorarios** (o decidir "te los contamos en la respuesta"), duración y frecuencia de las sesiones, plataforma y área de servicio.
4. **URL de la política de privacidad** y **página de líneas de ayuda por país**, verificadas. Aparecen en el formulario, el pie, Servicios, el test y los artículos.
5. **Confidencialidad / secreto profesional.**
6. **Revisión humana** de todo el copy de las Etapas 3 y 5, más los **43 pendientes de los artículos**: cifras sin fuente, 3 fuentes por verificar y erratas.
7. **Reseñas:** consentimiento para usarlas en otras páginas y verificar los enlaces de Hugo B. y Caro C.
8. **Test:** nombres de las 4 dimensiones y decidir si se corrige el cálculo original.
9. **Proveedor de newsletter**, **herramienta de analítica** y URL de LinkedIn de Código Calma.
10. Decisiones de robots.txt: CCBot y Bytespider.

## 7. Decisiones que tomé sin consultar
- Interpreté "el diseño de la reversión" como el design system propuesto en la revisión.
- Plugin del sitio en lugar de tema hijo, para conservar el Personalizador de Kadence.
- Sin modo oscuro por ahora (los tokens quedan preparados).
- El test conserva el cálculo original aunque tiene un error, porque corregirlo cambia el resultado que ve cada persona.
- Los testimonios de "Luis R." y "Ana M." se ocultan porque no tienen fuente.
- Las respuestas de FAQ con placeholders no se marcan con schema hasta completarse.

## 8. Próximos pasos recomendados
1. **Esta semana:** revisar el firewall de Hostinger (Etapa 1, paso 1) y borrar el campo "Sitio web" del usuario admin. Son 10 minutos y tienen el mayor impacto en GEO.
2. Reunir los datos del punto 6. Con los 5 primeros se pueden publicar las Etapas 1–3.
3. Aplicar las etapas en orden, en el staging de Hostinger si existe, y medir PageSpeed antes y después de la Etapa 4.
4. Instalar la analítica y marcar `generate_lead` como conversión. Verificar Search Console y Bing.
5. Conseguir una revisora o revisor clínico externo para el "Revisado por" de los artículos de salud mental (E-E-A-T).
6. Publicar según el calendario editorial, un artículo por semana, con resumen, definición, fuentes y caja de consulta desde el primer día.
7. Cada mes: consultas de prueba en ChatGPT, Perplexity, Gemini y Claude; revisión de los 404 de Rank Math; rendimiento.
8. A mediano plazo: páginas pilar para "Hábitos y conducta" e "IA y mente", un artículo de Francisca y otro de Emanuel (ya están en el calendario) y una prueba con lector de pantalla (NVDA o VoiceOver) del test.

## 9. Mapa del repositorio
- `.claude/agents/` y `.claude/skills/`: los 6 subagentes y las 6 skills del proyecto.
- `docs/auditoria/`: inventario, snapshot de producción, informes de auditoría y de QA, capturas antes/después y scripts.
- `docs/plan.md`, `docs/placeholders.md`, `docs/implementacion/`: el plan, los pendientes y las guías.
- `wp-content/plugins/codigo-calma/`: el plugin (CSS, fuentes, JS, PHP y datos).
- `contenido/etapa-N/`: bloques, correcciones, copy y datos de cada etapa.
- `staging/preview/`: la vista previa, las capturas, el rendimiento y el renderizador PHP.
