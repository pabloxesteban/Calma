# Vista previa de etapas

Reproduce cada etapa sobre el HTML real de producción, sin tocar WordPress.

```bash
python3 staging/preview/build.py etapa-1          # genera staging/preview/build/*.html
NODE_USE_ENV_PROXY=1 node staging/preview/capturas.js --preview docs/auditoria/capturas-despues-etapa-1
NODE_USE_ENV_PROXY=1 node staging/preview/capturas.js --live    /tmp/antes     # mismas métricas en producción
```

`build.py` aplica exactamente lo que se carga en el sitio:
1. CSS del plugin `wp-content/plugins/codigo-calma/assets/css/` (inyectado al final de `<head>`, como lo encola WordPress).
2. Bloques de `contenido/<etapa>/bloques/` (línea de tiempo del inicio, Servicios, formulario emulado).
3. `contenido/<etapa>/correcciones.json` (texto y niveles de encabezado).
4. Ajustes de página que se hacen en el editor (Servicios a ancho completo, título de Testimonios, H1 del blog) y los archivos que el plugin deja de cargar (Blocks Animation, Contact Form 7).

Límites: los assets (CSS de Kadence, imágenes, fuentes) vienen de producción en el momento de la captura; lo que depende de PHP (Rank Math, redirecciones) no se ve en la vista previa y se verifica en el sitio después de aplicar la guía.
