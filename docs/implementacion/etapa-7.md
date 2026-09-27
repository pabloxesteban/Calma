# Etapa 7 — Organismo digital (fase 1 + tarjetas): guía de aplicación

Dirección de arte: `docs/direccion-arte-organismo.md`. Esta etapa reemplaza la capa de movimiento de la Etapa 6.
Requisito: Etapas 1–5 aplicadas. Tiempo estimado: 30 minutos. Hacer una copia de seguridad antes.

| Pieza | Ruta en el repo |
|---|---|
| Plugin 1.6.0 (CSS `calma-etapa7.css` + JS `calma-organismo.js`) | `wp-content/plugins/codigo-calma/` |
| Bienvenida con cifras | `contenido/etapa-7/bloques/inicio-bienvenida.html` |
| Línea de tiempo | `contenido/etapa-7/bloques/inicio-linea-de-tiempo.html` |
| Bloque de los seis estados | `contenido/etapa-7/bloques/inicio-momentos.html` |
| Generador de los tres bloques | `contenido/etapa-7/generar-bloques.py` |

## Qué cambia
- **Paleta y tipografía.** Fondo de papel cálido, texto en tinta azulada y verde azulado para los datos. El violeta queda solo en las etiquetas de categoría. Los acentos de los títulos van en itálica de Lora (reemplaza al degradado) y los rótulos científicos en monoespaciada.
- **Hero.** La flor queda dentro de una red viva y suelta que ocupa todo su sector:
  - los nodos (de tamaños y brillos distintos, con uniones curvas e irregulares) aparecen uno a uno y se conectan;
  - la red respira unos segundos y queda quieta;
  - el puntero, el dedo o el foco del teclado la perturban, los nodos se activan y la red vuelve sola al equilibrio;
  - al pasar sobre la flor, esta gira despacio, se ilumina y emite una onda que recorre la red.
  - No hace falta tocar el bloque del hero: el canvas lo agrega el JS.
- **Bienvenida.** El texto y las cifras van juntos en una columna y la ilustración al lado, sin la caja alta que dejaba espacio vacío. Las cifras llevan su figura: una rejilla de 100 puntos (74 encendidos) y una red de conexiones que se dibujan al entrar en pantalla. Los números y el texto no cambian.
- **Línea de tiempo.** Una línea que crece con el scroll (siempre nativo) y épocas que se encienden cuando la línea las alcanza. En escritorio, una figura fija a un costado se transforma con el scroll: objeto → red → dispositivo → plataforma → inteligencia. Mismo texto de la Etapa 1.
- **"¿Cómo son tus momentos con la tecnología?"** Las 6 tarjetas giratorias pasan a ser seis estados mentales:
  - cada estado tiene un micro-organismo animado (pulsación, agrupamiento, división, flujo sin destino, interferencia, baja frecuencia);
  - el hallazgo y la fuente se abren con un botón accesible;
  - los textos, los hallazgos y las fuentes son los mismos que hoy.
- **Tarjetas del blog.** Más chicas y editoriales: sin sombra, sin bordes redondeados y sin caja; una línea de tinta sobre el texto, la categoría como rótulo y el resumen en 3 líneas.
  - Al pasar el puntero, la imagen se desplaza, aparece una textura y una línea conecta el título con la lectura.
  - Las imágenes que están fuera de la primera pantalla se descubren como una lámina al llegar.
- **Cuadros de acceso** (Aprender más / Consulta / Recursos): planos, sin redondeo; al pasar, el borde se oscurece y la ilustración se desplaza apenas.
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

## Paso 3 · Inicio: bienvenida (5 min)
1. Seleccionar la fila completa «Te damos la bienvenida a Código Calma»: título, texto, ilustración y las dos cajas de cifras.
2. Reemplazarla por un bloque **HTML personalizado** a ancho completo con `contenido/etapa-7/bloques/inicio-bienvenida.html`.
3. El bloque muestra un placeholder visible para la **fuente de las cifras**, que sigue pendiente (`docs/placeholders.md`).

## Paso 3b · Inicio: línea de tiempo (3 min)
Reemplazar el bloque **HTML personalizado** de la línea de tiempo (el de la Etapa 1) por `contenido/etapa-7/bloques/inicio-linea-de-tiempo.html`.

## Paso 4 · Comprobar (10 min)
- Inicio en escritorio: la red aparece, respira unos 4 s y queda quieta; el mouse la perturba y vuelve; sobre la flor, la flor gira y sale una onda.
- Línea de tiempo: al bajar, la línea crece, las épocas se encienden y la figura se transforma; al subir, vuelve.
- Celular: la red es más liviana y responde al toque; el scroll no se bloquea.
- "Ver el hallazgo" abre y cierra con teclado (Tab + Enter) y el lector de pantalla anuncia "expandido/contraído".
- Activar "Reducir movimiento" en el pie: nada se mueve y la preferencia se mantiene al recargar.
- Purgar la caché (LiteSpeed y CDN de Hostinger).

Si hay que editar un texto de la bienvenida, la línea de tiempo, los estados o las cifras, cambiarlo en `contenido/etapa-7/generar-bloques.py` y ejecutar `python3 contenido/etapa-7/generar-bloques.py`.

## Tercera ronda de ajustes
| Pieza | Qué cambia | Cómo se aplica |
|---|---|---|
| **Seis estados** | Vuelven a ser tarjetas que se dan vuelta, como en el diseño original. Toda la tarjeta es clicable y el botón "Dar vuelta y ver el hallazgo" es el control accesible. Al llegar a la sección, cada tarjeta se "asoma" una vez para mostrar que se puede girar, y al pasar el puntero se inclina. El dorso va en tinta oscura con el hallazgo y la fuente, y "Volver a la pregunta" (o Escape) la devuelve. | Mismo bloque del Paso 2 (`inicio-momentos.html`, regenerado) |
| **Línea de tiempo** | La figura de la izquierda cuenta una idea: "cada vez más cerca". Una persona de perfil y, en cada época, la tecnología dibujándose más cerca de su cabeza: la computadora en el escritorio, un globo conectado, el teléfono junto a la cara, plataformas alrededor y, al final, una red dentro de la cabeza. Arriba, el año de la época en grande. | Mismo bloque del Paso 3b (`inicio-linea-de-tiempo.html`, regenerado) |
| **Accesos** (Aprender más / Solicitar una consulta / Recursos gratuitos) | Los personajes de las ilustraciones originales, redibujados en SVG por partes, llegan a su pose con el scroll:<br>• Aprender más: se sienta, escribe y las redes aparecen de a una.<br>• Solicitar una consulta: entra caminando, levanta el teléfono y aparece un mensaje escribiéndose.<br>• Recursos gratuitos: se deja caer en el sillón, abre el libro y cae el PDF.<br>Al llegar, parpadean y hacen su gesto. El botón queda debajo del dibujo, sin taparlo. | Reemplazar la fila de las 3 tarjetas (y la fila vacía) por un bloque **HTML personalizado** con `contenido/etapa-7/bloques/inicio-accesos.html` |
| **Lecturas recientes** | En el Inicio, las entradas dejan de verse como blog: son un índice editorial.<br>• La primera va destacada, grande.<br>• El resto van en filas numeradas (categoría · título · fecha · flecha); en escritorio la imagen aparece al pasar sobre la fila y en celular queda como miniatura.<br>El bloque de entradas de Kadence no se toca: lo arma el CSS. La página del Blog mantiene las tarjetas. | Agregar un bloque **HTML personalizado** con `contenido/etapa-7/bloques/inicio-lecturas-cabecera.html` justo encima del bloque de entradas del Inicio |
