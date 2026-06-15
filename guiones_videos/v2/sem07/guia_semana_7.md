---
documento: Guía Semana 7 — La maquinaria del outbound
modulo: 4 — El sistema
semana: 7
formato: guia_pdf_v3
fuente: LIMPIO_S7.md (v1 · 2026-06-12)
copyright: © Siete Academy. Todos los derechos reservados.
---

# Semana 7 — La maquinaria del outbound

**Módulo 4 — El sistema** · **Semana 7 de 8** · **Abre el Módulo 4**

## Cómo está organizada esta semana

**Tiempo estimado real del alumno:** ~5 horas

- Contenido asincrónico (lectura activa): ~3 h
- 3 ejercicios intercalados: ~40 min
- Arranque de la prueba final: lectura del brief del caso + sus primeras etapas (~1 h).

La Semana 8 cierra la prueba final del curso. Por eso esta semana ya empiezas a leer el caso: es largo y conviene que lo recorras con calma antes del cierre.

---

## Pregunta central de la semana

***¿Cómo se combina gente, canales, tiempo e infraestructura para que esto funcione a escala?***

Al terminar la semana, vas a poder:

- Diseñar una secuencia multicanal coherente para un contexto dado y justificar cada decisión de orden y de tiempo.
- Identificar la variante de acceso al decisor correcta según la información que tengas del prospecto.
- Explicar qué determina si un correo llega a la bandeja de entrada o no.
- Reconocer que las herramientas instrumentan el concepto; no son el concepto.

---

## Bloque 1 — Outbound como sistema, no como "escribirle a alguien"

Hasta ahora el curso te dio criterio individual: cómo leer el negocio, cómo entender al comprador, cómo escribir, cómo conversar. Ahora toca el último acercamiento: **cómo se arma todo eso como sistema**.

### La diferencia entre artesano y operador de sistema

Un SDR que trabaja como **artesano** piensa cada prospecto por separado. Estudia la empresa, escribe el correo, vigila si responde, decide el próximo paso. Funciona muy bien — con 5 prospectos por semana. Con 50, se quema. Con 200, se vuelve imposible.

Un SDR que opera un **sistema** piensa distinto. Diseña una arquitectura donde el volumen es función de la configuración, no del esfuerzo diario. Define sus ICPs (el perfil de cliente ideal: tamaño, rubro, país y demás características que hacen a una empresa buena candidata), sus secuencias, sus cadencias, sus canales. Después alimenta el sistema y vigila las métricas. El trabajo cotidiano es **mantener el sistema corriendo y ajustar cuando hace falta**, no "decidir cada prospecto".

### Por qué importa

Un SDR que trabaja solo a mano, con una cartera chica de cuentas, produce pocas reuniones calificadas al mes. Un SDR que opera un sistema bien diseñado produce del orden de 15 a 20 reuniones al mes. La diferencia no es que uno trabaje más — es que uno **diseñó la infraestructura que multiplica su trabajo**.

### Cuándo conviene el modo artesanal

No es "sistema siempre". Hay casos donde lo artesanal rinde:

- **Cuentas de altísimo valor.** Justifican varias horas de investigación por cuenta.
- **Nuevos mercados donde el ICP es incierto.** Cuando todavía no sabes a quién le estás vendiendo, primero aprendes a mano y, recién cuando entiendes el patrón, armas el sistema.
- **Reactivación de cuentas frías:** cuentas que pasaron por el sistema sin responder y que justifican un acercamiento de nuevo personal.

El resto —la enorme mayoría del trabajo— es sistema. Esta semana se trata de entender cómo se construye ese sistema.

---

## Bloque 2 — Los canales del outbound B2B

En la Semana 2 viste que una empresa B2B genera demanda por cuatro canales —inbound, outbound, referidos y alianzas— y que el outbound es uno de ellos. Ahora abrimos el outbound por dentro. Dentro del outbound se combinan varios **medios de contacto**, que también solemos llamar canales. Ojo con el nivel: estos no son "por dónde entra la demanda" (eso eran los cuatro de la Semana 2), sino "con qué medios contactas en frío". Son cinco.

### El perfil de cada canal

**1. Correo.**

