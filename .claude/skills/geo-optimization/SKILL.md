---
name: geo-optimization
description: Optimización para motores generativos (GEO) en codigocalma.com — acceso de crawlers de IA (robots.txt + firewall/CDN de Hostinger), llms.txt, respuestas directas al inicio de cada artículo, definiciones citables, fuentes, autoría visible y consistencia de entidades. Úsala al tocar robots.txt, al crear o reestructurar artículos y páginas pilar, y al verificar que ChatGPT, Perplexity, Gemini y Claude pueden leer y citar el sitio.
---

# GEO — Código Calma

## 1. Acceso de crawlers
### robots.txt objetivo
WordPress genera robots.txt virtual; para controlarlo, editarlo en Rank Math (Ajustes generales → Editar robots.txt; archivo listo en `contenido/etapa-1/rank-math/robots.txt`) o subir un archivo físico `robots.txt` a la raíz.
```
# Código Calma — robots.txt
User-agent: *
Disallow: /wp-admin/
Allow: /wp-admin/admin-ajax.php
Disallow: /?s=
Disallow: /search/

# Buscadores y asistentes de IA: acceso permitido para indexar y citar
User-agent: GPTBot
Allow: /
User-agent: OAI-SearchBot
Allow: /
User-agent: ChatGPT-User
Allow: /
User-agent: ClaudeBot
Allow: /
User-agent: Claude-SearchBot
Allow: /
User-agent: Claude-User
Allow: /
User-agent: PerplexityBot
Allow: /
User-agent: Perplexity-User
Allow: /
User-agent: Google-Extended
Allow: /
User-agent: Applebot-Extended
Allow: /
User-agent: Bingbot
Allow: /

Sitemap: https://codigocalma.com/wp-sitemap.xml
```
Nota: un grupo `User-agent` específico reemplaza al `*` para ese bot, así que si se agrega `Disallow: /wp-admin/` a `*`, repetirlo en cada grupo de IA si se quiere excluir el admin también para ellos.

### Firewall / CDN
robots.txt no alcanza si el WAF bloquea. En hPanel de Hostinger revisar: **Seguridad → Protección contra bots / "AI Audit" / bloqueo de crawlers de IA**, reglas de CDN (hcdn) y cualquier plugin de seguridad. Verificar con:
```bash
for ua in "GPTBot/1.1" "OAI-SearchBot/1.0" "ChatGPT-User/1.0" "ClaudeBot/1.0" "Claude-User/1.0" \
          "PerplexityBot/1.0" "Perplexity-User/1.0" "Google-Extended" "Googlebot/2.1" "bingbot/2.0"; do
  printf "%-22s %s\n" "$ua" "$(curl -s -o /dev/null -w '%{http_code} %{size_download}B' -A "Mozilla/5.0 (compatible; $ua)" https://codigocalma.com/)"
done
```
Una prueba desde otra IP no garantiza nada: los bloqueos suelen ser por rango de IP del proveedor. Confirmar en los logs de acceso de Hostinger que aparecen hits 200 de esos bots, y probar pidiéndole a ChatGPT/Perplexity/Claude que lean una URL concreta.

## 2. llms.txt
Archivo Markdown en `https://codigocalma.com/llms.txt` (físico en la raíz). Estructura:
```markdown
# Código Calma
> Portal de ciberpsicología en español: cómo la tecnología influye en la conducta, la atención y el bienestar, con artículos basados en evidencia y acompañamiento uno a uno.

## Equipo
- [Tatiana X. Stacul](https://codigocalma.com/equipo/tatiana-x-stacul/): psicóloga, ciberpsicología y comportamiento.
- [Francisca Cortés Santoro](…): accesibilidad cognitiva y lenguaje.
- [Emanuel C. Franco](…): gestión de proyectos y procesos.

## Servicios
- [Mentoría y acompañamiento uno a uno](https://codigocalma.com/servicios/): 3 a 6 sesiones online, una persona por vez.

## Guías principales
- [¿Qué es la ciberpsicología?](https://codigocalma.com/ciberpsicologia/): …
- [Bienestar digital](https://codigocalma.com/bienestar-digital/): …

## Artículos
- [Título](URL): resumen de una línea.

## Opcional
- [Test de consumo digital](https://codigocalma.com/test/)
```
Mantenerlo sincronizado al publicar (o generarlo desde el plugin codigo-calma).

## 3. Estructura citable de cada artículo
Sin cambiar la voz ni el contenido de la autora, **agregar** estructura:
1. **Bloque "En resumen"** (40–60 palabras) justo después del H1 y los metadatos: responde la pregunta del título en forma directa, autocontenida, sin "en este artículo veremos".
2. **Definición** del concepto central en una oración: "El tecnoestrés es el malestar psicológico asociado al uso intensivo o forzado de tecnologías digitales (Brod, 1984)."
3. **H2 como preguntas** reales cuando encaje ("¿Cómo saber si tengo tecnoestrés?").
4. **Listas y tablas** para pasos, síntomas, comparaciones.
5. **Datos con fuente y año** en el texto ("un estudio con 122.058 participantes (JAMA Network Open, 2025)").
6. **Sección "Fuentes"** al final con enlaces (DOI, PMC, organismo).
7. **Caja de autoría**: nombre, rol, enlace a su página, "Publicado" y "Actualizado", y [COMPLETAR: revisión profesional] si aplica.
8. **Preguntas frecuentes** (2–4) solo si responden dudas reales; marcarlas con FAQPage (skill `schema-markup`).

### Ejemplo (artículo sobre autoeficacia)
> **En resumen:** Querer hacer algo y sentirse capaz de hacerlo no es lo mismo. La autoeficacia —la confianza en la propia capacidad para realizar una tarea concreta— explica por qué a veces, aun con motivación, nos paralizamos. Se fortalece con pequeños logros, modelos cercanos y un entorno que reduzca la fricción.
> *(Texto nuevo de estructura; el cuerpo del artículo se mantiene.)*

## 4. Entidad y autoría
- Mismo nombre, rol y bio breve en: página de equipo, caja de autor, schema Person, LinkedIn.
- Usuario WordPress con nombre visible real (no "admin"); una cuenta por autora/autor.
- `sameAs` con perfiles verificables. Nada de credenciales sin confirmar: `[COMPLETAR: matrícula profesional]`.

## 5. Checklist
- [ ] Todos los bots de IA reciben 200 (prueba + logs).
- [ ] robots.txt con grupos explícitos y Sitemap.
- [ ] `/llms.txt` publicado y actualizado.
- [ ] Cada artículo: "En resumen", definición, fuentes, autoría visible, fechas.
- [ ] Páginas pilar con definición en la primera oración.
- [ ] Sin contenido oculto o distinto para bots.
- [ ] Prueba manual trimestral: preguntar a ChatGPT, Perplexity, Gemini y Claude "¿qué es la ciberpsicología?" / temas de los pilares y registrar si citan el sitio.
