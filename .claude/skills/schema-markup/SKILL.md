---
name: schema-markup
description: Plantillas JSON-LD para codigocalma.com — Organization, Person (cada profesional), ProfessionalService, WebSite, Article/BlogPosting, FAQPage y BreadcrumbList, con reglas para no inventar datos. Úsala al agregar o revisar datos estructurados en plantillas del tema hijo o en páginas concretas.
---

# Schema markup — Código Calma

## Reglas
- JSON-LD en `<head>` (vía `wp_head` en el tema hijo o plugin SEO), un `@graph` por página, entidades enlazadas por `@id`.
- **Solo datos visibles en la página y verificados.** Títulos, matrículas, universidades, precios, horarios, dirección: si no están confirmados, no van en el schema (y en la página va `[COMPLETAR: …]`).
- No usar `Review`/`AggregateRating` sobre la propia organización (Google no lo muestra y los testimonios deben ser reales y verificables).
- Validar en https://validator.schema.org y en la prueba de resultados enriquecidos de Google.

## IDs estables
- Organización: `https://codigocalma.com/#organization`
- Sitio: `https://codigocalma.com/#website`
- Servicio: `https://codigocalma.com/servicios/#service`
- Personas: `https://codigocalma.com/equipo/<slug>/#person`

## Organization + WebSite (todas las páginas)
```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Organization",
      "@id": "https://codigocalma.com/#organization",
      "name": "Código Calma",
      "url": "https://codigocalma.com/",
      "logo": { "@type": "ImageObject", "url": "https://codigocalma.com/[COMPLETAR: ruta-logo-512.png]", "width": 512, "height": 512 },
      "description": "Portal de ciberpsicología y bienestar digital en español, con mentoría y acompañamiento uno a uno.",
      "email": "hola@codigocalma.com",
      "sameAs": ["[COMPLETAR: URL LinkedIn de Código Calma]"],
      "founder": { "@id": "https://codigocalma.com/equipo/tatiana-x-stacul/#person" },
      "member": [
        { "@id": "https://codigocalma.com/equipo/tatiana-x-stacul/#person" },
        { "@id": "https://codigocalma.com/equipo/francisca-cortes-santoro/#person" },
        { "@id": "https://codigocalma.com/equipo/emanuel-c-franco/#person" }
      ],
      "knowsAbout": ["Ciberpsicología", "Bienestar digital", "Accesibilidad cognitiva", "Gestión de proyectos"]
    },
    {
      "@type": "WebSite",
      "@id": "https://codigocalma.com/#website",
      "url": "https://codigocalma.com/",
      "name": "Código Calma",
      "inLanguage": "es",
      "publisher": { "@id": "https://codigocalma.com/#organization" },
      "potentialAction": { "@type": "SearchAction", "target": "https://codigocalma.com/?s={search_term_string}", "query-input": "required name=search_term_string" }
    }
  ]
}
```
> Revisar si "founder" es correcto antes de publicar: [COMPLETAR: confirmar fundadora/es].

## Person (una por profesional, en su página de equipo y referenciada en artículos)
```json
{
  "@type": "Person",
  "@id": "https://codigocalma.com/equipo/tatiana-x-stacul/#person",
  "name": "Tatiana X. Stacul",
  "jobTitle": "Psicóloga",
  "description": "Psicóloga especializada en ciberpsicología y comportamiento en entornos digitales.",
  "url": "https://codigocalma.com/equipo/tatiana-x-stacul/",
  "image": "[COMPLETAR: foto profesional]",
  "worksFor": { "@id": "https://codigocalma.com/#organization" },
  "knowsAbout": ["Ciberpsicología", "Ciencias del comportamiento", "Neurociencias", "Concienciación en ciberseguridad"],
  "alumniOf": "[COMPLETAR: universidad del grado en Psicología — solo si se confirma]",
  "hasCredential": "[COMPLETAR: matrícula profesional — solo si se confirma]",
  "sameAs": ["[COMPLETAR: LinkedIn]"]
}
```
Las entradas con `[COMPLETAR…]` **se eliminan del JSON** hasta tener el dato (un placeholder en JSON-LD publicado es un error); el placeholder se mantiene en la página visible y en `docs/placeholders.md`.
Francisca Cortés Santoro: `jobTitle` "Especialista en accesibilidad cognitiva y lenguaje". Emanuel C. Franco: `jobTitle` "Gestor de proyectos y procesos" [COMPLETAR: confirmar denominación].