- **Escala:** alta (miles de correos al mes).
- **Fricción inicial:** baja (el prospecto abre o archiva en segundos).
- **Sincronía:** asíncrono (cada uno responde cuando puede, no en el momento).
- **Retorno:** la mayoría de los correos en frío no recibe respuesta; solo una fracción responde, y los buenos remitentes responden bastante mejor que el promedio.
- **Cuándo funciona:** casi siempre, como **canal base**. Si el outbound fuera una dieta, el correo son los carbohidratos.

**2. Teléfono.**

- **Escala:** media-baja (decenas de llamadas al día por SDR).
- **Fricción inicial:** alta (interrumpe).
- **Sincronía:** sincrónico (ocurre en tiempo real, los dos a la vez).
- **Retorno:** conecta pocas veces —la mayoría no atiende un número desconocido—, pero cuando conecta, pesa: la conversación verbal resuelve en tiempo real lo que el correo no resuelve.
- **Cuándo funciona:** como **amplificador del correo**. Después de 2 correos, una llamada hace que tu nombre ya sea familiar.

**3. LinkedIn.**

- **Escala:** media (limitada por el algoritmo y las políticas de la plataforma).
- **Fricción inicial:** baja para conectar, alta para los mensajes (se parecen mucho al spam).
- **Sincronía:** asíncrono.
- **Retorno:** útil para **investigar** y para un **micro-contacto**, no para vender a alto volumen.
- **Cuándo funciona:** como fuente de señales y punto de contacto complementario. Mala idea tratarlo como "otro canal de correo en frío".

**4. WhatsApp.**

- **Escala:** baja (selectivo — solo cuando tienes un número verificado).
- **Fricción inicial:** muy alta si es en frío, baja si es tras un contacto previo.
- **Sincronía:** semi-sincrónico (a veces responden al instante, a veces más tarde).
- **Retorno:** en LATAM B2B es el canal de **mayor tasa de respuesta cuando se usa bien**. Pero si lo usas mal, te bloquean.
- **Cuándo funciona:** como empujón tras un contacto previo, para precalificar después de agendar, o para confirmar el día antes.

**5. Video personalizado.**

- **Escala:** baja (artesanal).
- **Fricción inicial:** variable.
- **Sincronía:** asíncrono, pero con carga emocional alta.
- **Retorno:** cuando es genuino, obtiene del orden de 2 a 3 veces más respuesta que un correo tradicional. Pero toma varios minutos por video.
- **Cuándo funciona:** con cuentas artesanales y reactivaciones de cuentas frías que justifican el tiempo.

### Por qué no existe "el canal mejor"

El SDR novato busca "la receta de canal". La realidad es que cada canal tiene una función dentro del sistema. Querer elegir uno solo es como preguntar qué herramienta es mejor para construir un mueble: usas la sierra para cortar y el martillo para clavar.

---

## Bloque 3 — Multicanal: por qué combinar le gana a usar uno solo

Hay consenso amplio en la industria sobre esto, y se repite año tras año: las secuencias multicanal —correo más llamada más LinkedIn, como mínimo— generan del orden de **2 a 3 veces más respuesta** que las que usan solo correo. La magnitud exacta varía según el contexto, la industria y el rigor del estudio, pero la dirección es consistente (lo viste en la Semana 2).

Y no es marketing — es **consecuencia lógica**. Cada canal alcanza a un subconjunto del ICP. La gente que abre correos no es exactamente la misma que atiende llamadas, ni la misma que acepta LinkedIn. Al combinar 2 o 3 canales, amplías la cobertura.

### Por qué el canal único tiene techo

- **Solo correo:** una parte de los prospectos nunca abre tus correos (filtros, bandeja saturada, desconfianza hacia remitentes desconocidos). Pierdes ese segmento entero.
- **Solo teléfono:** una parte nunca atiende llamadas de desconocidos. Y si no hubo un correo antes, la primera llamada no tiene contexto.
- **Solo LinkedIn:** una parte no usa LinkedIn activamente, y quienes lo usan pueden ignorar mensajes de desconocidos.

El multicanal no elimina esos sesgos — los **diversifica**. Esa diversificación es la razón por la que gana.

### Pero "multicanal" no es "tirar cosas al azar"

