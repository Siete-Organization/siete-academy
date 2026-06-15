# Kit de armado en Studio — Semana 7 (Módulo 4)

> Para construir los 3 videos **a mano en HeyGen Studio** (decisión 2026-06-11: los
> templates de la cuenta no exponen variable de texto, así que no se generan por API).
> Acá tenés el **texto hablado limpio** de cada video, ya sin `[SLIDE:...]`, sin headers
> ni markdown — listo para pegar en el script del avatar. Fuente: los `.md` corregidos
> de `sem07/` (alineados a `LIMPIO_S7.md` de NICO, regla híbrida ya aplicada).

## Antes de pegar — 3 cosas que aplican a los 3 videos

1. **Activá el Brand Glossary "Video Agent Pronunciation"** (id `0e3e834da76f4f988fac667e40fcbbaf`)
   en el proyecto. Ya tiene: B2B→"bi tu bi", B2C→"bi tu ci", SDR→"es di ar", LOB→"el ou bi".
   Para esta semana, verificá además que **LinkedIn**, **WhatsApp**, **Apollo**, **ZoomInfo**
   y demás nombres de herramientas suenen bien; si alguno se lee raro, agregalo al glosario
   en vez de tocar el texto/subtítulos.
2. **Voz en español:** confirmá que la voz del template renderiza en español (en
   `heygen_defaults.json` la voz figuraba como `language: English` — probable co-causa del
   mal acento). Si suena en inglés, cambiá la voz a la variante ES.
3. **Pausas al enumerar:** donde el guion lista "Uno… Dos… Tres…" o "Variante 1… Variante 2…",
   insertá un **Pause** (botón Pause, ~0.5s) entre cada ítem. El texto ya viene con cada ítem
   en su propio párrafo para que sea fácil ubicarlos.

---

## Video 1 — `intro` · "La maquinaria del outbound" (~3.4 min)

**Fixes visuales en Studio:**
- Animación encima del avatar → quitar/reemplazar el overlay (mismo criterio que S1).
- **[SLIDE: Objetivos de la Semana 7]:** mostrar los 4 objetivos del guion (secuencia
  multicanal / variante de acceso / entregabilidad / herramientas instrumentan el concepto).

**Texto para pegar:**

```
Un SDR que trabaja a mano, prospecto por prospecto, produce del orden de cinco a diez reuniones al mes. Un SDR que opera un sistema produce quince a veinte.

La diferencia no es que uno trabaje más. Es que uno diseñó la infraestructura que multiplica su trabajo.

Esta semana te metes con esa infraestructura.

Hasta acá el curso te dio criterio individual. Cómo leer un negocio, cómo entender al comprador, cómo escribir, cómo conversar. Las Semanas 5 y 6 te enseñaron a construir mensajes que se sostienen y a manejar la conversación real con el prospecto.

Esta semana abre el Módulo 4, El sistema —el último zoom del curso—. Y la pregunta central cambia. Ya no es "cómo lo hago bien yo". Es:

¿Cómo se combinan gente, canales, tiempo e infraestructura para que esto funcione a escala?

Bienvenido a la maquinaria del outbound.

Al terminar esta semana vas a poder hacer cuatro cosas concretas:

Uno. Diseñar una secuencia multicanal coherente para un contexto dado, y justificar cada decisión de orden y de tiempo. Vas a entender por qué el correo va primero, por qué la llamada amplifica, y por qué WhatsApp es empujón y no entrada.

Dos. Identificar la variante de acceso al decisor correcta según la información que tengas del prospecto. Cada empresa le llama distinto; acá lo vas a tratar como un diagnóstico de situación.

Tres. Explicar qué determina si un correo llega a la bandeja de entrada, o no. Vas a entender por qué el mejor correo del mundo, enviado desde una casilla quemada, no convierte nada.

Cuatro. Reconocer que las herramientas instrumentan el concepto; no son el concepto. Esta distinción es la que separa al SDR que transfiere su conocimiento de una empresa a otra del que tiene que aprender todo de cero cada vez que cambia de trabajo.

Estas cuatro cosas son lo que diferencia a un SDR que trabaja a mano de uno que opera un sistema. Y son la base de la Semana 8, donde vamos a juntar todo el curso.

Una cosa importante. Esta semana también arrancas a leer el brief de la prueba final del curso, que cierras en la Semana 8. El caso es largo y exige criterio integrado de los cuatro módulos. Te conviene tener tiempo para leerlo con calma esta semana.

Vamos al contenido. Nos vemos en el siguiente video.
```

