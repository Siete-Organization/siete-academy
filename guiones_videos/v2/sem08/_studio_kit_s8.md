# Kit de armado en Studio — Semana 8 (Módulo 4)

> Para construir los 3 videos **a mano en HeyGen Studio** (decisión 2026-06-11: los
> templates de la cuenta no exponen variable de texto, así que no se generan por API).
> Acá tenés el **texto hablado limpio** de cada video, ya sin `[SLIDE:...]`, sin headers
> ni markdown — listo para pegar en el script del avatar. Fuente: los `.md` corregidos
> de `sem08/` (alineados al master de NICO `LIMPIO_S8.md`).

## Antes de pegar — 3 cosas que aplican a los 3 videos

1. **Activá el Brand Glossary "Video Agent Pronunciation"** (id `0e3e834da76f4f988fac667e40fcbbaf`)
   en el proyecto. Ya tiene: B2B→"bi tu bi", B2C→"bi tu ci", SDR→"es di ar", LOB→"el ou bi".
   Para S8 confirmá además: **AE→"ei i"**, **ICP→"ai ci pi"**, **CRM→"ci ere eme"**,
   **VP→"vi pi"**. Si alguno suena mal, agregalo al glossary; no toques el texto/subtítulos.
2. **Voz en español:** confirmá que la voz del template renderiza en español. Si suena en
   inglés, cambiá la voz a la variante ES.
3. **Pausas al enumerar:** donde el guion lista "Uno… Dos… Tres…" (las 10 etapas, los 3
   filtros, los 5 atributos), insertá un **Pause** (~0.5s) entre cada ítem. El texto ya
   viene con cada ítem en su propio párrafo para que sea fácil ubicarlos.

---

## Video 1 — `intro` · "Del proceso al mindset de mejora continua" (~3 min)

**Fixes visuales en Studio:**
- Animación encima del avatar → quitar/reemplazar el overlay.
- Slide "Objetivos de la Semana 8": que muestre las 3 capacidades (proceso de 10 etapas /
  leer métricas y diagnosticar / formular hipótesis), no más.

**Texto para pegar:**

```
Llegamos a la última semana del curso. Y es, también, la más intensa.

La Semana 7 te mostró las piezas sueltas: canales, secuencias, entregabilidad. Esta semana las vas a conectar en un solo proceso, vas a aprender a operarlo todos los días y a leerlo cuando algo falla.

Si las primeras siete semanas fueron sobre entender el outbound, esta es sobre operarlo.

En la Semana 7 vimos los componentes del sistema. Pero tener los componentes no alcanza: hay que saber cómo se vuelven una operación que produce reuniones, semana tras semana, sin depender de la suerte.

La pregunta central de esta semana es justamente esa, traducida a operación diaria: ¿cómo se ejecuta esto todos los días, y cómo sabes si está funcionando?

Y debajo de esa hay una segunda pregunta, más profunda: cuando deja de funcionar —y va a dejar de funcionar—, ¿cómo lo diagnosticas sin adivinar?

Al terminar esta semana —y el curso— vas a poder hacer tres cosas concretas.

Una. Describir el proceso outbound de punta a punta, en sus diez etapas, y ubicar tu responsabilidad en cada una. Vas a entender por qué el proceso es lineal, y por qué saltar una etapa amplifica el problema en todo lo que viene después.

Dos. Leer un tablero de métricas y diagnosticar dónde está el problema, recorriendo el embudo hacia arriba por descarte. Esto es lo que separa al SDR que arregla cosas del que prueba cosas al azar.

Tres. Formular hipótesis de mejora basadas en señales del día a día, no en intuiciones sueltas. Vas a aprender el ciclo de mejora continua aplicado al outbound, y la regla de oro: una sola variable por experimento.

Estas tres capacidades son lo que te permite ejercer el rol después del curso. Sin proceso, sin diagnóstico y sin mindset de iteración, el SDR se quema. Con las tres, perduras.

El formato es el de siempre: este video de intro con el mapa, dos videos de contenido, y la guía adjunta al módulo con todo desarrollado bloque por bloque.

Pero esta semana también cierra el curso: incluye la prueba del Módulo 4, la prueba final integradora —que continúa el caso que empezaste a leer en la Semana 7, más un video de defensa— y la sesión en vivo de cierre con el profesor. Es la carga más alta del curso. Bloquea el calendario con anticipación.

Vamos al contenido. Nos vemos en el siguiente video.
```

