---
name: design-system
description: Design system de Código Calma — tokens de color, tipografía, espaciado, radios y sombras; componentes (botones, tarjetas, tarjetas de paso, badges, header, footer, CTA, formularios) y modo oscuro coherente. Úsala antes de escribir o revisar cualquier CSS, bloque de Kadence o plantilla del sitio, y para unificar el estilo (menú negro vs. páginas lavanda).
---

# Design system — Código Calma

Fuente única de verdad visual. Todo valor sale de un token `--cc-*`. Se implementa como CSS global del tema hijo de Kadence (`wp-content/themes/kadence-child/assets/css/cc-design-system.css`) y se mapea a la paleta global de Kadence (`--global-palette1…15`) para que los bloques existentes hereden sin tocar cada página.

## 1. Tokens

### Color (modo claro)
Parte de la paleta actual (azul `#64b2e5`, lavanda `#dad4f6`, pizarra `#0f172a`) pero corrige contraste.

| Token | Valor | Uso | Contraste sobre `--cc-bg` |
|---|---|---|---|
| `--cc-bg` | `#f8fafc` | fondo general | — |
| `--cc-surface` | `#ffffff` | tarjetas | — |
| `--cc-surface-soft` | `#f1eefc` | secciones lavanda suaves | — |
| `--cc-lavender` | `#dad4f6` | acentos, fondos de badge | decorativo |
| `--cc-text` | `#0f172a` | texto principal | 17,0:1 |
| `--cc-text-muted` | `#475569` | texto secundario | 7,2:1 |
| `--cc-primary` | `#1d5f94` | botón primario, enlaces | 6,4:1 (texto blanco encima: 6,7:1) |
| `--cc-primary-hover` | `#174d78` | hover/activo | 8,5:1 |
| `--cc-accent` | `#64b2e5` | ilustraciones, bordes, íconos grandes (nunca texto pequeño ni fondo de texto blanco: 2,3:1) | 2,2:1 |
| `--cc-violet` | `#5b3fb8` | badges de texto, eyebrow | 7,1:1 |
| `--cc-navy` | `#16214d` | bloques de CTA, footer | — |
| `--cc-on-navy` | `#ffffff` | texto sobre navy | 15,5:1 |
| `--cc-border` | `#e2e8f0` | bordes de tarjetas | — |
| `--cc-focus` | `#1d5f94` | anillo de foco (2 px + offset 2 px) | ≥ 3:1 |
| `--cc-success` / `--cc-error` | `#1f7a4d` / `#b42318` | formularios | ≥ 4,5:1 |

> Verificá cada combinación nueva con una calculadora de contraste (WCAG 2.x). Texto normal ≥ 4,5:1; texto ≥ 24 px o 19 px bold ≥ 3:1; bordes/íconos funcionales ≥ 3:1.

### Tipografía
Hoy se cargan 3 familias desde Google Fonts (Lora, Inter, Jost). Unificar a **2**, alojadas localmente (woff2, `font-display: swap`, subset latin + latin-ext):
- Títulos: `--cc-font-heading: "Lora", Georgia, serif;` (700)
- Cuerpo e interfaz: `--cc-font-body: "Inter", system-ui, -apple-system, "Segoe UI", sans-serif;` (400, 600)

Escala fluida (máx. 6 tamaños):
```
--cc-fs-xs:   0.875rem;                          /* 14px: metadatos */
--cc-fs-sm:   1rem;                              /* 16px: UI, badges */
--cc-fs-base: clamp(1.0625rem, 1rem + .25vw, 1.125rem); /* 17–18px cuerpo */
--cc-fs-lg:   clamp(1.25rem, 1.1rem + .6vw, 1.5rem);    /* H3 */
--cc-fs-xl:   clamp(1.5rem, 1.2rem + 1.4vw, 2.25rem);   /* H2 */
--cc-fs-2xl:  clamp(1.875rem, 1.4rem + 2.4vw, 3rem);    /* H1 */
--cc-lh-body: 1.65; --cc-lh-heading: 1.2; --cc-measure: 68ch;
```

### Espaciado (base 4 px)
```
--cc-space-1: 4px;  --cc-space-2: 8px;  --cc-space-3: 12px; --cc-space-4: 16px;
--cc-space-5: 20px; --cc-space-6: 24px; --cc-space-8: 32px; --cc-space-10: 40px;
--cc-space-12: 48px; --cc-space-16: 64px; --cc-space-20: 80px;
--cc-gutter: clamp(20px, 5vw, 32px);           /* margen lateral de página */
--cc-section-y: clamp(48px, 8vw, 96px);        /* separación vertical entre secciones */
--cc-container: 1160px; --cc-container-text: 720px;
```

### Radios, sombras, movimiento
```
--cc-radius-sm: 8px; --cc-radius: 16px; --cc-radius-lg: 24px; --cc-radius-pill: 999px;
--cc-shadow-sm: 0 1px 2px rgb(15 23 42 / .06);
--cc-shadow: 0 4px 16px rgb(15 23 42 / .08);
--cc-ease: cubic-bezier(.2,.7,.2,1); --cc-dur: 180ms;
```
Toda animación dentro de `@media (prefers-reduced-motion: no-preference)`.