El error del novato con el multicanal es: mandar correo, llamar al día siguiente, mandar LinkedIn, mandar WhatsApp y volver a llamar. Todo en cinco días. El prospecto se siente **perseguido**, no valorado. Resultado: reportes, bloqueos, mala fama.

Multicanal bien hecho es **coordinación**, no saturación. Ahí entra la **secuencia**.

---

## Bloque 4 — Concepto de secuencia y cadencia

### Qué es una secuencia

Una secuencia es **un conjunto ordenado de toques multicanal con reglas de ramificación según la respuesta del prospecto**. (Un "toque" es cada contacto individual que haces: un correo, una llamada, un mensaje. "Ramificación" es la regla de qué camino sigue la secuencia según lo que haga el prospecto.)

Sus elementos:

- **Conjunto ordenado:** hay un orden específico — no es una lista al azar.
- **Toques multicanal:** correo, llamada, WhatsApp y LinkedIn combinados.
- **Reglas de ramificación:** qué pasa si el prospecto responde (un camino) y qué pasa si no responde (otro).

Así se ve una secuencia armada, para un decisor con teléfono disponible. No es una plantilla para copiar: es un ejemplo, y su forma depende del contexto.

| Paso | Día | Canal | Acción |
| --- | --- | --- | --- |
| 1 | 0 | Correo | Primer correo con gancho específico |
| 2 | 2 | Correo | Seguimiento asíncrono |
| 3 | 4 | Teléfono | Llamada que referencia los correos |
| 4 | 6 | Correo | Ángulo nuevo + pregunta distinta |
| 5 | 9 | Correo | Seguimiento |
| 6 | 11 | WhatsApp | Empujón (si hay número verificado) |
| 7 | 13 | Teléfono | Segundo y último intento |

**Reglas de ramificación:**

- Si el prospecto responde en cualquier paso → la secuencia automática se pausa y el SDR toma el control manual.
- Si no responde después del último paso → la cuenta se archiva con un recordatorio de recontacto a unos meses.

### Cadencia: el tiempo entre toques

La cadencia es **cuánto pasa entre un toque y el siguiente**. Tres reglas:

**Regla 1 — Ni tan pegado que incomode.** Mandar 3 correos en 4 días al mismo prospecto se siente a persecución. Apretar muchos toques en una semana garantiza el bloqueo.

**Regla 2 — Ni tan separado que te olviden.** Si el toque 1 fue hace tres semanas y el toque 2 es hoy, el prospecto no te conecta con el primer mensaje. Es como arrancar de cero.

**Regla 3 — Acorde a la velocidad del prospecto.** Un C-level (los cargos de máxima jerarquía: gerente general, director financiero y similares) demora más en responder que un mando medio. Un sector regulado (servicios financieros) se mueve más lento que una startup. La cadencia se ajusta al tempo del prospecto, no al tuyo.

### Cuántos toques

La cadencia que mejor rinde combina **pocos toques bien espaciados**: del orden de seis a ocho toques (lo viste en la Semana 2), separados unos días entre sí, dentro de una ventana de un par de semanas. Más toques no es mejor: pasados los primeros, cada toque adicional rinde cada vez menos, y empieza a pesar más el riesgo de molestar que el de que te olviden.

### Ejercicio intercalado 1 — Diseña una secuencia multicanal

Prospecto: **Camila, Directora de Operaciones** de una empresa de e-commerce de 300 empleados. Tienes su correo verificado y su teléfono corporativo (confirmado en LinkedIn). No hay señal urgente — tu gancho se basa en su anuncio de expansión a Chile, hecho hace 30 días.

Diseña una secuencia de **5-6 toques** para Camila. Para cada toque, decide:

- Canal.
- Día (relativo al toque 1).
- Intención del mensaje (qué aporta a la secuencia).

**Respuesta sugerida (una entre varias):**

| Toque | Día | Canal | Intención |
| --- | --- | --- | --- |
| 1 | 0 | Correo | Primer correo con gancho específico (expansión a Chile + desafío típico de operaciones multi-país) |
| 2 | 3 | Correo | Seguimiento corto con ángulo nuevo (caso de una empresa parecida que atravesó la misma expansión) |
| 3 | 5 | Teléfono | Llamada que referencia los correos + apertura con permiso |
| 4 | 8 | Correo | Correo nuevo con pregunta distinta (no repetir) |
| 5 | 12 | Teléfono | Segundo intento de llamada + despedida si no contesta |
| 6 | 15 | Correo | Último correo — cierra abierto ("si esto cambia, aquí estoy") |

