# Kit de armado en Studio — Semana 2 (Módulo 1)

> Para construir los 3 videos **a mano en HeyGen Studio** (decisión 2026-06-11: los
> templates de la cuenta no exponen variable de texto, así que no se generan por API).
> Acá tenés el **texto hablado limpio** de cada video, ya sin `[SLIDE:...]`, sin headers
> ni markdown — listo para pegar en el script del avatar. Fuente: los `.md` corregidos
> de `sem02/` (alineados a `LIMPIO_S2.md` de NICO).

## Antes de pegar — 3 cosas que aplican a los 3 videos

1. **Activá el Brand Glossary "Video Agent Pronunciation"** (id `0e3e834da76f4f988fac667e40fcbbaf`)
   en el proyecto. Ya tiene: B2B→"bi tu bi", B2C→"bi tu ci", SDR→"es di ar", LOB→"el ou bi".
   Para esta semana suman siglas habladas: **AE→"ei i"**, **CSM→"ci es em"**, **ABM→"ei bi em"**.
   Esto arregla la pronunciación sin tocar el texto/subtítulos.
2. **Voz en español:** confirmá que la voz del template renderiza en español (en
   `heygen_defaults.json` la voz figuraba como `language: English` — probable co-causa del
   mal acento). Si suena en inglés, cambiá la voz a la variante ES.
