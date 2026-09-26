---
name: seo-audit
description: Checklist reproducible de auditoría SEO técnica y on-page para codigocalma.com (WordPress + Kadence en Hostinger). Úsala al auditar el sitio, antes y después de cada etapa de cambios, o al publicar una página o artículo nuevo. Incluye comandos para medir y el formato del informe.
---

# SEO audit — Código Calma

## Cómo correrla
1. Listar URLs: `curl -s https://codigocalma.com/wp-sitemap.xml` y cada sub-sitemap (`wp-sitemap-posts-post-1.xml`, `-page-1`, `-taxonomies-category-1`, `-taxonomies-post_tag-1`, `-users-1`).
2. Descargar HTML de cada URL a `docs/auditoria/snapshot-AAAA-MM-DD/html/`.
3. Extraer señales por URL con el script de la sección 4 y completar la tabla.
4. Medir Core Web Vitals mobile en PageSpeed Insights (campo + laboratorio) para: inicio, servicios, contacto, un artículo largo, blog.
5. Registrar resultados en `docs/auditoria/informes/seo.md` con fecha.

## Checklist técnico
- [ ] `robots.txt` accesible (200), sin `Disallow` de recursos CSS/JS, con `Sitemap:`. Coordinar reglas de bots de IA con la skill `geo-optimization`.
- [ ] Sitemap XML válido, solo URLs indexables (200, canonical propio, sin noindex). Excluir usuarios si el autor es "admin"; excluir páginas de prueba/duplicadas.
- [ ] HTTPS, una sola versión de host (sin www ↔ con www duplicado), 301 permanentes.
- [ ] Canonical autorreferente en todas las páginas indexables (hoy falta en `/blog/` y archivos de categoría).
- [ ] Sin duplicados: `/blog/` vs `/entradas/`; slug `descargas-2`; `sobre_tatiana` → `sobre-tatiana` (301).
- [ ] Códigos: sin 404 internos, sin cadenas de redirección.
- [ ] `lang="es"` (o `es-AR`/`es-419` según público) en `<html>`.
- [ ] Core Web Vitals: LCP < 2,5 s, CLS < 0,1, INP < 200 ms (percentil 75, mobile).
- [ ] Imágenes: webp/avif, `width`/`height`, `srcset`, `loading="lazy"` excepto LCP (`fetchpriority="high"`, sin lazy).
- [ ] Fuentes: locales, woff2, preload de 1–2 archivos, ≤ 2 familias.
- [ ] JS/CSS: sin plugins de bloques duplicados cargando en todas las páginas (ZoloBlocks + Kadence Blocks + Blocks Animation); diferir no críticos.
- [ ] Caché: LiteSpeed configurado, HTML cacheado, compresión br/gzip.
- [ ] Datos estructurados válidos (skill `schema-markup`).
- [ ] Open Graph + Twitter Card en todas las URLs.
- [ ] Página 404 útil con buscador y enlaces a pilares.

## Checklist on-page (por URL)
- [ ] Exactamente 1 `<h1>`, descriptivo, con la palabra clave. Jerarquía H2→H3 sin saltos.
- [ ] `<title>` único, 50–60 caracteres: `Palabra clave principal: beneficio | Código Calma`.
- [ ] Meta description única, 140–160 caracteres, en tuteo, con beneficio.
- [ ] Slug corto, minúsculas, guiones, sin stopwords innecesarias.
- [ ] Primer párrafo responde la intención (ver `geo-optimization`).
- [ ] Enlaces internos: ≥ 3 contextuales (pilar, relacionados, servicio) con anclas descriptivas (no "Leer más" / "Continuar" solos).
- [ ] Enlaces externos a fuentes con autoridad, `rel` apropiado.
- [ ] `alt` descriptivo en imágenes de contenido; `alt=""` solo en decorativas.
- [ ] Autor real visible y fecha de publicación/actualización.
- [ ] Ortografía y tildes revisadas (ej.: "autoría", no "autoria").

## Formato de hallazgo
| URL | Problema | Evidencia | Impacto | Esfuerzo | Solución |
|---|---|---|---|---|---|
| /blog/ | Sin canonical | no hay `<link rel="canonical">` | Medio | Bajo | Plugin SEO o `wp_head` en tema hijo |

## 4. Script de extracción (Python, sin dependencias)
```python
import re, glob, html, os
for f in sorted(glob.glob('docs/auditoria/snapshot-*/html/*.html')):
    s = open(f, encoding='utf-8').read()
    g = lambda p: (m.group(1) if (m := re.search(p, s, re.S)) else None)
    print(os.path.basename(f),
          'title=', html.unescape(g(r'<title>(.*?)</title>') or '')[:70],
          'desc=', bool(g(r'<meta name="description" content="([^"]*)')),
          'canonical=', bool(g(r'rel="canonical" href="([^"]*)')),
          'og=', 'og:title' in s, 'jsonld=', s.count('application/ld+json'),
          'h1=', len(re.findall(r'<h1[\s>]', s)))
```

## Ejemplo de metadatos
- Página: Servicios
  - title: `Mentoría en ciberpsicología uno a uno | Código Calma` (52)
  - description: `Acompañamiento online, una persona por vez: psicología y hábitos digitales, accesibilidad cognitiva y gestión de proyectos. Cuéntanos qué necesitas.` (≈150)
