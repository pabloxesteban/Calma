---
name: conversion-page
description: Estructura y checklist para páginas que generan solicitudes de consulta en codigocalma.com (servicios, contacto, inicio, landing de cada profesional) y para captura de emails. Úsala al diseñar o reescribir esas páginas, el formulario de consulta (Kadence Form), los CTA dentro de artículos o el bloque de newsletter. Ética de salud mental incluida: sin urgencia falsa ni promesas de resultados.
---

# Conversion page — Código Calma

## Estructura de la página de servicios (orden recomendado)
1. **Hero con propuesta de valor** (1 pantalla en mobile)
   - Eyebrow: "Acompañamiento individual".
   - H1 que diga qué y para quién: "Mentoría uno a uno para ordenar tu relación con la tecnología y tu trabajo".
   - Subtítulo de 1–2 líneas con el mecanismo: "Una persona por vez, de tres a seis sesiones online, con un plan por escrito para sostenerlo sin nosotros."
   - CTA primario "Solicitar una consulta" + secundario "Ver cómo trabajamos" (ancla).
   - 3 datos de encuadre (ya existen): Una persona por vez · 3 a 6 sesiones · Online.
2. **¿Es para ti?** 3–5 situaciones reconocibles en primera persona ("Intento cambiar hábitos digitales y no se sostienen"), y también "cuándo no es para ti" (urgencias, tratamiento clínico) → confianza.
3. **Proceso en pasos** (existe: 3 pasos). Cada paso: número dentro de la tarjeta, título, 1–2 líneas, qué te llevas.
4. **Con quién trabajas**: foto [COMPLETAR], nombre, rol, 1 línea de enfoque, 3 temas, enlace a su página, y CTA "Consultar con Tatiana" que preselecciona el área en el formulario.
5. **Confianza**: formación declarada (verificada), enfoque basado en evidencia con enlaces a artículos, testimonios **existentes** con nombre abreviado y consentimiento [COMPLETAR: confirmar consentimiento], confidencialidad.
6. **Preguntas frecuentes** (4–6): duración, modalidad, honorarios [COMPLETAR], qué pasa en el primer encuentro, confidencialidad, diferencia con psicoterapia.
7. **CTA final** con reaseguro: "¿Empezamos con calma?" + respuesta en 48 h hábiles + "si no es el lugar, te lo decimos".
8. **Aviso de cuidado**: "Si estás atravesando una crisis o corres riesgo, contacta a los servicios de emergencia de tu país. [COMPLETAR: líneas de ayuda]".

## Formulario de consulta (mínima fricción)
Campos:
1. Nombre (obligatorio) — label "¿Cómo te llamas?"
2. Email (obligatorio) — "¿A qué correo te respondemos?"
3. Área (radio, opcional, preseleccionable por URL `?area=`): Hábitos digitales y comportamiento · Accesibilidad cognitiva · Gestión de proyectos · No lo sé todavía
4. Mensaje (obligatorio, 3 filas) — "Cuéntanos en unas líneas qué está pasando" + ayuda: "Con unas líneas basta. Evita datos sensibles de salud."
5. Consentimiento de privacidad (checkbox obligatorio con enlace).
Botón: "Enviar mi consulta". Tras enviar: mensaje en pantalla + email automático: "Recibimos tu mensaje. Te respondemos en 48 horas hábiles con quién del equipo encaja mejor."
Técnico: labels en español (hoy "Name", "Message" en inglés), `autocomplete="name"`/`"email"`, errores bajo el campo, anti-spam sin CAPTCHA visual (honeypot / Turnstile), evento de conversión (`generate_lead`) en analítica si existe.

## CTA repetido
- Header (botón fijo), hero, después del proceso, después del equipo, final.
- En artículos: caja al final relacionada con el tema ("¿Te identificas con esto? Tatiana acompaña procesos de cambio de hábitos digitales → Solicitar una consulta") y no más de un CTA intermedio.

## Captura de emails
- Lead magnet con lo existente: "Test de consumo digital" y "Descargas". Oferta: "Recibe una reflexión breve sobre bienestar digital cada 15 días" [COMPLETAR: frecuencia real].
- Proveedor: el sitio ya tiene integraciones de Kadence con MailerLite / FluentCRM / GetResponse → elegir uno [COMPLETAR: proveedor].
- Formulario: solo email + consentimiento; doble opt-in; ubicaciones: final de artículo, footer, página de descargas.

## Checklist
- [ ] Propuesta de valor entendible en 5 segundos (prueba con alguien ajeno).
- [ ] CTA primario visible sin scroll en 390 px, contraste ≥ 4,5:1, alto ≥ 48 px.
- [ ] Formulario ≤ 5 campos, labels visibles en español, errores claros.
- [ ] Qué pasa después de enviar, explicado.
- [ ] Sin testimonios, cifras ni credenciales inventadas.
- [ ] Aviso de urgencias visible.
- [ ] Evento de conversión medible.

## Ejemplo de microcopy
| Antes | Después |
|---|---|
| Name / Message / Enviar | ¿Cómo te llamas? / Cuéntanos en unas líneas qué está pasando / Enviar mi consulta |
| Leer más | Leer "Por qué tu fuerza de voluntad es más lista de lo que crees" (texto accesible) |
