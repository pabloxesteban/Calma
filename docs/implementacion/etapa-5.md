# Etapa 5 — GEO y reestructuración del blog: guía de aplicación

Requisito: Etapas 1–4 aplicadas. Tiempo estimado: 1,5 horas + la revisión de Tatiana (es la condición para publicar: todo el texto nuevo está marcado como pendiente de su revisión). Copia de seguridad antes.

| Pieza | Ruta en el repo |
|---|---|
| Plugin 1.4.0 (llms.txt, En resumen, Fuentes, importadores) | `wp-content/plugins/codigo-calma/` |
| Estructura de los 15 artículos | `contenido/etapa-5/articulos.json` (copia en `plugin/data/`) |
| Taxonomía y 16 redirecciones | `contenido/etapa-5/taxonomia.json` (copia en `plugin/data/`) |
| Página pilar ¿Qué es la ciberpsicología? | `contenido/etapa-5/bloques/ciberpsicologia.html` (fuente: `pilar-ciberpsicologia.md`) |
| Apertura de Bienestar digital | `contenido/etapa-5/bloques/bienestar-digital-apertura.html` |
| Pendientes para la autora (43) | `contenido/etapa-5/pendientes-autora.md` |
| Calendario editorial oct–dic 2026 | `contenido/etapa-5/calendario-editorial.md` |

Todo lo que hace el plugin se probó en el WordPress local con Kadence y Rank Math (ver `docs/auditoria/informes/qa-etapa-5.md`).

## Paso 0 · Revisión de Tatiana (antes de todo)
1. `contenido/etapa-5/pendientes-autora.md`: resúmenes, definiciones adaptadas, fuentes verificadas (confirmar que son las que usó), cifras sin fuente y erratas.
2. `contenido/etapa-5/pilar-ciberpsicologia.md` y `bienestar-digital-apertura.md`.
3. Descripciones de las 6 categorías en `taxonomia.json` (campo `validacion`).
Si cambia algún texto, editar el JSON o el Markdown y volver a generar: `python3 contenido/etapa-5/generar-bloques.py`.

## Paso 1 · Plugin 1.4.0 (5 min)
Subir y reemplazar. Agrega:
- **`/llms.txt`** generado del contenido publicado. Tiene equipo, servicios, guías, temas y artículos con su resumen, y se regenera al guardar. Comprobar `https://codigocalma.com/llms.txt`.
  - Si Rank Math u otro plugin ya sirve un `llms.txt`, desactivar esa opción.
  - Si responde 404, ir a Ajustes → Enlaces permanentes → Guardar.
- **"En resumen"** al inicio de cada entrada y **"Fuentes"** al final, desde campos de la entrada. Se reflejan en el JSON-LD como `abstract` y `citation`.
- **Página pilar:** Article + FAQPage generados desde su contenido. Solo entran las preguntas sin placeholders.
- **Herramientas → Código Calma: blog:** vista previa y botones para aplicar la taxonomía y la estructura de los artículos.

## Paso 2 · Taxonomía (10 min)
Herramientas → **Código Calma: blog** → "Taxonomía y redirecciones":
1. Revisar la tabla (crear/actualizar 6 categorías, 15 etiquetas, asignar 15 entradas, eliminar 3 categorías y 13 etiquetas, 16 redirecciones).
2. **Aplicar**. Con Rank Math → Redirecciones activo, las 301 se crean solas; si alguna fila dice "ERROR", crearla a mano con la tabla de `taxonomia.json`.
3. Resultado: cada entrada queda con **una** categoría; `/category/ciberpsicologia/` y `/tag/ciberpsicologia/` → página pilar; categorías y etiquetas viejas → sus equivalentes. La caja de consulta de cada artículo usa el área de su categoría nueva (campo `area_cta`).
4. Equivalente por consola: `wp calma taxonomia --dry-run` y luego `wp calma taxonomia`.

## Paso 3 · Estructura de los artículos (5 min)
Misma pantalla → "Resúmenes, fuentes y encabezados" → revisar (15 entradas, fuentes verificadas por entrada, encabezados a subir) → **Aplicar**.
- Carga los resúmenes, las 8 definiciones adaptadas y las **10 fuentes verificadas**. Las 3 "[verificar]" no se publican.
- En los 7 artículos sin H2, sube a H2 los encabezados de sección, sin cambiar su texto. Cada entrada guarda una revisión para deshacer.
- Equivalente: `wp calma geo-import --dry-run` / `wp calma geo-import`.

## Paso 4 · Página pilar (10 min)
Páginas → Ciberpsicología → Editor de código → reemplazar todo por `contenido/etapa-5/bloques/ciberpsicologia.html`.
- Ajustes de Kadence: ancho completo, sin caja, **título oculto** (el H1 está en el bloque).
- En Rank Math, el título sugerido es «¿Qué es la ciberpsicología? Definición, áreas y ejemplos | Código Calma».

## Paso 5 · Bienestar digital (5 min)
Páginas → Bienestar digital: justo debajo del H1, reemplazar los párrafos «El bienestar digital emerge cuando…» y «Es usar los dispositivos con intención…» por un bloque HTML personalizado con `bienestar-digital-apertura.html`.

## Paso 6 · Caja de autora (5 min)
Personalizar → Entradas → **Caja de autora**: activada (usa la biografía de la usuaria "Tatiana X. Stacul", Etapa 4).

## Paso 7 · Comprobar (10 min)
- Un artículo:
  - "En resumen" arriba y H2 en las secciones;
  - "Fuentes" con enlaces DOI al final;
  - caja de consulta y caja de autora.
- `/category/psicologia/` → 301 a `/category/habitos-y-conducta/`.
- `/llms.txt` muestra los resúmenes.
- Validar la pilar y un artículo en validator.schema.org.
- Purgar caché.

## Paso 8 · Seguimiento GEO (mensual)
1. Probar en ChatGPT (con búsqueda), Perplexity, Gemini y Claude: «¿Qué es la ciberpsicología?», «¿qué es la autoeficacia?», «¿cómo gestionar el tecnoestrés?», «¿importan más las horas de pantalla o el tipo de uso?». Anotar si citan codigocalma.com.
2. Revisar en los logs de Hostinger que los bots de IA reciben 200 (el firewall de la Etapa 1).
3. Publicar según `calendario-editorial.md` (un artículo por semana con resumen, definición, fuentes y caja de consulta desde el primer día).