## 2. Componentes

### Botón
```css
.cc-btn{display:inline-flex;align-items:center;justify-content:center;gap:var(--cc-space-2);
  min-height:48px;padding:12px 24px;border-radius:var(--cc-radius-pill);
  font:600 var(--cc-fs-sm)/1.2 var(--cc-font-body);text-decoration:none;
  transition:background var(--cc-dur) var(--cc-ease);}
.cc-btn--primary{background:var(--cc-primary);color:#fff;}
.cc-btn--primary:hover{background:var(--cc-primary-hover);}
.cc-btn--on-dark{background:#fff;color:var(--cc-navy);}          /* dentro de bloques navy */
.cc-btn--secondary{background:transparent;color:var(--cc-primary);box-shadow:inset 0 0 0 2px currentColor;}
.cc-btn:focus-visible{outline:2px solid var(--cc-focus);outline-offset:3px;}
```
Regla: un primario por pantalla. "Solicitar una consulta" siempre `--primary` (o `--on-dark` sobre navy). Nunca texto blanco sobre `#64b2e5`.

### Tarjeta
```css
.cc-card{background:var(--cc-surface);border:1px solid var(--cc-border);border-radius:var(--cc-radius);
  padding:clamp(20px,4vw,32px);box-shadow:var(--cc-shadow-sm);}
```

### Tarjeta de paso (proceso)
El número vive **dentro** del padding, nunca con posición negativa.
```css
.cc-step{position:relative;display:grid;grid-template-columns:auto 1fr;gap:var(--cc-space-4);
  align-items:start;padding:clamp(20px,4vw,32px);}
.cc-step__num{inline-size:40px;block-size:40px;border-radius:50%;display:grid;place-items:center;
  background:var(--cc-primary);color:#fff;font-weight:700;}
```

### Badge / eyebrow
```css
.cc-badge{display:inline-block;padding:4px 12px;border-radius:var(--cc-radius-pill);
  background:var(--cc-surface-soft);color:var(--cc-violet);font:600 var(--cc-fs-xs)/1.4 var(--cc-font-body);
  letter-spacing:.04em;text-transform:uppercase;}
```
Una categoría de blog = un color de badge fijo (máx. 6).

### Header
Un único header para todo el sitio: fondo `--cc-surface`, logo + menú, botón primario "Solicitar una consulta" a la derecha (en mobile, dentro del drawer y como botón fijo inferior opcional). Se elimina la variante negra.

### Footer
Fondo `--cc-navy`, 3–4 columnas (mobile: apiladas): marca + descripción de 1 línea; navegación; recursos (blog, test, descargas); contacto + LinkedIn + newsletter; fila legal (privacidad, aviso "no es un servicio de urgencias", ©).

### Sección
```css
.cc-section{padding-block:var(--cc-section-y);padding-inline:var(--cc-gutter);}
.cc-section > *{max-width:var(--cc-container);margin-inline:auto;}
```
Nunca secciones vacías: una sección sin contenido se elimina, no se "rellena" con padding.

### Formularios (Contact Form 7)
Label visible encima, input `min-height:48px`, borde `--cc-border` 1px → 2px `--cc-primary` en foco, error bajo el campo en `--cc-error` con ícono + texto.

## 3. Modo oscuro
Solo si se ofrece en todo el sitio; se activa con `prefers-color-scheme: dark` y/o `[data-theme="dark"]`. Se reasignan tokens, no componentes:
```
--cc-bg:#0b1020; --cc-surface:#131a33; --cc-surface-soft:#1b2347; --cc-text:#e8ecf5;
--cc-text-muted:#a9b3c9; --cc-primary:#8cc8ef; (texto sobre primario: #0b1020)
--cc-border:#27304f; --cc-navy:#070b18; --cc-violet:#c4b5fd;
```
Imágenes con fondo blanco: `background: var(--cc-surface)` + padding. Re-verificar contrastes.

## 4. Checklist de aplicación
- [ ] Ningún color o espacio hardcodeado fuera del archivo de tokens.
- [ ] Header y footer idénticos en todas las plantillas (página, entrada, archivo, búsqueda, 404).
- [ ] Margen lateral ≥ 20 px en 360 px; sin scroll horizontal.
- [ ] Tarjetas con padding ≥ 20 px; números de paso dentro de la tarjeta.
- [ ] Sin franjas vacías > 48 px antes del contenido o del footer.
- [ ] Botón primario contraste ≥ 4,5:1 y alto ≥ 48 px.
- [ ] Fuentes locales, máximo 2 familias, `font-display: swap`, preload de la del H1.
- [ ] Animaciones respetan `prefers-reduced-motion` y no dejan contenido desplazado fuera de pantalla (bug actual del hero en 390 px).

## 5. Ejemplo: antes / después
Antes (servicios): botón `color:#334155` sobre `#64b2e5` (4,46:1, alto 62 px con borde del mismo color); inicio: `#fff` sobre `#64b2e5` (2,32:1 ❌).
Después: `.cc-btn--primary` `#fff` sobre `#1d5f94` (6,7:1 ✅) o `.cc-btn--on-dark` `#16214d` sobre `#fff` dentro del bloque navy (15,5:1 ✅).
