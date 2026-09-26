# Auditoría de estrategia de contenidos — codigocalma.com

Fecha: 2026-09-26 · Fuente: `docs/auditoria/snapshot-2026-09-26/` (txt/, html/, api/) · Alcance: taxonomía, clusters, E-E-A-T y plan editorial. No se modificó nada del sitio ni de otros archivos del repositorio.

## 1. Resumen

- **15 artículos, todos firmados por el usuario WordPress `admin`** (`posts.json`, `"author": 1`), que el tema muestra como «Tatiana X. Stacul». No hay página de autora enlazada ni caja de autor.
- **La taxonomía no refleja los temas reales.** 9 de 15 artículos tienen 2 categorías; «Ciberpsicología» existe como categoría (id 13, 7 usos) y como etiqueta (id 28, 8 usos). Tres artículos están mal clasificados: *¿Por qué fallamos al intentar cambiar conductas?* (nudge/cudge, cultura de equipos) está en Ciberseguridad; *5 puntos del caso Meta* (redes sociales) y *El estigma de la estructura* (IA y escritura) están en «Neurociencia y tecnología».
- **Etiquetas:** 15 en total, 4 sin uso (awareness-humano, liderazgo_consciente, neuroplasticidad, terapia_online). 7 tienen un solo uso. Los slugs mezclan `_` y `-`. **6 artículos no tienen ninguna etiqueta** (los 5 más recientes y *El arte de rediseñar tu entorno*), no solo los 2 más recientes.
- **Enlazado interno casi nulo.** En el cuerpo de los 15 artículos solo hay **1 enlace contextual** a otro artículo (autoeficacia → *¿Qué modela nuestro comportamiento?*). Ningún artículo enlaza a una página pilar, a `/test/` ni a `/servicios/`. Las páginas pilar `/ciberpsicologia/` y `/bienestar-digital/` no enlazan a ningún artículo.
- **Fuentes:** solo *IA y apoyo emocional* tiene bibliografía formal. Hay cifras sin fuente, como «70 % de los jóvenes y 56 % de los profesionales» en *Tecnoestrés* (línea 31 del txt) o «45 millones de computadoras» y «10.000 millones de dólares» en *ILOVEYOU*. Solo *Infancias figitales* enlaza a una fuente externa (cibervoluntarios.org).
- **La página `/ciberpsicologia/` no funciona como pilar.** Tiene unas 100 palabras, su H1 es «Ciberpsicología y bienestar digital» y no define el término. Compite con `/bienestar-digital/` por la misma intención de búsqueda.
- **Propuesta:** 6 categorías temáticas (subáreas de la ciberpsicología), 15 etiquetas limpias, 17 redirecciones 301, 6 clusters, páginas `/equipo/<slug>/`, 12 temas nuevos en 3 meses y la reescritura de `/ciberpsicologia/` como «¿Qué es la ciberpsicología?».

## 2. Taxonomía propuesta

**Principio:** todo el sitio es ciberpsicología, así que esa palabra no debe ser una categoría. Pasa a ser el **pilar raíz** (`/ciberpsicologia/`), y las categorías son sus subáreas. Cada artículo lleva **una** categoría principal y entre 2 y 5 etiquetas que no repiten el nombre de la categoría. Se conservan los slugs existentes cuando es posible para reducir redirecciones.

### 2.1 Categorías (6)

