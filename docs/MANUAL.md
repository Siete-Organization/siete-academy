# Manual de proceso y usabilidad — Siete Academy

> **Versión:** 1.0 · **Fase actual:** A (iteración sobre feedback completada) → B (infra prod) pendiente
> **Audiencia:** equipo operativo (admin, profesores), equipo técnico (recibe el handoff) y referentes de negocio.
> **Documentos hermanos:** [`FLUJOGRAMAS.md`](FLUJOGRAMAS.md) · [`ARQUITECTURA.md`](ARQUITECTURA.md) · [`HANDOFF.md`](../HANDOFF.md)

---

## 1. ¿Qué es Siete Academy?

LMS (Learning Management System) propietario de **Siete** para formar **SDR (Sales Development Representatives)** en cohortes híbridas estilo Reforge: **70% on-demand + 30% en vivo**.

El sistema cubre el ciclo completo:

1. **Captación** del aspirante (landing público + formulario público).
2. **Selección** (revisión humana, asistida por scoring de Claude).
3. **Onboarding** del alumno en una cohorte.
4. **Formación** (módulos con video/lectura, quizzes, entregables, sesiones Zoom en vivo, comunidad Slack).
5. **Evaluación** (auto-score MCQ + revisión del profesor, con borrador IA opcional).
6. **Certificación** (emisión manual al 100% de progreso, con código de verificación pública).
7. **Colocación / Placement** (Kanban ATS para mover candidatos entre etapas hasta colocarlos con clientes).

**Fase 0 (piloto, mayo 2026):** 1 módulo, 1 cohorte, 10–15 alumnos. Sin integraciones reales (Firebase / SMTP / Anthropic configurables vía `.env`).

---

## 2. Roles y permisos

El backend autoriza por **role** (custom claim de Firebase en producción; en dev se usa `X-Dev-User: <email>` como bypass). Hay 4 roles:

| Rol | Email demo (seed) | Qué puede hacer |
|---|---|---|
| **admin** | `admin@siete.com` | Todo. Aprueba aplicaciones, crea cohortes, edita curso, gestiona placement, ve analytics. |
| **teacher** | `teacher@siete.com` | Dashboard de cohortes/alumnos. Revisa entregas, califica, da comentarios libres, emite certificados. |
| **student** | `student@siete.com` (Luis 40%), `camila@siete.com` (75%), `diego@siete.com` (100%) | Consume contenido, entrega pruebas, ve feedback, asiste a sesiones en vivo. |
| **recruiter** | `recruiter@siete.com` | Solo ve candidatos en stages `approved`/`presented`/`placed`. Botón "agendar entrevista" abre `mailto:`. |

> Endpoints de seguridad:
> - `require_roles("admin")` → `backend/app/modules/auth/dependencies.py:82`
> - El bypass dev-auth está **bloqueado** si `APP_ENV != development` (`dependencies.py:32`).

---

## 3. Estructura general del producto

### 3.1 Flujo macro

```
Landing pública (/)
  └── /apply  (formulario público, rate-limited 5/h por IP)
        └── Postulación queda en cola → admin la revisa
              ├── Rechazada  → email de rechazo (stub en dev)
              └── Aprobada   → admin crea User + Enrollment manual
                    └── Welcome email + link Slack de cohorte
                          └── Alumno entra a /student
                                └── Consume módulos → entrega pruebas
                                      └── Profesor revisa (con borrador IA opcional)
                                            └── 100% progreso → admin/teacher emite certificado
                                                  └── Alumno aparece en placement (stage `applying`)
                                                        └── Admin avanza por etapas hasta `placed`
                                                              └── Recruiter externo ve `approved/presented/placed`
```

### 3.2 Páginas del frontend (rutas SPA, prefijo `/academy/` en prod)

