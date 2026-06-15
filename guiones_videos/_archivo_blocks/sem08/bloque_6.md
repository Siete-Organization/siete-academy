---
video: Sem 8 — Bloque 6
modulo: 4 — El sistema
semana: 8 — Del proceso al mindset
titulo: Diagnóstico por descarte — encontrar la causa raíz
duracion_estimada: ~7:30
palabras_aprox: 1080
ejercicio: si — Ejercicio 2 (Tabla de Juan, diagnóstico anti-IA)
fuente_doc: SDR_Academy_Siete_Documento_Maestro.md, líneas 11082-11160
---

# Bloque 6 — Diagnóstico por descarte: encontrar la causa raíz

## [GANCHO ~20s]

Cuando una métrica cae, el SDR novato hace lo siguiente: cambia el copy, cambia el asunto, hace A/B testing, pide una lista nueva. **Prueba cosas al azar.**

Eso es ruido.

El SDR bueno **recorre el funnel por descarte**: de aguas abajo hacia aguas arriba, **con una pregunta por etapa**.

## [CONTEXTO ~15s]

Vamos al principio que organiza el método, el recorrido completo con un ejemplo, y al final un ejercicio que es la mejor prueba que vas a tener del curso.

## [EL PRINCIPIO ~30s]

**[SLIDE: El principio del diagnóstico]**

**Un problema en el paso N se detecta por la métrica del paso N+1.**

Si el show rate cae —que es la métrica de la etapa ocho—, **la causa probablemente está en la etapa siete o antes**. Y se descarta yendo etapa por etapa hacia arriba, hasta encontrar dónde se originó el síntoma.

No hay que adivinar. Hay que **leer los números en el orden correcto**.

## [EL RECORRIDO DEL FUNNEL ~3:00]

**[SLIDE: Caso de ejemplo — cayó el show rate]**

Supongamos que cayó el **show rate**: la gente no se está presentando a las reuniones agendadas. Hacemos el recorrido completo, con una pregunta por etapa.

**Pregunta uno. ¿La métrica aguas abajo también cayó?** Por ejemplo, conversión empresa a reunión calificada.

Si **sí**: el problema se amplía aguas abajo. Confirma que el síntoma es real, no ruido.

Si **no**: probablemente es ruido estadístico, seguir midiendo unas semanas más antes de actuar.

**Pregunta dos. ¿La precalificación estaba funcionando?** Etapa nueve.

Si **no se hacía**: ahí está el problema. La gente se olvida, o no estaba seriamente interesada. No hubo recordatorio veinticuatro a cuarenta y ocho horas antes.

Si **sí se hacía**: seguir subiendo.

**Pregunta tres. ¿El agendamiento está bien hecho?** Etapa ocho.

¿Se confirmó fecha, hora, canal, y quién participa?

¿Los prospectos tienen la invitación de calendario?

Si **no**: ahí está el problema.

**Pregunta cuatro. ¿La calificación era real?** Etapa siete.

¿Los prospectos que dijeron "sí" realmente entendían qué iban a ver en la reunión? Si se les ofreció reunión antes de tiempo, o sin explicar de qué se trata, **el prospecto dijo sí por cortesía**, pero no se va a presentar.

**Pregunta cinco. ¿La gestión de respuestas mapea bien el interés?** Etapa seis.

¿Se están clasificando bien los "sí" del tipo "dale, agendemos", versus "sí, mandame info"? Son muy distintos. El primero es interés. El segundo es despedida educada.

## [EL ERROR DEL NOVATO ~30s]

**[SLIDE: Por qué empezar por el mensaje es un error]**

El error del SDR novato es **empezar por "cambiemos el mensaje" —etapa cuatro—** sin haber chequeado las etapas seis a nueve primero.

¿Resultado? Si el problema estaba en la precalificación, cambiar el mensaje **no mueve nada**. El SDR cambia el copy, espera dos semanas, no ve mejora, cambia otra vez. Cuando finalmente diagnostica el problema real, ya pasaron seis semanas.

## [CHECK DE COMPRENSIÓN — Ejercicio 2 ~2:30]

Vamos con un caso real. Es un ejercicio de tres preguntas. Está diseñado para que solo lo apruebe un SDR que **entendió el método**, no uno que adivinó.

**[SLIDE: Tabla de métricas de Juan, 4 semanas]**

Estas son las métricas semanales del SDR Juan. La semana cuatro muestra la anomalía.

- **Bounce rate:** 2.1, luego 2.3, luego 2.0, luego 2.2 por ciento. **Estable.**
- **Reply rate:** 2.4, luego 2.5, luego 2.3, luego **cero coma siete**. **Caída fuerte.**
- **Meeting rate sobre reply:** 25, 26, 24, 25 por ciento. **Estable.**
- **Show rate:** 72, 74, 71, 73 por ciento. **Estable.**
- **Precalificación aprobada:** 88, 90, 87, 89 por ciento. **Estable.**

Juan **no cambió** copy, ICP, cadencia, volumen ni herramientas. **Nada.**

**[SLIDE: Pregunta]**

**¿Cuál es la hipótesis más probable, y qué chequea primero?**

a) El copy se gastó, hay que cambiarlo y hacer A/B testing del asunto.
b) Cambió el ICP por estacionalidad, hay que esperar dos semanas.
c) Problema de deliverability: los emails están cayendo a spam o promociones. Primero hay que abrir Postmaster Tools y revisar la reputación del dominio.
d) Problema de calificación: las preguntas de cold call no están filtrando bien.

*[Pausa breve]*

¿Elegiste la **c**? Estás en lo correcto.

Y mirá el razonamiento, porque es el corazón del método.

Las métricas aguas abajo —meeting rate sobre reply, show rate, precalificación— **están estables**. Si el ICP o el copy fueran el problema, **la calidad de los replies también caería**. Pero no cae: los pocos replies que llegan **son igual de buenos que antes**. Lo que cambió **no es la calidad, es la cantidad**.

El bounce rate sigue bajo —dos coma dos por ciento—, así que la lista no se contaminó. Pero la reputación del dominio pudo caer por otras razones: denuncias spam, volumen excesivo, warmup mal hecho en un dominio nuevo.

**Los emails se están entregando técnicamente, pero caen a spam o promociones.** Por eso el reply rate se derrumbó sin que las demás métricas se muevan.

**La acción concreta**: abrir **Google Postmaster Tools** y revisar la reputación de cada dominio activo en las últimas dos semanas. Si la reputación cayó, buscar el día en que empezó la caída, y correlacionar con cualquier evento. En paralelo: correr **mail-tester punto com** desde cada dominio para ver si el score está por debajo de seis sobre diez.

**Y nada de cambiar el copy hasta descartar deliverability.**

Si llegaste a la respuesta correcta con el razonamiento correcto, **entendiste el método**. No memorizaste una receta.

## [CIERRE Y PUENTE ~15s]

Ya sabés diagnosticar. En el próximo bloque vamos al **otro lado del proceso**: cuando todo funciona, ¿cómo se mejora? El **ciclo PDCA** y la disciplina de **una variable por experimento**.

Nos vemos en el Bloque 7.

---

**Fuentes de este bloque:**
- Goldratt (1984). *The Goal*. North River Press.
- Deming, W. E. (1982). *Out of the Crisis*. MIT Press.
