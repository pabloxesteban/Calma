# Etapa 4 — SEO técnico, datos estructurados y rendimiento: guía de aplicación

Requisito: Etapas 1–3 aplicadas (la 3, con el copy revisado). Tiempo estimado: 2–2,5 horas. Copia de seguridad antes.

| Pieza | Ruta en el repo |
|---|---|
| Plugin 1.3.0 (JSON-LD, importador SEO, logo sin prioridad alta) | `wp-content/plugins/codigo-calma/` |
| Títulos y descripciones de 34 URLs | `contenido/etapa-4/seo-metadatos.json` (copiado en `plugin/data/`) |
| robots.txt con el sitemap de Rank Math | `contenido/etapa-4/rank-math/robots.txt` |
| Imagen para redes (1200×630) | `wp-content/plugins/codigo-calma/assets/img/og-codigo-calma.jpg` |

Todo lo que hace el plugin se probó en un WordPress 7 local con Kadence, Kadence Blocks y Rank Math (ver `docs/auditoria/informes/qa-etapa-4.md`).

## Paso 1 · Plugin 1.3.0 (5 min)
Subir y reemplazar. Agrega:
- **JSON-LD** en un único `@graph` por página:
  - todas las páginas: Organization y WebSite (con buscador);
  - Servicios: ProfessionalService y FAQPage (solo la pregunta con respuesta completa; las demás se suman cuando dejen de tener placeholders);
  - `/equipo/`: las tres Person;
  - cada página de persona: Person y ProfilePage;
  - entradas: BlogPosting (autora, fechas, categoría, etiquetas) y la persona autora;
  - BreadcrumbList en todas las páginas interiores.
  - Sin ningún dato no verificado: foto, universidad, matrícula y perfiles de Francisca y Emanuel se agregan con el filtro `calma_schema_personas` cuando estén confirmados.
- **Herramientas → Código Calma: SEO:** tabla de vista previa y botón para importar títulos, descripciones, palabra clave y Open Graph en Rank Math. Equivale a `wp calma seo-import`.

## Paso 2 · Rank Math: módulos y ajustes (25 min)
1. **Rank Math → Panel → Módulos:** activar *Mapa del sitio*, *Redirecciones* y *Monitor 404*. **Dejar desactivado *Schema*** (el plugin genera el JSON-LD; con los dos activos se duplica). *Análisis SEO* y *Content AI* opcionales, desactivados por rendimiento.
2. **Títulos y metas → Global:** separador "|"; **imagen OpenGraph por defecto:** subir `og-codigo-calma.jpg` (Medios) y elegirla; tipo de tarjeta de Twitter: "Resumen con imagen grande".
3. **Títulos y metas → Local SEO:** tipo "Organización", nombre "Código Calma", logo = logo del sitio, correo hola@codigocalma.com. Sin dirección ni teléfono (no hay datos confirmados).
4. **Títulos y metas → Otros:**
   - Archivos por fecha: **desactivados**.
   - Archivos de autor: **desactivados**, porque el sitio tiene una sola autora; la página de autora es `/equipo/tatiana-x-stacul/`.
   - Páginas de búsqueda y 404: noindex.
5. **Títulos y metas → Etiquetas:** **noindex** (hasta la limpieza de la Etapa 5). **Categorías:** indexar; "Noindex categorías vacías" activado.
6. **Mapa del sitio:** incluir Entradas, Páginas y Categorías; **excluir** Etiquetas, Autores y Medios.
7. **Ajustes generales → Editar robots.txt:** pegar `contenido/etapa-4/rank-math/robots.txt` (cambia solo la línea `Sitemap:` a `sitemap_index.xml`).
8. Verificar `https://codigocalma.com/sitemap_index.xml` y que `/wp-sitemap.xml` redirige o deja de listarse.

## Paso 3 · Importar metadatos (5 min)
Herramientas → **Código Calma: SEO** → revisar que las 34 filas digan "listo" (si alguna dice "no encontrado", falta crear esa página o el slug no coincide) → **Importar metadatos en Rank Math**. Luego abrir 2–3 URLs y ver el código fuente: `<title>`, `meta description`, `og:title`, `og:image` y un solo `<script type="application/ld+json" class="calma-schema">`.

