# Prompt de optimización — Revisión Módulo 1 (videos HeyGen)

> Reestructuración de los comentarios del líder de la academia sobre los videos del
> Módulo 1 generados en HeyGen. Cada ítem indica **dónde** se arregla (guion `.md`,
> config de voz HeyGen, o template de HeyGen Studio) porque el pipeline
> (`tools/heygen_generate_videos.py`) **borra** los `[SLIDE:...]` y el markdown: el
> `.md` solo controla el **texto que habla el avatar**, no los visuales.

Archivos del módulo:
- `guiones_videos/v2/sem01/intro.md` — Intro Módulo 1
- `guiones_videos/v2/sem01/contenido_1.md` — Bloques 1-3 (buying cycle)
- `guiones_videos/v2/sem01/contenido_2.md` — Bloques 4-6 (roles, lifecycle, LOB)
- Fuente: `SDR_Academy_Siete_Documento_Maestro.md` (líneas ~2518-2987)

---

## A. CONTENIDO — corrección del modelo de etapas (PRIORIDAD ALTA)

El error de fondo: el segundo set de etapas está encuadrado como *"cómo te ve el
prospecto a ti"*. Es incorrecto. El modelo correcto del líder:

- **Set 1 (5):** etapas **internas del prospecto**, desde su punto de vista interno →
  *Awareness · Consideración · Evaluación · Decisión · Implementación* (ya correcto, Bloque 3).
- **Set 2 (5):** etapas con las que **la empresa proveedora (tú/Siete) cataloga al
  prospecto** según en qué punto del proceso de venta está →
  *Prospect · MQL · SQL · Opportunity · Customer* **(⏳ lista pendiente de confirmación
  del líder — ver bloqueo abajo)**.

> ✅ **RESUELTO (2026-06-10/11):** el líder confirmó vía `LIMPIO_S1.md` el Set 2 =
> **Prospect · MQL · SQL · Opportunity · Customer** (5, termina en Customer; post-venta =
> Atención al Cliente). Los 3 `.md` de `sem01/` ya están corregidos. Texto hablado listo
> para Studio en `sem01/_studio_kit_s1.md`.

### A1. Reescribir Bloque 5 de `contenido_2.md` (líneas ~50-69)
- Cambiar el encuadre: NO "así es como te ven los prospectos en tu CRM / cómo te ve a
  ti", SÍ "así es como tu empresa cataloga al prospecto según su etapa en el proceso de venta".