| # | Categoría propuesta | Slug | Origen | Enfoque (la descripción de la categoría debe tener ≥ 80 palabras y enlazar a su pilar) |
|---|---|---|---|---|
| 1 | Bienestar digital | `bienestar` (se mantiene) | Bienestar digital | Tiempo de pantalla, consumo digital, tecnoestrés, crianza digital → pilar `/bienestar-digital/` |
| 2 | Hábitos y conducta | `habitos-y-conducta` (nuevo) | absorbe Psicología | Ciencia del comportamiento, hábitos, autoeficacia, diseño del comportamiento → pilar nuevo `/habitos-digitales/` |
| 3 | IA y mente | `ia-y-mente` (nuevo) | parte de Ciberpsicología | Cómo pensamos, sentimos y confiamos ante la IA; ética → pilar nuevo `/ia-y-salud-mental/` |
| 4 | Redes sociales y plataformas | `redes-sociales` (nuevo) | parte de Neurociencia | Plataformas, algoritmos, comparación social, responsabilidad de las empresas → pilar futuro |
| 5 | Ciberseguridad y factor humano | `ciberseguridad` (se mantiene, cambia el nombre) | Ciberseguridad | Ingeniería social, sesgos y cultura de seguridad → pilar nuevo `/ciberseguridad-humana/` |
| 6 | Neurociencia y atención | `neurociencia` (se mantiene, cambia el nombre) | Neurociencia y tecnología | Cerebro, atención, sueño, carga cognitiva |

- **Se eliminan:** «Ciberpsicología» (categoría), «Psicología» y «Sin categoría». Antes de borrar «Sin categoría» hay que asignar «Bienestar digital» como categoría por defecto en Ajustes → Escritura.
- Las categorías 4, 5 y 6 quedan con 1 artículo cada una. Se completan con el plan editorial (§6). La alternativa es fusionar «Neurociencia y atención» dentro de «Hábitos y conducta», pero no la recomiendo: la neurociencia es parte de la formación que declara la autora.
- La descripción actual de Ciberseguridad («Prácticas, tecnologías y procesos diseñados para proteger sistemas…», `category_ciberseguridad.txt`) es una definición genérica. Hay que reescribirla desde el factor humano.

### 2.2 Etiquetas limpias (15; slugs en minúsculas con guion)

`salud-mental` · `tecnoestres` · `tiempo-de-pantalla` · `consumo-digital` · `habitos` · `autoeficacia` · `diseno-del-comportamiento` · `sesgos-cognitivos` · `atencion` · `infancia-y-adolescencia` · `trabajo-digital` · `etica-digital` · `ingenieria-social` · `apoyo-emocional` · `lenguaje-claro`

Cuatro etiquetas tienen hoy un solo uso (tecnoestres, ingenieria-social, apoyo-emocional, lenguaje-claro; esta última es la que conecta con el servicio de Francisca). Todas tienen artículos previstos en §6. **No se crean etiquetas nuevas sin que haya al menos 2 artículos previstos para ellas.**

### 2.3 Tabla artículo → categoría

