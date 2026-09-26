# Formulario de contacto — ajustes del bloque (Etapa 1)

El formulario de `/contacto/` es un **Kadence Advanced Form** (ID 2625), no Contact Form 7.
Dónde: **Kadence Blocks > Forms > (formulario 2625)**, o en la página Contacto > seleccionar el bloque Formulario > "Editar formulario".
Resuelve: CRO-01/02/03, A11Y-09/10, UX-20. Textos: `docs/auditoria/informes/cro-copy.md` §6.3.

## 1. Ajustes generales del formulario
| Ajuste | Valor |
|---|---|
| Estilo > Label style | **Above** (etiqueta encima del campo; hoy es "infield", la etiqueta se mete en la caja y desaparece al escribir) |
| Estilo > Fondo | Claro (quitar "is dark") |
| Mensajes > Éxito | **Recibimos tu mensaje.** Te respondemos en 48 horas hábiles desde hola@codigocalma.com con quién del equipo encaja mejor y cómo sería el primer encuentro. Si no lo ves, revisa la carpeta de spam. |
| Mensajes > Error general | No pudimos enviar tu mensaje. Revisa los campos marcados o escríbenos directamente a hola@codigocalma.com. |
| Mensajes > Campo obligatorio | Este dato es necesario para poder responderte. |
| Anti-spam | Activar el honeypot de Kadence (Spam > "Honeypot"). Sin CAPTCHA visual. |
| Correo de notificación | Sin cambios (sigue llegando a hola@codigocalma.com). |

## 2. Campos
| Campo | Etiqueta | Texto de ayuda (Help text) | Obligatorio | Avanzado |
|---|---|---|---|---|
| Texto (nombre) | ¿Cómo te llamas? | — | **Sí** (hoy no) | Auto complete: `name` |
| Email | ¿A qué correo te respondemos? | Solo lo usamos para responderte. | Sí | Auto complete: `email` |
| Textarea (mensaje) | Cuéntanos qué te trae | Con unas líneas basta. Por favor, evita incluir datos sensibles de salud: este mensaje puede leerlo más de una persona del equipo. | Sí | Filas: 4 |
| **Nuevo:** Accept (casilla) | He leído la política de privacidad y acepto que usen mis datos para responder a mi consulta. | — | Sí | Enlace a la política: [COMPLETAR: URL de la política de privacidad] |
| Botón | Enviar mi consulta | — | — | — |

## 3. Textos alrededor del formulario (bloques de la página)
- Debajo del botón, párrafo nuevo: «Te respondemos en 48 horas hábiles. Si vemos que este no es el lugar, también te lo decimos.»
- Antes del botón (o debajo del anterior), aviso breve: «Este espacio no es un servicio de urgencias. Si estás en crisis o en riesgo, contacta ahora con los servicios de emergencia de tu país.» + enlace [COMPLETAR: líneas de ayuda].
- El párrafo en cursiva actual («Este mensaje podrá ser leído…») se puede borrar: su contenido pasa al texto de ayuda del mensaje.
- Las tres viñetas de preguntas se mantienen en la Etapa 1; en la Etapa 3 se reemplazan por la opción "¿Sobre qué quieres consultar?".

## 4. Verificación
- Enviar un mensaje de prueba con todos los campos y otro dejando vacío el nombre: debe mostrar el error bajo el campo.
- Recorrer el formulario solo con teclado (Tab / Shift+Tab / Espacio en la casilla / Enter).
