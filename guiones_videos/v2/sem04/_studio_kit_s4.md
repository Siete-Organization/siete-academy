# Kit de armado en Studio — Semana 4 (Módulo 2)

> Para construir los 3 videos **a mano en HeyGen Studio** (decisión 2026-06-11: los
> templates de la cuenta no exponen variable de texto, así que no se generan por API).
> Acá tenés el **texto hablado limpio** de cada video, ya sin `[SLIDE:...]`, sin headers
> ni markdown — listo para pegar en el script del avatar. Fuente: los `.md` corregidos
> de `sem04/` (alineados a `LIMPIO_S4.md` de NICO).

## Antes de pegar — 3 cosas que aplican a los 3 videos

1. **Activá el Brand Glossary "Video Agent Pronunciation"** (id `0e3e834da76f4f988fac667e40fcbbaf`)
   en el proyecto. Ya tiene: B2B→"bi tu bi", B2C→"bi tu ci", SDR→"es di ar", **LOB→"el ou bi"**.
   Sumá si hace falta: ICP→"i ci pi", CMO→"ci eme ou", CFO→"ci ef ou", VP→"vi pi", ROI→"ar ou ai".
2. **Voz en español:** confirmá que la voz del template renderiza en español (en
   `heygen_defaults.json` la voz figuraba como `language: English` — probable co-causa del
   mal acento). Si suena en inglés, cambiá la voz a la variante ES.
3. **Pausas al enumerar:** donde el guion lista "Uno… Dos… Tres…", insertá un **Pause**
   (botón Pause, ~0.5s) entre cada ítem. En el ejercicio en vivo, donde el texto dice
   "[Pausa breve]", poné un **Pause más largo** (~1.5-2s) para que el alumno responda mentalmente
   antes de la corrección. El texto ya viene con cada ítem en su propio párrafo para que sea fácil ubicarlos.

---

## Video 1 — `intro` · "Entender al comprador — qué te llevas esta semana" (~3.5 min)

**Texto para pegar:**

```
Imagina dos SDRs en la misma empresa, con el mismo producto, las mismas herramientas y el mismo volumen de prospectos. Uno convierte al uno por ciento. El otro, al tres por ciento. El triple.

La diferencia no es el producto ni la lista. La diferencia es qué tan profundo entiende cada uno a la persona del otro lado del email.

La Semana 3 fue sobre el negocio: cómo entender una empresa por dentro —su modelo, sus métricas, su competencia, sus dolores—. Esta semana cambiamos de zoom. Pasamos del negocio a la persona dentro del negocio.

La pregunta central que abre toda la semana es: ¿quién está del otro lado del correo, y qué le importa?

Si la Semana 3 te enseñó a leer la empresa, la Semana 4 te enseña a leer al ser humano que toma —o frena— la decisión.

Al terminar esta semana vas a poder hacer cuatro cosas concretas:

Uno. Construir un ICP y un buyer persona para un cliente hipotético, y aplicar los dos filtros en el orden correcto. Vas a entender por qué confundirlos es la causa más común de pipeline contaminado.

Dos. Diferenciar las motivaciones y los miedos de cada rol dentro de un comité de compra. Vas a distinguir, por cómo se comporta cada persona, quiénes impulsan la decisión, quiénes solo conversan y quién la bloquea.

Tres. Reconocer timing signals reales —señales de momento como cambios de liderazgo, crecimiento agresivo, regulación, cambios operativos— y distinguirlas del ruido que confunde al SDR novato.

Cuatro. Identificar la diferencia entre un prospecto "no listo" y uno que "no encaja". Suenan igual, pero tratarlos igual te cuesta meses de trabajo desperdiciado y un pipeline que arranca de cero cada trimestre.

Estas cuatro capacidades son el cierre del Módulo 2. Lo que viene después —escritura persuasiva y conversación— se construye encima de esto.

Esta semana cierra el Módulo 2. Al final te esperan la prueba del módulo y la sesión en vivo. Vamos al primer video de contenido.
```

---

## Video 2 — `contenido_1` · "ICP, buyer persona y la psicología del decisor" (Bloques 1-3, ~8.5 min)

**Texto para pegar:**

