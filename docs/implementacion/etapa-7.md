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
| **Línea de tiempo** | La figura de la izquierda es abstracta, con puntos como el resto del sitio, y cuenta cómo la tecnología fue conectando a las personas; cada punto es una persona. Se transforma con el scroll:<br>• 1975–1985: pocas tienen computadora.<br>• 1990–2000: muchas se conectan a través de unos pocos nodos (la Web).<br>• 2000–2010: todas llevan su dispositivo y están conectadas entre sí.<br>• 2010–2020: se agrupan alrededor de plataformas.<br>• Hoy: un sistema de IA en el centro, conectado con todas.<br>Arriba, el año de la época en grande; abajo, la aclaración "Figura ilustrativa: cada punto es una persona". | Mismo bloque del Paso 3b (`inicio-linea-de-tiempo.html`, regenerado) |
| **Accesos** (Aprender más / Solicitar una consulta / Recursos gratuitos) | Los personajes de las ilustraciones originales, redibujados en SVG por partes, llegan a su pose con el scroll:<br>• Aprender más: se sienta, escribe y las redes aparecen de a una.<br>• Solicitar una consulta: entra caminando, levanta el teléfono y aparece un mensaje escribiéndose.<br>• Recursos gratuitos: se deja caer en el sillón, abre el libro y cae el PDF.<br>Al llegar, parpadean y hacen su gesto. El botón queda debajo del dibujo, sin taparlo. | Reemplazar la fila de las 3 tarjetas (y la fila vacía) por un bloque **HTML personalizado** con `contenido/etapa-7/bloques/inicio-accesos.html` |
| **Lecturas recientes** | En el Inicio, las entradas van en una grilla "bento" con tamaños distintos:<br>• la primera, ancha, con la imagen al lado;<br>• la segunda, alta;<br>• las dos siguientes, compactas;<br>• las dos últimas, anchas.<br>Cada tarjeta tiene un tono suave según su categoría y un número de índice grande, y es clicable entera. La lectura de siempre se mantiene (imagen, categoría, título, resumen, "Leer más"). El bloque de entradas de Kadence no se toca: lo arma el CSS. La página del Blog mantiene sus tarjetas. | Agregar un bloque **HTML personalizado** con `contenido/etapa-7/bloques/inicio-lecturas-cabecera.html` justo encima del bloque de entradas del Inicio |

## Quinta ronda de ajustes
- **Sin rótulos grises.** Se quitaron los rótulos de sección ("Ciberpsicología · para todos los días", "Seis estados…", "Cinco épocas…", "Blog · lecturas recientes") y los "Fig. …" de los estados, la línea de tiempo y los accesos.
  - El rótulo del hero ("Portal de ciberpsicología") y los de Servicios y Equipo se ocultan por CSS; el texto sigue en el HTML por si se quieren recuperar.
- **Tarjetas que giran.** El texto "Dar vuelta y ver el hallazgo" pasa a ser un círculo con la flecha; al pasar el puntero aparece "Ver más". En celular, "Ver más" se ve siempre.
  - Dada vuelta, un clic en cualquier parte de la tarjeta la devuelve (salvo en el enlace de la fuente); el botón "Volver" sigue para el teclado.
  - El foco solo se mueve cuando se usa el teclado.
- **Flor.** Gira despacio con el scroll mientras el hero está en pantalla, y al pasar el puntero.
- **Red del hero.** Pasa a ser un circuito que continúa las pistas de los pétalos: rutas a 45° que terminan en nodos, sobre una retícula de puntos. La red no se deforma: lo que se mueve son las señales.
  - Al cargar, las pistas crecen desde la flor y algunas señales salen hacia afuera.
  - Al pasar sobre la flor, sale una señal por cada pista.
  - Al acercar el puntero a un nodo, la señal viaja del nodo a la flor, que se ilumina al recibirla.
  - Todo se detiene solo cuando no quedan señales en viaje.

Todo esto va en los mismos archivos (plugin y bloques regenerados); los pasos de aplicación no cambian.

