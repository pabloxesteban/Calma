---
name: design-system
description: Design system de Código Calma — tokens de color, tipografía, espaciado, radios y sombras; componentes (botones, tarjetas, tarjetas de paso, badges, header, footer, CTA, formularios) y modo oscuro coherente. Úsala antes de escribir o revisar cualquier CSS, bloque de Kadence o plantilla del sitio, y para unificar el estilo (menú negro vs. páginas lavanda).
---

# Design system — Código Calma

Fuente única de verdad visual. Todo valor sale de un token `--calma-*`. Se implementa como CSS global del tema hijo de Kadence (`wp-content/themes/kadence-child/assets/css/calma-design-system.css`) y se mapea a la paleta global de Kadence (`--global-palette1…15`) para que los bloques existentes hereden sin tocar cada página.

## 1. Tokens

### Color (modo claro)
Parte de la paleta actual (azul `#64b2e5`, lavanda `#dad4f6`, pizarra `#0f172a`) pero corrige contraste.

| Token | Valor | Uso | Contraste sobre `--calma-bg` |
|---|---|---|---|
| `--calma-bg` | `#f8fafc` | fondo general | — |
| `--calma-surface` | `#ffffff` | tarjetas | — |
| `--calma-surface-soft` | `#f1eefc` | secciones lavanda suaves | — |
| `--calma-lavender` | `#dad4f6` | acentos, fondos de badge | decorativo |
| `--calma-text` | `#0f172a` | texto principal | 17,0:1 |
| `--calma-text-muted` | `#475569` | texto secundario | 7,2:1 |
| `--calma-primary` | `#1d5f94` | botón primario, enlaces | 6,4:1 (texto blanco encima: 6,7:1) |
| `--calma-primary-hover` | `#174d78` | hover/activo | 8,5:1 |
| `--calma-accent` | `#64b2e5` | ilustraciones, bordes, íconos grandes (nunca texto pequeño ni fondo de texto blanco: 2,3:1) | 2,2:1 |
| `--calma-violet` | `#5b3fb8` | badges de texto, eyebrow | 7,1:1 |
| `--calma-navy` | `#16214d` | bloques de CTA, footer | — |
| `--calma-on-navy` | `#ffffff` | texto sobre navy | 15,5:1 |
| `--calma-border` | `#e2e8f0` | bordes de tarjetas | — |
| `--calma-focus` | `#1d5f94` | anillo de foco (2 px + offset 2 px) | ≥ 3:1 |
| `--calma-success` / `--calma-error` | `#1f7a4d` / `#b42318` | formularios | ≥ 4,5:1 |

> Verificá cada combinación nueva con una calculadora de contraste (WCAG 2.x). Texto normal ≥ 4,5:1; texto ≥ 24 px o 19 px bold ≥ 3:1; bordes/íconos funcionales ≥ 3:1.

### Tipografía
Hoy se cargan 3 familias desde Google Fonts (Lora, Inter, Jost). Unificar a **2**, alojadas localmente (woff2, `font-display: swap`, subset latin + latin-ext):
- Títulos: `--calma-font-heading: "Lora", Georgia, serif;` (700)
- Cuerpo e interfaz: `--calma-font-body: "Inter", system-ui, -apple-system, "Segoe UI", sans-serif;` (400, 600)

Escala fluida (máx. 6 tamaños):
```
--calma-fs-xs:   0.875rem;                          /* 14px: metadatos */
--calma-fs-sm:   1rem;                              /* 16px: UI, badges */
--calma-fs-base: clamp(1.0625rem, 1rem + .25vw, 1.125rem); /* 17–18px cuerpo */
--calma-fs-lg:   clamp(1.25rem, 1.1rem + .6vw, 1.5rem);    /* H3 */
--calma-fs-xl:   clamp(1.5rem, 1.2rem + 1.4vw, 2.25rem);   /* H2 */
--calma-fs-2xl:  clamp(1.875rem, 1.4rem + 2.4vw, 3rem);    /* H1 */
--calma-lh-body: 1.65; --calma-lh-heading: 1.2; --calma-measure: 68ch;
```

### Espaciado (base 4 px)
```
--calma-space-1: 4px;  --calma-space-2: 8px;  --calma-space-3: 12px; --calma-space-4: 16px;
--calma-space-5: 20px; --calma-space-6: 24px; --calma-space-8: 32px; --calma-space-10: 40px;
--calma-space-12: 48px; --calma-space-16: 64px; --calma-space-20: 80px;
--calma-gutter: clamp(20px, 5vw, 32px);           /* margen lateral de página */
--calma-section-y: clamp(48px, 8vw, 96px);        /* separación vertical entre secciones */
--calma-container: 1160px; --calma-container-text: 720px;
```

### Radios, sombras, movimiento
```
--calma-radius-sm: 8px; --calma-radius: 16px; --calma-radius-lg: 24px; --calma-radius-pill: 999px;
--calma-shadow-sm: 0 1px 2px rgb(15 23 42 / .06);
--calma-shadow: 0 4px 16px rgb(15 23 42 / .08);
--calma-ease: cubic-bezier(.2,.7,.2,1); --calma-dur: 180ms;
```
Toda animación dentro de `@media (prefers-reduced-motion: no-preference)`.