| Artículo (slug) | Categoría actual | Categoría propuesta | Etiquetas propuestas | Justificación |
|---|---|---|---|---|
| por-que-tu-fuerza-de-voluntad-es-mas-lista-de-lo-que-crees | Psicología | Hábitos y conducta | habitos, autoeficacia, trabajo-digital | Voluntad, agotamiento del ego y creencias; sin etiquetas hoy |
| la-diferencia-entre-querer-y-ser-capaz-entendiendo-la-autoeficacia | Psicología | Hábitos y conducta | autoeficacia, habitos | Bandura y las fuentes de la autoeficacia; sin etiquetas hoy |
| por-que-fallamos-al-intentar-cambiar-conductas | Ciberseguridad | Hábitos y conducta | diseno-del-comportamiento, sesgos-cognitivos, trabajo-digital | Nudge/cudge, paternalismo afectivo e insensibilidad al alcance. No trata de seguridad; se enlaza desde el cluster de ciberseguridad por la cultura de equipos |
| ia-y-apoyo-emocional-saber-la-autoria-cambia-tu-perspectiva | Ciberpsicología | IA y mente | apoyo-emocional, sesgos-cognitivos, infancia-y-adolescencia, salud-mental | Estudio sobre la percepción de consejos de IA frente a profesionales en jóvenes; sin etiquetas hoy |
| el-estigma-de-la-estructura-x-entonces-y | Neurociencia y tecnología | IA y mente | sesgos-cognitivos, lenguaje-claro | Prejuicio de «esto lo escribió una IA». No trata de neurociencia |
| infancias-figitales | Bienestar + Ciberpsicología | Bienestar digital | infancia-y-adolescencia, tiempo-de-pantalla, salud-mental | Crianza y acompañamiento crítico frente a control parental |
| calidad-vs-cantidad-la-hipotesis-de-ricitos-de-oro | Bienestar + Ciberpsicología | Bienestar digital | tiempo-de-pantalla, consumo-digital, salud-mental | Hipótesis de Ricitos de Oro (Przybylski) |
| autoevaluacion-del-consumo-digital-… | Bienestar + Ciberpsicología | Bienestar digital | consumo-digital, tiempo-de-pantalla, atencion, habitos | Guía práctica; es el satélite natural de `/test/` |
| preguntas-clave-para-entender-y-cuidar-nuestro-cerebro | Neurociencia y tecnología | Neurociencia y atención | salud-mental, atencion, habitos | Salud cerebral general. Hoy tiene la etiqueta mindfulness_digital, que no corresponde |
| 5-puntos-clave-que-el-caso-de-meta-nos-deja-en-salud-mental | Neurociencia y tecnología | Redes sociales y plataformas | salud-mental, etica-digital, infancia-y-adolescencia | Documentos judiciales, proyecto Mercury y ética de plataformas. No trata de neurociencia |
| reflexiones-eticas-sobre-el-desarrollo-de-la-inteligencia-artificial | Ciberpsicología + Neurociencia | IA y mente | etica-digital, trabajo-digital | Ética de la IA: sesgos algorítmicos, privacidad, empleo |
| descubriendo-que-modela-nuestro-comportamiento | Bienestar digital | Hábitos y conducta | habitos, diseno-del-comportamiento, sesgos-cognitivos | Introducción a la ciencia del comportamiento; es la base del cluster |
| la-tecnologia-te-supera-como-identificar-y-gestionar-el-tecnoestres | Bienestar + Ciberpsicología | Bienestar digital | tecnoestres, trabajo-digital, salud-mental, atencion | Definición, síntomas y gestión del tecnoestrés |
| el-arte-de-redisenar-tu-entorno | Bienestar + Ciberpsicología | Hábitos y conducta | habitos, diseno-del-comportamiento, atencion | Wendy Wood: los hábitos dependen del contexto; sin etiquetas hoy |
| como-un-te-quiero-infecto-45-millones-de-computadoras-… | Ciberseguridad | Ciberseguridad y factor humano | ingenieria-social, sesgos-cognitivos, diseno-del-comportamiento | ILOVEYOU visto como ingeniería social y arquitectura de elección |

Resultado: Bienestar digital 4 · Hábitos y conducta 5 · IA y mente 3 · Redes sociales 1 · Ciberseguridad 1 · Neurociencia 1.

Correcciones menores permitidas por la regla 3:

- Título «saber la autoria, cambia» → «saber la autoría cambia».
- En *Fuerza de voluntad*: «Si, la creencia importa» → «Sí, la creencia importa».
- Títulos en mayúscula inicial solamente, no en Title Case: «Calidad vs. cantidad: la hipótesis de Ricitos de Oro», «Preguntas clave para entender y cuidar nuestro cerebro», «5 puntos clave…», «Reflexiones éticas…», «Autoevaluación del consumo digital…».

## 3. Redirecciones 301 (categorías y etiquetas eliminadas)

Como no hay plugin SEO, las redirecciones se hacen con el plugin *Redirection* o con reglas en `.htaccess` (LiteSpeed). Deben cubrir también `/feed/` y `/page/N/` con regex, por ejemplo `^/category/psicologia(/.*)?$`. Después hay que purgar LiteSpeed y el CDN.