---

## Video 2 — `contenido_1` · "Del artesano al sistema" (Bloques 1-4, ~8 min)

**Fixes visuales en Studio:**
- Animación encima del avatar → quitar/reemplazar overlay.
- **[SLIDE: Los 5 canales del outbound B2B]:** que aparezcan los 5 (correo, teléfono,
  LinkedIn, WhatsApp, video), no solo 3 o 4.
- **Caso Camila:** mostrar la tabla/timeline de los 6 toques en 15 días y las 4 opciones (a-d).

**Texto para pegar:**

```
Un SDR que trabaja como artesano piensa cada prospecto por separado: estudia la empresa, escribe el correo, vigila si responde, decide el próximo paso. Funciona muy bien con cinco prospectos por semana. Con cincuenta, se quema. Con doscientos, se vuelve imposible.

Un SDR que opera un sistema piensa distinto. Y produce el triple de reuniones.

En este video cubrimos los primeros cuatro temas de la semana: la diferencia entre trabajar a mano y operar un sistema, los cinco canales del outbound B2B y para qué sirve cada uno, por qué combinar canales le gana a usar uno solo, y qué es exactamente una secuencia con su cadencia. Cierra con un caso para que diseñes una secuencia.

Un SDR artesano piensa cada prospecto por separado. Estudia la empresa, escribe el correo, vigila la respuesta, decide el próximo paso. Cada decisión es manual. A cinco prospectos por semana funciona; a cincuenta, se quema; a doscientos, no escala.

Un SDR que opera un sistema diseña una arquitectura donde el volumen es función de la configuración, no del esfuerzo diario. Define sus clientes ideales, sus secuencias, sus cadencias, sus canales. Después alimenta el sistema y vigila las métricas. El trabajo cotidiano es mantener el sistema corriendo y ajustar cuando hace falta, no "decidir cada prospecto".

Un SDR que trabaja solo a mano, con una cartera chica de cuentas, produce pocas reuniones calificadas al mes. Un SDR que opera un sistema bien diseñado produce del orden de quince a veinte reuniones al mes. No es que trabaje más. Es que diseñó la infraestructura que multiplica su trabajo.

No es "sistema siempre". Hay tres casos donde lo artesanal gana. Cuentas de altísimo valor, que justifican varias horas de investigación por cuenta. Nuevos mercados donde el cliente ideal todavía es incierto: primero aprendes a mano y, recién cuando entiendes el patrón, armas el sistema. Y la reactivación de cuentas frías que pasaron por el sistema sin responder. El resto —la enorme mayoría del trabajo— es sistema.

En la Semana 2 viste que una empresa B2B genera demanda por cuatro canales —inbound, outbound, referidos y alianzas—. Ahora abrimos el outbound por dentro. Adentro se combinan cinco medios de contacto, que también solemos llamar canales. La pregunta correcta no es "cuál es el mejor". Es qué hace cada uno.

Correo. Escala alta —miles de correos al mes—. Fricción baja: el prospecto abre o archiva en segundos. Asíncrono. La mayoría de los correos en frío no recibe respuesta; solo una fracción responde, y los buenos remitentes responden bastante mejor que el promedio. Es el canal base. Si el outbound fuera una dieta, el correo son los carbohidratos.

Teléfono. Escala media-baja —decenas de llamadas al día—. Alta fricción: interrumpe. Conecta pocas veces, porque la mayoría no atiende un número desconocido; pero cuando conecta, pesa, porque la conversación verbal resuelve en el momento lo que el correo no resuelve. Funciona como amplificador del correo: después de dos correos, una llamada hace que tu nombre ya sea familiar.

LinkedIn. Escala media, limitada por el algoritmo y las políticas de la plataforma. Baja fricción para conectar, alta para los mensajes —se parecen mucho al spam—. Sirve para investigar y para un micro-contacto, no para vender a alto volumen. Mala idea tratarlo como "otro canal de correo en frío".

WhatsApp. Escala baja, selectivo —solo cuando tienes un número verificado—. Muy alta fricción si es en frío, baja si hubo un contacto previo. En LATAM B2B es el canal de mayor tasa de respuesta cuando se usa bien. Pero si lo usas mal, te bloquean. Sirve como empujón tras un contacto previo, no como entrada.

Video personalizado. Escala baja, artesanal. Cuando es genuino, obtiene del orden de dos a tres veces más respuesta que un correo tradicional. Pero toma varios minutos por video. Sirve para cuentas artesanales y reactivaciones de cuentas frías que justifican el tiempo.

El correo abre. El teléfono amplifica. LinkedIn da información. WhatsApp empuja. El video rescata. Los cinco juntos son la maquinaria. Querer elegir uno solo es como preguntar qué herramienta es mejor para construir un mueble: usas la sierra para cortar y el martillo para clavar. No compiten.

Hay consenso amplio en la industria sobre esto, y se repite año tras año: las secuencias multicanal —correo más llamada más LinkedIn, como mínimo— generan del orden de dos a tres veces más respuesta que las que usan solo correo. Lo viste en la Semana 2.

Y no es marketing. Es consecuencia lógica. Cada canal alcanza a un subconjunto del cliente ideal. La gente que abre correos no es exactamente la misma que atiende llamadas, ni la misma que acepta LinkedIn. Al combinar dos o tres canales, amplías la cobertura.

Mira lo que pasa con un solo canal. Solo correo: una parte de los prospectos nunca abre tus correos —filtros, bandeja saturada, desconfianza— y pierdes ese segmento entero. Solo teléfono: una parte nunca atiende llamadas de desconocidos, y sin un correo antes, la primera llamada no tiene contexto. Solo LinkedIn: una parte no lo usa activamente, y quienes lo usan pueden ignorar a desconocidos. El multicanal no elimina esos sesgos: los diversifica. Esa diversificación es la razón por la que gana.

Una advertencia. El error del novato es mandar un correo, llamar al día siguiente, mandar LinkedIn, mandar WhatsApp y volver a llamar, todo en cinco días. ¿Resultado? El prospecto se siente perseguido, no valorado. Reportes, bloqueos, mala fama.

Multicanal bien hecho es coordinación, no saturación. Y la coordinación se llama secuencia.

Una secuencia es un conjunto ordenado de toques multicanal, con reglas de ramificación según la respuesta del prospecto. Tres cosas: un orden específico —no una lista al azar—, toques multicanal —correo, llamada, WhatsApp y LinkedIn combinados—, y reglas de qué pasa según el prospecto responda o no.

Si responde en cualquier paso, la secuencia automática se pausa y el SDR toma el control manual. Si no responde después del último paso, la cuenta se archiva con un recordatorio de recontacto a unos meses.

La cadencia es cuánto tiempo pasa entre un toque y el siguiente. Tres reglas.

Una. Ni tan pegado que incomode. Tres correos en cuatro días al mismo prospecto se sienten a persecución. Apretar muchos toques en una semana garantiza el bloqueo.

Dos. Ni tan separado que te olviden. Si el toque uno fue hace tres semanas y el toque dos es hoy, el prospecto no te conecta con el primer mensaje. Es como arrancar de cero.

Tres. Acorde a la velocidad del prospecto. Un alto ejecutivo demora más en responder que un mando medio. Un sector regulado, como servicios financieros, se mueve más lento que una startup. La cadencia se ajusta al tempo del prospecto, no al tuyo.

La cadencia que mejor rinde combina pocos toques bien espaciados: del orden de seis a ocho toques —lo viste en la Semana 2—, separados unos días entre sí, dentro de una ventana de un par de semanas. Más toques no es mejor: pasados los primeros, cada toque adicional rinde cada vez menos, y empieza a pesar más el riesgo de molestar que el de que te olviden.

Vamos con un caso para que diseñes una secuencia.

Camila es Directora de Operaciones de una empresa de e-commerce de trescientos empleados. Tienes su correo verificado y su teléfono corporativo, confirmado en LinkedIn. No hay señal urgente: el gancho se basa en su anuncio de expansión a Chile, hecho hace treinta días.

Te muestro una secuencia posible. Toque uno, día cero: correo con gancho específico —la expansión a Chile—. Toque dos, día tres: correo con ángulo nuevo —un caso de una empresa parecida—. Toque tres, día cinco: llamada que referencia los correos. Toque cuatro, día ocho: correo con una pregunta distinta. Toque cinco, día doce: segunda llamada, con despedida si no contesta. Toque seis, día quince: último correo, que cierra abierto.

Pregunta: ¿Cuál es la decisión clave de este diseño?

a) Que usa muchos canales distintos.
b) Que arranca con teléfono para sorprender al prospecto.
c) Que se limita a seis toques en quince días, en vez de saturar con doce toques en veinte días.
d) Que termina con una llamada agresiva.

¿Elegiste la c? Estás en lo correcto, prestaste atención.

Solo seis toques en quince días. No doce en veinte. La disciplina de cortar antes cuida dos cosas: la reputación del remitente y la experiencia del prospecto. El instinto del novato es agregar más toques "porque más es más". Pero pasados los primeros, cada toque adicional rinde cada vez menos. Lo que ganas en cobertura, lo pierdes en irritación.

Complementa este contenido con las guías adjuntas al módulo. Ahí vas a encontrar el desarrollo completo de los cuatro bloques: el perfil de cada uno de los cinco canales con escala, fricción y retorno; los tres casos donde lo artesanal sí rinde; la secuencia tipo de siete toques con sus reglas de ramificación; y las tres reglas de cadencia con ejemplos.

Ya tienes la diferencia entre artesano y sistema, los cinco canales, por qué combinar le gana a usar uno solo, y qué es una secuencia con su cadencia.

En el segundo video respondemos las preguntas que faltan: por qué el orden de los canales no es intuición sino lógica operativa, cómo diagnosticar la variante de acceso al decisor según la información que tienes, qué determina que un correo llegue a la bandeja de entrada, y por qué las herramientas instrumentan el concepto, pero no son el concepto.

Nos vemos en el video 2.
```