| Ruta | Acceso | Propósito |
|---|---|---|
| `/` | público | Landing marketing |
| `/apply` | público | Formulario de aplicación (mín. 100 palabras por respuesta + video corto) |
| `/login` | público | 4 botones demo (bypass) — en prod, Google Auth |
| `/account` | todos los roles | Editar perfil (display_name, photo_url) |
| `/student` | student | Dashboard: progreso de cohorte, banner Slack, share LinkedIn |
| `/student/module/:id` | student | Lecciones (video YouTube embebido o lectura no descargable) + quizzes + material de apoyo |
| `/student/feedback` | student | Comentarios directos del profesor + reviews por entrega |
| `/student/calendar` | student | Sesiones Zoom en vivo + ventanas de módulo + grabaciones |
| `/student/certificate` | student | (Legacy, fuera del nav) certificado del alumno |
| `/teacher` | teacher/admin | Dashboard con cohortes y tabla de alumnos; emite certificados |
| `/teacher/reviews` | teacher/admin | Cola de revisiones con búsqueda + filtros (con borrador Claude visible) |
| `/admin` | admin | Atajos a las 5 secciones de admin |
| `/admin/applications` | admin | Aprobar/rechazar aplicaciones (con score Claude si existe) |
| `/admin/course` | admin | CRUD módulos, lecciones, material, pruebas |
| `/admin/cohorts` | admin | CRUD cohortes, ventanas de módulo, alumnos, Slack URL |
| `/admin/placement` | admin | ATS Kanban (7 stages) |
| `/admin/analytics` | admin | Métricas del programa |
| `/recruiter` | recruiter/admin | Listado de talento aprobado |

---

## 4. Procesos operativos paso a paso

A continuación, los **procedimientos canónicos** que el equipo operativo debe seguir. Cada uno enumera las precondiciones, los pasos, qué se dispara automáticamente y dónde verificar el resultado.

### 4.1 Proceso A — Postulación pública

**Actor:** aspirante anónimo. **Endpoint:** `POST /applications` (público, rate-limit `5/hour/IP`).

1. El aspirante entra a `/academy/apply`.
2. Completa: nombre, email, teléfono (opcional), **LinkedIn URL** (obligatorio), país, idioma de respuesta.
3. Responde **3 preguntas abiertas** (`why_sales`, `achievement`, `hours_per_week`) con **mínimo 100 palabras cada una** (validación frontend + backend).
4. Adjunta **video corto** (URL externa, p. ej. Loom/YouTube unlisted).
5. Submit → ve pantalla "Tu aplicación está en nuestra mesa".
6. Backend dispara dos tareas Celery (en dev corren inline):
   - `notify_submitted` → email de acuse al aspirante.
   - `score_application_task` → si `ANTHROPIC_API_KEY` está set, Claude puntúa (0–100) y guarda `ai_score` + `ai_notes`.

**Verificación:** la aplicación aparece en `/admin/applications` con status `submitted`.

### 4.2 Proceso B — Revisión y aprobación de aplicaciones

**Actor:** admin. **Endpoints:** `GET /applications`, `GET /applications/{id}`, `POST /applications/{id}/review`.

1. Admin entra a `/admin/applications`.
2. Filtra por status (`submitted` por defecto). Selecciona una aplicación.
3. Revisa: respuestas, video, LinkedIn, país, score Claude (si existe).
4. Decide:
   - **Aprobar** → `status="approved"` + opcionalmente `admin_notes`.
   - **Rechazar** → `status="rejected"` + nota.
5. Backend dispara `notify_decision` (email al aspirante).

> ⚠️ **Importante:** la aprobación **NO crea automáticamente** el `User` ni el `Enrollment`. Es una decisión de Fase 0 para tener control granular (ver `HANDOFF.md` punto 10). El admin debe ir a `/admin/cohorts` y hacerlo manual.

### 4.3 Proceso C — Crear cohorte y enrolar alumnos

**Actor:** admin. **Endpoints:** `POST /cohorts`, `PATCH /cohorts/{id}`, `POST /enrollment`, `PATCH /enrollment/{id}`.

1. Admin entra a `/admin/cohorts`.
2. Crea cohorte: nombre único, fechas inicio/fin, idioma base, `max_students`.
3. (Opcional) Pega **`slack_invite_url`** del canal Slack de la cohorte.
4. Define **ventanas de módulo** (`ModuleWindow`): para cada módulo del curso, fija `opens_at`, `closes_at` y `live_session_at`. Esto controla cuándo el alumno **ve** ese módulo.
5. Selecciona la cohorte → tabla "Alumnos de la cohorte".
6. **Agregar alumno**: dropdown filtra usuarios `role=student`. Al elegir uno → `POST /enrollment` con `user_id` + `cohort_id`.
7. Backend dispara `_send_welcome_email` con link Slack en el idioma del alumno.

**Mover entre cohortes**: usar `PATCH /enrollment/{id}` con `cohort_id` nuevo (respeta unique `user_id+cohort_id`).

