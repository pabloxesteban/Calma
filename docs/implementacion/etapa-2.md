# Etapa 2 — Design system unificado + test accesible: guía de aplicación

Requisito: Etapa 1 aplicada. Tiempo estimado: 1,5–2 horas. Hacer copia de seguridad antes (hPanel → Copias de seguridad).

| Pieza | Ruta en el repo |
|---|---|
| Plugin actualizado (v1.1.0) | `wp-content/plugins/codigo-calma/` (nuevo: `assets/fonts/`, `calma-fonts.css`, `calma-etapa2.css`) |
| Pie de página | `contenido/etapa-2/footer/pie-widget.html` |
| Herramientas | `contenido/etapa-2/bloques/herramientas-habitos.html` |
| Test de consumo digital | `contenido/etapa-2/bloques/test-consumo-digital.html` + `.md` |
| Encabezados | `contenido/etapa-2/correcciones.md` |

## Paso 1 · Actualizar el plugin (5 min)
Plugins → Añadir nuevo → Subir plugin → `codigo-calma.zip` (nueva versión) → **Reemplazar la actual con la subida**.
Qué agrega:
- **Tipografía:** Lora para títulos e Inter para texto, alojadas en el sitio (sin Google Fonts). Se deja de cargar Jost, Sora y Playfair; cuerpo de 17–18 px con interlineado 1,65; escala de títulos única.
- **Header:** blanco con borde, logo de 48 px (baja la versión de 150 px en lugar de la de 512 px), navegación con estado activo subrayado.
- **Componentes:** botones en píldora de 48 px, tarjetas de artículos (imagen 16:9, badge de categoría con un color por categoría, resumen de 4 líneas, "Leer más" de 44 px), metadatos con "Publicado"/"Actualizado", lectura de artículos a 68 caracteres por línea, enlaces subrayados, lavanda más suave en las secciones.
- **Footer:** estilos del pie en 4 columnas (el contenido se pega en el paso 3).

## Paso 2 · Personalizador de Kadence (20 min)
Apariencia → Personalizar:
1. **Tipografía:** Cuerpo = "Inherit" o fuente del sistema; Títulos = "Inherit". (El plugin ya define Inter y Lora; así Kadence no vuelve a pedir Google Fonts. Si existe la opción "Cargar Google Fonts localmente", dejarla desactivada.)
2. **Encabezado → Constructor:** en la fila principal, a la derecha, agregar el elemento **Botón**: texto "Solicitar una consulta", enlace `/contacto/`, estilo relleno, tamaño mediano.
3. **Encabezado → Mobile / Drawer:** agregar el elemento **Botón** debajo de la navegación mobile: mismo texto y enlace.
4. **Logo:** ancho 48 px (escritorio y mobile).

## Paso 3 · Menús y widgets (15 min)
1. Apariencia → Menús → **Crear menú** "Menú mobile" con este orden, sin submenús: Inicio, Ciberpsicología, Bienestar digital, Blog, Herramientas, Test de consumo digital, Descargas, Servicios, Sobre Tatiana, Contacto. Ubicación: **Navegación mobile**. (El menú principal de escritorio no cambia.)
2. Apariencia → Widgets → **Footer 1**: agregar un bloque "HTML personalizado" y pegar `contenido/etapa-2/footer/pie-widget.html`.
3. Personalizar → **Pie de página → Constructor**: fila central con 1 columna y el elemento "Footer 1". Quitar de la fila superior el ícono social y el HTML "© 2026 Código Calma" (quedan dentro del nuevo pie).
4. Completar los dos placeholders del pie cuando existan: URL de la política de privacidad y enlace a líneas de ayuda.

## Paso 4 · Herramientas (10 min)
Páginas → Herramientas → editar. Localizar el bloque **HTML personalizado** que empieza con el comentario "BLOQUE WORDPRESS — Herramientas de calma v3" (tarjetas en carrusel) y reemplazar todo su contenido por `contenido/etapa-2/bloques/herramientas-habitos.html`. Después aplicar `contenido/etapa-2/correcciones.md` (niveles de encabezado de las apps).

## Paso 5 · Test de consumo digital accesible (15 min)
Seguir `contenido/etapa-2/bloques/test-consumo-digital.md`: reemplaza el bloque HTML personalizado del test (estilos, pantallas y script) por la versión accesible. Probar completo con teclado (Tab, flechas, Espacio, Enter) y en el celular.

## Paso 6 · Purgar caché y comprobar
LiteSpeed Cache → Purgar todo; hPanel → CDN → Purgar. Revisar: Inicio, un artículo, Blog, Servicios, Herramientas, Test (hasta el resultado), menú mobile y pie.

## Deshacer
Plugins → subir la versión anterior de `codigo-calma` (Etapa 1); Revisiones de cada página para los bloques; Personalizador → quitar el botón y el widget del pie.