> Nota: el bloque "Fuentes de este video" del `.md` es para la sección de Bibliografía en
> la plataforma, **no se narra** — no lo pegues en el script del avatar.

---

## Video 3 — `contenido_2` · "Orden, variantes, entregabilidad y herramientas" (Bloques 5-8, ~8.5 min)

**Fixes visuales en Studio:**
- Animación encima del avatar → quitar/reemplazar overlay.
- **[SLIDE: Las 6 variantes]:** que se vean las 6 completas —incluida la 5 (recontacto con
  ángulo nuevo) y la 6 (cuenta de altísimo valor, artesanal)—. No cortar en 4.
- **[SLIDE: Los 4 factores]** de entregabilidad: reputación, calentamiento, volumen por
  casilla, autenticación.
- **Caso de variantes:** mostrar el enunciado y las 4 opciones (a-d).

**Texto para pegar:**

```
Cuando un buen SDR diseña una secuencia multicanal, no elige el orden por intuición. Cuando manda correos, no asume que llegan a la bandeja de entrada. Y cuando aprende una herramienta, no la confunde con el concepto que esa herramienta ejecuta.

Esos son los cuatro temas que cierran la semana.

En este video cubrimos los últimos cuatro temas: por qué el orden correo–llamada–WhatsApp tiene una lógica operativa concreta, las seis variantes de acceso al decisor según la información que tengas, qué es la entregabilidad y por qué te importa aunque no la configures, y la regla más valiosa de la semana: las herramientas instrumentan el concepto, no son el concepto. Cierra con un caso de variantes y la síntesis de la semana.

Cuatro razones por las que el correo va primero. Una. Introduce contexto sin imponer presencia: el prospecto lo abre si quiere y lo ignora si quiere. Dos. Establece el nombre del remitente, así cuando el teléfono suene unos días después, el nombre no es del todo desconocido. Tres. Escala: puedes mandar cincuenta correos en una hora, no cincuenta llamadas en frío. Cuatro. Deja registro: el correo queda escrito y sirve de ancla para conversaciones futuras —"te escribí hace diez días sobre…"—.

La llamada va después por tres razones. Amplifica el correo: llega con contexto —"te escribí la semana pasada"— y deja de ser una interrupción al azar. Resuelve en tiempo real objeciones o dudas que el correo no habría resuelto. Y obliga a decidir: el correo puede quedar "para después"; la llamada pide respuesta ahora.

WhatsApp es empujón, no entrada, por tres razones, todas críticas. Se percibe como espacio personal: meterse ahí sin contacto previo se siente invasivo. El riesgo de bloqueo es alto si parece spam o masivo, y un bloqueo es definitivo. Y funciona mejor con contexto previo: "te escribí hace unos días sobre tal cosa" más WhatsApp es aceptable; WhatsApp en frío, sin historia, es bloqueo.

El orden estándar en LATAM B2B. Toques uno y dos, correo. Toque tres, llamada —después de dos correos—. Toques cuatro y cinco, correos con ángulos nuevos. Toque seis, WhatsApp si hay número verificado —empujón—. Toque siete, última llamada. LinkedIn corre en paralelo: conectar e investigar al mismo tiempo que la secuencia principal, sin contar como toque de la cadencia.

Este es el bloque más importante de la semana. La idea de fondo: según la información que tengas del prospecto, tu acercamiento cambia. Hay seis variantes, pero no están todas en el mismo plano.

Las cinco primeras responden a una sola pregunta: qué contacto tienes del decisor. Se resuelven con un árbol de decisión. La sexta es de otra naturaleza: no depende de la información que tengas, sino del valor de la cuenta.

Variante 1. Tienes correo y teléfono verificados del decisor. Acercamiento: multicanal proactivo —el correo abre, la llamada amplifica, WhatsApp empuja—. Secuencia típica: seis a siete toques en unos trece a quince días. Es el escenario más favorable, y el menos frecuente.

Variante 2. Tienes solo correo verificado, sin teléfono. Acercamiento: correo con paciencia. Más toques por correo —cuatro o cinco—, cadencia más espaciada, y el teléfono en la firma para migrar a multicanal si responde. Aplica cuando el decisor no tiene teléfono público.

Variante 3. No tienes contacto del decisor. Acercamiento: vía referidores dentro de la empresa. Buscas champions potenciales —un mando medio del área, uno o dos niveles debajo del decisor— y les pides orientación. No les vendes. Es la mayoría del outbound B2B, donde más tiempo invierte el SDR típico.

Variante 4. Un referidor te dio el contacto del decisor. Acercamiento: retomas al decisor mencionando al referidor como ancla, sobre todo en los primeros dos toques. La conversión esperada es bastante mayor que la del contacto frío absoluto, y la cadencia puede acelerarse porque ya no es frío total.

Variante 5. Ya contactaste antes sin éxito —recontacto—. Acercamiento: ventana de enfriamiento de unos meses. Cuando lo retomas, lo haces con un ángulo nuevo —no repites el mismo mensaje—. Referencias la interacción anterior sin culpar al prospecto. Secuencia típica: tres o cuatro toques compactos con ángulo fresco. Exige llevar un registro riguroso de cuándo contactaste y con qué resultado.

Variante 6. Cuenta de altísimo valor. Esta es de otra naturaleza: no depende de qué datos tengas, sino de que el valor de la cuenta justifique salir del sistema y trabajarla a mano. Acercamiento: artesanal —investigación profunda, personalización máxima, video, toques distintos a la secuencia sistemática—. No sigue un patrón: depende del contexto de la cuenta. Aplica a una porción muy chica de los prospectos, y puede montarse sobre cualquiera de las cinco anteriores.

Cómo diagnosticar la variante. Antes de escribir, primero la compuerta de valor: ¿esta cuenta justifica salir del sistema y trabajarla a mano? Si sí, variante 6, sin importar qué contacto tengas. Si no, sigues el árbol según tu información: ¿tienes contacto verificado del decisor? Si te lo pasó un referidor, variante 4; si tienes correo y teléfono, variante 1; si tienes solo correo, variante 2. ¿No tienes contacto del decisor? Si nunca lo contactaste, variante 3 —vía referidores—; si ya lo contactaste sin éxito, variante 5 —recontacto—.

Una nota para tu carrera. Cada empresa donde termines trabajando va a llamar a estas variantes de forma distinta. Lo que aprendes es a diagnosticar, no a memorizar nombres. El nombre cambia; el criterio conceptual se queda.

Puedes escribir el mejor correo en frío del mundo. Si no llega a la bandeja de entrada del prospecto, nada de lo anterior sirve. La entregabilidad es que tus correos efectivamente aterricen en la bandeja de entrada, y no en spam ni en promociones. El SDR no configura la entregabilidad —de eso se encarga el equipo técnico— pero tiene que entender los conceptos, porque determinan si su trabajo sirve o no.

Cuatro factores. Reputación del dominio. El arroba de tu correo tiene una reputación que los proveedores —Google, Microsoft— llevan por dentro. Un dominio nuevo arranca con reputación baja. Se gana con tiempo, volumen razonable y respuestas reales; se pierde con quejas de spam, rebotes altos y envíos masivos.

Calentamiento. Calentar un dominio nuevo es subir el volumen de a poco. Un dominio nuevo no puede mandar envíos masivos desde el primer día: empieza con poco, interactúa con casillas que responden, y sube de a poco. Si te saltas el calentamiento, el dominio se quema enseguida.

Volumen por casilla. Los proveedores limitan cuántos correos puede mandar una sola casilla por día antes de tratarla como spam. Pasar ese techo te marca como remitente masivo y sube la probabilidad de caer a spam.

Autenticación técnica. Existen unos registros de autenticación del dominio —los vas a oír nombrar como SPF, DKIM y DMARC— que le dicen a los proveedores "este dominio es legítimo". Los configura el equipo técnico; tú solo entiendes que existen y para qué sirven.

Una casilla quemada es una que quedó marcada por los proveedores como mala. Las señales: los rebotes suben, la tasa de respuesta cae en seco sin que hayas cambiado el mensaje, y los correos empiezan a ir a spam. Rehabilitarla toma semanas. Por eso las operaciones serias tienen una reserva de dominios: cuando uno se quema, activan otro.

Aunque no configures nada, eres parte activa de la higiene. Si cargas listas con correos sin validar, los rebotes suben y quemas casillas. Si mandas volumen excesivo "porque quieres alcance", quemas casillas. Si ignoras una caída de respuestas, dejas que el problema escale.

Un concepto es una idea operativa. Una herramienta es el software que la ejecuta. La relación es de una sola dirección: el concepto vive más allá de la herramienta. Las herramientas se reemplazan; los conceptos se quedan.

Base de datos de prospectos con filtros y señales: Apollo, ZoomInfo, Crunchbase, Lusha. Motor de secuencias multicanal: Reply, Outreach, Salesloft, Instantly, Smartlead. Marcador para llamadas: Aircall, Dialpad, JustCall. Validación de correos antes de enviar: ZeroBounce, NeverBounce. Calentamiento automatizado de dominios: MailReach, Smartlead Warmup. Monitoreo de entregabilidad: Postmaster Tools, MXToolbox, GlockApps. En cada par, el concepto está estable. La columna de herramientas es la que cambia.

Si aprendes "Apollo" como si fuera el concepto, cuando tu empresa cambie de herramienta —y en unos años va a pasar— te vas a sentir perdido. Si aprendes el concepto —"base de datos de prospectos con filtros y validación"—, transfieres el conocimiento en una semana, aprendiendo nada más la interfaz nueva. Cada vez que aprendas una herramienta nueva, pregúntate: "¿qué concepto está instrumentando esta herramienta?" Si la respuesta es clara, la herramienta es fácil. Si la respuesta es "me dicen que se usa así", cava más hondo hasta entender el porqué.

Vamos con un caso para que diagnostiques la variante.

Hace cinco meses le enviaste una secuencia completa a un decisor en una fintech chilena. Respondió al cuarto toque diciendo: "No es el momento." Pasaron cinco meses. La empresa anunció expansión regional la semana pasada.

Pregunta: ¿Qué variante aplica?

a) Variante 1: correo más teléfono del decisor.
b) Variante 3: sin contacto del decisor, vía referidores.
c) Variante 5: recontacto tras el enfriamiento, con un ángulo nuevo —la expansión—.
d) Variante 6: cuenta de altísimo valor, artesanal.

¿Elegiste la c? Estás en lo correcto, prestaste atención.

Tres elementos clave: ya pasó la ventana de enfriamiento de unos meses, apareció una señal nueva —la expansión—, y el "no es el momento" original dejó la puerta abierta, no fue rechazo definitivo. Es el escenario clásico de la variante 5. Retomas con un ángulo fresco, referencias brevemente el contacto anterior sin culpar al prospecto, y el ángulo es la expansión, no el producto.

El error del novato sería tratar esto como contacto frío y arrancar de cero. Pero ya tienes historia. Aprovéchala.

Recapitulemos lo que te llevas:

Uno. El outbound es sistema, no artesanía la mayor parte del tiempo. Los SDRs que producen quince reuniones al mes o más son operadores de sistemas, no artesanos.

Dos. Cinco canales, cinco funciones. Correo abre, teléfono amplifica, LinkedIn da información, WhatsApp empuja, video rescata. Querer elegir uno solo rompe la maquinaria.

Tres. El multicanal le gana al canal único —del orden de dos a tres veces más respuesta— porque diversifica los sesgos del prospecto. Pero solo si es coordinación, no saturación.

Cuatro. Una secuencia es orden más multicanal más reglas de ramificación. Cadencia bien calibrada: pocos toques —del orden de seis a ocho— bien espaciados, dentro de una ventana de un par de semanas.

Cinco. Seis variantes de acceso al decisor: cinco según qué contacto tienes del decisor, más la cuenta de altísimo valor como excepción que se trabaja a mano. No es "ruta", es diagnóstico. Y el criterio se transfiere entre empresas.

Seis. La entregabilidad define si tu trabajo sirve: que el correo llegue a la bandeja de entrada. Cuatro factores —reputación, calentamiento, volumen por casilla y autenticación—.

Siete. Las herramientas instrumentan el concepto. Si dominas el concepto, te adaptas en días a cualquier conjunto de herramientas. Si solo dominas la herramienta, arrancas de cero cada vez.

Complementa este contenido con las guías adjuntas al módulo. Ahí desarrollamos las seis variantes una por una con su secuencia típica y su ejemplo, los cuatro factores de entregabilidad con casos de diagnóstico de casillas quemadas, los pares de concepto-herramienta detallados, y más casos del ejercicio de variantes para que practiques.

En la Semana 8 cerramos el curso. Juntamos todo: el proceso de punta a punta del SDR, las métricas que de verdad importan, el diagnóstico por descarte cuando una métrica cae, y el mindset de mejora continua. Y cierras el caso de la prueba final que arrancaste a leer esta semana.

Nos vemos la semana que viene.
```

> Nota: el bloque "Fuentes de este video" del `.md` es para la Bibliografía en plataforma,
> **no se narra**.
