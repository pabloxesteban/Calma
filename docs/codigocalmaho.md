# codigocalmaho · Handoff del rediseño de codigocalma.com

Estado al 11 de octubre de 2026. Este documento resume dónde está el proyecto, qué falta y cómo seguir, para retomarlo en otra sesión o pasárselo a otra persona.

## 1. Qué es el proyecto
Rediseño completo de **codigocalma.com**, el portal de ciberpsicología de Tatiana X. Stacul (psicóloga, argentina, vive en Dinamarca), con Francisca Cortés Santoro (accesibilidad cognitiva) y Emanuel C. Franco (gestión de proyectos).

- **Objetivos:** sitio de referencia en español, buen SEO y GEO (visibilidad en IAs), más solicitudes de consulta y un diseño unificado que funcione bien en el celular.
- **Plataforma:** WordPress en Hostinger, tema Kadence, Kadence Blocks, Rank Math y caché LiteSpeed. El sitio está publicado y funcionando; el rediseño se aplica sobre ese WordPress, sin migrar nada.

## 2. Dónde está todo
| Qué | Dónde |
|---|---|
| Repositorio y rama | `pabloxesteban/Calma`, rama `claude/focused-babbage-403shx` |
| Vista previa (noindex, formularios desactivados) | https://pabloxesteban.github.io/Calma/vista-previa/ |
| Exploración de estilos (A, B y C) | https://pabloxesteban.github.io/Calma/exploracion/ |
| Plugin del sitio (versión 1.7.0-etapa7) | `wp-content/plugins/codigo-calma/` |
| Bloques HTML para pegar en WordPress | `contenido/etapa-7/bloques/` (se regeneran con `python3 contenido/etapa-7/generar-bloques.py`) |
| Guía de implementación paso a paso | `docs/implementacion/etapa-1.md` a `etapa-7.md` (la 7 tiene los pasos 3c a 3l) |
| Datos pendientes `[COMPLETAR]` | `docs/placeholders.md` |
| Informes de QA (accesibilidad, móvil) | `docs/auditoria/informes/qa-etapa-7.md` |
| Capturas | `docs/auditoria/capturas-despues-etapa-7/` y `docs/diseno/` |
| Dirección de arte | `docs/direccion-arte-organismo.md` |

## 3. Estado actual
**Rediseño terminado en todas las páginas**, publicado en la vista previa y revisado: axe-core da 0 violaciones en 14 páginas en 2 anchos, no hay desborde a 320 px y respeta "Reducir movimiento".

Páginas rediseñadas:
- Inicio
- Ciberpsicología (pilar)
- Bienestar digital
- Herramientas
- Test de consumo digital
- Descargas
- Servicios
- Contacto
- Equipo y los tres perfiles
- Testimonios
- Blog
- Artículos: tiempo de lectura, índice, "Sigue explorando" y mapa de temas

**Nada está aplicado todavía en el WordPress real.** El sitio publicado sigue igual hasta que Tatiana apruebe.

## 4. Decisiones de diseño tomadas (no reabrir sin motivo)
- **Patrón común (tomado del Test):**
  - cabecera con título grande a la izquierda y figura propia a la derecha, que se arma una vez al cargar;
  - títulos de sección a la izquierda, del mismo tamaño;
  - tarjetas blancas con borde fino y esquinas suaves, sin sombras;
  - figura animada arriba a la izquierda en cada tarjeta, etiqueta, título y texto;
  - una luz tenue que sigue al puntero.
- **Fondo "red clara":** papel `#faf8f4` con cuadrícula tenue. Nada oscuro.
- **Tonos por tema y persona:**

  | Tema | Persona | Tono |
  |---|---|---|
  | Psicología | Tatiana | arena |
  | IA | Francisca | lavanda |
  | Neurociencia | Emanuel | celeste |
  | Bienestar | — | verde |
  | Tecnología | — | terracota |

- **Movimiento:** cada animación pasa una vez (menos de 5 s), al entrar en pantalla o al pasar el puntero. No hay animaciones infinitas ni scroll secuestrado.
- **Inicio:**
  - "Lecturas recientes" queda con su diseño anterior (tarjetas con el tono de cada tema);
  - la flor con la red, la línea de tiempo, los seis momentos y el mapa quedan como estaban.
- **Personaje:** la chica con el teléfono, redibujada en SVG en `contenido/etapa-7/ilustraciones.py`.
  - En el Inicio: le llegan un corazón, un "me gusta" y un mensaje.
  - En Contacto: escribe y envía un avión de papel, y aparece el tilde de "enviado".
- **Test:** los emojis originales redibujados en línea fina (disquete, casete, nube, ✓ ⚠ 🔵 y los íconos de cada perfil).
- **Testimonios:** formato de reseña de Google con las 14 reseñas reales (`contenido/etapa-7/testimonios.json`). No se usa el logo de Google.
- **El mapa de temas y "Sigue explorando"** leen las entradas de WordPress en vivo. Lo que Tatiana publique aparece solo.

