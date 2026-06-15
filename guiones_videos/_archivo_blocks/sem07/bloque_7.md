---
video: Sem 7 — Bloque 7
modulo: 4 — El sistema
semana: 7 — La maquinaria del outbound
titulo: Deliverability como concepto fundamental
duracion_estimada: ~7:00
palabras_aprox: 990
ejercicio: si — Ejercicio 3 (Diagnóstico por descarte)
fuente_doc: SDR_Academy_Siete_Documento_Maestro.md, líneas 10412-10472
---

# Bloque 7 — Deliverability como concepto fundamental

## [GANCHO ~20s]

Podés escribir el mejor cold email del mundo. Si no llega al inbox del prospecto, **nada de lo anterior sirve**.

**Deliverability** es la ciencia, y un poco el arte, de que tus emails aterricen en el inbox. Y no en spam, ni en promociones.

## [CONTEXTO ~15s]

El SDR **no configura** deliverability. Eso es trabajo del Outbound Specialist. Pero tiene que **entender los conceptos**. Porque la higiene de deliverability **se rompe muy fácil**, y se rompe por cosas que el SDR sí controla.

## [CONCEPTO CENTRAL ~4:00]

**[SLIDE: Los 4 factores de deliverability]**

**Factor uno. Reputación del dominio.**

Cada dominio de envío —el "arroba" de tu correo— tiene un **score de reputación** que los proveedores como Google y Microsoft mantienen internamente. Los dominios nuevos arrancan con reputación baja. La reputación **se gana** con tiempo, volumen razonable, y respuestas. **Se pierde** con spam reports, bounces altos, y envíos masivos.

**Factor dos. Warmup.**

Un dominio nuevo **no puede mandar outreach masivo desde el día uno**. Necesita "calentarse" durante dos a cuatro semanas: mandar volúmenes bajos, interactuar con casillas que responden, ir subiendo volumen gradualmente.

**Si saltás el warmup, el dominio se quema en cuarenta y ocho horas y no sirve más.**

**Factor tres. Volumen por casilla por día.**

Los proveedores limitan cuántos emails puede mandar una sola casilla por día antes de clasificar como spam. En Google y Microsoft, el techo útil está **entre ochenta y cien emails diarios por casilla**. Pasar ese número es una señal de bulk sender. Y más probabilidad de caer a spam.

**Factor cuatro. Autenticación técnica.**

SPF. DKIM. DMARC. Son tres registros DNS que le dicen a los proveedores: "este dominio es legítimo". **Sin ellos, los emails caen a spam automáticamente.** Los configura IT o el Outbound Specialist. Vos entendés que existen, y que sin ellos no se manda nada.

**[SLIDE: Qué es una "casilla quemada"]**

Una casilla que quedó en lista negra de los proveedores. Los síntomas:

- **Bounces altos**, por encima del cinco por ciento.
- Los emails van a spam en mail-tester punto com, con score por debajo de seis sobre diez.
- **La tasa de respuesta cae drásticamente, sin cambio de copy.**
- Postmaster Tools de Google reporta Compliance Status bajo, o Spam Rate alto.

Una vez quemada, **rehabilitarla toma semanas**. Por eso una agencia de outbound como Siete tiene una **infraestructura de dominios de reserva**: cuando uno se quema, activan otro.

## [POR QUÉ EL SDR TIENE QUE ENTENDER ESTO ~50s]

**[SLIDE: Cómo el SDR rompe deliverability sin saberlo]**

Aunque vos no configures nada, **podés romper la infraestructura** sin querer si:

- **Cargás listas con emails no validados.** Eso genera bounces altos. Los bounces altos queman casillas.
- **Mandás doscientos emails al día por casilla porque "querés volumen".** El techo es cien. Pasarlo te marca como bulk sender.
- **Ignorás señales tempranas** de caída de reply rate.

El SDR es **parte activa de la higiene de deliverability**. Aunque no configure nada.

## [CHECK DE COMPRENSIÓN — Ejercicio 3 ~1:45]

**[SLIDE: Caso de diagnóstico]**

Un SDR nota que su reply rate **cayó de dos coma uno por ciento, a cero coma cuatro por ciento**, en las últimas dos semanas. No cambió el copy. No cambió el ICP. No cambió la cadencia.

**Pregunta: ¿Cuál es la hipótesis más probable, y qué chequea primero?**

a) El copy se "gastó", hay que cambiarlo. Probar A/B testing en el asunto.
b) Cambió el comportamiento del mercado, hay que esperar dos semanas.
c) Problema de deliverability. Uno o más dominios se quemaron, o la reputación cayó. Revisar Postmaster Tools y mail-tester.
d) El ICP está mal definido. Reformular criterios.

*[Pausa breve]*

¿Elegiste la **c**? Estás en lo correcto.

Y acá viene la lección crítica del bloque: **cuando una métrica cae sin que cambien las variables del mensaje, el problema casi siempre está en el canal, no en el mensaje**.

**[SLIDE: Checklist de diagnóstico en orden]**

Qué chequear, en orden:

**Uno.** Abrir Google Postmaster Tools. Revisar la reputación de cada dominio activo.

**Dos.** Correr mail-tester punto com desde cada dominio. Ver si el score cayó.

**Tres.** Revisar bounces de las últimas dos semanas. Si subieron, probablemente hubo carga de emails no validados.

**Cuatro.** Verificar warmup de dominios de reserva. Si un dominio se quemó, el reemplazo debería estar listo.

**El error del SDR novato ante este problema:** empezar a "probar cosas". Cambiar el copy. Hacer A/B testing del asunto. Llamar a los prospectos para compensar.

Pero **el problema no es el mensaje. Es el canal**. Y hasta que no se resuelva deliverability, **nada de lo demás va a mover la aguja**.

## [CIERRE Y PUENTE ~15s]

Ya entendés la infraestructura invisible. Nos queda un último bloque para cerrar la semana, y va sobre algo que parece obvio y casi nadie aplica bien: cómo tratar a las **herramientas**. Apollo, Reply, Outreach. Te adelanto el principio: **son instrumentación del concepto, no el concepto**.

Nos vemos en el Bloque 8.

---

**Fuentes de este bloque:**
- Google Postmaster Tools (documentación oficial).
- MailReach. *Deliverability Best Practices*.
- Instantly (2026). *Cold Email Benchmark Report*.