| Origen | Destino | Motivo |
|---|---|---|
| /category/ciberpsicologia/ | /ciberpsicologia/ | La categoría se elimina y su autoridad pasa al pilar raíz |
| /category/psicologia/ | /category/habitos-y-conducta/ | Fusión |
| /category/sin-categoria/ | /blog/ | Vacía |
| /tag/ciberpsicologia/ | /ciberpsicologia/ | Duplicaba la categoría |
| /tag/ciberseguridad/ | /category/ciberseguridad/ | Duplicaba la categoría |
| /tag/inteligencia_artificial/ | /category/ia-y-mente/ | Duplica la nueva categoría |
| /tag/neurociencias/ | /category/neurociencia/ | Duplicaba la categoría |
| /tag/redes_sociales/ | /category/redes-sociales/ | Duplica la nueva categoría |
| /tag/salud_mental/ | /tag/salud-mental/ | Normalización del slug |
| /tag/mindfulness_digital/ | /tag/atencion/ | Mal aplicada; fusión |
| /tag/tecnologia/ | /blog/ | Demasiado genérica |
| /tag/transformacion_digital/ | /category/ciberseguridad/ | Su único uso era ILOVEYOU |
| /tag/awareness-humano/ | /category/ciberseguridad/ | Sin uso |
| /tag/neuroplasticidad/ | /category/neurociencia/ | Sin uso |
| /tag/liderazgo_consciente/ | /blog/ | Sin uso |
| /tag/terapia_online/ | /blog/ | Sin uso. No se redirige a /servicios/ porque el servicio es mentoría, no terapia |
| /author/admin/ | /equipo/tatiana-x-stacul/ | Tras reasignar la autoría (§5) |

Otras redirecciones relacionadas, fuera de la taxonomía: `/sobre_tatiana/` → `/equipo/tatiana-x-stacul/` y `/descargas-2/` → `/descargas/` (el slug «-2» indica un duplicado). `/entradas/` y `/blog/` muestran el mismo listado (`entradas.txt`, `blog.txt`): hay que conservar uno solo y redirigir el otro con 301.

## 4. Clusters y enlazado interno

| Cluster | Pilar | Satélites | Recursos | Servicio relacionado |
|---|---|---|---|---|
| Raíz | /ciberpsicologia/ («¿Qué es la ciberpsicología?») | Los 6 archivos de categoría y los 5 pilares de abajo | /test/, /herramientas/, /descargas/ | /servicios/ |
| A. Bienestar digital | /bienestar-digital/ (existe; ampliar) | Tecnoestrés, Calidad vs. cantidad, Autoevaluación, Infancias figitales | /test/, /herramientas/, descarga «Ansiedad funcional vs. desbordada» | Tatiana: «Desgaste y atención fragmentada en el trabajo digital» |
| B. Hábitos y conducta | /habitos-digitales/ (nuevo: «Cómo cambiar hábitos digitales según la evidencia») | ¿Qué modela nuestro comportamiento?, Rediseñar tu entorno, Autoeficacia, Fuerza de voluntad, ¿Por qué fallamos…? | /test/ | Tatiana: «Hábitos tecnológicos que intentas cambiar y no se sostienen» |
| C. IA y mente | /ia-y-salud-mental/ (nuevo) | IA y apoyo emocional, El estigma de la estructura, Reflexiones éticas sobre la IA | — | Tatiana; Francisca (lenguaje claro), desde *El estigma* |
| D. Ciberseguridad y factor humano | /ciberseguridad-humana/ (nuevo: «Psicología de la ciberseguridad») | ILOVEYOU; ¿Por qué fallamos…? (enlace cruzado) | Descargas «Guía de ciberseguridad para psicólogos» y «The Psychology of Trust» | Tatiana (concienciación). Emanuel («normativa y procesos») [COMPLETAR: confirmar si el equipo ofrece este servicio a organizaciones] |
| E. Redes sociales | Pilar cuando haya ≥ 4 satélites | Caso Meta; Infancias (enlace cruzado) | — | Tatiana |
| F. Neurociencia y atención | Por ahora sin pilar (el archivo de categoría hace de hub) | Preguntas clave sobre el cerebro | — | — |

### Enlaces internos a agregar (el anchor es orientativo; hay que insertarlo en una frase existente sin cambiar el fondo del texto)