3. **Pausas al enumerar:** donde el guion lista "Uno… Dos… Tres…" (o "Criterio uno…
   Criterio dos…"), insertá un **Pause** (botón Pause, ~0.5s) entre cada ítem. El texto ya
   viene con cada ítem en su propio párrafo para que sea fácil ubicarlos.

---

## Video 1 — `intro` · "El rol del SDR — qué te llevas esta semana" (~3 min)

**Texto para pegar:**

```
Imagina que conseguiste la reunión. El prospecto te dice: "Dame precios y me cuentas cómo funciona la integración."

Lo que respondas en los próximos diez segundos puede valer veinte mil dólares al año. O puede quemar la venta antes de que el vendedor que cierra entre a la mesa.

En la Semana 1 viste cómo compra una empresa: comité, capas invisibles, etapas del buying cycle, roles del comité de decisión. Esa semana fue del otro lado de la mesa.

Esta semana cambiamos de lado. Vamos al tuyo. La pregunta central es: ¿qué vende un SDR realmente, y hasta dónde llega su responsabilidad?

Es la semana de cierre del Módulo 1. Te quiero anticipar qué vas a poder hacer al final.

Al terminar esta semana vas a poder hacer seis cosas concretas:

Uno. Ubicar al SDR dentro de la función comercial B2B completa —marketing, el SDR, el AE (el vendedor que cierra) y el encargado de cuidar al cliente ya firmado—, y entender por qué los cuatro roles existen separados.

Dos. Distinguir los cuatro canales por donde una empresa genera demanda —inbound, outbound, referidos y alianzas—, y saber cuándo aplica cada uno.

Tres. Explicar qué es el outbound —la prospección en frío— específicamente, las tres condiciones para que tenga sentido, y los escenarios donde simplemente no aplica. Esto último te ahorra meses trabajando contra un canal mal elegido.

Cuatro. Separar los hitos que vende el SDR de los que vende el AE. Este es el concepto pilar de la semana. Si lo internalizas, casi todos los errores típicos del SDR novato desaparecen.

Cinco. Aplicar los cuatro criterios de una reunión calificada a un caso concreto —que la empresa encaje con tu cliente ideal, que el contacto sea quien decide o un aliado validado, que asista, y que pase la precalificación—.

Seis. Articular qué significa un buen handoff —el pase del prospecto del SDR al AE—, y por qué es la pieza más infravalorada del rol moderno.

Esta semana cierra el Módulo 1. Al final te van a esperar dos cosas más: la prueba del Módulo 1 y el cierre del módulo. Organízate para llegar a las dos antes de arrancar el Módulo 2.

Vamos al contenido. Nos vemos en el siguiente video.
```

---

## Video 2 — `contenido_1` · "Tu lugar en la función comercial y los hitos que vendes" (Bloques 1-4, ~8.5 min)

**Fixes visuales en Studio:**
- **Los canales de demanda:** si la slide los muestra como iconos, deben ser **4**
  —inbound, outbound, referidos, alianzas—. **No incluir ABM como quinto canal** (ABM va
  como "estrategia", no como canal). La versión vieja con 5 canales quedó obsoleta.
- **La cadena de hitos:** la slide debe mostrar **5 hitos** (Reunión → Asistencia +
  precalificación → Demostración → Propuesta → Cierre). **Quitar el sexto hito**
  ("Renovación/expansión"): ya no es parte de la cadena.
- Animación encima del avatar → quitar/reemplazar overlay.

**Texto para pegar:**

```
Si te tuviera que apostar todo el curso a un solo concepto, sería este.

La diferencia entre un SDR bueno y uno promedio no es cuánto trabaja. No es cuántos emails manda. Es entender exactamente qué hito le toca vender, y qué hito no le toca.

Eso es lo que vamos a construir hoy.

En este video cubrimos los primeros cuatro temas de la semana: cómo se organiza tu lado de la mesa, los cuatro canales por donde una empresa genera demanda, qué es el outbound y cuándo no aplica, y —el concepto pilar de toda la semana— la cadena de hitos y qué vendes tú dentro de ella. Cierra con un caso que te va a doler la primera vez que lo veas.

De tu lado de la mesa hay un equipo, aunque desde afuera no se vea. Hay cuatro roles principales.

Marketing. Genera demanda entrante: contenido, anuncios, posicionamiento en buscadores, charlas online. Opera antes del primer contacto comercial. Se le mide por los contactos interesados que entrega y cuánto cuesta cada uno.

SDR. Prospecta en frío, califica contactos y agenda reuniones. Opera entre el contacto inicial y la oportunidad real. Se le mide por reuniones calificadas agendadas. Este es tu rol.

AE —Account Executive, el vendedor que cierra—. Cierra ventas. Toma la reunión que le pasas, hace la demostración, profundiza, negocia y firma. Se le mide por el ingreso cerrado.

CSM —Customer Success Manager, el que cuida al cliente ya firmado—. Lo maneja después de la venta: la puesta en marcha, la renovación, que crezca. Se le mide por que el cliente se quede, crezca y esté satisfecho.

¿Por qué existen separados? Porque prospectar en frío exige una mentalidad y una disciplina distintas a cerrar ventas, y mezclar las dos tareas en una misma persona hace que una de las dos se sacrifique. Esa separación es lo que permite que una empresa crezca de forma ordenada. Un AE que también prospecta deja de prospectar cuando tiene ventas activas —que son las que le pagan las comisiones—. El flujo de nuevos negocios entra en olas. Un SDR dedicado prospecta todo el día. El flujo se vuelve parejo y los números, predecibles.

Sácalo en limpio: no eres un AE chico, no eres un asistente del AE. Eres un rol específico con métricas propias.

No todo contacto entra por el mismo camino. Una empresa B2B madura usa cuatro canales en paralelo.

Uno. Inbound —el cliente llega solo a ti—. El prospecto viene a ti, atraído por contenido o anuncios. Cuando aparece ya investigó. Menos resistencia, mejor conversión, pero caro de construir.

Dos. Outbound —tú lo contactas en frío—. Es lo que vas a hacer los próximos seis meses. Escalable y enfocable —eliges a quién le hablas—, pero con mucha resistencia y tasas de respuesta bajas.

Tres. Referidos. Alguien —un cliente contento, un empleado, un socio— te presenta al prospecto. Es el canal de mayor conversión —a veces diez veces más que el outbound—, pero de volumen variable. No se puede forzar.

Cuatro. Alianzas. Otra empresa —un integrador, un proveedor complementario, un canal de distribución— te trae contactos ya calificados. Es el de mayor apalancamiento, pero el más lento de construir.

Una aclaración. Quizás escuches hablar de ABM —marketing basado en cuentas—. Ojo: ABM no es un canal, es una estrategia, una forma de elegir y trabajar a quién le hablas. En vez de prospectar muchas empresas en general, eliges un grupo chico de cuentas muy estratégicas y montas campañas muy personalizadas sobre ellas. Lo importante: ABM se monta sobre los canales de arriba —sobre todo el outbound—, no los reemplaza.

Implicación para ti: aunque tu canal principal es el outbound, los otros se van a cruzar con el tuyo todo el tiempo. Saber cuál está operando en cada caso te ahorra mensajes mal calibrados.

El outbound B2B es el proceso sistemático de identificar empresas que encajan con tu cliente ideal, contactarlas en frío por varios canales —email, llamada, LinkedIn, WhatsApp—, y llevarlas a aceptar una reunión con el AE.

Tres palabras clave: sistemático —es un proceso repetible, no magia personal—, en frío —el prospecto no te pidió nada, no te conoce—, y varios canales —combinarlos genera alrededor de tres veces más respuesta que cualquier canal usado solo—.

El outbound funciona cuando se cumplen tres condiciones al mismo tiempo. Una. Cliente ideal identificable y alcanzable —puedes armar la lista de empresas que cumplen criterios claros—. Dos. Un precio que justifica el costo —un software B2B típico de quinientos a cinco mil dólares al mes, o ventas de una vez de diez mil para arriba en servicios—. Tres. Un ciclo de venta que aguanta el modelo —contactar al prospecto seis u ocho veces antes de la reunión—.

El outbound no aplica en tres escenarios: productos masivos de precio bajo, un cliente ideal demasiado amplio y sin distinción, y ventas que dependen al cien por ciento de una demostración visual.

Y un dato que define cómo medir tu propio trabajo: quince reuniones calificadas al mes es un buen punto de partida para un SDR bien entrenado, con margen de mejora hasta unas veinte. La conversión de empresa contactada a reunión agendada está entre uno y tres por ciento. Y el tiempo hasta producir a pleno es de tres a cuatro meses. No se lo dices al prospecto. Lo sabes tú, para no desanimarte cuando los primeros meses no parecen brillantes.

Acá llegamos al concepto pilar de la semana. Una venta B2B completa pasa por cinco hitos secuenciales, cada uno con un responsable distinto.

Uno. Reunión. El prospecto acepta encontrarse con el AE. Responsable: SDR.

Dos. Asistencia más precalificación. Llega a la reunión y pasa los cuatro criterios mínimos. Responsable: SDR.

Tres. Demostración. El AE presenta el producto y profundiza en la necesidad. Responsable: AE.

Cuatro. Propuesta. Responsable: AE.

Cinco. Cierre. El prospecto firma. Responsable: AE.

La venta se cierra en el hito cinco. Lo que viene después —que el cliente renueve o compre más— ya no es parte de esta cadena: es la relación con el cliente ya firmado, y vive en otra área. No es parte de la venta ni trabajo del SDR.

El SDR vende dos cosas, no la cadena entera. La reunión, y la asistencia más precalificación. No vende la demostración, no vende la propuesta, no vende el cierre.

¿Por qué importa tanto? Porque un SDR novato —con ganas y miedo a perder el negocio— cruza hitos. Tres cruces típicos: hace una mini-demo por teléfono y quema la curiosidad antes de tiempo. Da un rango de precio y el AE pierde margen. Ofrece una concesión y regala algo sin nada a cambio.

Regla práctica: cuando un prospecto te pregunta algo fuera de tu zona, lo rediriges al AE. No es cortarlo. Es ponerlo en el lugar correcto.

Vamos con un caso para que veas lo fácil que es caer.

Prospecto Martín: "Me interesa lo que plantean. Cuéntame, ¿cómo manejan ustedes la integración con Salesforce? Porque tenemos cinco años con Salesforce y no queremos migrar datos."

SDR: "Excelente que preguntes, Martín. Nuestra plataforma tiene un conector nativo con Salesforce que sincroniza en tiempo real, no hace falta migrar, se integra con tu instancia actual. Además soportamos objetos personalizados y los flujos bidireccionales están cubiertos. ¿Quieres que te mande un diagrama técnico de cómo se ve la arquitectura?"

Pregunta: ¿Qué hito cruzó el SDR?

a) Hito 1 — la reunión. Ya no va a haber reunión.
b) Hito 3 — demostración. Hizo una micro-demo técnica y prometió material que corresponde a la etapa de evaluación.
c) Hito 4 — propuesta. Hizo una propuesta comercial.
d) No cruzó ningún hito. Respondió bien la pregunta técnica.

¿Elegiste la b? Estás en lo correcto, prestaste atención.

El SDR salió de su rol y entró al del AE. ¿Por qué es problemático? Cuando el AE entre a la reunión, el prospecto ya vio parte de la demo técnica. Y peor: el SDR hizo afirmaciones específicas —"conector nativo", "sincronización en tiempo real", "objetos personalizados"— que el AE va a tener que confirmar o desmentir.

Lo que el SDR debería haber respondido es algo así: "Dale, la integración con Salesforce es tema clave. Francisco —el AE— conoce todos los detalles técnicos y va a poder contarte exactamente cómo se maneja sin migración. ¿Te anoto ese tema como prioritario para la reunión?"

Misma cordialidad, mismo interés, cero cruce de hito.

Complementa este contenido con las guías adjuntas al módulo. Ahí vas a encontrar el desarrollo completo de los cuatro bloques: la arquitectura de la función comercial con lo que se le mide a cada rol, los cuatro canales con su ventaja y desventaja específica —y por qué ABM es una estrategia y no un canal—, las tres condiciones del outbound y los tres escenarios donde no aplica con ejemplos, la cadena de cinco hitos con casos detallados de cada cruce típico, y dos ejercicios adicionales para que practiques identificar cuándo estás por cruzar.

Ya sabes cómo se organiza tu lado de la mesa, los cuatro canales que existen, qué es el outbound y qué hitos vendes tú.

En el segundo video respondemos las dos preguntas que faltan: qué define una reunión calificada en concreto, y cómo se entrega esa reunión al AE para que la venta arranque con ventaja, no a ciegas.

Nos vemos en el video 2.
```

> Nota: el bloque "Fuentes de este video" del `.md` es para la sección de Bibliografía en
> la plataforma, **no se narra** — no lo pegues en el script del avatar.

---

## Video 3 — `contenido_2` · "Reunión calificada, handoff y mentalidad" (Bloques 5-7, ~8 min)

**Fixes visuales en Studio:**
- **Los 4 criterios de reunión calificada:** la slide debe listar los 4 con el nombre
  plano —empresa dentro del cliente ideal · contacto que decide o aliado validado ·
  asiste · pasa la precalificación—. Evitar las siglas ICP/KDM en pantalla.
- **La cadena de hitos / cierre del módulo:** si reaparece la cadena, mismo criterio que
  en el Video 2 (5 hitos, sin "renovación" como hito).
- Animación encima del avatar → quitar/reemplazar overlay.

**Texto para pegar:**

```
Conseguiste la reunión. El prospecto agendó. Te felicitas.

Pero una reunión por sí sola no sirve de nada. Una reunión con la persona equivocada es peor que no tener reunión: quema el tiempo del AE, mete ruido en el sistema, y daña la confianza dentro de tu equipo.

Hoy vemos el filtro que evita que eso pase.

Cerramos la semana y el módulo con tres temas: los cuatro criterios que definen una reunión calificada, el handoff —el pase del prospecto del SDR al AE, la pieza más infravalorada del rol—, y la mentalidad que te separa del SDR promedio. Termina con un caso de calificación para que apliques el filtro en vivo, y una síntesis del módulo entero.

Primero la distinción de métrica. Una reunión agendada es el hito uno —el prospecto dijo "dale, agendemos"—. Una reunión calificada requiere cuatro criterios al mismo tiempo. Se miden por separado. Si un SDR agenda cuarenta al mes y solo ocho califican, tiene un problema serio. Está agendando con gente que no decide, o fuera del cliente ideal.

Una reunión es calificada si cumple los cuatro criterios. No tres. No "depende". Los cuatro.

Criterio uno. La empresa está dentro de tu cliente ideal. Rubro correcto, tamaño correcto, país correcto, características relevantes —por ejemplo, que tenga comercio electrónico o equipo de ventas propio—.

Criterio dos. El contacto es quien decide, o un aliado validado. Tiene autoridad para decidir sobre el tema. O —si no decide él— tiene llegada directa al decisor y puede traerlo a la mesa. Y ojo: "validado" significa que hay evidencia real de esa llegada —ya te presentó a alguien, te mostró cómo va a mover el tema adentro—, no que el contacto simplemente diga que puede. Una promesa de acceso no es acceso. Lo que no cumple: un analista junior que dijo "interesante" sin ninguna relación con quien decide.

Criterio tres. Asiste a la reunión. Parece obvio, pero hay que decirlo. La persona aparece el día y la hora acordados. Lo que no vale: que mande a otra persona que no cumple el criterio dos.

Criterio cuatro. Pasa la precalificación mínima. Existe el problema que tu oferta resuelve. No hay un bloqueador absoluto. Hay algún indicio de momento razonable —no urgente, pero el tema está en el horizonte—.

Si falta uno solo, no es calificada. Y lo más importante: no debería haberse generado en primer lugar. Parte de tu trabajo como SDR es filtrar antes, no después.

Cuando entregas la oportunidad al AE pasa algo que parece administrativo, pero que determina el futuro del negocio. Le llamamos handoff —el pase del prospecto del SDR al AE—. Y de hacerlo bien o mal depende que el AE entre a la reunión con ventaja o casi a ciegas.

Un handoff completo cubre cinco bloques:

Uno. Información de la empresa —nombre, rubro, tamaño, y la señal que usaste para abrir la conversación—.

Dos. Información del contacto —rol, responsabilidades, cómo se involucra en la decisión—.

Tres. Contexto del contacto —cuánto tardó en responder, por qué canal, qué ángulos probaste, qué funcionó—. Esto le sirve al AE para calibrar el nivel de interés.

Cuatro. Qué dijo el prospecto en la precalificación —respuestas concretas a su situación, su necesidad y su momento—.

Cinco. Advertencias —bloqueadores posibles, política interna detectada, otras personas involucradas que se mencionaron—.

Tres cosas que no deben aparecer: especulaciones sin base —frases como "creo que este negocio va a ser fácil" distorsionan la expectativa del AE—, información irrelevante, y chismes internos que recogiste por ahí.

Si el handoff es incompleto, mira lo que le pasa al AE. Pregunta cosas que tú ya preguntaste y el prospecto se frustra. Asume cosas que no son y pierde credibilidad. No conoce los bloqueadores y se choca contra ellos en vivo. El AE puede tener la mejor técnica de cierre del mundo. Si llega mal preparado por culpa de un handoff pobre, la venta se quema antes de empezar. Por eso es la pieza más infravalorada del SDR moderno, y la que más separa al bueno del promedio.

Hay una percepción común de que el SDR es "la base de la pirámide". Como si fuera un rol mecánico. Esa percepción está equivocada.

Un SDR bueno tiene tres ingredientes, no uno.

Ejecutor. Sí, hay trabajo repetitivo. Muchos emails. Muchas llamadas. La consistencia es la variable número uno. Sin ella, ningún otro ingrediente importa.

Con criterio. Cada email, cada llamada, cada precalificación exige una decisión. ¿Esta empresa encaja con tu cliente ideal? ¿Vale la pena insistir? ¿Cómo manejo esta objeción? El criterio se construye con los fundamentos del curso. Por eso esta primera mitad parece "teórica": sin esa base, la ejecución se vuelve mecánica.

Que entiende el negocio. Tres negocios, en realidad. El de la empresa que representas. El del rubro del cliente. Y el del decisor con el que hablas. A esto le dedicamos todo el Módulo 2.

La mayoría de los SDR buenos no se quedan siendo SDR para siempre. El camino típico en B2B es: SDR, luego AE, luego AE senior, luego gerente de ventas, luego director. El conocimiento que construyes los primeros dieciocho a veinticuatro meses como SDR es la base de todo ese camino.

Vamos con un caso para que apliques el filtro de los cuatro criterios.

Reunión con el director financiero de una empresa B2B de trescientos cincuenta empleados, dentro de tu cliente ideal. El director llega a la reunión. En los primeros minutos dice: "Ya renovamos contrato por tres años con el competidor el mes pasado."

Pregunta: ¿Esta reunión califica?

a) Sí, califica. Encaja con el cliente ideal, el contacto decide, asistió.
b) No califica. Falta el criterio 1 — el cliente ideal.
c) No califica. Falta el criterio 4 — la precalificación. Hay un bloqueador absoluto: contrato de tres años recién firmado.
d) Califica con observaciones.

¿Elegiste la c? Estás en lo correcto, prestaste atención.

Encaja con el cliente ideal. El contacto decide —es el director financiero—. Asistió. Pero la precalificación falla porque hay un bloqueador absoluto: contrato fresco por tres años con el competidor. Eso no se destraba con una buena demostración.

Y acá viene la lección operativa, lo que sí o sí te tienes que llevar: este caso debía haberse detectado antes de agendar, con preguntas de precalificación en el primer contacto. Algo tan simple como: "¿Trabajan hoy con alguna solución para esto? ¿Hace cuánto?" hubiera evitado meterle treinta minutos al AE.

Cuando llega a la reunión, ya es tarde. Tu trabajo como SDR es filtrar más arriba, no esperar a que el AE descubra el problema en vivo.

Recapitulemos en siete puntos lo que te llevas de la semana —y del Módulo 1—:

Uno. La función comercial B2B se divide en cuatro roles: Marketing, SDR, AE, CSM. Existen separados para que el negocio sea predecible.

Dos. Hay cuatro canales de demanda: inbound, outbound, referidos y alianzas. El outbound es uno de los cuatro. Y ABM no es un canal: es una estrategia que se monta sobre ellos.

Tres. El outbound funciona con tres condiciones: cliente ideal alcanzable, precio que justifica el costo, ciclo que aguanta el modelo.

Cuatro. El SDR vende dos hitos, no la cadena entera: la reunión, y la asistencia más precalificación. Cruzar hitos es el error más caro y más común del SDR novato.

Cinco. Una reunión calificada cumple cuatro criterios acumulativos: cliente ideal, contacto que decide o aliado validado, asistencia, precalificación. Reunión agendada y reunión calificada son métricas distintas.

Seis. El handoff es sagrado: cinco bloques de información, sin especulaciones, sin chismes. Define si el AE entra con ventaja o a ciegas.

Siete. El SDR no es operario, no es cazador de comisiones, no es asistente del AE. Es ejecutor con criterio que entiende el negocio.

Complementa este contenido con las guías adjuntas al módulo. Ahí desarrollamos los cuatro criterios con sus fallas posibles, dos casos más de calificación —además del que acabas de ver—, el formato operativo del handoff en una página listo para copiar, y un check final con la evaluación de un handoff real de MediFlow.

Cerraste el Módulo 1. ¿Qué viene? En la Semana 3 arrancamos el Módulo 2 con la pregunta central: ¿cómo entiendes a una empresa que no conocías hace cinco minutos? Vamos a ver cómo una empresa gana dinero, cómo compite y qué la hace rentable.

Antes, dos cosas para cerrar el Módulo 1: la prueba del Módulo 1 y el cierre del módulo. Organízate para llegar a las dos esta semana.

Nos vemos en el Módulo 2.
```

> Nota: el bloque "Fuentes de este video" del `.md` es para la Bibliografía en plataforma,
> **no se narra**.
