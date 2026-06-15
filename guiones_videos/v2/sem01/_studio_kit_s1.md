# Kit de armado en Studio — Semana 1 (Módulo 1)

> Para construir los 3 videos **a mano en HeyGen Studio** (decisión 2026-06-11: los
> templates de la cuenta no exponen variable de texto, así que no se generan por API).
> Acá tenés el **texto hablado limpio** de cada video, ya sin `[SLIDE:...]`, sin headers
> ni markdown — listo para pegar en el script del avatar. Fuente: los `.md` corregidos
> de `sem01/` (correcciones del líder ya aplicadas).

## Antes de pegar — 3 cosas que aplican a los 3 videos

1. **Activá el Brand Glossary "Video Agent Pronunciation"** (id `0e3e834da76f4f988fac667e40fcbbaf`)
   en el proyecto. Ya tiene: B2B→"bi tu bi", B2C→"bi tu ci", SDR→"es di ar", **LOB→"el ou bi"**.
   Esto arregla el "bi dos be" sin tocar el texto/subtítulos.
2. **Voz en español:** confirmá que la voz del template renderiza en español (en
   `heygen_defaults.json` la voz figuraba como `language: English` — probable co-causa del
   mal acento). Si suena en inglés, cambiá la voz a la variante ES.
3. **Pausas al enumerar:** donde el guion lista "Uno… Dos… Tres…", insertá un **Pause**
   (botón Pause, ~0.5s) entre cada ítem. El texto ya viene con cada ítem en su propio
   párrafo para que sea fácil ubicarlos.

---

## Video 1 — `intro` · "Anatomía de la venta B2B" (~2.4 min)

**Fixes visuales en Studio (feedback del líder):**
- ~seg 18: "cuadritos" raros → revisar esa escena/animación del template.
- Animación encima del avatar → quitar/reemplazar el overlay.

**Texto para pegar:**

```
Imagina que vendes una herramienta empresarial. Mandas un email perfecto: claro, breve, al contacto correcto. Y nada. Silencio durante tres semanas.

No es tu email. Es que del otro lado hay un sistema que no se mueve como tú crees.

En el video de bienvenida planteamos la pregunta que abre todo este curso: ¿cómo toman decisiones de compra las empresas, y en qué se diferencia eso, estructuralmente, de una decisión personal?

Esta primera semana se llama "Anatomía de la venta B2B". Antes de entrar al contenido, te quiero anticipar dos cosas: qué vas a poder hacer al final de la semana, y cómo está organizado el material.

Al terminar esta semana vas a poder hacer cuatro cosas concretas:

Uno. Describir las etapas de un buying cycle B2B —awareness, consideración, evaluación, decisión, implementación—, con sus duraciones típicas y por qué cada una existe.

Dos. Identificar los stakeholders que participan en una decisión: quién decide, quién veta, quién usa, quién paga, y por qué casi nunca son la misma persona.

Tres. Explicar el ciclo de vida del prospecto —cómo la empresa que vende clasifica a un cliente potencial, de Prospect a Customer— y ubicar tu trabajo de SDR dentro de él.

Cuatro. Articular por qué un deal B2B es estructuralmente distinto de una venta B2C —no solo "más grande", estructuralmente distinto.

Estas cuatro cosas son el cimiento de todo lo que vamos a construir en las siete semanas siguientes. Si las internalizas, el resto del curso te va a hacer mucho más sentido.

Cada semana del curso tiene tres componentes que se complementan:

Uno. Este video de intro —el que estás viendo ahora—, que te da el mapa de la semana.

Dos. Un video de contenido, que profundiza el concepto más importante con un ejercicio resuelto en vivo. Es el siguiente.

Tres. La guía adjunta al módulo, en PDF, con el contenido completo desarrollado bloque por bloque, todos los ejercicios y la bibliografía. Está hecha para que la consultes mientras trabajas, no para leerla una vez de corrido.

Mi recomendación: mira primero los dos videos para tener el mapa mental; después abre la guía y trabájala con calma.

Vamos al contenido. Nos vemos en el siguiente video.
```

---

## Video 2 — `contenido_1` · "Cómo se decide una compra B2B" (Bloques 1-3, ~7.7 min)