| Desde | Hacia | Anchor sugerido |
|---|---|---|
| Tecnoestrés | Autoevaluación · /test/ · /bienestar-digital/ · /servicios/ | «evalúa tu consumo digital» · «test de consumo digital» · «bienestar digital» · «acompañamiento individual» |
| Autoevaluación | /test/ · /herramientas/ · Calidad vs. cantidad | «haz el test» · «apps de registro de uso» · «calidad frente a cantidad» |
| Calidad vs. cantidad | Autoevaluación · Infancias figitales | «autoevaluación» · «infancias figitales» |
| Infancias figitales | Caso Meta · Calidad vs. cantidad | «lo que revelaron los documentos de Meta» · «hipótesis de Ricitos de Oro» |
| ¿Qué modela nuestro comportamiento? | Rediseñar tu entorno · Autoeficacia · Fuerza de voluntad · ¿Por qué fallamos? | Uno por concepto mencionado |
| Rediseñar tu entorno | ¿Qué modela…? · Fuerza de voluntad | «ciencia del comportamiento» · «fuerza de voluntad» |
| Fuerza de voluntad | Autoeficacia (el texto ya menciona «autoeficacia») · Preguntas clave sobre el cerebro | «autoeficacia» · «cuidar tu cerebro» |
| Autoeficacia | Fuerza de voluntad · /servicios/ | «fuerza de voluntad» · «acompañamiento» |
| ¿Por qué fallamos? | ILOVEYOU · ¿Qué modela…? · /ciberseguridad-humana/ | «arquitectura de elección» · «qué modela la conducta» |
| ILOVEYOU | ¿Por qué fallamos? · /descargas/ | «diseñar con la emoción» · «guía de ciberseguridad» |
| IA y apoyo emocional | El estigma de la estructura · Reflexiones éticas | «prejuicio contra el texto estructurado» · «ética de la IA» |
| El estigma de la estructura | IA y apoyo emocional · /servicios/ (Francisca) | «saber la autoría» · «lenguaje claro» |
| Reflexiones éticas | IA y apoyo emocional · Caso Meta | «apoyo emocional con IA» · «responsabilidad de las plataformas» |
| Caso Meta | Calidad vs. cantidad · Infancias · Reflexiones éticas | — |
| Preguntas clave sobre el cerebro | Tecnoestrés · Fuerza de voluntad | «estrés tecnológico» · «voluntad» |
| /ciberpsicologia/ y /bienestar-digital/ | Todos los satélites de su cluster | Bloque «Artículos de este tema» (Kadence Posts filtrado por categoría) |

## 5. Plan E-E-A-T

**Páginas de equipo.** Crear `/equipo/` como índice y tres perfiles:

- `/equipo/tatiana-x-stacul/`
- `/equipo/francisca-cortes-santoro/`
- `/equipo/emanuel-c-franco/`

Cada perfil lleva el mismo esquema:

- Nombre y rol, tomados de /servicios/ (texto ya publicado).
- Foto.
- Bio breve de 50 a 70 palabras, con la misma versión en la caja de autor.
- Formación **declarada por la persona**, marcada como «declarada» mientras no esté verificada.
- Áreas de trabajo, enlazadas al servicio.
- Artículos escritos y revisados, en un listado automático.
- Enlaces sameAs.
- Schema `Person`, con `sameAs`, `jobTitle` y `worksFor` = Código Calma.

El único sameAs que ya existe es https://www.linkedin.com/in/tatiana-staculpsi/ (`html/sobre_tatiana.html`). Los tres de «Sobre Tatiana» (Grado en Psicología, Máster en Neurociencias, Coaching Empresarial) **se mantienen solo como declarados** hasta completar institución y año.

**Autoría real en WordPress.**

- Crear un usuario por persona con rol Autor, nombre visible y slug del tipo `tatiana-x-stacul`.
- Reasignar los 15 artículos de `admin` a Tatiana.
- Aplicar la 301 de `/author/admin/`.
- Avisar al agente de seguridad de que `/author/admin/` expone el nombre de usuario administrador.

