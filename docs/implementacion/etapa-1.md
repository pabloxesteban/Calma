# Etapa 1 — Arreglos críticos: guía de aplicación en WordPress

Quién la aplica: una persona con acceso a **wp-admin** y **hPanel**. Tiempo estimado: 2–3 horas.
Todo lo que se pega o se sube está en la rama `claude/focused-babbage-403shx`:

| Pieza | Ruta en el repo |
|---|---|
| Plugin del sitio (design system + correcciones) | `wp-content/plugins/codigo-calma/` |
| Bloques de reemplazo | `contenido/etapa-1/bloques/` |
| Correcciones de texto y encabezados | `contenido/etapa-1/correcciones.md` (generado de `correcciones.json`) |
| Formulario | `contenido/etapa-1/bloques/formulario-contacto.md` |
| Rank Math | `contenido/etapa-1/rank-math/` |
| Vista previa y capturas | `staging/preview/`, `docs/auditoria/capturas-despues-etapa-1/` |

> Orden recomendado: 0 → 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8. Cada paso se puede verificar por separado. Si algo sale mal, el paso 0 permite volver atrás.

---

## Paso 0 · Copia de seguridad (5 min)
1. hPanel → Sitios web → codigocalma.com → **Archivos → Copias de seguridad** → "Crear nueva copia de seguridad" (archivos + base de datos).
2. Anotar la fecha y hora. Si hay un entorno de staging en Hostinger (hPanel → WordPress → Staging), usarlo para probar los pasos 2–7 antes de producción.

## Paso 1 · Firewall y antibots de Hostinger (15 min + soporte) — GEO-01/02
El bloqueo de las IA **no está en robots.txt**: GPTBot recibe `429` en `/blog/` y en URLs con parámetros, y cualquier visitante recibe a veces un `403` o la pantalla reCAPTCHA «Bot Verification» (`/.lsrecap/recaptcha`).
1. hPanel → Sitios web → codigocalma.com → **Seguridad** y **Rendimiento → CDN**: buscar opciones tipo «Bloqueo de bots de IA / AI crawlers», «Protección antibots», «Rate limiting», «reCAPTCHA». Permitir: GPTBot, OAI-SearchBot, ChatGPT-User, ClaudeBot, Claude-User, Claude-SearchBot, PerplexityBot, Perplexity-User, Google-Extended, Applebot-Extended, bingbot.
2. WordPress → **LiteSpeed Cache → General / Seguridad**: si "reCAPTCHA" o "Bot protection" está activo, relajar el umbral o desactivarlo para bots verificados.
3. Si no hay opción visible, abrir ticket con soporte. Texto y evidencia (request-ids) listos en `docs/auditoria/informes/geo.md` §2.5.
4. **Verificar:** con la herramienta de ChatGPT/Perplexity/Claude, pedir que lean `https://codigocalma.com/blog/`; y en hPanel → Registros de acceso, que los bots reciban 200 (comandos en geo.md §2.5).

## Paso 2 · Plugin "Código Calma" (10 min) — UX-03/04/06/11/13/14/16/24, A11Y-02…05/13/15/20
Se entrega como **plugin** y no como tema hijo: al activar un tema hijo, WordPress no traslada los ajustes del Personalizador de Kadence (logo, menús, colores, encabezado) y habría que rehacerlos. El plugin aplica lo mismo sin cambiar de tema.
1. Comprimir la carpeta `wp-content/plugins/codigo-calma/` en `codigo-calma.zip` (la carpeta dentro del zip).
2. Plugins → Añadir nuevo → Subir plugin → instalar → **Activar**.
3. Qué hace (no requiere configurar nada):
   - Tokens del design system (`--calma-*`) y paleta de Kadence con contraste AA: azul principal `#1d5f94` (6,7:1) en lugar de `#64b2e5` (2,3:1).
   - Neutraliza las animaciones que dejaban texto fuera de pantalla o invisible.
   - Quita las franjas vacías de las páginas "encajonadas" y ajusta márgenes laterales (20 px) y tamaños de títulos en mobile.
   - Menú mobile claro (fin del "menú negro").
   - Foco visible, botones de 48 px, formulario legible.
   - Deja de cargar Contact Form 7 (instalado pero sin uso).
   - H1 "Blog" en la página de entradas si Kadence lo tiene oculto.
4. **Recomendado (mismo efecto, desde el panel, para que el editor muestre los mismos colores):**
   - Personalizar → Colores globales: paleta 1 = `#1d5f94`, paleta 2 = `#174d78`; botones: fondo `#1d5f94`, fondo hover `#174d78`, texto blanco.
   - Personalizar → Encabezado → **Drawer/Menú mobile**: fondo `#ffffff`, enlaces `#0f172a`.
   - Personalizar → Blog → Archivo de entradas: **Mostrar título** activado.
5. **Verificar:** la home en el celular (texto de bienvenida completo, sin cortes), el menú mobile (blanco), los botones (azul oscuro con texto blanco).

## Paso 3 · Desactivar Blocks Animation (2 min) — UX-03/04/05
Plugins → **Blocks Animation** → Desactivar. El plugin ya neutraliza las animaciones, pero desactivar el plugin evita cargar su JavaScript. (Si en el futuro se quieren animaciones, que sean sutiles y respeten "reducir movimiento".)