## 2. Componentes

### Botón
```css
.calma-btn{display:inline-flex;align-items:center;justify-content:center;gap:var(--calma-space-2);
  min-height:48px;padding:12px 24px;border-radius:var(--calma-radius-pill);
  font:600 var(--calma-fs-sm)/1.2 var(--calma-font-body);text-decoration:none;
  transition:background var(--calma-dur) var(--calma-ease);}
.calma-btn--primary{background:var(--calma-primary);color:#fff;}
.calma-btn--primary:hover{background:var(--calma-primary-hover);}
.calma-btn--on-dark{background:#fff;color:var(--calma-navy);}          /* dentro de bloques navy */
.calma-btn--secondary{background:transparent;color:var(--calma-primary);box-shadow:inset 0 0 0 2px currentColor;}
.calma-btn:focus-visible{outline:2px solid var(--calma-focus);outline-offset:3px;}
```
Regla: un primario por pantalla. "Solicitar una consulta" siempre `--primary` (o `--on-dark` sobre navy). Nunca texto blanco sobre `#64b2e5`.

### Tarjeta
```css
.calma-card{background:var(--calma-surface);border:1px solid var(--calma-border);border-radius:var(--calma-radius);
  padding:clamp(20px,4vw,32px);box-shadow:var(--calma-shadow-sm);}
```

### Tarjeta de paso (proceso)
El número vive **dentro** del padding, nunca con posición negativa.
```css
.calma-step{position:relative;display:grid;grid-template-columns:auto 1fr;gap:var(--calma-space-4);
  align-items:start;padding:clamp(20px,4vw,32px);}
.calma-step__num{inline-size:40px;block-size:40px;border-radius:50%;display:grid;place-items:center;
  background:var(--calma-primary);color:#fff;font-weight:700;}
```

### Badge / eyebrow
```css
.calma-badge{display:inline-block;padding:4px 12px;border-radius:var(--calma-radius-pill);
  background:var(--calma-surface-soft);color:var(--calma-violet);font:600 var(--calma-fs-xs)/1.4 var(--calma-font-body);
  letter-spacing:.04em;text-transform:uppercase;}
```
Una categoría de blog = un color de badge fijo (máx. 6).

### Header
Un único header para todo el sitio: fondo `--calma-surface`, logo + menú, botón primario "Solicitar una consulta" a la derecha (en mobile, dentro del drawer y como botón fijo inferior opcional). Se elimina la variante negra.

### Footer
Fondo `--calma-navy`, 3–4 columnas (mobile: apiladas): marca + descripción de 1 línea; navegación; recursos (blog, test, descargas); contacto + LinkedIn + newsletter; fila legal (privacidad, aviso "no es un servicio de urgencias", ©).

### Sección
```css
.calma-section{padding-block:var(--calma-section-y);padding-inline:var(--calma-gutter);}
.calma-section > *{max-width:var(--calma-container);margin-inline:auto;}
```
Nunca secciones vacías: una sección sin contenido se elimina, no se "rellena" con padding.

### Formularios (Kadence Form)
Label visible encima, input `min-height:48px`, borde `--calma-border` 1px → 2px `--calma-primary` en foco, error bajo el campo en `--calma-error` con ícono + texto.

## 3. Modo oscuro
Solo si se ofrece en todo el sitio; se activa con `prefers-color-scheme: dark` y/o `[data-theme="dark"]`. Se reasignan tokens, no componentes:
```
--calma-bg:#0b1020; --calma-surface:#131a33; --calma-surface-soft:#1b2347; --calma-text:#e8ecf5;
--calma-text-muted:#a9b3c9; --calma-primary:#8cc8ef; (texto sobre primario: #0b1020)
--calma-border:#27304f; --calma-navy:#070b18; --calma-violet:#c4b5fd;
```
Imágenes con fondo blanco: `background: var(--calma-surface)` + padding. Re-verificar contrastes.

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
Después: `.calma-btn--primary` `#fff` sobre `#1d5f94` (6,7:1 ✅) o `.calma-btn--on-dark` `#16214d` sobre `#fff` dentro del bloque navy (15,5:1 ✅).

## 6. Prefijo y convivencia con el CSS existente
Se usa el prefijo `calma-` (`--calma-*`, `.calma-*`) porque el CSS inline de Servicios y Herramientas ya usa `.cc-*` con un reset (`.cc li{padding:0}`, `.cc p{margin:0}`) que anula padding y márgenes. Antes de aplicar el design system en esas páginas, eliminar sus `<style>` inline y migrar el marcado a clases `calma-*`.
Tampoco se admiten documentos HTML completos pegados en bloques "HTML personalizado" (caso de la línea de tiempo del inicio: su `body{padding:40px}` afecta a todo el sitio).