## Paso 4 · URLs y redirecciones (20 min)
1. **Descargas → `/descargas/`**:
   - Medios → buscar la imagen "descargas" (ID 1839) → Editar → **slug** `descargas-imagen` (es lo que ocupa `/descargas/`).
   - Páginas → Descargas → slug `descargas`.
   - Rank Math → Redirecciones: `descargas-2` → `/descargas/` (301).
   - En menús, pie y enlaces internos, cambiar `/descargas-2/` por `/descargas/` (el pie: `contenido/etapa-2/footer/pie-widget.html`).
2. **Autora:** Rank Math → Redirecciones: `author/admin` → `/equipo/tatiana-x-stacul/` (301).
3. **www → sin www en un salto** (SEO-23): hPanel → Dominios → redirección, o al inicio de `.htaccess`:
   ```apache
   RewriteEngine On
   RewriteCond %{HTTP_HOST} ^www\.codigocalma\.com$ [NC]
   RewriteRule ^(.*)$ https://codigocalma.com/$1 [R=301,L]
   ```
4. Rank Math → Monitor 404: revisar a la semana y redirigir lo que tenga visitas.

## Paso 5 · Usuaria autora (15 min) — E-E-A-T
1. Usuarios → Añadir: nombre de usuario `tatiana-x-stacul`, nombre "Tatiana", apellido "X. Stacul", nombre público "Tatiana X. Stacul", rol Autora, sitio web `https://codigocalma.com/equipo/tatiana-x-stacul/`, biografía [COMPLETAR: bio breve validada].
2. Usuarios → admin → **Eliminar** → "Atribuir todo el contenido a: Tatiana X. Stacul" (conserva las entradas). Antes, crear otra cuenta de administración con un nombre que no sea "admin" (seguridad) si no existe.
3. (Opcional) En el perfil, campo personalizado `calma_persona` = `tatiana-x-stacul` para el JSON-LD. Si no se completa, el plugin ya asigna Tatiana por defecto.

## Paso 6 · Imágenes y rendimiento (30 min)
1. **LiteSpeed Cache → Optimización de imágenes:**
   - pedir la optimización de toda la biblioteca;
   - activar "**Imagen WebP**" y "**Reemplazo WebP**" (y AVIF si el plan lo permite).
2. **LiteSpeed Cache → Opciones de página:**
   - Carga diferida de imágenes: **activada**, excluyendo la clase `calma-hero__media` (la imagen principal del inicio no debe diferirse);
   - "Añadir dimensiones que faltan": activado.
3. **CSS/JS:**
   - LiteSpeed → Page Optimization: combinar/minificar CSS y JS **sin** "carga diferida de JS" en el primer intento, y revisar el sitio;
   - desactivar **Contact Form 7** (el plugin ya no lo carga; así también sale del admin);
   - si ZoloBlocks solo se usa en las tarjetas giratorias del inicio, dejarlo (ya está acotado).
4. **Testimonios:**
   - reemplazar las 3 imágenes rotas (`testimonio-6.jpg`, `-9.jpg`, `-10.jpg`) o quitar esos bloques de imagen;
   - en las 4 imágenes sin dimensiones, volver a insertarlas desde Medios para que tengan `width`/`height`.
5. Purgar caché (LiteSpeed y CDN).

## Paso 7 · Medición (20 min)
1. **Analítica** [COMPLETAR: herramienta de analítica]. Si se usa Google Analytics 4 con Site Kit o GTM, el evento `generate_lead` ya se envía al `dataLayer` en cada consulta (Etapa 3): marcarlo como conversión.
2. **Google Search Console** y **Bing Webmaster Tools:** verificar el dominio (DNS en hPanel), enviar `sitemap_index.xml`, revisar "Páginas" y "Mejoras" (migas, FAQ) a los 7–14 días.
3. **Validar el JSON-LD:** [validator.schema.org](https://validator.schema.org) y la [prueba de resultados enriquecidos](https://search.google.com/test/rich-results) en Inicio, Servicios, una página de equipo y un artículo.
4. **PageSpeed Insights (mobile)** en Inicio, Servicios, un artículo y Blog antes y después del paso 6. Objetivo: LCP < 2,5 s, CLS < 0,1, INP < 200 ms.

## Deshacer
Plugin anterior (1.2.0); Rank Math → Redirecciones (borrar); los metadatos importados se editan o vacían en cada página (caja de Rank Math).