## Paso 4 · Inicio: línea de tiempo (10 min) — UX-01/02/05, SEO-11
1. Páginas → Inicio → editar. Localizar el bloque **HTML personalizado** con la línea de tiempo (empieza con `<!DOCTYPE html>`), hacia el final, después de los artículos.
2. Borrar todo su contenido y pegar `contenido/etapa-1/bloques/inicio-linea-de-tiempo.html`.
3. Buscar en la página una **fila vacía** (bloque Fila sin contenido, `kb-row-layout-id1204_addcaa-c1`) y párrafos vacíos entre bloques: eliminarlos.
4. **Verificar:** en mobile, el sitio ya no tiene 40 px de margen a cada lado en la home, y la línea de tiempo se ve como lista vertical.

## Paso 5 · Servicios (10 min) — UX-08/09/10/12, A11Y-06
1. Páginas → Servicios → editar → menú ⋮ → **Editor de código**. La página es un único bloque HTML personalizado (con dos `<style>`).
2. Borrar todo y pegar `contenido/etapa-1/bloques/servicios.html`. Volver al editor visual y comprobar que es un bloque "HTML personalizado".
3. Panel lateral → **Ajustes de Kadence de la página** (icono K): Diseño del contenido = **Ancho completo (Fullwidth)**, Estilo del contenido = **Sin caja (Unboxed)**, Relleno vertical = **Desactivado**. (Igual que Inicio y Contacto.)
4. **Verificar:** las tarjetas de "Qué ocurre en cada etapa" tienen margen interno y el número queda dentro; el título "Mentorías y acompañamiento uno a uno" es H1; el botón final es blanco con texto azul marino.

## Paso 6 · Correcciones de texto y encabezados (60–90 min) — 64 errores, H1 únicos
Seguir `contenido/etapa-1/correcciones.md` página por página. Cada fila dice **dónde** (bloque o campo), **antes** y **después**.
- **Títulos de entradas (T01–T09):** cambiar solo el título, **no** el enlace permanente.
- **Encabezados (tipo "encabezado"):** seleccionar el bloque → barra de herramientas → nivel (H1, H2… o "P" en Advanced Heading).
- **Testimonios:** Páginas → Testimonios → ajustes de Kadence → **Mostrar título** (queda como H1 "Testimonios").
- **Categoría interina (K01):** "¿Por qué fallamos…" pasa de Ciberseguridad a Psicología.
- Quedan fuera, a propósito, las correcciones que necesitan a la autora o permiso (listadas al final de correcciones.md).

## Paso 7 · Formulario de contacto (15 min) — CRO-01/02/03, A11Y-09/10
Seguir `contenido/etapa-1/bloques/formulario-contacto.md`. Requiere la URL de la política de privacidad ([COMPLETAR]); si todavía no existe, crear la página "Política de privacidad" (Ajustes → Privacidad → generar página) y revisarla antes de enlazarla.

## Paso 8 · Rank Math (20 min) — GEO-04, SEO-05, SEO-08
1. Plugins → Añadir nuevo → **Rank Math SEO** → Instalar → Activar. Asistente: modo **Fácil**; conectar la cuenta es opcional (se puede omitir).
2. Rank Math → Panel → **Módulos**: activar solo *Redirecciones*, *Monitor 404* y *SEO local* desactivado. **Desactivar por ahora** *Schema* y *Mapa del sitio* (llegan en la Etapa 4, para no duplicar datos ni cambiar la URL del sitemap todavía) y *Análisis SEO / Content AI*.
3. Rank Math → Ajustes generales → **Editar robots.txt**: pegar `contenido/etapa-1/rank-math/robots.txt`. Si Rank Math avisa que existe un archivo físico, borrar `public_html/robots.txt` en el Administrador de archivos (hoy no existe: el actual es el virtual de WordPress).
4. Apariencia → Menús: el ítem **Blog** apunta hoy a `/entradas/`: cambiarlo a la página **Blog** (`/blog/`). Luego Páginas → Entradas → pasar a **Borrador**.
5. Rank Math → Redirecciones: crear las de `contenido/etapa-1/rank-math/redirecciones.md`.
6. **Autora (SEO-08, GEO-05):** Usuarios → admin → **Sitio web**: cambiar `https://codigocalma.com/codigocalma` (da 404) por `https://codigocalma.com/sobre_tatiana/`. Completar "Información biográfica" con la bio breve [COMPLETAR: bio validada por Tatiana]. (El usuario definitivo con nombre propio llega en la Etapa 4.)
7. **Verificar:** `https://codigocalma.com/robots.txt` muestra el nuevo contenido; `/entradas/` redirige a `/blog/`; la firma de la autora en un artículo ya no da 404.

## Paso 9 · Vaciar caché y comprobar
LiteSpeed Cache → **Purgar todo**; hPanel → CDN → **Purgar caché**. Revisar en el celular: Inicio, Servicios, Contacto, un artículo, Blog.

---

## Qué queda fuera de la Etapa 1 (a propósito)
- Header con CTA, footer completo, tipografía local, componentes: **Etapa 2**.
- Hero de inicio y servicios con CTA arriba, páginas de equipo, newsletter: **Etapa 3**.
- Metas, Open Graph, schema, sitemap, redirecciones de URLs, rendimiento de imágenes: **Etapa 4**.
- Taxonomía, "En resumen", fuentes, llms.txt, test accesible: **Etapa 5**.

## Deshacer
- Plugin: Plugins → **Código Calma** → Desactivar (el sitio vuelve a verse como antes).
- Bloques: cada página tiene **Revisiones** (panel lateral → Revisiones) para volver a la versión anterior.
- Rank Math: desactivar el plugin restaura el robots.txt virtual de WordPress.