## Sexta ronda de ajustes
- **Flor:** gira más lento con el scroll (unos 27° cada 600 px; antes eran 72°).
- **Tarjetas que giran:** una por vez. Al dar vuelta una, la que estaba girada vuelve a su estado original.
- **Línea de tiempo:** se quitó la frase "Figura ilustrativa: cada punto es una persona".
- **Accesos:**
  - El personaje está rediseñado como ilustración plana con volumen: el mismo cuerpo redondeado del original, con degradado de marca, ojos con brillo, mejillas y objetos de color. Las animaciones de llegada son las mismas.
  - Cada tarjeta es un enlace completo con título, una línea que dice adónde lleva y un botón con flecha:
    - "Aprende ciberpsicología" → página de Ciberpsicología;
    - "Solicita una consulta" → Contacto;
    - "Recursos gratuitos" → Descargas ("Libros y guías de Tatiana X. Stacul para descargar sin costo", según la página de Descargas).
  - Se reemplaza el mismo bloque: `inicio-accesos.html`, regenerado.

## Paso 3c · Mapa de temas y "Sigue explorando" (10 min)
El plugin 1.7.0 dibuja el mapa con `includes/mapa.php` a partir de `data/mapa-temas.json`.

1. **Inicio:** entre "¿Cómo son tus momentos con la tecnología?" y los accesos, agregar un bloque **Código corto** con `[calma_mapa]` (es lo que contiene `contenido/etapa-7/bloques/inicio-mapa.html`).
2. **Página pilar (Ciberpsicología):** al final de la sección «Los temas de la ciberpsicología en Código Calma», otro bloque **Código corto** con `[calma_mapa]`.
3. **Blog:** en la página del Blog, encima del listado de entradas, un bloque **Código corto** con `[calma_mapa]`. Si el Blog es el archivo de entradas de Kadence y no una página editable, usar la opción de Kadence para agregar contenido antes del archivo.
4. **Artículos:** no hay nada que hacer. Al final de cada entrada, después de las fuentes y antes de la caja de consulta, aparece solo **"Sigue explorando"**: el artículo en el centro y los 4 más conectados alrededor, con el motivo de cada conexión ("Comparten: hábitos, autoeficacia").

### De dónde sale la información
Todo sale de datos que ya estaban en el proyecto; no se agregó información nueva.

| Parte | Fuente |
|---|---|
| Qué artículos hay en cada tema | La categoría asignada a cada una de las 15 entradas en la reorganización del blog de la Etapa 5 (`contenido/etapa-5/taxonomia.json`, "asignacion"). |
| Por qué dos temas (o dos artículos) están conectados | Las etiquetas que comparten sus artículos, en ese mismo archivo. Por ejemplo, IA y Tecnología se unen porque tienen artículos etiquetados con "Ética digital", "Sesgos cognitivos", "Salud mental" e "Infancia y adolescencia". El grosor de la línea es la cantidad de etiquetas en común. |
| Artículos relacionados de "Sigue explorando" | Misma fórmula: 1 punto por etiqueta compartida + 2 si son de la misma categoría; se muestran los 4 con más puntos. |
| Descripción corta de cada tema | Resumen de la descripción de cada categoría escrita en la Etapa 5 (pendiente de revisión de Tatiana). La del centro es la definición de la página pilar (también pendiente). |
| Títulos de los artículos | Los títulos publicados, con las correcciones ortográficas de las etapas 1 a 5. |
| Los seis temas | Los que pediste en la dirección de arte (Psicología, Ciberpsicología, IA, Neurociencia, Bienestar digital, Tecnología), vinculados a las categorías del blog así: Psicología → Hábitos y conducta · Neurociencia → Neurociencia y atención · IA → IA y mente · Tecnología → Redes sociales y plataformas + Ciberseguridad y factor humano · Bienestar digital → Bienestar digital. |