- Bajar de **6 a 5 etapas**: quitar "Renovación / Churn / Expansión" del set (es
  post-venta, fuera del scope SDR; mención opcional de una línea como "lo posterior lo
  maneja Client Success", sin nombrarlo como un segundo lifecycle).
- **Eliminar por completo** el sub-bloque "[SLIDE: Atención — dos lifecycles distintos]"
  y el párrafo del "customer lifecycle de Siete" (14 etapas Need→Advocate). El líder:
  *"esto en realidad está todo mal"*.

Texto puente propuesto (reemplaza la transición vieja):
> "Hasta acá viste las 5 etapas por las que pasa el prospecto desde adentro: su propio
> proceso de compra. Ahora mira el mismo recorrido desde tu lado: las 5 etapas con las
> que tu empresa cataloga a ese mismo prospecto según en qué punto del proceso de venta
> está. Mismas personas, clasificadas desde tu CRM."

### A2. Limpiar referencias colaterales al encuadre viejo
- `contenido_2.md` L20-22 (GANCHO): "¿dónde estás tú en su CRM?" → reformular a "cómo
  tu empresa clasifica al prospecto en su propio sistema".
- `contenido_2.md` L26 (CONTEXTO): "el lifecycle del prospecto —cómo te ven a ti en su
  sistema—" → "cómo tu empresa cataloga al prospecto según su etapa en el proceso de venta".
- `contenido_2.md` L138 (SÍNTESIS, punto Cinco): "Lifecycle del prospecto, distinto del
  lifecycle del cliente. No los mezcles." → "Lifecycle del prospecto: las 5 etapas con
  las que tu empresa lo cataloga, de Prospect a Customer."
- `contenido_1.md` L129 (CIERRE): "dónde estás tú en su CRM" → "cómo tu empresa lo
  cataloga en el CRM".
- `intro.md` L37 (objetivo 3): revisar redacción para que sea consistente (hoy dice
  "ciclo de vida del prospecto, de Prospect a Customer" — OK, solo alinear el verbo).

### A3. Documento Maestro — fuera de alcance (lo revisa el líder)
El mismo error vive en `SDR_Academy_Siete_Documento_Maestro.md` Bloque 5 (L2838-2880).
**Decisión (2026-06-10):** por ahora corregir SOLO los guiones de video. El Documento
Maestro lo revisa y corrige el **líder de la academia**. Queda la nota para que la fuente
se alinee después (si no, el error se re-propaga a futuros contenidos).

---

## B. PRONUNCIACIÓN — Brand Glossary de HeyGen (NO en el texto del guion)

> ✅ **HECHO (inspección API 2026-06-11):** el Brand Glossary ya existe —
> **"Video Agent Pronunciation"**, id `0e3e834da76f4f988fac667e40fcbbaf` — con B2B→"bi tu bi",
> B2C→"bi tu ci", SDR→"es di ar" y **LOB→"el ou bi"** (agregado hoy vía
> `POST /v1/brand_voice/{id}`). El param en `/v2/template/{id}/generate` se llama
> **`brand_voice_id`**. Falta solo: activarlo en Studio + validar idioma de la voz (punto 3).

**Investigación HeyGen 2026-06-10 — mecanismo confirmado:**

HeyGen tiene una función nativa de **Pronunciation / Brand Glossary**:
- En el editor: doble clic en la palabra → "Pronunciation" → se respelea con guiones
  (ej. `B2B` → `bi-tu-bi`). **Afecta solo el audio, NO el texto visible** → los
  subtítulos quedan limpios. Justo lo que necesitamos.
- Cada regla se guarda en el **Brand Glossary** (reutilizable en todos los videos); se
  puede cargar por CSV. En el editor, las palabras con regla salen en violeta itálica.
- **El Template API aplica el Brand Glossary** (reglas de pronunciación) al renderizar,
  y el `brand_glossary_id` se reutiliza entre Translation/Proofread/Template.

**Plan:**
1. Crear un Brand Glossary "Siete Academy" (una vez) con:
   - **B2B** → `bi-tu-bi`
   - **B2C** → `bi-tu-ci`
   - **LOB** → `el-ou-bi`
   - Recomendado agregar (mismo riesgo, no señalados): SDR, AE, CRM, ICP, MQL, SQL, ROI,
     RFP, KPI, PO, CEO, CFO, VP, IT.
2. Conectar el glossary al pipeline: agregar `brand_glossary_id` al payload de
   `tools/heygen_generate_videos.py` (o dejarlo como glossary por defecto de la cuenta
   para que se aplique solo). ⏳ **Verificar el nombre exacto del parámetro contra la
   API en vivo** (las páginas de migración no lo confirmaron; necesita API key, sin créditos).
3. Validar idioma de la voz: en `tools/heygen_defaults.json` figura `"language":
   "English"` (voz MX, `voice_id` con formato ElevenLabs). Confirmar que renderiza en
   español — probable co-causa del "bi-dos-be".

---

## C. RITMO / PAUSAS al enumerar

Síntoma: termina una idea numerada y pasa al siguiente número sin pausa.

**Investigación HeyGen 2026-06-10:**
- Nativo (editor): botón **Pause** en el script = incrementos de 0.5s, editable para
  pausas más largas (incluso escenas de solo silencio).
- Vía API: SSML `<break time="0.5s"/>` con `input_type: "ssml"`. Antes verificar
  `support_pause` del voice en `GET /v3/voices`.
- ⚠️ **Limitación a verificar:** nuestro template recibe el guion en una variable de
  tipo `text` (`script`). Las pausas del botón Pause y el SSML podrían **no pasar** por
  una variable de texto plano. Si no pasan, las opciones son: (a) partir las
  enumeraciones en escenas separadas en Studio, (b) escenas de pausa, (c) bajar `speed`
  a ~0.95. Confirmar contra la API en vivo.
- En el guion (sí ayuda igual): cada ítem enumerado en su **propio párrafo** (doble
  salto de línea) para forzar respiración.

---

## D. PRODUCCIÓN VISUAL — template HeyGen Studio + investigación API

Estos NO se arreglan editando `.md` (los `[SLIDE:...]` se eliminan en el pipeline).

> ✅ **RESUELTO (inspección API 2026-06-11):** el `template_id` que teníamos
> (`c1e07437…4931e`) **no existe** en la cuenta. Los dos templates reales
> (`08f619e2…9a0` y `9f3a2c41…955`, ambos "La Realidad del B2B vs C") devuelven
> **`variables: {}`** → no exponen variable de texto, así que **la API no puede inyectar
> los guiones**. **Decisión 2026-06-11: Semana 1 se arma manual en Studio.** Los 4 bugs
> visuales de abajo son trabajo manual de todos modos.

**Investigación HeyGen 2026-06-10 — qué se puede vía API y qué no:**
- El Template API solo puede **reemplazar variables explícitamente definidas** en el
  template: `text`, `image`, `video`, `audio`, `voice`, `avatar`.
- Las **secuencias de iconos, animaciones de escena, overlays y los "cuadritos" son
  diseño de escena en Studio** → **NO controlables por API**, salvo que un icono puntual
  haya sido definido como variable `image` (improbable en una secuencia animada).
- **Conclusión:** los 4 bugs visuales de abajo son **trabajo manual en HeyGen Studio**
  sobre el template. La API solo sirve para (a) re-renderizar después de arreglar, y
  (b) intercambiar elementos que SÍ sean variables de imagen.
- ⏳ **Paso de verificación definitivo (read-only, sin créditos):** existe un endpoint
  para **listar las variables/escenas de un template** (devuelve scene IDs, scripts y
  variables). Correrlo con el `template_id` real enumera exactamente qué es variable vs
  qué está "horneado". Requiere `template_id` + `HEYGEN_API_KEY`.

Notas de producción por video (para quien edita el template en Studio):

| Video | Timestamp | Problema | Acción |
|---|---|---|---|
| Intro Mód 1 | ~seg 18 | "Cuadritos" raros | Revisar escena/animación del template |
| Buying cycle | al enumerar etapas | Solo aparecen iconos de awareness/consideración/evaluación; faltan decisión e implementación | Agregar iconos de las 5 etapas (el guion sí tiene las 5) |
| (varios) | ~min 1:00 | Iconos se cortan | Ajustar encuadre/escala de iconos |
| (todos) | sobre el avatar | Animaciones encima del avatar quedan raras | Reemplazar/quitar overlay de animación |

Nota aparte (no urgente): avatar "muy IA" — se acepta para lanzar rápido; mejorar en
próximas ediciones.

---

## Resumen de dónde se arregla cada comentario

- **Guion `.md` (yo):** modelo de etapas (A1-A2), paragraphing de pausas (C).
- **Config voz HeyGen:** pronunciación B2B/B2C/LOB + idioma (B), pausas/break/speed (C).
- **Template Studio / API (investigar):** cuadritos, iconos faltantes/cortados, overlays (D).
- **Decisión pendiente:** corregir Documento Maestro (A3).