```
Hay una confusión que comete casi todo SDR novato y que es la causa número uno de pipeline contaminado: confundir el ICP con el buyer persona.

No son lo mismo. Y no aplicar los dos filtros, en el orden correcto, te llena el CRM de conversaciones que nunca convierten. Sumale a eso una segunda trampa: dentro del comité, solo una minoría mueve de verdad la decisión hacia el sí. El resto conversa o se opone: responde emails, agenda reuniones, es amable, y el deal no avanza.

En este video cubrimos los primeros tres temas de la semana: cómo se distinguen ICP y buyer persona y cómo se aplican en cadena, cómo se mueve un comité por dentro —quién impulsa, quién solo conversa y quién bloquea— y cómo detectar quién mueve la aguja de verdad, y la psicología profunda del decisor B2B —qué lo motiva, qué lo frena, y por qué la primera línea de tu email decide todo—. Hay un ejercicio en vivo en el medio para que apliques lo aprendido.

ICP —que en inglés es Ideal Customer Profile, o perfil de cliente ideal— es la empresa. Qué industria, qué tamaño, qué geografía, qué características hacen que tu oferta tenga sentido para ese negocio.

El buyer persona —el perfil de la persona que decide dentro de esa empresa— es la persona. Qué rol tiene, qué le importa, qué la frena, qué busca en su carrera.

Son filtros distintos y acumulativos. Una empresa puede ser un ICP perfecto, y el buyer persona que tienes enfrente puede no serlo. Un banco de ochocientos empleados puede encajar perfecto con tu ICP. Pero si estás hablando con un analista junior sin llegada al decisor, el buyer persona no está ahí, aunque la empresa sí.

Un ICP bien construido tiene entre cuatro y seis criterios: industria específica —"banca minorista con operación multinacional", no "servicios financieros"—, tamaño en empleados o facturación, geografía, características operativas como tecnologías que usan o regulación que les aplica, y —clave— exclusiones explícitas. Qué no es ICP, aunque encaje en los otros criterios. Un ICP sin exclusiones tiende a ser demasiado amplio. Las exclusiones hacen al filtro real.

Un buyer persona tiene seis ingredientes: rol exacto —"VP de Marketing" no es lo mismo que "CMO" ni "Brand Manager"—, nivel de decisión en la compra, motivaciones, frenos, canales donde es alcanzable, y tipo de mensaje que le resuena.

Cómo se aplican. Filtro uno: ¿la empresa encaja con el ICP? Si no, archiva. Si sí, vas al paso dos. Filtro dos: ¿hay un buyer persona válido en esa empresa? Si no, archivas o buscas referidor. Si sí, prospecta. Saltarse el segundo filtro —mandar cold email al primer contacto que aparece en Apollo sin validar autoridad— es el error más común del SDR nuevo.

En la Semana 1 viste los roles de un comité: quién pone el dinero, quién evalúa que funcione, quién la usa, quién puede frenarla. Ese es el organigrama de la compra. Esta semana sumamos un segundo eje, el comportamiento: cómo reacciona cada persona frente a tu propuesta. Y es independiente del rol —dos personas con el mismo cargo se comportan distinto—.

En este segundo eje, cada persona cae en uno de tres grupos: los que impulsan, los que solo conversan, y el que bloquea.

Los que impulsan tienen la credibilidad y la voluntad de empujar el cambio hacia adentro. Hay tres perfiles. El proactivo, que ve una oportunidad de mejorar el negocio y empuja —"esto nos sirve, vamos por esto"—. El que divulga, que comparte ideas nuevas con sus colegas y al que buscan por su criterio: enseña dentro de la empresa. Y el escéptico, que cuestiona, pide evidencia, evalúa con dureza, pero cuando se convence empuja con fuerza.

Los que solo conversan participan y son accesibles, pero no tienen el peso ni la voluntad de mover la decisión. También hay tres. El que negocia información, que comparte lo que sabe solo si ve un beneficio propio. El amistoso, amable, fácil de conseguir reuniones, pero sin peso real en el comité. Y el que busca beneficio propio, que usa la decisión como palanca para su carrera.

Aparte de los dos grupos está el que bloquea: no es que hable y no mueva, frena el cambio activamente. A veces por razones legítimas —ya tiene un proveedor cómodo—, a veces por política interna. Lo típico: un Director de Tecnología frente a una plataforma nueva que su equipo tendría que implementar y mantener, así que se opone aunque le sirva al negocio.

Y aquí está lo que cambia todo: en cualquier comité, solo una minoría mueve de verdad la decisión hacia el sí; el resto conversa o se opone. Apuntar al grupo equivocado es la trampa dulce del outbound: los que solo conversan son accesibles, responden emails, agendan reuniones. Pero el deal no avanza.

Cómo los detectas, rápido. El que impulsa cuestiona lo que dices, conecta tu tema con lo que pasa adentro, comparte información útil, menciona a otras personas que habría que involucrar. El que solo conversa responde genérico, acepta todo sin fricción, no trae preguntas propias, nunca propone a quién más sumar.

Un SDR con criterio detecta temprano a los que solo conversan y los trata como referidores —pueden conectarte con los que sí impulsan— en vez de confundirlos con aliados internos reales.

Vamos a aplicar estos perfiles de conducta en dos casos reales.

Mauro te responde: "Interesante. Antes de avanzar, ¿tienes casos de estudio con empresas de nuestro tamaño que hayan medido impacto específico en métricas de operación? Quiero ver datos reales."

Pregunta: ¿qué perfil de conducta es Mauro?

a) El proactivo. b) El amistoso. c) El escéptico. d) El que bloquea.

[Pausa breve]

¿Elegiste la c? Estás en lo correcto, prestaste atención. Mauro es el escéptico. Pide datos concretos, cuestiona antes de avanzar. Y eso es buena noticia: cuando el escéptico se convence, empuja con fuerza. Tu trabajo es darle la evidencia que pide, no esquivarla.

Ramiro responde: "Estuve leyendo el material que me compartiste. Voy a mostrárselo al comité ejecutivo el jueves, me parece exactamente lo que necesitamos conversar para este semestre."

Pregunta: ¿qué perfil de conducta es Ramiro?

a) El que busca beneficio propio. b) El que divulga. c) El que negocia información. d) El amistoso.

[Pausa breve]

¿Elegiste la b? Estás en lo correcto. Ramiro es el que divulga: comparte material con el comité interno, enseña dentro de la empresa. Es oro para ti. Dale más material que pueda usar internamente. Mientras él lo lleva puertas adentro, tu trabajo avanza solo.

Saber el rol —y si la persona impulsa, conversa o bloquea— es el primer filtro. Para escribir un mensaje que resuene, necesitas entender qué mueve y qué frena al decisor como persona.

Los cuatro motores: avance de carrera —cada proyecto es una apuesta personal sobre su reputación—, status interno —ser visto como "el que trae innovación"—, resultados medibles —ROI, eficiencia, ahorro, pero solo si se combinan con los anteriores—, y evitar riesgo —en empresas maduras, el motor más fuerte casi nunca es ganar, es no perder—.

Los tres frenos: costo de cambio —implementación, re-entrenamiento, convencer al equipo—, miedo al error público —rara vez se dice en reuniones, pero gobierna decisiones—, y fatiga de proveedores —los roles C-level reciben emails de cincuenta SDRs por semana, su default ya no es "evalúo", es "ignoro salvo excepción"—.

Tu competencia real no son los otros proveedores. Tu competencia es la fatiga de proveedores. Tu trabajo es ser la excepción.

Última pieza, y es la más importante. Tenemos dos modos de pensar. El pensamiento rápido —Sistema 1— es veloz, intuitivo, emocional, usa atajos. El pensamiento deliberado —Sistema 2— es lento, racional, exige esfuerzo.

Cuando un decisor B2B recibe tu email, decide con el pensamiento rápido, en los primeros segundos, si sigue leyendo. Si el email no pasa ese filtro, el pensamiento deliberado nunca se activa. No importa cuán bien razonado esté el cuerpo. La primera línea tiene que resonar emocional e intuitivamente con algo que el decisor ya está pensando o sintiendo. Si la primera línea no engancha, el email murió antes de empezar.

Complementa este contenido con las guías adjuntas al módulo. Ahí vas a encontrar el desarrollo completo de cada perfil de conducta con frases típicas y patrones, los dos casos adicionales del ejercicio —el que negocia información y la que bloquea—, los seis ingredientes del buyer persona con ejemplos por industria, y la matriz completa de motores y frenos por nivel jerárquico.

Ya sabes a qué empresa, a qué persona y con qué psicología estás escribiendo. En el segundo video respondemos las dos preguntas que faltan: cuándo archivar un prospecto definitivo y cuándo archivar con fecha, y qué señales de timing son reales y cuáles son ruido. Nos vemos en el video 2.
```