## 5. Reglas del proyecto
- **No inventar** testimonios, cifras, títulos, matrículas ni credenciales. Lo que falta va como `[COMPLETAR: …]` y se lista en `docs/placeholders.md`.
- **Contenido de salud mental:** tono cuidadoso, sin promesas de resultados y con fuentes confiables. Se mantiene el texto y la voz de los artículos; solo se corrigen errores.
- **Prioridad:** contenido > legibilidad > accesibilidad > rendimiento > interacción > espectáculo.
- **No publicar en producción.** Todo queda en la rama y en la vista previa (noindex) hasta que haya aprobación.

## 6. Pendiente
**De Tatiana y del equipo** (detalle en `docs/placeholders.md`):
- fotos, bios y formación de Tatiana, Francisca y Emanuel;
- matrícula o habilitación, y las modalidades reales (mentoría o psicoterapia);
- honorarios o la decisión de no publicarlos, y el área de servicio;
- líneas de ayuda por país (Argentina, España, Dinamarca…);
- política de privacidad: URL y texto (le aplica el RGPD porque trabaja desde la UE). Si usa analítica, también un aviso de cookies;
- fuente del 74 % y de los 6 mil millones del Inicio;
- nombres de las 4 dimensiones del test;
- revisión de los textos nuevos (pilar, descripciones de temas, resúmenes) y de las categorías y etiquetas del blog.

**Técnico, cuando apruebe** (guía en `docs/implementacion/`):
1. Copia de seguridad completa en Hostinger. Si se puede, aplicar primero en una copia de prueba (staging).
2. Subir el plugin `codigo-calma` 1.7.0.
3. Pegar los bloques de cada página siguiendo las etapas 1 a 7.
4. Ajustar el Personalizador de Kadence:
   - ocultar el título en las páginas que tienen su propio H1 (por ejemplo, Testimonios);
   - desactivar "Publicaciones relacionadas".
5. Importar la configuración de Rank Math y aplicar la taxonomía del blog (etapa 5).
6. Revisar que en `calma-etapa7.css` el id de la página del Test sea el correcto (`page-id-1941`).
7. Vaciar la caché de LiteSpeed y probar el formulario de contacto.

Tiempo estimado de implementación: entre una tarde y un día.

## 7. Cómo trabajar en el repo
```bash
python3 contenido/etapa-7/generar-bloques.py   # regenera los bloques HTML
python3 staging/preview/build.py               # arma la vista previa local (staging/preview/build/)
python3 staging/preview/exportar-pages.py      # exporta a vista-previa/ para GitHub Pages
```
- **QA móvil:** `NODE_USE_ENV_PROXY=1 node staging/preview/capturas.js --preview <salida> [páginas]`
- **QA accesibilidad:** `NODE_USE_ENV_PROXY=1 AXE_PATH=<axe.min.js> node docs/auditoria/scripts/a11y-qa-etapa.js --preview <salida.json>`
- **Navegador:** Chromium en `/opt/pw-browsers/chromium`.
- **Archivos principales:**
  - estilos: `assets/css/calma-etapa7.css`;
  - movimiento: `assets/js/calma-organismo.js`;
  - mapa con datos en vivo: `includes/mapa.php`.

## 8. Contexto comercial
- **Precio sugerido para Tatiana:** 700 a 900 USD (referencia: 800 USD), con la implementación incluida.
  - Presentarlo como descuento sobre un valor de 2.500 a 3.000 USD.
  - Pagos 50/50.
  - A cambio del descuento: permiso para usarlo en el portfolio y crédito en el pie del sitio.
  - Alternativa "Esencial" a 500 USD.
- **Mantenimiento:** 30 días de garantía y después un abono de 25 a 40 USD por mes; lo extra, 15 a 20 USD por hora. Si no quiere abono, por tarea.
- **Cobro:**
  - en USD, neto de comisiones (Wise, Payoneer o transferencia);
  - factura E por exportación de servicios (confirmar con un contador);
  - el hosting, el dominio y los plugins pagos siguen a nombre de ella.
- **Cuidado:** es la psicóloga del desarrollador. Acuerdo por escrito, pago en dinero (no en sesiones) y el sitio no se habla en sesión.
- Los montos son orientativos, no son datos de mercado verificados.

## 9. Próximos pasos posibles
1. Armar el presupuesto y el mensaje para Tatiana.
2. Cuando apruebe: implementar en staging, revisar con ella y pasar a producción.
3. Completar los placeholders a medida que lleguen los datos.
4. Aparte (otro proyecto): presupuesto de un sitio para una inmobiliaria en México, en USD. Falta saber si el cliente usa EasyBroker u otro sistema.