---

## Video 2 — `contenido_1` · "El proceso de punta a punta y la ejecución diaria" (Bloques 1-4, ~8 min)

**Fixes visuales en Studio:**
- **Las 10 etapas:** la slide debe mostrar las 10 en el orden correcto —ICP, listas,
  limpieza/validación, diseño de secuencia, carga de contactos, ejecución diaria, gestión
  de respuestas, agendamiento, precalificación, handoff al AE—. Ojo: **precalificación va
  en la 9, después de agendamiento** (orden de NICO), y hay etapa de **carga de contactos**
  en la 5.
- Slide "día tipo": si se muestra como tabla, respetar las dos franjas de contactabilidad.
- Animación encima del avatar → quitar/reemplazar overlay.

**Texto para pegar:**

```
La Semana 7 te mostró las piezas: canales, secuencias, entregabilidad. Sueltas.

Ahora vamos a conectarlas en un solo proceso de diez etapas. Y vas a aprender la regla que gobierna todo el sistema: cuando una etapa falla, todo lo que viene después se rompe.

En este video cubrimos los primeros cuatro temas de la semana: las diez etapas del proceso outbound, cómo se arma una lista buena, por qué la limpieza no es opcional, y cómo se trabaja un día real con estructura. Cierra con un ejercicio para que diseñes tu propio día.

Vamos por las diez, en orden.

Uno. Definición de ICP. Quién es el cliente ideal: criterios duros —industria, tamaño, geografía— más señales de compra.

Dos. Armado de listas. Convertir el ICP en una lista concreta de empresas y contactos.

Tres. Limpieza y validación. Verificar que los correos sean reales y que las empresas estén operativas.

Cuatro. Diseño de secuencia. Orden, canales, tiempo y reglas de ramificación. Lo hiciste en la Semana 7.

Cinco. Carga de contactos a las secuencias. Cuántos contactos metes al sistema. Y ojo, no es "todos los que tengas": es cuántos puede procesar tu infraestructura de correos y tu tiempo de SDR sin saturarse. Sobre esto volvemos en el segundo video.

Seis. Ejecución diaria. Mandar los toques, hacer las llamadas, gestionar WhatsApp.

Siete. Gestión de respuestas. Clasificar cada respuesta: interés, objeción, pedido de info, rechazo, fuera del rol.

Ocho. Agendamiento. Coordinar fecha, hora, canal y participantes de la reunión.

Nueve. Precalificación —el filtro previo a la reunión—. Confirmar que el prospecto cumple los criterios mínimos para que la reunión valga la pena, y que va a llegar alguien con peso real en la decisión, no un mando medio sin llegada. Lo viste en la Semana 6. Y fíjate algo: va después del agendamiento a propósito. Tener la reunión ya agendada te da la excusa natural para escribirle —"ya que nos vamos a ver, te hago un par de preguntas para llegar mejor preparados"— y precalificar sin fricción.

Diez. Handoff al AE —el paso de contexto al ejecutivo de cuenta—. Pasarle toda la información sin pérdida.

Tu tramo como SDR llega hasta el handoff de una reunión calificada. El discovery a fondo y el cierre son del AE: empiezan después de esta última etapa.

La regla del proceso: es lineal. Si una etapa está mal, la siguiente amplifica el problema. No lo arregla.

Un ejemplo. Saltas la etapa tres —limpieza— y mandas a una lista sin validar. Una porción de los correos rebota. Los proveedores te marcan como remitente masivo poco confiable. Tu reputación cae. Y las siguientes semanas tu tasa de respuesta baja en todo el sistema. Un atajo de treinta minutos te cuesta semanas.

Por eso el SDR con experiencia invierte mucho tiempo en las etapas uno a tres, aunque no se "vean" en las métricas de reuniones. Son la fundación.

Una lista buena no es cuantos más contactos, mejor. Es la mayor cantidad posible de contactos que cumplen el ICP, con información verificada.

Hay tres filtros que aplica el SDR con criterio.

Filtro uno. Filtros duros, el ICP estructural. Industria —por ejemplo, software B2B o fintech—, tamaño —digamos, cincuenta a quinientos empleados—, geografía y cargo objetivo. Los criterios que definen quién es prospecto y quién no.

Filtro dos. Filtros de señal. Hechos que indican que ahora es buen momento: acaba de levantar una ronda de inversión —señal de capacidad de compra—, anunció expansión regional —señal de necesidad nueva—, contrató mucha gente en los últimos meses, o cambió de VP de Ventas hace poco —señal de apertura a cambios—.

Filtro tres. Filtros negativos: la lista negra que nunca contactas. Antes de mandar nada, excluye sí o sí a tres grupos: las empresas que ya son tus clientes, las que ya están en tu pipeline en una etapa avanzada —volver a entrar en frío genera ruido y confunde al prospecto— y tus competidores. Contactar a cualquiera de estos en frío no solo no suma: resta. Por eso la exclusión se hace antes del envío, no después.

Una lista enorme sin filtros de señal responde poco. Una lista más chica, con filtros de señal precisos, responde varias veces mejor. La productividad por toque se multiplica. El esfuerzo de armar bien la lista se paga con volumen de reuniones, no con volumen de correos.

Por eso la regla del SDR con criterio: buena parte del tiempo en preparación —ICP, listas, limpieza—. El novato casi no prepara y ejecuta a ciegas, y produce menos reuniones aunque trabaje más horas.

La limpieza parece trabajo administrativo. No lo es. Es un seguro de entregabilidad. Mira la cadena del daño cuando se salta.

Uno. Mandas correos a direcciones que no existen. La tasa de rebote sube por encima del umbral que toleran los proveedores.

Dos. Los proveedores —Google, Microsoft— te clasifican como remitente masivo poco confiable.

Tres. Tu reputación de dominio cae de alta a media, o a baja.

Cuatro. Los siguientes correos que mandes, incluso los correctos, caen a spam en vez de a la bandeja de entrada.

Cinco. La tasa de respuesta se derrumba en todo el sistema, no solo en la lista contaminada.

Seis. Tienes que activar un dominio de reserva y esperar semanas hasta recuperar reputación.

Un atajo de treinta minutos se paga con semanas de recuperación.

Lo que tienes que aprenderte es el concepto: existe una capa de validación antes del envío, y saltarla rompe el sistema aguas abajo. Hay herramientas que lo instrumentan, pero no te aprendas los nombres. Cuando cambies de empresa vas a usar otra. El concepto se queda.

Hay una idea de la gestión de operaciones que aplica directo al outbound: el rendimiento de un sistema está limitado por su recurso más escaso. En una operación de outbound, ese recurso es el tiempo cognitivo del SDR. Hay mil tareas que podrían hacerse; solo algunas mueven la aguja. La disciplina diaria consiste en proteger el tiempo del SDR para esas tareas.

Hay tres categorías de trabajo.

Categoría uno. Alta concentración. Acá vive casi todo el valor que produces: escribir correos personalizados, hacer llamadas, investigar las cuentas del día, gestionar respuestas con criterio. Requiere foco sostenido, en bloques sin interrupciones: chat cerrado, notificaciones apagadas.

Categoría dos. Baja concentración. Lo administrativo: cargar listas, actualizar el CRM, revisar las métricas del día anterior, responder mensajes de coordinación. Se hace en lotes, en horarios específicos. Nunca se intercala con la alta concentración.

Categoría tres. Sincronización. Reuniones internas y precalificaciones agendadas. Tienen horario fijo y se respeta.

El SDR novato mezcla chat, correos, llamadas y CRM en bloques de diez minutos. Cambia de contexto decenas de veces al día y pierde una parte importante de su productividad solo en el costo de cambiar de tarea. A fin de mes hace la mitad del volumen que podría. No por flojera. Por falta de estructura.

Eres SDR. Esta semana tienes estas responsabilidades:

Mandar ochenta correos nuevos, ya limpios y listos para enviar.

Hacer cuarenta llamadas.

Tienes dos precalificaciones agendadas: una a las once y media, otra a las dieciséis.

Tu jefe te pidió un análisis rápido de por qué cayó la tasa de respuesta de la cuenta X, para el uno a uno de las quince y media.

¿Cuál de estas estructuras es la correcta?

a) Empezar el día respondiendo el chat y los correos internos, hacer las llamadas cuando "te dé la cabeza", y dejar la personalización de correos para el final.

b) Métricas y plan a primera hora. El análisis para el uno a uno temprano y fresco. Las llamadas en las dos franjas de mejor contactabilidad —media mañana y media tarde—. La personalización de correos en bloques largos. Las precalificaciones a sus horarios. CRM y handoffs al cierre.

c) Hacer las cuarenta llamadas seguidas a la mañana, los ochenta correos seguidos a la tarde, y meter las precalificaciones cuando caigan.

d) Trabajar correos y llamadas en bloques de quince minutos alternados, para "no aburrirte".

¿Elegiste la b? Estás en lo correcto, prestaste atención.

Mira lo clave. El análisis para el uno a uno se hace temprano y fresco, no a las tres de la tarde con la cabeza cansada. Las llamadas van en las dos franjas de mejor contactabilidad. La personalización va en bloques largos, no goteada. Y todo lo administrativo se agrupa al final.

La opción a es el anti-patrón completo: el chat al principio te rompe la cabeza para todo el día. La c ignora las franjas de contactabilidad. Y la d es exactamente el error de cambio de contexto que te roba productividad.

Complementa este contenido con las guías adjuntas al módulo. Ahí vas a encontrar el desarrollo completo de los cuatro bloques: las diez etapas con ejemplos reales de qué pasa cuando se salta cada una, los tres filtros de lista con plantilla de aplicación, la cadena del daño desarrollada, un día tipo completo en tabla con horarios LATAM, y un ejercicio adicional de armado de día.

Ya tienes el proceso, las listas, la limpieza y el día. En el segundo video de la semana respondemos las preguntas que faltan: cómo se lee el embudo de métricas, cómo se diagnostica cuando algo cae, cómo se mejora sin adivinar, y qué te llevas del curso completo.

Nos vemos en el video 2.
```