### 4.4 Proceso D — Editar el curso (módulos, lecciones, pruebas, material)

**Actor:** admin. **Endpoints:** `GET /courses/{id}/admin`, `PATCH /courses/modules/{id}`, etc.

1. Admin entra a `/admin/course`.
2. Selecciona curso → ve árbol con módulos, lecciones, recursos, pruebas.
3. **Lecciones** (`Lesson.kind`):
   - `video` → solo `youtube_id` (unlisted recomendado, embed `nocookie`).
   - `reading` → markdown inline; renderizado con `user-select: none` y `@media print { display: none }` → **no descargable** por diseño (requisito del cliente).
4. **Material de apoyo** (`ModuleResource`): tipo (`pdf|ppt|video|doc|link`) + `title` + `url`. Abre en **nueva pestaña** (intencional: son referencias externas).
5. **Pruebas** (`Assessment`): 5 tipos disponibles, comparten schema pero `config` JSON varía:
   - `mcq` — preguntas + opciones; auto-grade.
   - `written` — prompt; entrega texto; revisión humana.
   - `prospection_db` — base de prospección a entregar (file URL).
   - `cold_call_video` — video URL (Loom/Vidyard).
   - `team_exercise` — ejercicio grupal.
6. Cada texto del curso vive en 3 idiomas (`*_translations`).

### 4.5 Proceso E — Alumno consume contenido y entrega pruebas

**Actor:** student.

1. Entra a `/student` → ve sus cohortes activas, progreso global y banner Slack.
2. Selecciona un módulo (debe estar dentro de la **ventana** `opens_at..closes_at` de su cohorte).
3. Pasa por las lecciones; al completar una se dispara `POST /enrollment/{id}/progress` con `lesson_id` + `watched_pct` + `completed=true` → recalcula `progress_pct`.
4. Al final del módulo, completa las **pruebas**:
   - MCQ → submit auto-graded (`status=auto_graded`, `auto_score`).
   - Resto → submit queda `pending_review`.
5. En `/student/feedback` ve los reviews del profesor (con score y feedback) y comentarios libres.

### 4.6 Proceso F — Profesor revisa entregas

**Actor:** teacher (o admin). **Endpoints:** `GET /assessments/submissions/pending`, `POST /assessments/submissions/{id}/review`, `GET /ai-review/submission/{id}`.

1. Entra a `/teacher` → ve dashboard con cohortes y tabla de alumnos (progreso, lecciones completadas, nota promedio, última actividad, certificado emitido).
2. Va a `/teacher/reviews` (cola pendiente).
3. Selecciona una entrega → si Claude generó borrador (`AIReview`), aparece como **sugerencia visible solo al profesor**.
4. Califica: `score` (0–100) + `feedback` (texto) + opcional `attachment_url` (PDF anotado, audio, etc.).
5. Submit → `Submission.status="reviewed"`, alumno ve la review en `/student/feedback`.

### 4.7 Proceso G — Comentarios directos del profesor

**Actor:** teacher (o admin). **Endpoints:** `POST /teacher/notes`, `GET /teacher/notes/student/{id}`, `GET /teacher/notes/me`.

1. Profesor en `/teacher` → fila de un alumno → botón **"✉ Enviar comentario"**.
2. Modal: textarea + tipo de adjunto (`link/pdf/ppt/video/doc`) + URL.
3. Submit → `TeacherNote` se persiste; aparece en el `/student/feedback` del alumno arriba de las reviews.

> Uso: feedback puntual, coaching, anuncios, compartir un recurso extra. **Independiente** de submissions.

### 4.8 Proceso H — Sesiones en vivo (Zoom)

**Actor:** teacher/admin (curador) y student (consumidor). **Endpoints:** `POST /live-sessions`, `GET /live-sessions/cohort/{id}`.

1. Admin/profesor crea `LiveSession` para una `ModuleWindow`: título + `zoom_url` + (opcional) `recording_url`.
2. Alumno la ve en `/student/calendar` agregada de todas sus cohortes.
3. La asistencia (`attendance` JSON) puede registrarse vía evento manual o webhook futuro de Zoom.

### 4.9 Proceso I — Emisión de certificado

**Actor:** admin o teacher. **Endpoint:** `POST /certificates/issue { user_id, cohort_id }`.

