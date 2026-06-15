---
video: Sem 8 — Bloque 5
modulo: 4 — El sistema
semana: 8 — Del proceso al mindset
titulo: Las métricas del outbound — qué mide cada una
duracion_estimada: ~6:45
palabras_aprox: 960
ejercicio: no
fuente_doc: SDR_Academy_Siete_Documento_Maestro.md, líneas 11021-11080
---

# Bloque 5 — Las métricas del outbound: qué mide cada una

## [GANCHO ~15s]

Cada etapa del proceso tiene una **métrica asociada**. Juntas, forman el funnel del SDR.

Y la lectura correcta del funnel es lo que te permite **saber dónde está el problema** sin adivinar.

## [CONTEXTO ~15s]

Vamos por el funnel etapa por etapa, una regla clave para interpretar caídas, y por qué hay una métrica que el SDR moderno **ya no mide**, aunque la mayoría sigue haciéndolo.

## [EL FUNNEL Y SUS MÉTRICAS ~3:00]

**[SLIDE: El funnel del SDR — métrica por etapa]**

Vamos por las etapas y su métrica.

**Etapas 1 a 3 — ICP, listas, limpieza.** Métrica: **bounce rate**, por debajo del tres por ciento. Mide salud de la lista y reputación del dominio.

**Etapas 4 y 5 — diseño de secuencia y ejecución.** Métrica: **reply rate**, entre dos y cinco por ciento es el benchmark LATAM. Mide relevancia del mensaje, más deliverability.

**Etapas 6 y 7 — gestión de respuestas y calificación.** Métrica: **meeting rate sobre reply**, entre el veinte y el treinta por ciento. Mide la calidad del flujo de respuesta.

**Etapa 8 — agendamiento.** Métrica: **show rate**, por encima del setenta por ciento. Mide la calidad del agendamiento. ¿La gente aparece a la reunión?

**Etapa 9 — precalificación.** Métrica: **precalificación aprobada**, por encima del ochenta y cinco por ciento. Mide la calidad del filtro: fit real, no forzado.

**Etapa 10 — handoff.** Métrica de síntesis: **conversión empresa a reunión calificada**, alrededor del uno por ciento. Es el resumen de todo el funnel.

## [LA REGLA CLAVE — SÍNTOMA VS CAUSA ~1:30]

**[SLIDE: Las métricas aguas abajo son síntomas. Aguas arriba son causas.]**

Esta es la idea más importante de todo el bloque.

**Si el show rate cae**, el síntoma se ve en la etapa 8. Pero **la causa probable está antes**: mala calificación en las etapas 6 y 7, mal agendamiento en la 8, falta de precalificación en la 9.

**Si el reply rate cae**, la causa puede estar en la lista —etapas 1 a 3—, en el mensaje —etapa 4—, en deliverability —etapas 4 y 5—, o en todo combinado.

Por eso **el diagnóstico siempre recorre el funnel de abajo hacia arriba**. Buscás dónde **se originó** el síntoma, no dónde **se observa**.

Esta diferencia es exactamente lo que separa a un SDR que arregla problemas de uno que **muda síntomas de un lado al otro sin entender la causa**.

## [LA MÉTRICA QUE EL SDR MODERNO YA NO MIDE ~1:15]

**[SLIDE: Por qué NO se mide open rate]**

Históricamente, outbound B2B medía el **open rate**: qué porcentaje de emails se abren. En 2026, **ya no es confiable**. Tres razones, en orden de impacto.

**Una. El pixel tracking daña la deliverability.**

El pixel es una imagen invisible en el email que "canta" cuando se abre. Los filtros anti-spam **lo detectan**, y clasifican el email como marketing. Cae a promociones o spam directamente.

**Dos. Apple Mail Privacy Protection distorsiona el dato.**

Desde 2021, Apple **pre-abre los emails en el servidor antes de entregarlos**. Eso infla el open rate artificialmente. Tu métrica te dice ochenta por ciento de apertura, y la realidad puede ser veinte.

**Tres. Otros clientes devuelven datos falsos.**

Outlook, o Gmail con imágenes apagadas, devuelven "open igual false" aunque el prospecto haya leído el email.

**[SLIDE: Lo que sí se mide en 2026]**

El SDR moderno reemplaza el open rate por cuatro métricas más sólidas.

- **Reply rate.** Dato comportamental duro. Si hay respuesta, hubo lectura.
- **Bounce rate.** Salud técnica de la lista.
- **Seed testing.** Mandar a casillas controladas propias para confirmar que el email llega al inbox.
- **Postmaster Tools.** Reputación del dominio, directo de la fuente.

Open rate es **un dato ruidoso que daña la infraestructura** a cambio de muy poco insight. Cualquier consultor que te recomiende optimizar open rate en 2026, **está leyendo la realidad de hace cinco años**.

## [CIERRE Y PUENTE ~15s]

Ya leés el funnel. En el próximo bloque vamos al método específico para **encontrar la causa raíz** cuando una métrica cae: **diagnóstico por descarte**. Es el método que separa al SDR que arregla problemas del que prueba cosas al azar.

Nos vemos en el Bloque 6.

---

**Fuentes de este bloque:**
- Bridge Group (2023). *SDR Metrics Report*.
- Instantly (2026). *Cold Email Benchmark Report*.
- Cognism (2025-2026). *State of Outbound*.
