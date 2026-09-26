# Reglas comunes a todos los subagentes de Código Calma

Lo leen todos los subagentes (`.claude/agents/`) antes de trabajar.

## Contexto del proyecto
- Sitio: https://codigocalma.com — portal de ciberpsicología en español con mentoría y acompañamiento uno a uno.
- Stack: WordPress 7.x en Hostinger (LiteSpeed Cache + CDN hcdn), tema **Kadence**, bloques **Kadence Blocks**, **ZoloBlocks**, **Blocks Animation**, **Kadence Form** (contacto; Contact Form 7 instalado sin uso), **AddToAny**. Sin plugin SEO.
- Equipo: Tatiana X. Stacul (psicóloga, ciberpsicología y comportamiento), Francisca Cortés Santoro (accesibilidad cognitiva y lenguaje), Emanuel C. Franco (gestión de proyectos y procesos).
- Voz de marca: **tuteo** en español neutro ("nos escribes", "te respondemos"), tono sereno, claro, sin urgencia artificial.
- Inventario y diagnóstico: `docs/auditoria/`.

## Reglas no negociables
1. **Nunca inventes** testimonios, reseñas, cifras, títulos, matrículas, credenciales, años de experiencia, clientes ni resultados. Si falta un dato, dejá un placeholder visible: `[COMPLETAR: descripción del dato]` y registralo en `docs/placeholders.md`.
2. **Salud mental**: tono cuidado, sin promesas de resultados ("vas a superar tu ansiedad"), sin diagnósticos a distancia, fuentes confiables (revistas revisadas por pares, organismos públicos: OMS, NIH/PMC, APA, Comisión Europea). Incluir aviso de que el servicio no reemplaza atención de urgencia cuando corresponda.
3. **Contenido de artículos**: mantener el texto de la autora. Solo se corrigen errores (ortografía, tildes, cifras mal expresadas) y se mejora estructura (encabezados, resumen inicial, listas, fuentes). Todo cambio de fondo se propone, no se aplica.
4. **Rendimiento**: LCP < 2,5 s, CLS < 0,1, INP < 200 ms; imágenes webp/avif con `width`/`height` declarados; nada de fuentes o scripts que bloqueen el render sin justificación.
5. **No publicar ni desplegar**: todo queda en la rama de trabajo para revisión humana.
6. Reportar en español, con evidencia (URL, selector, captura o línea de archivo) para cada hallazgo.