## ProfessionalService (página de servicios)
```json
{
  "@type": "ProfessionalService",
  "@id": "https://codigocalma.com/servicios/#service",
  "name": "Código Calma — Mentoría y acompañamiento uno a uno",
  "url": "https://codigocalma.com/servicios/",
  "description": "Acompañamiento online, una persona por vez, en tres a seis sesiones: hábitos digitales y ciberpsicología, accesibilidad cognitiva y gestión de proyectos.",
  "provider": { "@id": "https://codigocalma.com/#organization" },
  "areaServed": "[COMPLETAR: países o 'Online, hispanohablantes']",
  "availableLanguage": "es",
  "email": "hola@codigocalma.com",
  "hasOfferCatalog": {
    "@type": "OfferCatalog",
    "name": "Acompañamientos",
    "itemListElement": [
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Hábitos digitales y comportamiento", "provider": { "@id": "https://codigocalma.com/equipo/tatiana-x-stacul/#person" } } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Accesibilidad cognitiva y lenguaje claro", "provider": { "@id": "https://codigocalma.com/equipo/francisca-cortes-santoro/#person" } } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Gestión de proyectos y procesos", "provider": { "@id": "https://codigocalma.com/equipo/emanuel-c-franco/#person" } } }
    ]
  }
}
```
Sin `priceRange`, `address` ni `openingHours` hasta confirmarlos.

## BlogPosting (cada artículo)
```json
{
  "@type": "BlogPosting",
  "@id": "https://codigocalma.com/<slug>/#article",
  "headline": "Máx. 110 caracteres, igual al H1",
  "description": "= meta description",
  "image": { "@type": "ImageObject", "url": "…/imagen-1200x630.webp", "width": 1200, "height": 630 },
  "datePublished": "2026-07-19T09:00:00-03:00",
  "dateModified": "2026-07-19T09:00:00-03:00",
  "author": { "@id": "https://codigocalma.com/equipo/tatiana-x-stacul/#person" },
  "publisher": { "@id": "https://codigocalma.com/#organization" },
  "mainEntityOfPage": "https://codigocalma.com/<slug>/",
  "articleSection": "Categoría principal",
  "keywords": ["etiqueta 1", "etiqueta 2"],
  "inLanguage": "es",
  "citation": ["https://doi.org/10.1001/jamanetworkopen.2025.2193"]
}
```

## FAQPage (solo si las preguntas y respuestas son visibles en la página)
```json
{
  "@type": "FAQPage",
  "mainEntity": [
    { "@type": "Question", "name": "¿Cuántas sesiones dura el acompañamiento?",
      "acceptedAnswer": { "@type": "Answer", "text": "Entre tres y seis sesiones online, acordadas en el primer encuentro." } }
  ]
}
```
Nota: Google limita los resultados enriquecidos de FAQ a sitios de gobierno/salud con autoridad, pero el marcado sigue ayudando a la comprensión por motores generativos.

## BreadcrumbList
```json
{
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Inicio", "item": "https://codigocalma.com/" },
    { "@type": "ListItem", "position": 2, "name": "Blog", "item": "https://codigocalma.com/blog/" },
    { "@type": "ListItem", "position": 3, "name": "Psicología", "item": "https://codigocalma.com/category/psicologia/" },
    { "@type": "ListItem", "position": 4, "name": "Título del artículo" }
  ]
}
```

## Checklist
- [ ] Organization + WebSite en todas las páginas.
- [ ] Person por profesional, sin campos no verificados.
- [ ] ProfessionalService en /servicios/.
- [ ] BlogPosting en cada entrada con autor real y fechas ISO 8601 con zona horaria.
- [ ] BreadcrumbList coherente con migas visibles.
- [ ] FAQPage solo con FAQ visibles.
- [ ] Cero errores en validator.schema.org y Rich Results Test.