Nota: solo seis toques en quince días. No doce en veinte. La disciplina de cortar antes cuida la reputación del remitente y la experiencia del prospecto.

---

## Bloque 5 — La lógica del orden: correo → llamada → WhatsApp

Cuando un buen SDR diseña una secuencia multicanal, no elige el orden por intuición. Hay una lógica operativa detrás.

### Por qué el correo va primero

- **Introduce contexto** sin imponer presencia. El prospecto lo abre si quiere y lo ignora si quiere.
- **Establece el nombre del remitente.** Cuando el teléfono suene unos días después, el nombre no es del todo desconocido.
- **Escala.** Puedes mandar 50 correos en una hora. No puedes hacer 50 llamadas en frío en una hora.
- **Deja registro.** El correo queda escrito — sirve de ancla para conversaciones futuras ("te escribí hace 10 días sobre...").

### Por qué la llamada va después

- **Amplifica el correo.** La llamada llega con contexto ("te escribí la semana pasada") — deja de ser una interrupción al azar.
- **Resuelve en tiempo real** objeciones o dudas que el correo no habría resuelto.
- **Obliga a decidir.** El correo puede quedar "para después"; la llamada pide respuesta ahora.

### Por qué WhatsApp es empujón, no entrada

- **Se percibe como espacio personal.** Meterse ahí sin contacto previo se siente invasivo.
- **El riesgo de bloqueo es alto** si parece spam o masivo.
- **Funciona mejor con contexto previo.** "Te escribí hace unos días sobre tal cosa" + WhatsApp es aceptable. WhatsApp en frío, sin historia, es bloqueo.

### El orden estándar en LATAM B2B

- **Toques 1-2:** correo.
- **Toque 3:** llamada (después de 2 correos).
- **Toques 4-5:** correos con ángulos nuevos.
- **Toque 6:** WhatsApp (si hay número verificado) — empujón.
- **Toque 7:** última llamada.

LinkedIn corre en paralelo: conectar e investigar al mismo tiempo que la secuencia principal, **sin contar como toque de la cadencia**.

---

## Bloque 6 — Las variantes de acceso al decisor según la información disponible

Este es el bloque más importante de la semana. La idea de fondo: según la información que tengas del prospecto, **tu acercamiento cambia**. Hay seis variantes, pero no están todas en el mismo plano, y conviene tener clara la diferencia.

Las **cinco primeras** responden a una sola pregunta: **qué contacto tienes del decisor**. Se resuelven con un árbol de decisión.

La **sexta es de otra naturaleza**. No depende de la información que tengas, sino del **valor de la cuenta**: cuando una cuenta justifica salir del sistema y trabajarla a mano, lo haces sin importar qué datos tengas de ella. Es el modo artesanal del Bloque 1 aplicado al acceso, y puede montarse sobre cualquiera de las cinco anteriores.

### Las cinco variantes según tu contacto del decisor

**1. Tengo correo + teléfono verificados del decisor.**

- **Acercamiento:** multicanal proactivo. El correo abre, la llamada amplifica, WhatsApp empuja (si consigues el número).
- **Secuencia típica:** seis a siete toques en unos trece a quince días.
- **Cuándo aplica:** el escenario más favorable, y el menos frecuente.

**2. Tengo solo correo verificado del decisor (sin teléfono).**

- **Acercamiento:** correo con paciencia. Más toques por correo (cuatro o cinco), cadencia más espaciada, teléfono en la firma para migrar a multicanal si responde.
- **Secuencia típica:** cuatro o cinco correos en unos nueve a doce días.
- **Cuándo aplica:** cuando el decisor no tiene teléfono público o solo aparece su correo.

**3. No tengo contacto del decisor.**

