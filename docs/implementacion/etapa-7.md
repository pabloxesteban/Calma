# Etapa 7 — Organismo digital (fase 1 + tarjetas): guía de aplicación

Dirección de arte: `docs/direccion-arte-organismo.md`. Esta etapa reemplaza la capa de movimiento de la Etapa 6.
Requisito: Etapas 1–5 aplicadas. Tiempo estimado: 30 minutos. Hacer una copia de seguridad antes.

| Pieza | Ruta en el repo |
|---|---|
| Plugin 1.6.0 (CSS `calma-etapa7.css` + JS `calma-organismo.js`) | `wp-content/plugins/codigo-calma/` |
| Bloque de los seis estados | `contenido/etapa-7/bloques/inicio-momentos.html` |
| Bloque de las cifras | `contenido/etapa-7/bloques/inicio-cifras.html` |
| Generador de ambos bloques | `contenido/etapa-7/generar-bloques.py` |

## Qué cambia
- **Paleta y tipografía.** Fondo de papel cálido, texto en tinta azulada y verde azulado para los datos. El violeta queda solo en las etiquetas de categoría. Los acentos de los títulos van en itálica de Lora (reemplaza al degradado) y los rótulos científicos en monoespaciada.
- **Hero.** La flor queda en el centro de una red viva:
  - la red nace de la flor, se asienta y queda quieta;
  - el puntero, el dedo o el foco del teclado la perturban, los nodos se activan y la red vuelve sola al equilibrio.
  - No hace falta tocar el bloque del hero: el canvas lo agrega el JS.
- **Cifras.** Una rejilla de 100 puntos (74 encendidos) y una red de conexiones que se dibujan al entrar en pantalla. Los números y el texto no cambian.
- **"¿Cómo son tus momentos con la tecnología?"** Las 6 tarjetas giratorias pasan a ser seis estados mentales:
  - cada estado tiene un micro-organismo animado (pulsación, agrupamiento, división, flujo sin destino, interferencia, baja frecuencia);
  - el hallazgo y la fuente se abren con un botón accesible;
  - los textos, los hallazgos y las fuentes son los mismos que hoy.
- **Tarjetas del blog.** Al pasar el puntero:
  - la tarjeta gana profundidad y se inclina como máximo 1,5°;
  - la imagen se desplaza, aparece una textura y una línea conecta el título con la lectura.
  - Además, las imágenes que están fuera de la primera pantalla se descubren como una lámina al llegar.
- **Cuadros de acceso** (Aprender más / Consulta / Recursos): la tarjeta gana profundidad y la ilustración se desplaza apenas.
- **Se retiran**:
  - las entradas desde abajo;
  - el brillo y el salto de los botones;
  - el header de vidrio;
  - los halos que seguían al mouse;
  - el conteo de cifras.
- **Control "Reducir movimiento"** en el pie. Se recuerda en el navegador de cada visitante. No aparece si el sistema ya pide menos movimiento, porque en ese caso el sitio ya está quieto.

## Paso 1 · Plugin 1.6.0 (5 min)
Subir y reemplazar la carpeta del plugin. Ya no carga `calma-etapa6.css` ni `calma-motion.js` (se borraron del plugin).

## Paso 2 · Inicio: seis estados (10 min)
1. Páginas → Inicio → seleccionar la fila con el título «¿Cómo son tus momentos con la tecnología?». Es la fila completa: título, texto de ayuda y las 6 tarjetas de ZoloBlocks.
2. Reemplazarla por un bloque **HTML personalizado** a ancho completo con el contenido de `contenido/etapa-7/bloques/inicio-momentos.html`.
3. Borrar la **fila vacía** que queda debajo de las 3 tarjetas de acceso.

## Paso 3 · Inicio: cifras (5 min)
1. En la fila «Te damos la bienvenida», columna derecha, borrar las dos **cajas de información** (+74 % y +6 mil millones).
2. En su lugar, agregar un bloque **HTML personalizado** con `contenido/etapa-7/bloques/inicio-cifras.html`.
3. El bloque muestra un placeholder visible para la **fuente de las cifras**, que sigue pendiente (`docs/placeholders.md`).

## Paso 4 · Comprobar (10 min)
- Inicio en escritorio: la red se asienta en unos 3 s y queda quieta; al pasar el mouse cerca de la flor se perturba y vuelve.
- Celular: la red es más liviana y responde al toque; el scroll no se bloquea.
- "Ver el hallazgo" abre y cierra con teclado (Tab + Enter) y el lector de pantalla anuncia "expandido/contraído".
- Activar "Reducir movimiento" en el pie: nada se mueve y la preferencia se mantiene al recargar.
- Purgar la caché (LiteSpeed y CDN de Hostinger).

Si hay que editar un texto de los estados o las cifras, cambiarlo en `contenido/etapa-7/generar-bloques.py` y ejecutar `python3 contenido/etapa-7/generar-bloques.py`.