**Caja de autor.** Activar el Author Box de Kadence (Personalizar → Posts) con foto, bio, enlace a `/equipo/<slug>/` y LinkedIn. Debajo del título: «Por Tatiana X. Stacul · Revisado por [nombre] · Actualizado el [fecha]».

**«Revisado por».** Solo tiene sentido si revisa otra persona con competencia en el tema:

- **Artículos sensibles de salud mental:** Tecnoestrés, IA y apoyo emocional, Caso Meta, Preguntas sobre el cerebro, Infancias. La revisión debe hacerla una profesional de salud mental distinta de la autora: [COMPLETAR: revisor/a clínico/a externo/a con colegiación verificable]. Hoy el equipo tiene una sola psicóloga.
- **Revisión de lenguaje claro:** Francisca puede figurar como «Revisión de lenguaje claro», nunca como revisión clínica.
- **Ciberseguridad:** [COMPLETAR: revisor/a con experiencia en seguridad] o ninguno.

**Fechas.** Mostrar la fecha de publicación y «Actualizado el» solo cuando haya un cambio de fondo. Hoy **9 artículos comparten `modified` = 2026-06-08 18:09:24**, señal de una edición en lote, y el tema muestra esa fecha como actualización. Eso no refleja una revisión real. Además, ILOVEYOU (2024-03-09) y Rediseñar tu entorno (2025-02-12) tienen fechas anteriores al resto del blog: [COMPLETAR: confirmar la fecha real de publicación].

**Fuentes.** Añadir una sección «Fuentes» con enlaces a fuentes primarias en cada artículo:

| Artículo | Referencia a completar |
|---|---|
| Calidad vs. cantidad | Probablemente Przybylski y Weinstein (2017), *Psychological Science* [verificar] |
| Rediseñar tu entorno | Probablemente Wood, Tam y Witt (2005), *JPSP* [verificar] |
| Autoeficacia | Bandura (1977), *Psychological Review* |
| ¿Por qué fallamos? | [COMPLETAR: referencia del artículo de *Frontiers in Behavioral Economics*] |
| Caso Meta | [COMPLETAR: enlace a los documentos judiciales y al estudio con Nielsen] |
| Tecnoestrés | [COMPLETAR: fuente de las cifras 70 % / 56 %], o retirar las cifras |
| ILOVEYOU | [COMPLETAR: fuente de «45 millones» y «10.000 millones de dólares»] |

**Aviso de urgencia** en los artículos de salud mental: «Este contenido es educativo y no reemplaza atención profesional ni de urgencia» + [COMPLETAR: línea de ayuda o emergencias por país].

### Placeholders necesarios

Deben registrarse en `docs/placeholders.md`; no se hizo por el alcance de esta tarea.

1. [COMPLETAR: foto profesional de Tatiana X. Stacul]
2. [COMPLETAR: universidad y año del Grado en Psicología de Tatiana]
3. [COMPLETAR: institución y año del Máster en Neurociencias]
4. [COMPLETAR: entidad que certificó el Coaching Empresarial]
5. [COMPLETAR: número de colegiación y colegio/país, si aplica]
6. [COMPLETAR: ORCID de Tatiana, si existe]
7. [COMPLETAR: bio breve de Tatiana validada por ella, 50–70 palabras]
8. [COMPLETAR: foto, bio y formación declarada de Francisca Cortés Santoro]
9. [COMPLETAR: LinkedIn u otro perfil verificable de Francisca]
10. [COMPLETAR: foto, bio y formación o certificaciones declaradas de Emanuel C. Franco]
11. [COMPLETAR: LinkedIn u otro perfil verificable de Emanuel]
12. [COMPLETAR: revisor/a clínico/a externo/a y alcance de su revisión]
13. [COMPLETAR: fuentes de las cifras de Tecnoestrés, ILOVEYOU y el caso Meta]
14. [COMPLETAR: referencias primarias de Calidad vs. cantidad, Rediseñar tu entorno, ¿Por qué fallamos? y Autoeficacia]
15. [COMPLETAR: línea de ayuda o urgencias por país]
16. [COMPLETAR: fechas reales de publicación de ILOVEYOU y Rediseñar tu entorno]
17. [COMPLETAR: descripciones de las 6 categorías validadas por Tatiana]
18. [COMPLETAR: datos de volumen de búsqueda de los 12 temas (herramienta de palabras clave)]