---

## Video 3 — `contenido_2` · "No encaja vs no listo, timing signals y el 1% → 3%" (Bloques 4-6, ~8.5 min)

**Texto para pegar:**

```
Cuando un prospecto no avanza, hay dos razones que suenan parecidas y son estructuralmente distintas.

Puede que "no encaje": la empresa o la persona no califica como ICP ni como buyer persona. Nunca va a cerrar. Ni ahora, ni en dos años.

O puede que "no esté lista": la empresa o la persona sí califica, pero no está en el momento correcto para comprar.

Confundirlas cuesta. En las dos direcciones. Y la diferencia, a los dieciocho meses, es enorme.

Cerramos la semana —y el Módulo 2— con tres temas. Primero, cómo clasificar prospectos que no avanzan: el que "no encaja" versus el que "no está listo", con un ejercicio en vivo. Segundo, qué timing signals —señales de momento— son reales y cuáles son ruido. Y tercero, el cierre del módulo: por qué entender al comprador es lo que define en qué punto del rango de conversión caes.

Tratarlos igual te quema tiempo en las dos direcciones.

Si tratas un "no encaja" como "no listo": desperdicias seis a doce meses insistiendo con una cuenta que nunca va a cerrar. No es paciencia, es testarudez.

Si tratas un "no listo" como "no encaja": archivas una cuenta que podía cerrar en seis a nueve meses. Y probablemente cerró con tu competidor, que sí la retomó cuando el momento maduró.

Cuando una cuenta no avanza, hazte estas cuatro preguntas, en este orden.

Uno. ¿Cumple el ICP? Si no, "no encaja". Descarte definitivo.

Dos. ¿El contacto es un buyer persona válido, o un aliado interno con llegada al decisor? Si no, y no hay forma de llegar al decisor real, "no encaja" en la práctica.

Tres. ¿Hay dolor real, aunque no lo estén resolviendo ahora? Si no existe el problema en esta empresa, "no encaja".

Cuatro. ¿Hay un factor de momento que bloquea ahora? Por ejemplo: acaban de firmar con un competidor, están en reestructuración, el presupuesto ya está cerrado. Si sí, "no listo" con fecha concreta de recontacto. Archivas con un disparador.

Vamos con un caso.

Recibes esta respuesta: "Te agradezco, pero ya firmamos contrato por dos años con un competidor el mes pasado. Probablemente revisemos cuando vaya terminando."

Pregunta: ¿cómo clasificas esta cuenta?

a) "No encaja", descarte definitivo. b) "No listo" con recontacto en tres meses. c) "No listo" con recontacto en dieciocho a veintidós meses. d) Volver a insistir esta semana con otro ángulo.

[Pausa breve]

¿Elegiste la c? Estás en lo correcto, prestaste atención.

El contrato vence en veinticuatro meses. Lo ideal es contactarlos alrededor de dos meses antes de que empiecen a evaluar, no recién cuando expira. Si esperas a que el contrato venza, ya es tarde: la decisión se toma dos o tres meses antes. Por eso el recontacto correcto es entre dieciocho y veintidós meses.

Y aquí está la clave operativa: un SDR que hace bien esta distinción construye un banco de pipeline futuro ordenado. Cada trimestre activa los recontactos que tocan, y muchos de esos sí cierran cuando el momento mejoró. El SDR que no hace la distinción tira toda la lista cuando no le responden en cuatro semanas, y empieza de cero cada trimestre. A los dieciocho meses, la diferencia entre los dos es brutal.

Dentro de tu ICP, algunos prospectos están más listos que otros. Eso lo marcan las timing signals —las señales de momento—: eventos verificables en la vida de la empresa que aumentan la probabilidad de que haya apertura a conversar. Cuatro categorías.

Cambios de liderazgo. Nuevo VP de Ventas, CMO o CFO con menos de noventa días, especialmente si vino de afuera —no fue promoción interna—. Despido o renuncia del líder del área que usaría tu producto.

Crecimiento agresivo. Apertura de oficinas en nuevos países, contratación masiva en un área —quince o más posiciones en tres semanas—, cierre de ronda de inversión Serie B o posterior.

Regulación. Nueva normativa que entra en vigor en menos de ciento ochenta días en la industria del prospecto, o sanción regulatoria pública reciente.

Cambios operativos. Lanzamiento de nuevo producto o línea de negocio, anuncio público de transformación digital, fusión, adquisición o escisión reciente.

Y ahora las cinco trampas que confunden al SDR novato. Estos hechos parecen señal, pero no correlacionan con necesidad real:

Uno. "La empresa está creciendo en general." Todas dicen que crecen.

Dos. Posts del CEO sobre liderazgo o filosofía. Es comunicación de marca, no operación.

Tres. Reconocimientos genéricos —"Great Place to Work", "Top Employer"—.

Cuatro. Movimientos del competidor del prospecto.

Cinco. Posts puramente de marca sin contenido operativo, y noticias de más de seis meses.

Si después de diez a quince minutos de investigación no encontraste ninguna señal verificable, la empresa no está lista para tu cold email hoy. Dos opciones: archivar con un disparador —"revisar en dos meses si aparecen señales"— o tratarla como artesanal si es cuenta de alta prioridad, con investigación más profunda. Lo que no hagas: escribir sin señal y sin hipótesis. Eso es spam con buena tipografía.

Cerramos la semana —y el módulo— con el por qué de todo esto.

Ya viste en la Semana 2 que la conversión de empresa contactada a reunión agendada se mueve en un rango de uno a tres por ciento, con el tres por ciento como mejor caso. Lo que decide en qué punto de ese rango caes no es el producto —es el mismo—. No es la empresa —es la misma—. No son las herramientas —Apollo, Reply, Instantly son las mismas para todos—. No es el tiempo por prospecto —es similar—.

La diferencia es qué tan profundo entiende cada SDR al comprador específico al que escribe.

El SDR que manda muchos correos sin entender a quién le escribe se queda en el piso del rango. El SDR que manda menos correos, pero con mapeo dolor-solución, una señal verificable y una lectura correcta de con quién está hablando, llega al techo. Menos volumen con más criterio rinde más que más volumen a ciegas.

El anti-patrón del SDR nuevo es pensar que "más es más": más emails, más prospectos, menos investigación. La realidad es al revés: menos emails con más profundidad, menos prospectos con más calidad, más investigación, menos tiempo desperdiciado escribiendo a la gente equivocada.

Cerraste el Módulo 2. El hilo conductor es este: no escribes a empresas, escribes a personas específicas dentro de empresas específicas. Entender ambas —el negocio y la persona— es lo que separa el outbound que convierte del outbound que se ignora.

De la Semana 3 te llevas Business Model Canvas, unit economics, las cinco fuerzas de Porter, Jobs to Be Done, el mapeo dolor-solución y el error número uno del SDR nuevo.

De la Semana 4 te llevas ICP versus buyer persona, cómo se mueve un comité por dentro —los que impulsan, los que solo conversan y el que bloquea—, los cuatro motores y los tres frenos del decisor, el pensamiento rápido versus el deliberado aplicado al cold email, "no listo" versus "no encaja" con disparadores concretos, y cómo distinguir timing signals reales del ruido.

Complementa este contenido con las guías adjuntas al módulo. Ahí vas a encontrar las cuatro categorías de señales con ejemplos por industria, los dos casos adicionales del ejercicio de "no encaja / no listo" —incluyendo una reorganización interna—, las cinco fuentes para encontrar señales en orden de utilidad real, y el desarrollo completo del rango de conversión con casos por nivel de seniority.

Antes del Módulo 3 te quedan la prueba del Módulo 2 —alrededor de ochenta minutos— y la sesión en vivo del Módulo 2 —tres horas por Zoom—. Las dos se completan esta semana.

El Módulo 3 cambia de marcha por completo. Pasamos del entendimiento a la escritura y la conversación. Semana 5: escritura persuasiva. Semana 6: conversación y calificación. Es el módulo más práctico del curso, y donde todo lo anterior se vuelve cold email y cold call. Nos vemos en la sesión en vivo, y después en el Módulo 3.
```

> Nota: el bloque "Fuentes de este video" de cada `.md` es para la sección de Bibliografía en
> la plataforma, **no se narra** — no lo pegues en el script del avatar.