1. Cuando el alumno alcanza `progress_pct == 100`, en `/teacher` aparece el botón **"Emitir certificado"** en su fila.
2. Click → backend valida `enrollment.progress_pct == 100`. Si OK, crea `Certificate` con `verification_code` único.
3. Se envía email bilingüe al alumno con el código y el link de verificación.
4. **Verificación pública**: cualquiera entra a `/verify/{code}` (rate-limited `30/min/IP`). Si existe, ve nombre + cohorte + fecha; si no, 404.

> No hay emisión automática al 100% — decisión de Fase 0 para mantener control humano. Ver `HANDOFF.md` punto 8 para el hook de automatización futura.

### 4.10 Proceso J — Placement / ATS

**Actor:** admin (mueve), recruiter (consume vista filtrada). **Endpoints:** `/placement/...`.

**Stages del pipeline (orden importa para Kanban):**

```
applying → siete_interview → siete_test → approved → presented → placed
                                                                 ↓
                                                              rejected
```

1. Admin crea candidato: `POST /placement/candidates { user_id, cohort_id, summary, portfolio_url }`. Por default queda en `applying`.
2. Mueve por stages: `PATCH /placement/candidates/{id}/stage { stage, note }`. Cada cambio crea un `PlacementEvent` auditable.
3. Asigna admin responsable: `PATCH .../assign { admin_id }`.
4. **Recruiter externo** entra a `/recruiter` y solo ve `approved | presented | placed` (vista limpia, sin notas internas). Botón "agendar entrevista" abre `mailto:` con cuerpo pre-armado en idioma del candidato.

---

## 5. Convenciones de UX y diseño

### 5.1 Paleta (rebrand 2026 — matchea CSS real de wearesiete.com)

| Token Tailwind | Hex | Uso |
|---|---|---|
| `ink` | `#000` | Texto principal |
| `paper` | `#F5F5F7` | Background |
| `ember` | `#007AFF` | Accent / CTAs (System Blue) |
| `sky` | `#8FBDFF` | Accent suave |
| `bone` | `#DBDBDB` | Bordes |
| `ink-muted` | `#5D6C7B` | Texto secundario |
| `ink-faint` | `#999FAE` | Hints |

> Los **nombres son semánticos**. No los renombres aunque cambies el hex — `bg-ember` aparece en docenas de componentes.

### 5.2 Tipografía

- **Montserrat** (300–900) — todo el cuerpo.
- **JetBrains Mono** — labels, números, eyebrows.
- Cargado de Google Fonts en `frontend/index.html`.

### 5.3 Componentes

- **Botones**: pill (`rounded-full`), `font-semibold` por default. Variants ember con hover a `ember-soft`.
- **Layout** (`Layout.tsx`): header sticky con backdrop-blur, nav reactivo al rol, selector de idioma con banderas, menú avatar (foto o iniciales).
- **i18n**: 3 locales (`es/en/pt`), claves en `frontend/src/locales/{es,en,pt}/common.json`. **Toda string visible debe usar `t("key")`**. `returnObjects: true` está activado globalmente — permite que `t("home.modules")` devuelva arrays.

---

## 6. Datos de demo (seed)

`make seed` borra `siete_academy.db` y siembra:

- **6 usuarios:** 1 admin, 1 teacher, 3 students (Luis 40%, Camila 75%, Diego 100%), 1 recruiter.
- **2 cohortes:** SDR 001 (en curso, con alumnos), SDR 002 (vacía, para pruebas de "mover entre cohortes").
- **1 curso completo** con 4 módulos × N lecciones (mix video/reading) + material de apoyo + 5 pruebas (una de cada tipo).
- **8 aplicantes** con perfiles diferenciados (3 con score Claude pre-sembrado).
- **Submissions + reviews + AI drafts:** Camila tiene review escrita; Diego tiene entrega pendiente con borrador Claude.
- **4 candidatos en placement:** Luis `applying`, Camila `siete_interview`, Diego `siete_test`, Valeria `approved`.
- **1 sesión Zoom** del módulo 1.
- **1 certificado emitido** (Diego).

---

## 7. Limitaciones conocidas (Fase 0)