**Fixes visuales en Studio (feedback del líder):**
- **Buying cycle (las 5 etapas):** solo aparecían iconos de awareness/consideración/
  evaluación → **faltan decisión e implementación**. Agregar los 5 iconos (el guion sí
  nombra las 5).
- ~min 1:00: iconos se cortan → ajustar encuadre/escala.
- Animación encima del avatar → quitar/reemplazar overlay.

**Texto para pegar:**

```
Un estudiante quiere una laptop. La compra en dos días.

Una empresa de trescientos empleados quiere un CRM —un software para organizar sus clientes y sus ventas—. Tarda entre seis y doce meses, participan entre cinco y doce personas, y en más de un tercio de los casos no termina comprando nada.

Acá empieza todo lo que vas a aprender en este curso.

En este video cubrimos los primeros tres temas de la semana: qué hace al B2B estructuralmente distinto del B2C, cómo se mueve realmente la decisión adentro de una empresa, y por qué etapas pasa una compra B2B. Cierra con un caso para que apliques lo aprendido.

Una empresa no compra como compra una persona. Hay cinco diferencias estructurales que cambian todo.

Una. Cantidad de personas involucradas. En B2C decide una. En B2B, entre seis y diez en promedio. En compras grandes, quince o veinte.

Dos. Duración del ciclo. En B2C mide horas o días. En B2B mide meses. Una compra grande de software para una empresa puede tomar más de un año, desde el primer contacto hasta la firma.

Tres. Separación entre quien paga, quien decide y quien usa. En B2C es la misma persona. En B2B casi nunca: usa marketing, paga finanzas, decide el director, firma el CEO, revisa legal, certifica IT.

Cuatro. Racionalidad aparente, emocionalidad real. Se justifica con ROI, demos y casos de éxito. Pero la decisión final se mueve por carrera, miedo al error visible, peleas internas, lealtades viejas.

Cinco. Ticket más alto, consecuencias sostenidas. Equivocarse con un CRM cuesta dos años, afecta a cincuenta personas, y hay que explicarlo en el directorio. La aversión al error es muchísimo mayor.

Si le preguntas a un director por qué eligió a cierto proveedor, te va a dar una respuesta racional: una tabla comparativa, un cálculo de cuánto iban a ahorrar, una prueba de dos meses que confirmó la decisión.

Esa respuesta es verdadera en la justificación, pero falsa en la secuencia.

La mayoría de las decisiones B2B funcionan al revés de lo que parecen. Alguien dentro ya eligió quién quería que ganara. El proceso formal existió para justificar esa decisión frente a los demás.

No es ser malpensado. Es cómo funciona la mente humana, incluso en gente muy técnica: primero se decide rápido, medio por intuición, y después se arma la explicación racional que respalda esa decisión. En B2B se amplifica, porque el decisor también tiene que vender la decisión hacia adentro de su empresa.

Detrás de cada decisión hay cinco capas que nunca aparecen en la comparación formal: avance de carrera, estatus interno, costos no visibles del cambio, miedo al error público, y lealtades viejas con el proveedor actual.

Las decisiones B2B se toman en grupo, no por una sola persona. Y "ponerse de acuerdo" no significa votar: significa que nadie se oponga.

Es más fácil lograr un "sí" de una persona, que un "no me opongo" de cinco.

Implicación para ti: tu email no tiene que gustarle a tu contacto. Tiene que ser presentable dentro de la empresa. Si tu contacto lo lee y le encanta, pero piensa "esto no se lo puedo mostrar a mi director sin parecer ingenuo", tu email no llega a ningún lado.

Toda compra B2B pasa por cinco etapas.

Una. Awareness. El comprador no sabe que tiene el problema. Acá entra el outbound: no le vendes, le metes la pregunta en la cabeza.

Dos. Consideración. Reconoce el problema y empieza a explorar. Busca, pregunta a pares, pide referencias.

Tres. Evaluación. Armó una lista corta de tres a cinco opciones. Pide demos, hace tablas comparativas, llama a otros clientes. Acá se pierden más deals. Y no porque gane otro proveedor: porque el grupo no logra ponerse de acuerdo y todo queda congelado. De hecho, perder contra "no hacer nada" es más común que perder contra un competidor.

Cuatro. Decisión. Se elige proveedor. La política interna que vimos antes pesa más que la matriz.

Cinco. Implementación. Se firma y se implementa. Te importa porque las implementaciones que salen mal no renuevan, y una mala experiencia con tu industria cierra la puerta a futuro.

Dónde operas tú como SDR: principalmente en awareness y consideración. Tu trabajo es llevar al prospecto de "no lo estaba pensando" a "podría valer una reunión para entender mejor".

Vamos con un caso para que apliques lo aprendido.

Julia es gerenta de marketing en una empresa de e-commerce de ciento ochenta empleados. Recibió una propuesta de un nuevo proveedor de automatización de marketing. Le parece buena.

Pasan seis semanas. No agenda la reunión.

El SDR le hace follow-up. Julia responde: "Perdón por la demora. La propuesta me parece muy interesante. Déjame terminar un par de cosas internamente y me pongo en contacto."

Pasan otras cuatro semanas. Nada.

El SDR llama. Julia atiende y dice: "Mira, la verdad es que internamente estamos viendo cómo plantearlo. Mi jefa, Diana, fue quien validó al proveedor actual hace dos años, y no es fácil llevar la conversación de cambiarlo. Estoy viendo cómo presentarlo."

Pregunta: ¿Cuál es el factor principal que está frenando la decisión?

a) Julia no le ve valor al producto.
b) El precio es muy alto.
c) Hay un factor político interno: cambiar al proveedor que validó Diana implica contradecir a su jefa, y eso pesa más que el análisis técnico.
d) Julia no tiene autoridad para decidir.

¿Qué opción elegiste? ¿Fue la c? Entonces estás en lo correcto, prestaste atención.

Julia te lo está diciendo entre líneas. El proveedor no es el problema. El problema es que proponer un cambio implica una conversación difícil con su jefa. Esta es exactamente la clase de política interna invisible que gobierna las ventas B2B.

¿Qué debería hacer el SDR acá? El camino corto no es presionar por la demo. El camino corto es ayudar a Julia a armar la conversación interna. Algo como: "¿Qué argumentos te servirían para plantear esto a Diana? ¿Quieres que te mande un caso de uso específico, fácil de compartir?" Eso destraba lo que ninguna demo técnica va a destrabar.

Complementa este contenido con las guías adjuntas al módulo. Ahí vas a encontrar el desarrollo completo de los tres temas: las cinco diferencias B2C/B2B con ejemplos por industria, las cinco capas invisibles desarrolladas una por una, los datos de duración típica por etapa del buying cycle, y dos ejercicios adicionales —uno de awareness, otro de post-decisión— para que practiques identificar etapas en frío.

Ya sabes qué compra una empresa, cómo se mueve la decisión por dentro y por qué etapas pasa.

En el segundo video de la semana respondemos las dos preguntas que faltan: quiénes son las personas sentadas en esa mesa de decisión, y cómo tu empresa, la que vende, clasifica a ese prospecto en su propio sistema.

Nos vemos en el video 2.
```