## 6. Brechas temáticas, 12 temas nuevos y reescritura del pilar (octubre–diciembre 2026)

### Brechas

- **Definiciones de base:** no hay contenido que defina «qué es la ciberpsicología», ni que explique qué hace una ciberpsicóloga o dónde se estudia.
- **Temas de alta demanda sin cubrir:** uso problemático o «adicción» al móvil (el término ya aparece en /servicios/), FOMO, comparación social, doomscrolling, desconexión digital, sueño y pantallas, dark patterns y ciberacoso.
- **Ciberseguridad humana:** solo hay 1 artículo sobre phishing o ingeniería social, pese a que es un diferencial del sitio (hay 2 descargas sobre el tema).
- **Equipo sin contenido propio:** no hay nada firmado por Francisca (lectura fácil, carga cognitiva) ni por Emanuel (procesos).
- **IA de compañía:** no hay contenido sobre chatbots emocionales, un tema en auge que conecta con *IA y apoyo emocional*.

### Calendario

Ritmo: 1 artículo por semana. La fila 1 es la reescritura del pilar; las 12 siguientes son temas nuevos. El volumen de búsqueda debe verificarse; no se estima aquí.

| Sem. | Tema / título de trabajo | Intención de búsqueda | Consulta principal | Categoría · etiquetas | Autoría | Prioridad |
|---|---|---|---|---|---|---|
| 1–2 | ¿Qué es la ciberpsicología? (reescritura de /ciberpsicologia/, §7) | Informacional (definición) | «qué es la ciberpsicología» | Pilar raíz | Tatiana | Alta |
| 3 | Uso problemático del móvil: señales y qué dice la evidencia | Informacional / autoevaluación | «adicción al móvil síntomas» | Hábitos y conducta · habitos, salud-mental | Tatiana + revisión clínica | Alta |
| 4 | Por qué caemos en el phishing: los sesgos que explota la ingeniería social | Informacional | «por qué caemos en el phishing» | Ciberseguridad · ingenieria-social, sesgos-cognitivos | Tatiana | Alta |
| 5 | Doomscrolling: qué es y cómo cortar el bucle | Informacional | «doomscrolling qué es» | Bienestar digital · atencion, consumo-digital | Tatiana | Alta |
| 6 | FOMO y comparación social en redes | Informacional | «fomo qué es» | Redes sociales · salud-mental, sesgos-cognitivos | Tatiana | Media |
| 7 | Desconexión digital en el trabajo: límites que se sostienen | Informacional / práctica | «desconexión digital trabajo» | Bienestar digital · tecnoestres, trabajo-digital | Tatiana | Media |
| 8 | Pantallas y sueño: lo que sabemos y lo que no | Informacional | «pantallas antes de dormir» | Neurociencia · atencion, salud-mental | Tatiana + revisión | Media |
| 9 | Chatbots de compañía y apoyo emocional: usos y riesgos | Informacional | «chatbot apoyo emocional riesgos» | IA y mente · apoyo-emocional, etica-digital | Tatiana + revisión clínica + aviso de urgencia | Alta |
| 10 | Patrones oscuros: cómo las apps capturan tu atención | Informacional | «patrones oscuros diseño» | Redes sociales · diseno-del-comportamiento, etica-digital | Tatiana | Media |
| 11 | Lectura fácil y carga cognitiva: escribir para que se entienda | Informacional / comercial suave | «lectura fácil qué es» | Neurociencia y atención · lenguaje-claro, atencion | Francisca | Media |
| 12 | Cultura de ciberseguridad en equipos pequeños: procesos antes que culpas | Informacional B2B | «cultura de ciberseguridad empresa» | Ciberseguridad · ingenieria-social, trabajo-digital | Emanuel + Tatiana | Media |
| 13 | Pantallas en familia: acuerdos por edad, con fuentes (OMS, AAP) | Informacional | «tiempo de pantalla por edad» | Bienestar digital · infancia-y-adolescencia, tiempo-de-pantalla | Tatiana | Media |