| Limitación | Por qué | Cuándo se resuelve |
|---|---|---|
| Login solo por botones demo | Sin Firebase configurado | Fase B (NEXT_STEPS_PROD §2) |
| Emails se loguean, no se envían | Sin SMTP configurado | Fase B (set `SMTP_*`) |
| Borradores Claude no se generan en runtime | Sin `ANTHROPIC_API_KEY` | Fase B (set la key) |
| Celery corre inline | `task_always_eager=True` | Fase B (Redis + worker) |
| Archivos son URLs (no upload propio) | Decisión Fase 0 | Opcional Fase B (módulo `storage` + S3) |
| Slack es URL-based | Sin SLACK_BOT_TOKEN | Fase 1+ (`conversations.invite`) |
| Aprobación NO crea User+Enrollment | Decisión deliberada (control granular) | Fase 1 si se decide unificar |
| Certificado se emite manualmente | Decisión Fase 0 | Hook ya identificado en `enrollment/router.py::update_progress` |

---

## 8. Cómo verificar usabilidad antes de un release

```bash
make test       # pytest (60+) + vitest + playwright
make demo       # smoke manual con los 4 roles
```

**Recorrido de smoke manual** (≈ 10 minutos):

1. **Aspirante** → `/apply` → completar y enviar (validar mínimo 100 palabras).
2. **Admin** → `/admin/applications` → aprobar; `/admin/cohorts` → enrolar al nuevo alumno; `/admin/course` → editar una lección.
3. **Profesor** → `/teacher/reviews` → revisar la entrega de Diego (ver borrador Claude).
4. **Alumno** (`student@siete.com`) → `/student` → abrir módulo → completar lección → submitar MCQ → ver feedback.
5. **Reclutador** → `/recruiter` → ver Valeria → click "agendar entrevista" → revisa que abre `mailto:`.
6. Cambiar idioma a EN y PT → toda la UI debe reaccionar.

> Cada request lleva header `X-Request-ID`. Todo log backend lleva `rid=<16-chars>`. Si algo falla en UI, copia el `rid` y `grep` en logs.

---

## 9. Glosario

| Término | Definición |
|---|---|
| **Cohorte** | Grupo cerrado con fechas, idioma base, capacidad y comunidad Slack propia. |
| **Ventana de módulo** (`ModuleWindow`) | Periodo `opens_at..closes_at` durante el cual la cohorte ve un módulo del curso. |
| **Enrollment** | Inscripción de un alumno en una cohorte (unique por par user/cohorte). |
| **LessonProgress** | % visto + completado por lección/enrollment; alimenta `progress_pct` de Enrollment. |
| **Submission** | Entrega del alumno a una `Assessment`. |
| **TeacherReview** | Calificación + feedback humano de una submission. |
| **AIReview** | Borrador Claude visible solo al profesor (no al alumno). |
| **TeacherNote** | Comentario libre profesor → alumno (independiente de submission). |
| **PlacementCandidate** | Alumno en pipeline de colocación post-graduación. |
| **PlacementEvent** | Timeline auditable de cambios de stage / asignaciones / notas. |
| **WAT** | Workflows / Agents / Tools — framework documentado en `CLAUDE.md` para agentes IA del repo. |

---

## 10. Mapa rápido de "quién hace qué"

| Necesidad | Rol | Pantalla |
|---|---|---|
| "Quiero entrar al programa" | aspirante | `/apply` |
| "Quiero aprobar una aplicación" | admin | `/admin/applications` |
| "Quiero crear una cohorte y meter alumnos" | admin | `/admin/cohorts` |
| "Quiero editar el contenido del curso" | admin | `/admin/course` |
| "Quiero ver cómo va el grupo" | teacher/admin | `/teacher` |
| "Quiero revisar una entrega" | teacher | `/teacher/reviews` |
| "Quiero darle un mensaje a un alumno" | teacher | `/teacher` (modal) |
| "Quiero ver mi progreso" | student | `/student` |
| "Quiero ver feedback" | student | `/student/feedback` |
| "Quiero ver mis sesiones en vivo" | student | `/student/calendar` |
| "Quiero emitir un certificado" | teacher/admin | `/teacher` (botón en fila al 100%) |
| "Quiero verificar un certificado" | cualquiera | `/verify/{code}` (público) |
| "Quiero mover candidatos en el ATS" | admin | `/admin/placement` |
| "Quiero ver talento disponible" | recruiter | `/recruiter` |
| "Quiero ver métricas" | admin | `/admin/analytics` |

---

**Para detalle técnico** (modelos, endpoints, infra) → `ARQUITECTURA.md`.
**Para diagramas visuales** → `FLUJOGRAMAS.md`.
