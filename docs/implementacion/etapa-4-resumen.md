# Etapa 4 — Resumen de cierre

Estado: **lista para aplicar** (nada publicado). Guía: `docs/implementacion/etapa-4.md`. QA: `docs/auditoria/informes/qa-etapa-4.md` (aprueba; validación externa pendiente de producción).

| Área | Antes | Después |
|---|---|---|
| Meta description | 0 de 28 URLs | 34 URLs con título (50–60) y descripción (140–160) importables con un clic |
| Open Graph | Ninguno | Título/descripción por URL + imagen por defecto 1200×630 |
| Datos estructurados | Ninguno | `@graph` por página: Organization, WebSite, Person ×3, ProfilePage, ProfessionalService, FAQPage, BlogPosting, BreadcrumbList; sin datos no verificados |
| Sitemap | Nativo, con usuarios y 11 etiquetas finas | Rank Math: entradas, páginas y categorías; sin etiquetas, autores ni medios |
| Archivos finos | Fecha, autor "admin", etiquetas y categoría vacía indexables | Desactivados o noindex |
| URLs | `/descargas-2/`, `/author/admin/`, www en 2 saltos | `/descargas/` (301), autor → página de Tatiana, www en 1 salto |
| Autoría | Usuario "admin", enlace 404 | Usuaria "Tatiana X. Stacul" con web = su página de equipo |
| Rendimiento | CLS inicio 0,262; 3–5 peticiones a Google Fonts; LCP = logo de 512 px | CLS 0; 0 Google Fonts; LCP = H1/hero; WebP y carga diferida vía LiteSpeed |

## Pendiente
- Herramienta de analítica (el evento `generate_lead` ya está listo).
- Verificar Search Console / Bing y medir PageSpeed en producción tras aplicar.
- Completar en `calma_schema_personas` foto, formación y perfiles cuando estén confirmados.