Todos los artículos nuevos deben llevar un resumen inicial, H2 en forma de pregunta, sección de fuentes, caja de autor, al menos 3 enlaces internos (pilar, satélite y /test/ o /servicios/) y la fecha visible.

## 7. Revisión de /ciberpsicologia/ como pilar

**Estado actual (`txt/ciberpsicologia.txt`):**

- Unas 100 palabras. H1: «Ciberpsicología y bienestar digital».
- Dos párrafos: el primero dice que «una parte de la ciberpsicología estudia esa influencia»; el segundo pasa a hablar de bienestar digital.
- Una rejilla de 5 tarjetas (Bienestar, Herramientas, Test, Descargas, Blog).
- **No define el término**, no cita fuentes, no tiene autoría ni fecha y no enlaza a ningún artículo.
- La mezcla con «bienestar digital» hace que canibalice a `/bienestar-digital/`.
- Además funciona como padre de menú («Ciberpsicología → Ampliar»), lo que refuerza su papel de hub pero no de contenido.

**Propuesta.** La página hoy no tiene texto de autora que conservar, así que el contenido nuevo lo redacta o valida Tatiana:

- **Title:** «¿Qué es la ciberpsicología? Definición, áreas y ejemplos | Código Calma».
- **H1:** «¿Qué es la ciberpsicología?».
- **Extensión:** 1.800 a 2.500 palabras. Byline, «Revisado por» y «Actualizado el».

Estructura:

1. **Respuesta breve** (40–60 palabras): una definición en lenguaje claro, apta para fragmento destacado.
2. **H2 Origen y campo de estudio:** relación entre psicología e interacción humano-tecnología. Fuentes a verificar y enlazar: Suler (2004), «The Online Disinhibition Effect», *CyberPsychology & Behavior*; las revistas *Cyberpsychology, Behavior, and Social Networking* y *Cyberpsychology: Journal of Psychosocial Research on Cyberspace*; la entrada del APA Dictionary.
3. **H2 ¿Qué estudia?:** 6 subsecciones, una por categoría, cada una con 2–3 frases y enlace a su archivo y a sus satélites (hábitos y conducta, bienestar digital, redes sociales, IA y mente, ciberseguridad y factor humano, neurociencia y atención).
4. **H2 Ejemplos cotidianos:** efecto de desinhibición online, arquitectura de elección (enlace a ILOVEYOU), tiempo de pantalla frente a calidad de uso (enlace a Ricitos de Oro).
5. **H2 Ciberpsicología, psicología y bienestar digital: diferencias:** separa las intenciones de búsqueda y enlaza a /bienestar-digital/.
6. **H2 ¿Dónde se aplica?:** educación, organizaciones, diseño de producto, seguridad y acompañamiento individual. Sin promesas de resultados.
7. **H2 Mitos frecuentes:** «la dopamina de las redes», «las horas de pantalla lo explican todo». Solo con fuentes.
8. **H2 Recursos para empezar:** /test/, /herramientas/, /descargas/.
9. **FAQ:** ¿es una carrera?, ¿dónde se estudia? [COMPLETAR: datos verificables], ¿es lo mismo que terapia online? (no).
10. **Fuentes.**
11. **Caja de autora y CTA suave** a /servicios/: «Si quieres trabajarlo uno a uno, nos escribes».

**Cambios asociados:**

- Quitar «y bienestar digital» del H1.
- Mover el copy de bienestar a `/bienestar-digital/`.
- Recibir la 301 de `/category/ciberpsicologia/` y de `/tag/ciberpsicologia/`.
- Enlazar al pilar desde la portada, desde la descripción de cada categoría y desde el primer párrafo de al menos 5 artículos.
- Añadir schema `Article` + `BreadcrumbList` + FAQ, a cargo del agente SEO.
