# Etapa 6 — Modernización: movimiento y microinteracciones

Pedido: una web más moderna, con movimiento, que no se parezca a otras webs de plantilla. Se resuelve en el plugin (1.5.0), sin tocar contenido, salvo el acento en degradado de tres titulares (Inicio, Servicios, Equipo), que ya viene en los bloques de la Etapa 3.

## Qué agrega (`calma-etapa6.css` + `calma-motion.js`)
- **Titulares de impacto:** hero más grande y ajustado; "la tecnología" y "Código Calma" en degradado de marca (azul → violeta → verde azulado); eyebrows con línea en degradado.
- **Hero vivo:** fondo de degradados suaves que se desplazan con el puntero y el scroll; la flor entra con un giro suave y sigue levemente al puntero.
- **Header translúcido** (desenfoque tipo vidrio) que se compacta al bajar.
- **Entradas al hacer scroll:** secciones, tarjetas, pasos, testimonios, preguntas, línea de tiempo (sus puntos aparecen en secuencia) y pie aparecen con un fundido y desplazamiento corto, escalonados.
- **Tarjetas:** se elevan al pasar el cursor, con un brillo que sigue al puntero; las imágenes del blog hacen un zoom suave.
- **Botones:** degradado que se desplaza, brillo que cruza y leve elevación; flechas que avanzan en "Leer más" y enlaces de acción.
- **Cifras que se cuentan** al aparecer (+74 %, +6 mil millones).
- **Barra de progreso de lectura** en los artículos.
- CTA navy y pie con halo de color; números de pasos y aros de avatar en degradado; subrayados animados.

## Criterios (se mantienen los de las etapas anteriores)
- **Sin contenido oculto sin JavaScript** y nada de la primera pantalla se oculta (el H1 y el texto del hero aparecen al instante: no empeora el LCP).
- **Sin animaciones en bucle infinito** (WCAG 2.2.2): todo es entrada corta (≤ 0,8 s) o responde al scroll y al puntero.
- **`prefers-reduced-motion: reduce`** apaga entradas, parallax, brillos y elevaciones.
- axe-core con las animaciones activas: **0 violaciones** (Inicio, Servicios, un artículo; 390 y 1280 px).

## Aplicar
Actualizar el plugin a 1.5.0 (subir y reemplazar). Si ya se aplicó la Etapa 3, volver a pegar los hero de Inicio, Servicios y Equipo desde `contenido/etapa-3/bloques/` (incluyen el acento en degradado). Purgar caché.

## Vista previa en línea
`https://pabloxesteban.github.io/Calma/` (generada con `python3 staging/preview/exportar-pages.py`): sitio estático con todas las etapas, marcado "vista previa", `noindex` y formularios desactivados. Las imágenes y el CSS de Kadence se cargan desde codigocalma.com.