> Nota: el bloque "Fuentes de este video" del `.md` es para la sección de Bibliografía en
> la plataforma, **no se narra** — no lo pegues en el script del avatar.

---

## Video 3 — `contenido_2` · "Métricas, diagnóstico, mejora y cierre del curso" (Bloques 5-8, ~8.5 min)

**Fixes visuales en Studio:**
- **Embudo de métricas:** una métrica por tramo; arriba de todas la conversión empresa→
  reunión calificada (1-3%). No mostrar "open rate" como métrica viva (el guion explica
  por qué ya no se mide).
- **Tabla de Juan:** mostrar las 5 filas con la semana 4 resaltando solo la tasa de
  respuesta caída (0,7%); el resto estable.
- **Plan, Do, Check, Act:** rotular el ciclo con esos 4 pasos (sin atribución a autor).
- Slide "frase final" del cierre del curso: las herramientas se reemplazan / los conceptos
  se quedan.
- Animación encima del avatar → quitar/reemplazar overlay.

**Texto para pegar:**

```
Hay un solo número que resume todo el outbound: de cada cien empresas que contactas, terminan en una reunión que de verdad sirve entre una y tres —tres en el mejor caso—. Esa es la conversión que importa.

Ya tienes el proceso y la disciplina de ejecución. Ahora viene la parte que realmente separa al SDR que perdura del que no: leer las métricas, diagnosticar cuando algo falla, y mejorar sin adivinar. Y al final, cerramos el curso.

En este video cubrimos los últimos cuatro bloques: el embudo de métricas etapa por etapa, el método de diagnóstico por descarte —con un caso que es la mejor prueba del curso—, el mindset de mejora continua, y los cinco atributos del SDR que perdura. Cierra con la síntesis del curso completo.

Cada etapa del proceso tiene una métrica asociada. Juntas forman el embudo del SDR. Vamos de arriba hacia abajo.

Etapas uno a tres —ICP, listas, limpieza—. La tasa de rebote mide la salud técnica de la lista: cuántos correos rebotan y cómo está tu reputación de dominio.

Etapas cinco y seis —carga y ejecución—. La tasa de finalización de la secuencia te dice si cargaste de más: si saturas el sistema, quedan contactos varados a medio procesar que nunca terminan sus toques.

Etapa seis —ejecución—. La tasa de respuesta mide relevancia del mensaje más entregabilidad.

Etapa siete —gestión de respuestas—. Cuántas respuestas terminan en reunión agendada, y qué tan rápido contestas una respuesta entrante.

Etapa ocho —reunión realizada—. La tasa de asistencia: cuántas de las reuniones agendadas se realizan, es decir, cuántas veces la persona efectivamente aparece. Ojo: mide que la reunión ocurra, no el acto de agendar. Son cosas distintas.

Etapa nueve —precalificación—. Reuniones validadas por el AE. Se confirma con un retraso, cuando el AE toma la reunión y comprueba si el prospecto era el indicado.

Etapa diez —handoff—. Qué tan preparado llegó el AE: si tuvo todo el contexto o tuvo que improvisar.

Y por encima de todas, una métrica que sintetiza el embudo entero: la conversión de empresa contactada a reunión calificada. Es esa del orden del uno a tres por ciento, con tres como mejor caso. No pertenece a ninguna etapa: resume cuánto del total termina en una reunión que de verdad sirve.

Esta es la idea más importante del bloque. Las métricas aguas abajo son síntomas; las de aguas arriba son causas.

Si la tasa de asistencia cae, el síntoma se ve al final del proceso. Pero la causa probable está antes: un mal agendamiento, o una precalificación floja que dejó pasar gente sin interés real o sin peso en la decisión. Por eso el diagnóstico siempre recorre el embudo de abajo hacia arriba. Buscas dónde se originó el síntoma, no dónde se observa.

Y una nota práctica. Históricamente, el outbound medía la tasa de apertura —qué porcentaje de correos se abren—. Hoy ya no es confiable, por dos razones de peso.

Una. La privacidad de Apple Mail precarga los correos en sus propios servidores antes de entregarlos al dispositivo, y eso dispara el seguimiento aunque nadie haya abierto nada. Resultado: aperturas infladas artificialmente para buena parte del mercado.

Dos. Otros clientes —Outlook, o Gmail con las imágenes apagadas— registran "no abierto" aunque el prospecto sí haya leído el correo. El dato queda subestimado para ese segmento.

Entre las dos, la tasa de apertura queda con ruido en los dos sentidos. Mide cualquier cosa menos lo que parece medir. El SDR moderno la reemplaza por la tasa de respuesta —el prospecto respondió de verdad—, la tasa de rebote —salud técnica de la lista— y por revisar la reputación del dominio en las herramientas que la reportan.

Cuando una métrica cae, el SDR novato cambia el mensaje, cambia el asunto, hace una prueba A/B, pide una lista nueva. Prueba cosas al azar.

El SDR bueno recorre el embudo por descarte. La idea de fondo es sencilla: cada métrica refleja un tramo del proceso y las métricas están encadenadas. Cuando algo sale mal, no miras una métrica sola: comparas una métrica con la que tiene al lado. El problema está justo donde una métrica sana aguas arriba se convierte en una enferma aguas abajo. Ese salto te señala el tramo roto.

Por eso arrancas por el síntoma —la métrica mala— y subes etapa por etapa hasta encontrar la primera que está sana. El problema vive en el escalón entre esa métrica sana y la enferma que venías mirando. El error del novato es empezar por "cambiemos el mensaje" sin haber comparado antes las métricas vecinas.

Vamos con un caso. Es la mejor prueba del curso. Lee con calma.

Estas son las métricas semanales del SDR Juan. La semana cuatro muestra la anomalía.

Tasa de rebote: dos coma uno, dos coma tres, dos coma cero, dos coma dos por ciento. Estable.

Tasa de respuesta: dos coma cuatro, dos coma cinco, dos coma tres, cero coma siete. Caída fuerte.

Reuniones sobre respuestas: veinticinco, veintiséis, veinticuatro, veinticinco por ciento. Estable.

Tasa de asistencia: setenta y dos, setenta y cuatro, setenta y uno, setenta y tres por ciento. Estable.

Precalificaciones aprobadas: ochenta y ocho, noventa, ochenta y siete, ochenta y nueve por ciento. Estable.

Juan no cambió el mensaje, ni el ICP, ni la cadencia, ni el volumen, ni las herramientas. Nada.

¿Cuál es la hipótesis más probable, y qué revisa primero?

a) El mensaje se gastó; hay que cambiarlo y probar variantes del asunto.

b) Cambió el ICP por estacionalidad; hay que esperar dos semanas.

c) Problema de entregabilidad: los correos están cayendo a spam o promociones. Primero hay que revisar la reputación de cada dominio activo.

d) Problema de precalificación: el filtro previo no está funcionando.

¿Elegiste la c? Estás en lo correcto, prestaste atención.

Y mira el razonamiento, porque es el corazón del método.

Las métricas aguas abajo —reuniones sobre respuestas, tasa de asistencia, precalificaciones— están estables. Si el ICP o el mensaje fueran el problema, la calidad de las respuestas también caería. Pero no cae: los pocos que responden son igual de buenos que antes. Lo que cambió no es la calidad, es la cantidad de respuestas.

La tasa de rebote sigue baja, así que la lista no se contaminó. Pero la reputación del dominio pudo caer por otras razones: quejas de spam, volumen excesivo, un dominio nuevo mal calentado. Los correos se entregan técnicamente, pero caen a spam o promociones. Por eso la tasa de respuesta se derrumba sin que las demás métricas se muevan.

La acción concreta: revisar la reputación de cada dominio activo en las últimas dos semanas y correlacionar la caída con cualquier evento. Y nada de cambiar el mensaje hasta descartar la entregabilidad. El problema no es el mensaje, es el canal.

Si llegaste a la respuesta correcta con el razonamiento correcto, entendiste el método. No memorizaste una receta.

Hasta acá vimos proceso estable. Pero la verdad del outbound es que no es estable. Los filtros de spam cambian, los mercados se saturan, los mensajes que funcionaron hace seis meses dejan de funcionar. Un SDR que no itera se queda atrás.

Hay un ciclo clásico de mejora continua que aplica directo: Plan, Do, Check, Act —planificar, hacer, verificar, actuar—.

Plan, planificar. Formulas una hipótesis testeable: "Si cambio el asunto a uno que nombre a la empresa y su expansión a Chile, la tasa de respuesta sube." Concreta.

Do, hacer. Ejecutas sobre una muestra acotada. Cien prospectos, no quinientos.

Check, verificar. Mides el resultado contra la hipótesis. ¿Se cumplió? ¿En qué magnitud?

Act, actuar. Si funcionó, adoptas el cambio. Si no, vuelves a la versión anterior y formulas otra hipótesis. Sin sentimentalismos.

Y la regla de oro: un experimento es igual a una sola variable. Si cambias cuatro cosas a la vez y la tasa de respuesta sube, no aprendiste nada: no puedes aislar qué la movió. Mides antes, cambias una variable sobre muestra acotada, mides después. No hay intuición que reemplace al método, porque en outbound la variación natural es alta: el mismo mensaje puede dar una tasa de respuesta distinta de una semana a otra sin que hayas cambiado nada.

Vamos con un ejemplo rápido. Esta semana, tres prospectos respondieron con variantes de lo mismo: "Interesante, pero justo estamos con un rediseño organizacional y todo lo nuevo está pausado hasta el tercer trimestre." ¿Qué hipótesis formulas, y cómo la testeas?

Una hipótesis testeable se vería así: "hay una señal —empresas en rediseño organizacional— que es detectable en anuncios públicos y que predice 'no avanza ahora, pero se abre más adelante'. Si la filtro, puedo archivar con recontacto programado en vez de insistir ahora." Y el test: durante dos semanas, marco en el CRM las empresas donde detecto esa señal y, al cierre, veo qué porcentaje respondió con la misma objeción. Si es alto, la señal es predictiva y vale la pena armar un flujo específico.

Lo que no es hipótesis: "voy a cambiar el mensaje para esas empresas". Eso no testea nada: mezcla muchas variables a la vez. Una hipótesis tiene una sola variable, un método de medición y una magnitud esperada.

Último bloque. En outbound todo cambia: la herramienta, el cliente, el mercado, el producto. Pero hay cinco atributos que separan, consistentemente, al SDR que perdura del que no.

Uno. Disciplina de proceso. No saltea etapas aunque no lo vea nadie. Valida listas, precalifica reuniones, hace bien el handoff. Sabe que el atajo de hoy es el costo de mañana.

Dos. Lectura de métricas como segunda lengua. No dice "creo que la respuesta está baja". Dice: "la tasa de respuesta cayó la semana pasada; descarté el mensaje y el ICP porque las reuniones sobre respuestas se mantuvieron estables; reviso la reputación de los dominios ya".

Tres. Hipótesis, no intuiciones. Si cree que algo va a funcionar, lo formula como hipótesis testeable y lo prueba. No discute por sensación.

Cuatro. Tolerancia a la frustración estructural. El outbound es rechazo la mayor parte del tiempo. No se lo toma como algo personal y no pierde el foco después de una racha de llamadas sin contacto.

Cinco. Transferencia conceptual. Cuando cambia la herramienta, el cliente o el producto, no se rompe: transfiere los conceptos. Aprende el conjunto nuevo en una o dos semanas y vuelve al ritmo.

Los primeros cuatro se construyen con tiempo. El quinto es lo que esta Academy apuntó durante ocho semanas: criterio, no receta.

Repasemos las ocho semanas, rápido.

Módulo 1. Cómo funciona el juego de la venta B2B y cuál es tu rol.

Módulo 2. Cómo se entiende al otro lado: la empresa y la persona.

Módulo 3. Cómo se conecta en la práctica: escribir y conversar.

Módulo 4. Cómo se opera el sistema y cómo se mejora.

Si internalizaste los cuatro, tienes el marco completo para ejercer el rol en cualquier empresa de outbound B2B de LATAM.

Las herramientas se reemplazan. Los clientes cambian. El mercado muta. Los conceptos se quedan.

El alumno que sale de acá sabiendo por qué el multicanal le gana al canal único, por qué la precalificación no es opcional, por qué el diagnóstico va de aguas abajo hacia aguas arriba, puede entrar a cualquier empresa de outbound de LATAM y agregar valor desde la primera semana.

Porque no aprendiste "cómo se usa tal herramienta en tal empresa". Aprendiste qué es el outbound, cómo funciona y por qué funciona.

Complementa este contenido con las guías adjuntas al módulo. Es la guía más densa del curso: las métricas completas, el método de diagnóstico desplegado paso a paso, casos adicionales de descarte, el ciclo de mejora continua en plantilla, los cinco atributos con preguntas de auto-evaluación, y la sección de cierre del curso.

Lo que sigue ahora no es "la semana que viene". Es el camino de ejercer el rol. Esta semana te quedan la prueba del Módulo 4, la prueba final integradora —que continúa el caso de la Semana 7— y la sesión en vivo de cierre con el profesor. Después, empieza la siguiente parte.

Suerte. Y nos vemos en la sesión de cierre.
```

> Nota: el bloque "Fuentes de este video" del `.md` es para la Bibliografía en plataforma,
> **no se narra**.