> Nota: el bloque "Fuentes de este video" del `.md` es para la sección de Bibliografía en
> la plataforma, **no se narra** — no lo pegues en el script del avatar.

---

## Video 3 — `contenido_2` · "Quiénes deciden y dónde encajas tú" (Bloques 4-6, ~9.5 min)

**Fixes visuales en Studio (feedback del líder):**
- **Ciclo de vida del prospecto (las 5 etapas):** la slide debe mostrar las 5 correctas
  —Prospect → MQL → SQL → Opportunity → Customer— y **terminar en Customer** (eliminar
  cualquier "Renovación/Churn/Expansión" o el viejo "customer lifecycle de Siete" de 14
  etapas, que el líder marcó como "todo mal").
- Animación encima del avatar → quitar/reemplazar overlay.
- Si reaparece el listado de etapas como iconos, mismo criterio que el buying cycle: que
  estén las 5 completas.

**Texto para pegar:**

```
Ya sabes que del otro lado de tu email hay un comité, no una persona. La pregunta de este video es más concreta:

¿Quiénes son, exactamente, esas personas? ¿Cómo le hablas a cada una? Y cómo clasifica tu empresa a ese prospecto en su propio sistema?

Cerramos la semana con los tres temas que faltan: los nueve roles del comité de decisión, el ciclo de vida del prospecto —cómo tu empresa lo clasifica según su etapa en el proceso de venta—, y la disociación entre quien paga, quien aprueba y quien usa. Termina con un caso de stakeholders para que apliques lo aprendido.

Cualquier decisión de compra grande tiene cuatro roles centrales que vas a ver en casi todos los deals. A veces son cuatro personas distintas; a veces una misma persona cumple varios.

Uno. El que pone el dinero — decisor económico, o Economic Buyer. Tiene autoridad final sobre el presupuesto. Puede vetar o aprobar. Dueño, gerente general, director de área, VP. Le importa: cuánto va a recuperar de lo que invierte, el riesgo de error, el impacto en resultados.

Dos. El que evalúa que funcione — decisor técnico, o Technical Buyer. Revisa si la solución cumple los requisitos mínimos. No aprueba, pero puede vetar. Suele ser tecnología, seguridad o legal. Le importa: que no rompa nada de lo que ya tienen, que cumpla normas, que se pueda mantener.

Tres. El que la usa — usuario, o User Buyer. Quien va a trabajar con la solución día a día. En el papel no decide, pero su rechazo pesa muchísimo. Si los que la usan la odian, la implementación fracasa.

Cuatro. El aliado interno — coach o champion. Alguien dentro de la empresa que quiere que tú ganes y te va dando información de lo que pasa por dentro. Sin un aliado interno, ganar un deal complejo es muy difícil.

Más estos cinco que vas a encontrar muy seguido: influenciador (opinión que pesa pero no decide), bloqueador (se opone activamente al cambio), referidor (te conecta con el decisor —crítico para el SDR—), compras o procurement (no decide qué, decide cómo: precio, plazos, SLAs), y legal (valida contratos, puede frustrar deals que parecían cerrados).

Regla práctica para ti como SDR. Cada rol tiene una motivación y un miedo distintos. El economic buyer quiere ROI y le da miedo el error caro. El technical buyer quiere robustez y le da miedo lo que no previó. El usuario quiere facilidad y le da miedo aprender algo que no le sirve. Tu mensaje tiene que hablarle a los suyos, no a los de otro rol.

Un email al economic buyer hablando de "facilidad de uso" suena débil. Un email al usuario hablando de "ROI proyectado" suena fuera de contexto.

Hasta acá viste el proceso desde el lado de quien compra: las cinco etapas internas del cliente. Ahora damos vuelta la cámara y lo vemos desde tu lado, el de la empresa que vende.

A la empresa que todavía no te compró pero podría hacerlo se le llama prospecto. Y al camino que recorre ese prospecto en tu sistema, desde que aparece en tu radar hasta que firma, se le llama el ciclo de vida del prospecto. Es la etiqueta que tu empresa le pone a cada contacto según qué tan avanzada está la relación, y te sirve para saber qué te toca hacer a continuación con cada uno.

Cinco etapas, de la más fría a la más avanzada.

Una. Prospect. Encaja con tu cliente ideal —tu ICP— pero todavía no sabe que existes.
Dos. MQL (Marketing Qualified Lead). Levantó la mano de forma suave por su cuenta: descargó algo, fue a un webinar, siguió un email. En outbound muchas veces esta etapa se salta.
Tres. SQL (Sales Qualified Lead). Pasó el filtro de ventas: perfil correcto y señales reales de interés. Aquí empieza el trabajo activo del SDR.
Cuatro. Opportunity. Aceptó una reunión con el AE y hay una venta concreta sobre la mesa, con monto estimado.
Cinco. Customer. Firmó. Y acá termina la lista: ya es cliente.

Lo que pasa después de la firma —que renueve, que compre más o que se vaya— es otra historia, de otra área: Atención al Cliente. No es trabajo del SDR ni parte de esta lista.

Dónde operas tú: de Prospect a Opportunity. Tu trabajo es convertir un prospecto frío en un SQL, conseguir la reunión —ahí se crea la Opportunity— y pasársela al AE con contexto. A ese pase se le llama handoff. Después del handoff, el SDR sale de la conversación.

En empresas grandes, una LOB —Line of Business, o línea de negocio— es una unidad con su propio presupuesto, prioridades y decisiones de compra.

Un banco grande puede tener LOBs distintas para Banca Personal, Banca Empresas, Inversiones y Seguros. Cada una compra su propio CRM, elige sus propios proveedores. Tu decisor real no es "el banco", es el VP de la LOB específica que podría usar tu producto.

Y dentro de una LOB, las tres capas casi nunca son la misma persona:

Capa 1: Quién la usa. Vendedores, equipo operativo. Acá está tu champion potencial.
Capa 2: Quién la aprueba técnicamente. IT. No la elige, pero la puede vetar.
Capa 3: Quién la paga. VP de la LOB o Finanzas corporativa.

La situación clásica: el gerente quiere la herramienta, IT no objeta, pero el VP de Ventas dice "este trimestre el presupuesto ya está comprometido". El deal no cierra porque ninguno de los usuarios técnicos tenía el problema. El problema lo tenía quien firma el cheque.

Como SDR, en cuentas medianas o grandes, identifica las tres capas temprano. Champion + aprobador técnico + decisor económico. Una sola pata no alcanza.

Vamos con un caso para que apliques los roles del comité.

Imagina una empresa de doscientos cincuenta empleados evaluando un software de gestión de cadena de suministro. Hablamos de dos contactos.

Juan es VP de Operaciones. Va a firmar la PO final. Es claramente el decisor económico — eso es directo.

Pero el caso interesante es Ana.

Ana es Coordinadora de Operaciones. No decide nada formalmente, pero está obsesionada con que arreglen este problema desde hace un año. Tiene acceso directo a Juan. Y fue Ana quien te pasó el contacto de Juan.

Pregunta: ¿Qué rol juega Ana?

a) Bloqueadora.
b) Decisora técnica.
c) Coach o champion, y al mismo tiempo referidora.
d) Usuaria pasiva.

¿Elegiste la c? Estás en lo correcto, prestaste atención.

Ana es las dos cosas a la vez. Es coach porque quiere el cambio y te da información del juego interno. Y es referidora porque te pasó el contacto del decisor.

Y acá viene la parte operativa, lo que sí o sí te tienes que llevar: este perfil es oro para un SDR. Cuida a Ana. Hazle llegar material que ella pueda usar internamente: un caso de uso específico, un cálculo de impacto en su área, una frase corta que pueda copiar en un email a Juan. Tú no estás vendiendo el producto, estás equipándola para que ella lo venda hacia adentro.

Recapitulemos en seis puntos lo que te llevas de esta semana:

Uno. El B2B es estructuralmente distinto del B2C: comité de seis a diez, ciclos de seis a doce meses, separación entre quien paga y quien usa.

Dos. La decisión formal justifica una decisión que ya se tomó por carrera, política y miedo al error público.

Tres. Cinco etapas de buying cycle; el SDR opera en awareness y consideración.

Cuatro. Nueve roles posibles en el comité; cada uno con motivación y miedo distintos. Habla a los suyos, no a los de otro rol.

Cinco. Ciclo de vida del prospecto: cómo tu empresa lo clasifica, de Prospect a Customer. Lo posterior a la firma es de Atención al Cliente, no del SDR.

Seis. En empresas grandes, identifica las tres capas temprano: quién usa, quién aprueba, quién paga.

Lo que no te llevas, a propósito: scripts y plantillas. Eso viene en módulos 2 y 3. Lo que construiste esta semana es criterio para leer cualquier deal B2B que tengas enfrente.

Complementa este contenido con las guías adjuntas al módulo. Ahí desarrollamos los nueve roles uno por uno con su motivación y su miedo, los seis casos completos del lifecycle, y un anexo de cómo varían las dinámicas LOB por industria —retail, tecnología, servicios financieros—.

En la Semana 2 cambiamos de eje. Pasamos del "qué es un deal B2B" al rol del SDR dentro de ese deal. La pregunta central va a ser: ¿qué vende un SDR realmente, y hasta dónde llega su responsabilidad?

Nos vemos la semana que viene.
```

> Nota: el bloque "Fuentes de este video" del `.md` es para la Bibliografía en plataforma,
> **no se narra**.