- **Acercamiento:** vía referidores dentro de la empresa. Buscas champions potenciales (un mando medio del área, uno o dos niveles debajo del decisor) y les pides orientación, **no les vendes**. (Un "champion" es un aliado interno que quiere que tú ganes y te orienta desde adentro.)
- **Secuencia típica:** unos cuatro toques por referidor, con varios referidores de la misma empresa.
- **Cuándo aplica:** la mayoría del outbound B2B. Es donde más tiempo invierte el SDR típico.

**4. Un referidor me dio el contacto del decisor.**

- **Acercamiento:** retomas al decisor mencionando al referidor como ancla. La conversión esperada es bastante mayor que la del contacto frío absoluto.
- **Secuencia típica:** cinco o seis toques, con alusión clara al referidor en los primeros dos. La cadencia puede acelerarse (no es frío total).
- **Cuándo aplica:** después del éxito de las secuencias de referidores (variante 3).

**5. Ya contacté antes sin éxito (recontacto).**

- **Acercamiento:** ventana de enfriamiento de unos meses. Cuando lo retomas, **con un ángulo nuevo** — no repetir el mismo mensaje. Referencias la interacción anterior sin culpar al prospecto.
- **Secuencia típica:** tres o cuatro toques compactos con ángulo fresco.
- **Cuándo aplica:** hay que llevar un registro riguroso de cuándo se contactó y con qué resultado.

### La excepción: la cuenta de altísimo valor

**6. Cuenta de altísimo valor.**

- **Acercamiento:** artesanal. Investigación profunda, personalización máxima, video, toques distintos a la secuencia sistemática.
- **Secuencia típica:** no sigue un patrón — depende del contexto de la cuenta.
- **Cuándo aplica:** una porción muy chica de los prospectos: las cuentas cuyo valor potencial justifica salir del sistema.

### Cómo diagnosticar qué variante aplicar

Antes de escribir, primero la **compuerta de valor**: ¿esta cuenta justifica salir del sistema y trabajarla a mano? Si **sí** → variante 6 (artesanal), sin importar qué contacto tengas. Si **no**, sigue el árbol según tu información de contacto:

- ¿Tengo contacto verificado del decisor?
  - **Sí, y me lo pasó un referidor** → variante 4.
  - **Sí, con correo y teléfono** → variante 1.
  - **Sí, solo correo** → variante 2.
- ¿No tengo contacto del decisor?
  - **Nunca lo contacté** → variante 3 (vía referidores).
  - **Ya lo contacté sin éxito** → variante 5 (recontacto).

### Ejercicio intercalado 2 — Identifica la variante correcta

Para cada situación, decide qué variante aplica:

**A.** Prospectas a una fintech chilena. En tu base encuentras al Gerente de Growth con correo y teléfono. Nunca contactaron a esta empresa antes.

**B.** La VP de Marketing tiene correo verificado. El teléfono no aparece. La empresa no fue contactada antes.

**C.** No hay contactos del rol decisor. Encuentras 3 coordinadores y 2 gerentes de mando medio.

**D.** Un Gerente de Proyectos respondió a tu correo en frío diciendo: "Esto lo ve Patricia Fernández, te paso su correo: patricia@empresa.com".

**E.** Hace 5 meses le enviaste una secuencia completa a este decisor. Respondió al cuarto toque diciendo "no es el momento". Pasaron 5 meses y la empresa anunció expansión regional.

**F.** La asistente del CEO de una empresa de altísimo valor para ti aceptó tu solicitud de conexión en LinkedIn y te sigue.

**Respuestas:**

- **A → Variante 1** (correo + teléfono del decisor).
- **B → Variante 2** (solo correo).
- **C → Variante 3** (sin contacto del decisor, hay referidores disponibles).
- **D → Variante 4** (un referidor te dio el contacto del decisor).
- **E → Variante 5** (recontacto tras 5 meses + una señal nueva de expansión para usar como ángulo fresco).
- **F → Variante 6** (cuenta de altísimo valor + un contacto dentro del círculo del CEO = justifica el trabajo artesanal).

**Importante:** lo que aprendes es a diagnosticar, no a memorizar nombres. Cada empresa donde termines trabajando va a llamar a estas variantes de forma distinta. El criterio conceptual se queda.

---

## Bloque 7 — La entregabilidad como concepto fundamental

