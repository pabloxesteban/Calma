# Etapa 3 — Servicios y flujo de consulta: guía de aplicación

Requisito: Etapas 1 y 2 aplicadas. Tiempo estimado: 2 horas. **Antes de publicar, Tatiana, Francisca y Emanuel revisan los textos** (`contenido/etapa-3/copy.md`): todo el copy está marcado como pendiente de revisión humana. Copia de seguridad antes de empezar.

| Pieza | Ruta en el repo |
|---|---|
| Plugin 1.2.0 (caja de consulta, newsletter, área preseleccionada, evento de conversión) | `wp-content/plugins/codigo-calma/` |
| Servicios | `contenido/etapa-3/bloques/servicios.html` |
| Hero del inicio | `contenido/etapa-3/bloques/inicio-hero.html` |
| Contacto (intro + qué pasa después) | `contenido/etapa-3/bloques/contacto-intro.html` |
| Equipo (índice + 3 personas) | `contenido/etapa-3/bloques/equipo*.html` |
| Caja por entrada | `contenido/etapa-3/cta-por-entrada.json` |
| Textos (fuente) | `contenido/etapa-3/copy.md` |

## Paso 1 · Actualizar el plugin a 1.2.0 (5 min)
Subir `codigo-calma.zip` y reemplazar. Qué agrega:
- **Caja de consulta al final de cada entrada**, con la profesional según la categoría (Tatiana en hábitos y conducta; equipo en ciberseguridad) y aviso breve de urgencias en las de salud mental.
- **Preselección del área:** `/contacto/?area=habitos | accesibilidad | proyectos | no-se` marca la opción del formulario.
- **Evento `generate_lead`** en `dataLayer`/`gtag` al enviar un formulario de Kadence (se aprovecha cuando se instale la analítica, Etapa 4).
- **Newsletter:** `[calma_newsletter]` y bloque bajo la caja de cada entrada, **solo** cuando se configure un formulario (paso 7).
- **Ajustes → Lectura → "Código Calma · Consultas y newsletter":** ID del formulario de newsletter, título, texto y URL de líneas de ayuda (cuando exista, el aviso de urgencias enlaza ahí en lugar del placeholder).

## Paso 2 · Caja por entrada (5 min)
En "¿Por qué fallamos al intentar cambiar conductas?" → Opciones de pantalla → Campos personalizados → nombre `calma_cta_area`, valor `proyectos` (el tema es la gestión de procesos → Emanuel). En "Cómo un «te quiero» infectó…" → `calma_cta_area` = `equipo`. Para quitar la caja de una entrada: `ninguna`.

## Paso 3 · Servicios (10 min)
Páginas → Servicios → Editor de código → reemplazar TODO por `contenido/etapa-3/bloques/servicios.html` (sigue en ancho completo, sin caja). Verificar: el botón "Solicitar una consulta" está en la primera pantalla del celular; los tres "Consultar con…" abren Contacto con el área marcada; las preguntas frecuentes se abren con teclado (Enter/Espacio).

## Paso 4 · Inicio (10 min)
1. Páginas → Inicio → seleccionar la **primera fila** (fondo degradado con "PORTAL DE CIBERPSICOLOGÍA" y la flor) → eliminarla → en su lugar, bloque **HTML personalizado** con `contenido/etapa-3/bloques/inicio-hero.html` (ancho completo).
2. En la sección siguiente, "Te damos la bienvenida a Código Calma": nivel **H1 → H2** (el H1 ahora es el del hero). Ver `contenido/etapa-3/correcciones.json` (I20).

## Paso 5 · Contacto (15 min)
1. Páginas → Contacto: borrar el título, el párrafo "Para ofrecerte…", las 3 viñetas y el párrafo en cursiva que están **encima** del formulario, y poner en su lugar un bloque HTML personalizado con `contenido/etapa-3/bloques/contacto-intro.html`.
2. Formulario (Kadence Forms → formulario 2625): agregar un campo **Radio** entre el correo y el mensaje:
   - Etiqueta "¿Sobre qué quieres consultar?", no obligatorio, ayuda "Si no lo tienes claro, elige «Todavía no lo sé». Lo vemos juntos."
   - Opciones (etiqueta → valor): Hábitos digitales y comportamiento → `habitos` · Accesibilidad cognitiva → `accesibilidad` · Gestión de proyectos → `proyectos` · Todavía no lo sé → `no-se`.
3. Verificar: abrir `/contacto/?area=proyectos` → "Gestión de proyectos" aparece marcada.

## Paso 6 · Equipo (25 min)
1. Páginas → Añadir: **Equipo** (slug `equipo`) con `equipo.html`.
2. Tres páginas hijas de Equipo: **Tatiana X. Stacul** (slug `tatiana-x-stacul`), **Francisca Cortés Santoro** (`francisca-cortes-santoro`), **Emanuel C. Franco** (`emanuel-c-franco`), cada una con su `equipo-<slug>.html`.
3. En las 4: ajustes de Kadence → ancho completo, sin caja, **título oculto** (el H1 está en el bloque).
4. Cuando lleguen las fotos: en cada bloque, reemplazar `<span class="calma-avatar …">XX</span>` por `<img class="calma-avatar calma-avatar--lg" src="…webp" width="144" height="144" alt="Retrato de …">` y borrar la línea del placeholder de foto.
5. Menús (principal y mobile): "Sobre Tatiana" → **Equipo** (`/equipo/`). El pie ya enlaza a `/equipo/` (widget actualizado en `contenido/etapa-2/footer/pie-widget.html`: volver a pegarlo).
6. Rank Math → Redirecciones: `sobre_tatiana` → `https://codigocalma.com/equipo/tatiana-x-stacul/` (301). Luego pasar la página "Sobre Tatiana" a **borrador**.

## Paso 7 · Newsletter (cuando haya proveedor)
1. Elegir proveedor (MailerLite, FluentCRM o GetResponse: Kadence ya tiene integración) y activar **doble opt-in**.
2. Kadence Forms → nuevo formulario "Newsletter": campo Email (etiqueta visible "Tu correo electrónico"), casilla Accept obligatoria con la política de privacidad, botón "Quiero recibirla", acción → el proveedor elegido. Mensajes: `contenido/etapa-3/copy.md` §6.
3. Ajustes → Lectura → "ID del formulario de newsletter": el ID del formulario (número en la URL al editarlo). Título: «Una reflexión breve sobre bienestar digital, cada [frecuencia]».
4. Opcional: `[calma_newsletter]` en Descargas y debajo del resultado del test.

## Paso 8 · Purgar caché y comprobar
Inicio (hero con CTA), Servicios (FAQ con teclado), Contacto con `?area=`, las 4 páginas de equipo, 2 artículos (caja al final), `/sobre_tatiana/` redirige.