**Importante:**
- **Se actualiza solo.** En el sitio real, el mapa y "Sigue explorando" leen los artículos publicados directamente de WordPress (título, categoría y etiquetas). Cuando Tatiana publica, edita o borra una entrada, o cambia una categoría o etiqueta, el mapa se recalcula en la siguiente visita (la caché interna se borra sola; como mucho dura 24 h). No hay que tocar código ni regenerar nada. Condición: que cada entrada nueva tenga una de las categorías del blog y 2–4 etiquetas; sin etiquetas aparece en su tema pero sin conexiones.
- `data/mapa-temas.json` queda solo para las descripciones de los temas y como respaldo si WordPress no devuelve entradas (por ejemplo, en la vista previa estática). Si se agrega una categoría nueva que no está entre las seis vinculadas, hay que sumarla en `contenido/etapa-7/mapa.py` y regenerar con `python3 contenido/etapa-7/generar-bloques.py`.
- Las etiquetas y categorías se asignaron en la Etapa 5 leyendo cada artículo, y también las tiene que revisar la autora.
- Los enlaces a las categorías nuevas funcionan después de aplicar la taxonomía (Etapa 5, Paso 2).

## Paso 3d · Servicios y Contacto (15 min)
Mismo texto que la Etapa 3; cambian la forma y el orden.

**Servicios**
1. Reemplazar el bloque **HTML personalizado** de Servicios por `contenido/etapa-7/bloques/servicios.html`.
2. Cambios que trae:
   - en el hero, la figura **"tu recorrido"** (Nos escribes → Primer encuentro → De 3 a 6 sesiones → Tu plan por escrito), que se dibuja al cargar;
   - "Qué pasa en cada etapa" con los pasos **unidos por una línea que crece con el scroll**; cada paso se enciende al llegar;
   - las tarjetas del equipo con el tono de cada área;
   - "Cuándo no es para ti" y el aviso de urgencias en tono arcilla suave;
   - preguntas frecuentes sin cajas;
   - el cierre en celeste suave, en lugar del bloque oscuro.
3. Estos estilos son de los componentes, así que también actualizan **Equipo** y las páginas de cada profesional sin editarlas.

**Contacto**
1. Reemplazar el bloque de intro de la Etapa 3 por `contenido/etapa-7/bloques/contacto-intro.html` (título y párrafo; los pasos se mudan).
2. En la columna derecha, borrar la ilustración y agregar un bloque **HTML personalizado** con `contenido/etapa-7/bloques/contacto-proceso.html`: "Qué pasa después de enviar" con los tres pasos conectados.
3. En la columna derecha, en **Visibilidad**, activar que se vea también en tablet y celular (hoy está oculta). En celular queda debajo del formulario.
4. El formulario no se toca: los estilos del plugin hacen los campos más grandes y claros, y convierten las áreas de consulta en opciones que se eligen tocando toda la fila.

## Paso 3e · Lectura de artículos (5 min)
Casi todo lo hace el plugin, sin editar los artículos:
- **Tiempo de lectura:** junto a la fecha ("4 min de lectura"). Se calcula con el texto real del artículo a 200 palabras por minuto.
- **"En resumen"** destacado arriba, en celeste suave, con la definición en itálica.
- **Índice del artículo** ("En este artículo"), armado con los subtítulos que ya tiene cada artículo (H2; si hay menos de 3, también los H3):
  - en pantallas anchas va al costado y acompaña la lectura: marca la sección actual y las ya leídas, y una línea se llena mientras se lee;
  - en celular y tablet es un botón que despliega la lista.
- **Tipografía de lectura:** texto más grande, interlineado cómodo, subtítulos separados con una línea fina, viñetas en verde azulado y citas en itálica.
- **Cierre ordenado:** compartir, "Sigue explorando", la caja de consulta en tono arena, las fuentes y la navegación anterior/siguiente sin sombras.

**Una sola cosa en WordPress:** Apariencia → Personalizar → Diseño de entradas → desactivar **"Publicaciones relacionadas"**. Las reemplaza "Sigue explorando" (el CSS ya las oculta, pero conviene apagarlas para no cargarlas).

Todo esto se aplica solo a los artículos nuevos que publique Tatiana.