Puedes escribir el mejor correo en frío del mundo. Si no llega a la bandeja de entrada del prospecto, nada de lo anterior sirve. La **entregabilidad** (en inglés, *deliverability*) es que tus correos efectivamente lleguen a la bandeja de entrada, no a spam ni a promociones.

El SDR no configura la entregabilidad — de eso se encarga el equipo técnico. Pero **tiene que entender los conceptos**, porque determinan si su trabajo sirve o no.

### Los cuatro factores que determinan la entregabilidad

**1. Reputación del dominio.** Cada dominio de envío (el "@" de tu correo) tiene una reputación que los proveedores (Google, Microsoft) llevan por dentro. Un dominio nuevo arranca con reputación baja. Se gana con tiempo, volumen razonable y respuestas reales; se pierde con quejas de spam, rebotes altos y envíos masivos.

**2. Calentamiento.** Un dominio nuevo **no puede mandar envíos masivos desde el primer día**. Necesita calentarse —"calentar un dominio nuevo" es empezar con poco volumen, interactuar con casillas que responden, e ir subiendo de a poco—. Si te saltas el calentamiento, el dominio se quema enseguida y deja de servir.

**3. Volumen por casilla.** Los proveedores limitan cuántos correos puede mandar una sola casilla por día antes de tratarla como spam. Pasar ese techo te marca como remitente masivo y sube la probabilidad de caer a spam.

**4. Autenticación técnica.** SPF, DKIM y DMARC son registros de autenticación que le dicen a los proveedores "este dominio es legítimo". Sin ellos, los correos caen a spam casi automáticamente. Los configura el equipo técnico, pero tú entiendes que existen y para qué sirven.

### Qué es una "casilla quemada"

Una casilla que quedó marcada por los proveedores como mala. Las señales:

- Los rebotes suben.
- La tasa de respuesta cae en seco sin que hayas cambiado el mensaje.
- Los correos empiezan a ir a spam.

Una vez quemada, rehabilitarla toma semanas. Por eso las operaciones serias tienen una reserva de dominios — cuando uno se quema, activan otro.

### Por qué el SDR tiene que entender esto

Aunque no configure nada, el SDR es **parte activa de la higiene de la entregabilidad**. Si carga listas con correos sin validar, los rebotes suben y quema casillas. Si manda volumen excesivo porque "quiere alcance", quema casillas. Si ignora una caída de respuestas, deja que el problema escale.

### Ejercicio intercalado 3 — Diagnóstico por descarte

Un SDR nota que su tasa de respuesta cayó fuerte en las últimas dos semanas. No cambió el mensaje, ni el ICP, ni la cadencia. ¿Cuál es la hipótesis **más probable** y qué revisa primero?

**Hipótesis más probable:** un problema de entregabilidad. Uno o más dominios se quemaron o su reputación cayó.

**Qué revisar, en orden:** primero confirmar que el problema es del **canal** y no del mensaje. ¿Subieron los rebotes? (Señal de una lista mal validada). ¿Cayó la reputación de los dominios activos? ¿Están listos los dominios de reserva? El error del novato ante esta caída es empezar a "probar cosas" en el mensaje: cambiar el asunto, probar variantes, llamar a los prospectos. Pero el problema no es el mensaje — es el canal. Hasta que no se resuelva la entregabilidad, nada de lo demás va a mover la aguja.

---

## Bloque 8 — Las herramientas como instrumentación del concepto

Esta semana aprendiste muchos conceptos. El último cierre es sobre cómo tratar las **herramientas** que los ejecutan.

### La lógica de la instrumentación

Un concepto es una idea operativa. Una herramienta es el software que la ejecuta. **La relación es de una sola dirección:** el concepto vive más allá de la herramienta. Las herramientas se reemplazan; los conceptos se quedan.

Ejemplos:

