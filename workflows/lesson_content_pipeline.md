# Pipeline de contenido por lección

Workflow para producir las 5 piezas de cada lección del SDR Academy a partir del
documento maestro (`SDR_Academy_Siete_Documento_Maestro.md`).

Secuencia que renderiza la app (no se rompe):
**Video → Avatar IA → Presentación → Material → Examen.**

Toda lección termina seteando estos 5 campos del modelo `Lesson` + recursos
asociados + un `Assessment` (mcq) con `lesson_id`.

---

## Inputs por lección

| Campo `Lesson` | Origen | Formato |
|---|---|---|
| `youtube_id` | Video principal (Loom/YouTube unlisted) | string corto |
| `avatar_audio_url` | MP3 narración voice-over | URL público |
| `avatar_script` | Transcript del audio (para subtítulos + lectura) | texto plano |
| `presentation_url` | Deck publicado | URL Gamma/PDF |
| `presentation_blocks` | Sintesis bloques del doc maestro | JSON `[{title, bullets[], source}]` |
| Recursos (`module_resources`) | PDFs, papers, anexos | URL + kind |
| Examen (`Assessment`) | Micro-pruebas del doc maestro | `{questions: [...]}` |

---

## Paso a paso

### 1) Deck base — **Gamma**

Una sola vez: cargar tema Siete (colores + tipografía) en Gamma como brand.
Por cada semana:

1. Abrir Gamma → "Generate from text".
2. Pegar el bloque correspondiente del doc maestro (de "Semana X" hasta el cierre de fuentes).
3. Pedir 8-10 slides, theme Siete, formato 16:9.
4. Revisar y limpiar manualmente (Gamma a veces inventa subtítulos).
5. Exportar como **link público** (no editable) → este URL va a `presentation_url`.
6. En paralelo, copiar los bullets clave a `presentation_blocks` (JSON) para que la app los renderice incluso sin abrir Gamma.

> **Por qué Gamma y no Claude PPT:** Gamma tiene brand system reutilizable + 10× más rápido para batch de 32 lecciones. Si necesitás controlar slide-por-slide en una lección específica, usar Claude In PowerPoint puntualmente.

### 2) Script de narración — **Claude (Opus 4.7)**

Reutilizar la infra existente (`anthropic_client.py`) creando un stage al estilo
`ai_review/stages.py` — opcional para v1 si no automatizamos.

**Prompt manual** (Claude.ai o API):

```
Sos coach IA para SDR Academy Siete. Generá un script de narración voice-over de 90-120 segundos
para la siguiente lección. Tono: directo, segunda persona ("vos"), sin clichés motivacionales.
Estructura: hook → 1 pregunta central → mapa de los bloques → cierre con instrucción concreta.
No leas los slides — orientá al alumno sobre qué va a aprender y por qué importa.

LECCIÓN:
[pegar contenido del bloque del doc maestro]
```

Salida → `avatar_script`. Revisar tono antes de pasar a ElevenLabs.

### 3) Audio — **ElevenLabs**

1. Voz Siete (definir una sola): español neutro LATAM, voz masculina o femenina consistente.
2. Pegar el script aprobado en ElevenLabs.
3. Generar MP3.
4. Subir a Google Drive (o S3 cuando exista) → marcar **link público**.
5. Pegar URL en `avatar_audio_url`.

> **Coste estimado por lección:** ~120 seg de narración × 16 lecciones (8 semanas × 2) ≈ 32 min ≈ USD 10-15 con plan Creator de ElevenLabs.

### 4) Video principal — **Loom o grabación + Descript**

Opciones por orden de fricción:

- **Fast path:** grabar a cámara con un instructor humano (10-15 min) → subir a YouTube unlisted → tomar `youtube_id`.
- **Avatar full video (futuro):** HeyGen con la misma voz ElevenLabs. Útil cuando no hay disponibilidad de instructor o se quiere reuso multilingüe.

**Edición** con Descript:
1. Importar grabación.
2. Edición por transcript (eliminar muletillas, silencios, errores).
3. Exportar 1080p → subir a YouTube unlisted.

### 5) Material de apoyo

Por cada recurso: `kind` + `title` + `url`. Crear con `POST /courses/modules/{id}/resources` con `lesson_id` apuntando a la lección. La app los muestra en el paso 4 del stepper.

Tipos:
- `pdf` — handouts, papers académicos.
- `ppt` — link al deck Gamma (puede duplicar `presentation_url`).
- `link` — anexos, reports de industria, dashboards.
- `video` — referencias secundarias.
- `doc` — Google Docs con plantillas.

### 6) Examen — MCQ desde micro-pruebas del doc maestro

Cada semana del doc maestro trae 4 micro-pruebas Capa 1 con respuestas + explicación.
Mapearlas al schema:

```json
{
  "questions": [
    {
      "id": "q1",
      "type": "single",   // o "multi" / "match"
      "prompt": "...",
      "choices": [{"id": "a", "text": "..."}],
      "correct": ["c"],
      "explanation": "..."
    }
  ],
  "rules": {
    "attempts": 1,
    "time_per_question_seconds": 120,
    "shuffle": true,
    "feedback_after_each": true
  }
}
```

Crear con `POST /assessments` pasando `module_id` + `lesson_id`.
Umbral por defecto: `passing_score: 65.0` (alineado con la bandera roja del doc).

---

## Cómo seedear (Semana 1 ya hecho)

Ejemplo de referencia: `backend/app/scripts/seed_w1.py`. Para cada semana nueva:

1. Duplicar `seed_w1.py` → `seed_w2.py`, `seed_w3.py`, etc.
2. Reemplazar `LESSON_BODY_ES`, `AVATAR_SCRIPT_ES`, `PRESENTATION_BLOCKS_ES`, `MCQ_QUESTIONS`, `RESOURCES` con el contenido de esa semana.
3. Cambiar `order_index` (Semana 2 → 1, Semana 3 → 2, etc.).
4. Correr: `cd backend && .venv/bin/python -m app.scripts.seed_wN`.
5. Verificar en `/student/modules/{id}` que se ve la lección con los 5 pasos.

## Modelo de costos (piloto)

| Pieza | Herramienta | Costo unitario | × 16 lecciones |
|---|---|---|---|
| Deck | Gamma Pro | USD 16/mes | USD 16 total |
| Script | Claude Opus 4.7 API | ~USD 0.10/lección | USD 1.60 |
| Audio | ElevenLabs Creator | ~USD 0.30/min | USD 10 |
| Video edit | Descript Creator | USD 24/mes | USD 24 |
| Hosting video | YouTube unlisted | gratis | 0 |
| **Total piloto** | | | **~USD 50** |

Para v1 (cohorte real con avatar full video), migrar audio + avatar a HeyGen
(~USD 89/mes Creator). Reutilizar voz ElevenLabs ya generada.

## Checklist por lección antes de publicar

- [ ] `youtube_id` apunta a un unlisted accesible
- [ ] `avatar_audio_url` reproduce limpio (no clipping, sin ruido)
- [ ] `avatar_script` matchea palabra-por-palabra con el audio
- [ ] `presentation_url` abre público
- [ ] `presentation_blocks` tiene ≥ 4 bloques con `source` citada
- [ ] Recursos cargados con `lesson_id` (no a nivel módulo)
- [ ] MCQ funciona: probar como `student` → score ≥ 65 marca paso completo
- [ ] Locales: contenido en `es` (mínimo); `en`/`pt` cuando exista traducción