- **Concepto:** base de datos de prospectos con filtros de ICP y señales. **Herramientas:** Apollo, ZoomInfo, Crunchbase, Lusha.
- **Concepto:** motor de secuencias multicanal con reglas de ramificación. **Herramientas:** Reply.io, Outreach, Salesloft, Instantly, Smartlead.
- **Concepto:** marcador (en inglés, *dialer*) para llamadas con registro en el CRM. **Herramientas:** Aircall, Dialpad, JustCall, CloudTalk.
- **Concepto:** validación de correos antes de enviar. **Herramientas:** ZeroBounce, NeverBounce, Mailfloss.
- **Concepto:** calentamiento automatizado de dominios. **Herramientas:** MailReach, Instantly Warmup, Smartlead Warmup.
- **Concepto:** monitoreo de entregabilidad y reputación. **Herramientas:** Google Postmaster Tools, MXToolbox, GlockApps.

### Por qué esto importa para tu carrera

Si aprendes "Apollo" como si fuera el concepto, cuando tu empresa cambie de herramienta (y en unos años va a pasar) te sientes perdido. Si aprendes el **concepto** ("base de datos de prospectos con filtros y validación"), cuando cambie la herramienta transfieres el conocimiento en una semana, aprendiendo nada más la interfaz nueva.

Peor aún: si te cambias de empresa, te encuentras con un conjunto de herramientas completamente distinto. Las empresas B2B en LATAM usan combinaciones distintas: unas Apollo + Reply.io, otras ZoomInfo + Outreach, otras Lusha + Instantly. **El concepto es el mismo. Las herramientas varían.**

### La regla para el resto de tu carrera

Cada vez que aprendas una herramienta nueva en un trabajo nuevo, pregúntate: *¿qué concepto está instrumentando esta herramienta?* Si la respuesta es clara, la herramienta es fácil. Si la respuesta es "no sé, me dicen que se usa así", cava más hondo hasta entender el porqué.

---

## Síntesis de la semana

Lo que te llevas:

- **El outbound es sistema, no artesanía** (la mayor parte del tiempo). Los SDRs que producen 15 reuniones al mes o más son operadores de sistemas, no artesanos.
- **Cinco canales** con perfiles distintos: correo (base), teléfono (amplificador), LinkedIn (investigación + micro-contacto), WhatsApp (empujón tras contacto) y video (artesanal).
- **El multicanal le gana al canal único.** Del orden de 2 a 3 veces más respuesta.
- **Una secuencia es orden + multicanal + reglas de ramificación.** Cadencia bien calibrada: pocos toques (del orden de seis a ocho) bien espaciados, dentro de una ventana de un par de semanas.
- **La lógica del orden:** correo primero, llamada como amplificador, WhatsApp como empujón tras el contacto.
- **Variantes de acceso al decisor:** cinco según qué contacto tienes del decisor (correo + teléfono / solo correo / sin contacto / dado por un referidor / recontacto), más la cuenta de altísimo valor como excepción que se trabaja a mano. El criterio se queda aunque cada empresa llame a las variantes de otra forma.
- **La entregabilidad** es que el correo llegue a la bandeja de entrada. Cuatro factores: reputación, calentamiento, volumen por casilla y autenticación técnica.
- **Las herramientas instrumentan el concepto.** Cambian; el concepto se queda.

---

## Qué viene en la Semana 8

La próxima semana cierra el curso. Vas a ver:

- El **proceso outbound de punta a punta** (desde el ICP hasta el handoff, el momento en que el SDR entrega el contacto al AE).
- Las **métricas** que importan y las que no.
- El **diagnóstico por descarte** cuando una métrica cae.
- El **mindset de mejora continua**.

Para cerrar el Módulo 4 te quedan la prueba del módulo y una sesión en vivo con el profesor. Además, esta semana empiezas a leer el brief de la prueba final del curso: el caso es largo y conviene que lo leas con calma antes del cierre.

La Semana 8 es la más intensa del curso. Organízate.

---

## Bibliografía

- **Ross, A. & Tyler, M. (2011).** *Predictable Revenue*. PebbleStorm.
- **Bertuzzi, T. (2016).** *The Sales Development Playbook*. Moore-Lake.
- **Frost, A. & otros — HubSpot (2020-2023).** *Sales Statistics & Cold Outreach Benchmarks*. Reportes anuales.
- **Gartner (2020-2023).** *The B2B Buying Journey*. Reports anuales.
- **Google Postmaster Tools.** *Documentación de reputación y entregabilidad de dominios*. Google.
- **Validity / Return Path (2021-2023).** *Email Deliverability Benchmark Report*.
