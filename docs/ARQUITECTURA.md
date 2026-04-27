# Arquitectura técnica — Siete Academy

> Vista técnica complementaria al [`MANUAL.md`](MANUAL.md) (proceso) y [`FLUJOGRAMAS.md`](FLUJOGRAMAS.md) (diagramas).
> Fuente de verdad: el código (`backend/app/`, `frontend/src/`). Este documento explica el **por qué** y enumera los puntos de extensión más comunes.

---

## 1. Stack

| Capa | Tecnología | Notas |
|---|---|---|
| Frontend | React 18 + Vite + TypeScript + Tailwind + ShadCN | SPA. Routing con `react-router-dom`. i18n con `react-i18next`. |
| Backend | Python 3.12 + FastAPI + SQLAlchemy 2 + Alembic | Monolito modular (un módulo Python por dominio). |
| DB | SQLite (dev) / PostgreSQL (prod) | Mismo SQLAlchemy. Seed dev usa `Base.metadata.create_all`; prod usa Alembic. |
| Cache / queue | Redis | Backend de Celery + cache. |
| Tasks | Celery | `task_always_eager=True` en dev (corre inline). En prod: worker separado + beat. |
| Auth | Firebase Auth (custom claims) | En dev: bypass por header `X-Dev-User`. |
| AI | Anthropic Claude (`claude-opus-4-7` por default) | Usado para scoring de aplicaciones y borradores de feedback. |
| Email | SMTP (Resend recomendado) | Stub si `SMTP_HOST` no está configurado. |
| Infra | Hetzner VPS + Coolify + Docker + GitHub | Cloudflare Worker enruta `siete.com/academy/*` y `/api/academy/*`. |

---

## 2. Topología

```
Cliente (browser / móvil)
    │
    ▼
Cloudflare Worker
    ├── siete.com/*            → Webflow (marketing legacy)
    ├── siete.com/academy/*    → Frontend Vite (Caddy en Coolify)
    └── siete.com/api/academy/*→ Backend FastAPI
                                    ├── Postgres
                                    ├── Redis
                                    └── Celery worker (servicio aparte)
```

En **dev local**:

- Frontend `http://localhost:5173` (Vite)
- Backend `http://localhost:8000` (Uvicorn)
- Vite proxy: `/api/academy/*` → `http://localhost:8000/*` (rewrite el prefijo)
- Backend ajusta `root_path` solo cuando `APP_ENV != development`.

---

## 3. Estructura del repositorio

```
siete-academy/
├── backend/
│   ├── app/
│   │   ├── core/                # Config, DB, Firebase, Celery, i18n, logging, limiter, middleware
│   │   ├── modules/             # Un módulo Python por dominio
│   │   │   ├── auth/            # dependencies.py + router.py
│   │   │   ├── users/
│   │   │   ├── applications/
│   │   │   ├── cohorts/
│   │   │   ├── courses/
│   │   │   ├── enrollment/
│   │   │   ├── assessments/
│   │   │   ├── live_sessions/
│   │   │   ├── placement/
│   │   │   ├── certificates/
│   │   │   ├── teacher/
│   │   │   ├── ai_review/       # No expone modelos (usa los de assessments)
│   │   │   ├── notifications/   # services + tasks (Celery)
│   │   │   └── audit/           # PipelineRun, StageRun, AICallLog (auditoría)
│   │   ├── scripts/seed.py
│   │   └── main.py              # FastAPI app + include_router
│   ├── alembic/                 # 3 migraciones iniciales en versions/
│   ├── tests/                   # 60+ pytest
│   ├── pyproject.toml
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/          # Layout, ProtectedRoute, ui/* (button, card, input)
│   │   ├── pages/{admin,student,teacher,recruiter,apply,auth,account}/
│   │   ├── lib/                 # api.ts (axios), auth-context.tsx, firebase.ts, i18n.ts, logger.ts, utils.ts
│   │   ├── locales/{es,en,pt}/common.json
│   │   ├── App.tsx              # Routing
│   │   └── main.tsx
│   ├── tailwind.config.js
│   ├── vite.config.ts
│   └── Dockerfile
├── e2e/                         # Playwright
├── workflows/                   # SOPs WAT (markdown) — para agentes IA del repo
├── tools/                       # Scripts WAT
├── docker-compose.yml
├── Makefile
└── docs/                        # Esta carpeta — manual / flujogramas / arquitectura
```

> **Convención de módulo backend:** cada módulo tiene `models.py`, `schemas.py` (Pydantic), `services.py` (lógica reutilizable), `router.py` (endpoints), opcional `tasks.py` (Celery). Todo router se registra en `backend/app/main.py:68-79`.

---

## 4. Módulos backend en detalle

### 4.1 `auth`

- `dependencies.py:get_current_user` — resuelve `CurrentUser` desde header. Soporta dev bypass + Firebase. Provisiona usuario nuevo si el `firebase_uid` no existía.
- `dependencies.py:require_roles(*roles)` — factory de dependencias por rol.
- `router.py` — `GET /me` (echo del usuario actual).

### 4.2 `users`

- Modelo `User`: `id, firebase_uid (UK), email (UK), display_name, photo_url, role, locale, profile JSON, timestamps`.
- Endpoints: `GET /users` (admin, soporta `?role=student`), `PATCH /users/me`, `PATCH /users/{id}/role` (admin).

### 4.3 `applications`

- Modelo `Application`: aspirante anónimo (no `User` aún). Incluye `applicant_*`, `linkedin_url`, `country`, `locale`, `answers JSON`, `video_url`, `ai_score`, `ai_notes`, `status`, `admin_notes`, `reviewed_by_id`, `reviewed_at`.
- `POST /applications` público, **rate-limit `5/hour/IP`**. Dispara `notify_submitted` + `score_application_task`.
- `POST /applications/{id}/review` admin → status final + email.

### 4.4 `cohorts`

- Modelos `Cohort` (con `slack_invite_url`, `status: draft|open_applications|in_progress|completed|archived`) y `ModuleWindow` (unique cohorte+módulo, fechas + `live_session_at`).
- Endpoints: CRUD cohortes; CRUD ventanas; `PATCH /cohorts/{id}` editable (incluye Slack URL).

### 4.5 `courses`

- Modelos: `Course` + `CourseTranslation`, `Module` + `ModuleTranslation`, `Lesson` (`kind: video|reading`, `youtube_id`) + `LessonTranslation` (con `body` para readings), `ModuleResource` (`kind: pdf|ppt|video|doc|link`, URL-based).
- Endpoint admin: `GET /courses/{id}/admin` devuelve árbol con todas las traducciones + lecciones + recursos anidados.
- CRUD para módulos/lecciones/recursos/assessments (vía `assessments`).

### 4.6 `enrollment`

- `Enrollment` (unique user+cohorte) + `LessonProgress` (unique enrollment+lesson).
- Endpoint clave: `GET /enrollment/me` devuelve enrollments enriquecidos con `cohort_name` y `slack_invite_url`.
- `POST /enrollment` (admin) dispara `_send_welcome_email` (idioma del alumno + Slack).
- `POST /enrollment/{id}/progress` upsert lesson progress; idempotente.

### 4.7 `assessments`

- 3 modelos relacionados: `Assessment`, `Submission`, `TeacherReview`, `AIReview`.
- Tipos de `Assessment`: `mcq | written | prospection_db | cold_call_video | team_exercise`. `config JSON` varía por tipo.
- `POST /assessments/submissions`: si `type=mcq` → auto-graded; si no, encola `review_submission_task` para borrador Claude.
- Vista alumno: `GET /assessments/submissions/me/with-reviews` (LEFT JOIN single round-trip).
- Cola profesor: `GET /assessments/submissions/pending`.
- Review: `POST /assessments/submissions/{id}/review` (idempotente: actualiza si existe).

### 4.8 `live_sessions`

- `LiveSession` 1:1 con `ModuleWindow`. `zoom_url`, `recording_url`, `attendance JSON`.
- Endpoints: CRUD; vista de alumno agregada en `GET /live-sessions/me` (a través de cohortes).

### 4.9 `placement`

- `PlacementCandidate` (unique por user) + `PlacementEvent` (timeline auditable).
- 7 stages: `applying, siete_interview, siete_test, approved, presented, placed, rejected` (orden importa para Kanban).
- Endpoints: CRUD candidatos, `PATCH /candidates/{id}/stage`, `PATCH .../assign`, `PATCH .../update`.
- **Recruiter externo** sólo ve `approved | presented | placed` vía `GET /placement/recruiter/candidates` (sin notas internas).

### 4.10 `certificates`

- `Certificate` (unique user+cohort) con `verification_code` único (slug).
- `POST /certificates/issue` (admin/teacher) valida `enrollment.progress_pct == 100`. Crea + email bilingüe.
- `GET /certificates/verify/{code}` público, **rate-limit `30/min/IP`**.

### 4.11 `teacher`

- `TeacherNote` independiente de submissions (feedback libre o compartir recurso).
- Endpoints: `POST /teacher/notes`, `GET /teacher/notes/student/{id}`, `GET /teacher/notes/me`, `DELETE /teacher/notes/{id}`.
- `GET /teacher/dashboard` agrega cohortes + tabla rica de alumnos.
- `GET /teacher/pending` cola de revisiones con shape enriquecido.

### 4.12 `ai_review`

- No tiene modelos propios — usa `AIReview` de `assessments`.
- `tasks.py`:
  - `score_application_task(app_id)` — pre-screen con scoring 0-100.
  - `review_submission_task(submission_id)` — borrador `draft_feedback` + `score_suggestion`.
- Cada llamada se persiste en `ai_call_logs` (módulo `audit`) para auditar costo Anthropic.
- `GET /ai-review/submission/{id}` → consulta para teacher/admin.

### 4.13 `notifications`

- `services.send_email(to, subject, body_text)` — SMTP real si `SMTP_HOST` está set; si no, log `email.stubbed`.
- `tasks`: `notify_submitted`, `notify_decision` (Celery, eager en dev).

### 4.14 `audit`

- `PipelineRun`, `StageRun`, `AICallLog` — bloques del framework WAT más auditoría AI. No expuesto vía endpoints HTTP; usado internamente.

---

## 5. Frontend

### 5.1 Routing (`App.tsx`)

Las rutas están protegidas vía `<ProtectedRoute roles={[...]}>`:

| Ruta | Roles |
|---|---|
| `/`, `/apply`, `/login` | público |
| `/account` | todos los autenticados |
| `/student/*` | `student` |
| `/teacher`, `/teacher/reviews` | `teacher`, `admin` |
| `/admin/*` | `admin` |
| `/recruiter` | `recruiter`, `admin` |

### 5.2 Auth context (`lib/auth-context.tsx`)

- En dev: persiste `dev_user_email` en `localStorage`. Cada request añade header `X-Dev-User`.
- En prod: `firebase.ts` inicializa con `VITE_FIREBASE_*`. Token JWT enviado como `Authorization: Bearer ...`.
- `me` (data del usuario) se carga al montar la app llamando `GET /auth/me`.

### 5.3 API client (`lib/api.ts`)

- Axios con `baseURL = "/api/academy"` (en dev pasa por el proxy de Vite).
- Interceptor request: añade `X-Request-ID` (uuid corto, también usado por `logger.ts`).
- Interceptor response: mapea errores en formato consistente.

### 5.4 i18n (`lib/i18n.ts`)

- 3 locales: `es` (default), `en`, `pt`. Detector: `localStorage` → navigator.
- `returnObjects: true` activado globalmente — clave para rendering de listas/objetos (`home.modules`, `home.expectList`, etc.).
- Cada string visible debe usar `t("key")`. Las rutas de copy del landing viven en `home.*`.

### 5.5 Diseño (Tailwind)

- Tokens semánticos en `tailwind.config.js`. **No renombrar** aunque cambies hex.
- Componentes UI básicos en `components/ui/` (button, card, input).
- Layout global en `Layout.tsx` (sticky header con backdrop-blur, footer minimal).

---

## 6. Modelo de datos completo

23 tablas (3 migraciones Alembic). Resumen:

| Tabla | PK | Constraints clave |
|---|---|---|
| `users` | id | UK firebase_uid, UK email |
| `applications` | id | — |
| `cohorts` | id | UK name |
| `module_windows` | id | UK (cohort_id, module_id) |
| `courses` | id | UK slug |
| `course_translations` | id | UK (course_id, locale) |
| `modules` | id | — |
| `module_translations` | id | UK (module_id, locale) |
| `lessons` | id | — |
| `lesson_translations` | id | UK (lesson_id, locale) |
| `module_resources` | id | — |
| `enrollments` | id | UK (user_id, cohort_id) |
| `lesson_progress` | id | UK (enrollment_id, lesson_id) |
| `assessments` | id | — |
| `submissions` | id | — |
| `teacher_reviews` | id | UK submission_id |
| `ai_reviews` | id | UK submission_id |
| `live_sessions` | id | UK module_window_id |
| `placement_candidates` | id | UK user_id |
| `placement_events` | id | — |
| `certificates` | id | UK verification_code, UK (user_id, cohort_id) |
| `teacher_notes` | id | — |
| `pipeline_runs` | id | — |
| `stage_runs` | id | — |
| `ai_call_logs` | id | — |

**Cascadas** importantes:
- `Cohort` → `ModuleWindow` (CASCADE)
- `Course` → `Module` → `Lesson` (CASCADE)
- `Module` → `ModuleResource` y `Assessment` (CASCADE)
- `Enrollment` → `LessonProgress` (CASCADE)
- `Submission` → `TeacherReview` y `AIReview` (CASCADE)
- `User` borra → la mayoría de FKs van a `SET NULL` (reviewed_by_id, assigned_admin_id, actor_id) o `CASCADE` (enrollments, candidatos).

---

## 7. Endpoints — referencia rápida

> Lista completa: `grep -rn "@router\.\(get\|post\|patch\|delete\|put\)" backend/app/modules/`.

| Método | Path | Rol | Notas |
|---|---|---|---|
| `GET` | `/health` | público | smoke |
| `GET` | `/auth/me` | autenticado | echo del CurrentUser |
| `GET` | `/users` | admin | `?role=student` filtra |
| `PATCH` | `/users/me` | autenticado | edita `display_name`, `photo_url` |
| `PATCH` | `/users/{id}/role` | admin | promueve/degrada |
| `POST` | `/applications` | público | rate-limit 5/h/IP |
| `GET` | `/applications` | admin | filtros `status`, `limit`, `offset` |
| `GET` | `/applications/{id}` | admin | shape completo |
| `POST` | `/applications/{id}/review` | admin | aprueba/rechaza |
| `POST` `GET` `PATCH` `DELETE` | `/cohorts[/{id}]` | admin | CRUD |
| `GET` | `/cohorts/{id}/windows` | autenticado | usado por `/student` |
| `POST` `PATCH` `DELETE` | `/cohorts/{id}/windows[/{wid}]` | admin | CRUD ventanas |
| `GET` | `/courses/{id}` | autenticado | shape público (alumno) |
| `GET` | `/courses/{id}/admin` | admin | shape completo (con traducciones) |
| `PATCH` `DELETE` | `/courses/modules/{id}` | admin | edita/elimina módulo |
| `PATCH` `DELETE` | `/courses/lessons/{id}` | admin | edita/elimina lección |
| `POST` `PATCH` `DELETE` | `/courses/.../resources[/{id}]` | admin | CRUD material |
| `POST` `PATCH` `DELETE` | `/assessments[/{id}]` | admin | CRUD pruebas |
| `GET` | `/assessments/module/{id}` | autenticado | listado por módulo |
| `POST` | `/assessments/submissions` | autenticado | submit + encola Claude |
| `GET` | `/assessments/submissions/pending` | teacher/admin | cola |
| `GET` | `/assessments/submissions/me[/with-reviews]` | autenticado | mías + feedback |
| `POST` | `/assessments/submissions/{id}/review` | teacher/admin | califica |
| `POST` | `/enrollment` | admin | enrola + welcome email |
| `GET` | `/enrollment/me` | autenticado | mis cohortes (con Slack URL) |
| `GET` | `/enrollment/by-cohort/{id}` | admin | tabla por cohorte |
| `PATCH` `DELETE` | `/enrollment/{id}` | admin | mover/desasignar |
| `POST` | `/enrollment/{id}/progress` | autenticado | upsert lesson progress |
| `POST` `GET` | `/live-sessions[...]` | varía | CRUD + lista cohorte |
| `POST` | `/placement/candidates` | admin | crear |
| `GET` | `/placement/candidates[?stage=]` | admin | listar Kanban |
| `GET` | `/placement/candidates/{id}` | admin | detalle + eventos |
| `PATCH` | `/placement/candidates/{id}/stage` | admin | mover stage (audita) |
| `PATCH` | `/placement/candidates/{id}/assign` | admin | asignar admin |
| `PATCH` | `/placement/candidates/{id}` | admin | edita summary/portfolio/notes |
| `GET` | `/placement/recruiter/candidates` | recruiter/admin | vista limpia |
| `POST` | `/certificates/issue` | admin/teacher | emite si 100% |
| `GET` | `/certificates/me` | autenticado | mis certificados |
| `GET` | `/certificates/verify/{code}` | público | rate-limit 30/min/IP |
| `GET` | `/ai-review/submission/{id}` | teacher/admin | borrador Claude |
| `GET` | `/teacher/dashboard` | teacher/admin | cohortes + tabla rica |
| `GET` | `/teacher/pending` | teacher/admin | cola enriquecida |
| `POST` `GET` `DELETE` | `/teacher/notes[...]` | teacher/admin para crear; cualquiera para leer las suyas | comentarios libres |

---

## 8. Decisiones clave (no revertir sin pensar)

(Versión condensada del bloque "Decisiones de diseño" en `HANDOFF.md`.)

1. **Dev-auth bypass solo si `APP_ENV=development`.** El check vive en `auth/dependencies.py:32` — no quitarlo.
2. **Archivos = URLs externas.** Material, adjuntos, videos. Si quieres upload propio: módulo nuevo `storage` + `UploadFile` + S3.
3. **Email stub** si SMTP no está configurado (`notifications/services.py`).
4. **Celery eager** en dev (`task_always_eager=True`). Prod: Redis + worker + beat.
5. **Schema vía `create_all` en dev**, Alembic en prod. Cualquier modelo nuevo → migración nueva antes de deploy.
6. **Lecciones `reading`** son no-descargables por diseño (CSS `user-select: none` + `@media print { display: none }`). Requisito explícito del cliente.
7. **Material de apoyo abre en nueva pestaña** (intencional: son referencias externas).
8. **Certificado se emite manual** desde dashboard del profesor. Hook para auto-emisión: `enrollment/router.py::update_progress` cuando `progress_pct == 100`.
9. **Slack es URL-based** hoy. Hook para integración real: `enrollment/router.py::_send_welcome_email`. Necesita `SLACK_BOT_TOKEN` + `Cohort.slack_channel_id`.
10. **Aprobar aplicación NO crea User+Enrollment** automáticamente. Decisión Fase 0 (control granular). Para unificar: añadir `cohort_id?` opcional en `ApplicationReview` + lógica condicional en `services.review_application`.
11. **Dev-auth ve solo los 6 usuarios sembrados.** Para más usuarios en dev, modificar `seed.py`.

---

## 9. Observabilidad

- **Logs JSON estructurados** en `core/logging.py`. Cada línea lleva `rid=<16-chars>`.
- **Request ID** propagado: frontend (`logger.ts`) genera UUID corto y lo manda como header `X-Request-ID`. Middleware backend (`middleware.py`) lo bindea al contexto. Toda línea de log dentro del request lleva ese rid.
- **Auditoría AI**: cada llamada a Claude se persiste en `ai_call_logs` (model, request, response, duration_ms, error). Útil para estimar costo.
- **Auditoría placement**: cada cambio de stage/asignación/nota crea un `PlacementEvent` (timeline por candidato).
- En **prod recomendado**: Sentry SDK frontend + backend, UptimeRobot sobre `/api/academy/health`.

---

## 10. Seguridad

- **Rate limiting** (SlowAPI) en endpoints públicos:
  - `POST /applications` → `5/hour/IP`
  - `GET /certificates/verify/{code}` → `30/min/IP`
- **CORS**: orígenes en `settings.cors_origins` (config `ALLOWED_ORIGINS` separados por coma).
- **Headers expuestos**: `X-Request-ID` (para correlación cliente).
- **Auth**:
  - Token Bearer de Firebase verificado vía `firebase_admin.auth.verify_id_token`.
  - Usuarios provisionados al primer login si el `firebase_uid` no existe.
- **Roles** validados con `require_roles()`. Rechazos con 403.
- **Validación de input**: Pydantic schemas en cada endpoint.
- **Pendiente Fase B (NEXT_STEPS_PROD)**:
  - Headers de seguridad (CSP, HSTS, X-Frame-Options).
  - CSRF si se introducen forms server-rendered.
  - Audit más fino de cambios admin (hoy hay PlacementEvent y ai_call_logs; se podría extender a `application.review`, `enrollment.created`, etc. — varios ya tienen `log.info` estructurado).

---

## 11. Tests

| Suite | Cantidad | Comando |
|---|---|---|
| Pytest backend | 60+ | `make test-backend` |
| Vitest frontend | 3 | `make test-frontend` |
| Playwright e2e | 2 | `make test-e2e` |
| Todo | — | `make test` |

Nota: tests backend usan SQLite en memoria + fixtures por módulo. Mantener cobertura sobre rutas críticas: aplicaciones, enrollment, submissions, certificate issue/verify, placement state machine.

---

## 12. Deploy

Resumen de Coolify (detalle paso a paso en `NEXT_STEPS_PROD.md`):

```
GitHub repo (push a main)
  │
  ▼
Coolify webhook → docker build (5 servicios)
  ├── api          (FastAPI multi-stage)
  ├── web          (Vite build + Caddy)
  ├── postgres
  ├── redis
  └── celery-worker
       └── healthchecks Coolify + Let's Encrypt TLS

DNS: Cloudflare apunta siete.com a Coolify
Cloudflare Worker: enruta /academy/* y /api/academy/*
```

**Variables de entorno mínimas para prod** (ver `.env.example`):

```
APP_ENV=production
APP_SECRET_KEY=<random>
ALLOWED_ORIGINS=https://siete.com
PUBLIC_BASE_URL=https://siete.com
DATABASE_URL=postgresql+psycopg://...
REDIS_URL=redis://...
DEV_AUTH_BYPASS=false
CELERY_ALWAYS_EAGER=false

FIREBASE_CREDENTIALS_JSON=...
FIREBASE_PROJECT_ID=...

ANTHROPIC_API_KEY=...
ANTHROPIC_MODEL=claude-opus-4-7

SMTP_HOST=smtp.resend.com
SMTP_PORT=587
SMTP_USER=...
SMTP_PASSWORD=...
SMTP_FROM=Siete Academy <noreply@siete.com>
```

---

## 13. Puntos de extensión (recetas comunes)

| Quiero... | Hago... |
|---|---|
| Agregar un nuevo tipo de assessment | Añadir literal en `Assessment.type` + branch en `assessments/services.py::submit` + UI en `AdminCourse.tsx` |
| Auto-emitir certificado al 100% | En `enrollment/router.py::update_progress`, cuando se calcule `progress_pct == 100`, llamar `services.issue_if_eligible(...)` |
| Migrar de Slack URL a API real | Reemplazar el bloque de `_send_welcome_email` que arma `slack_line` por una llamada a `conversations.invite`. Requiere `Cohort.slack_channel_id` nuevo |
| Soportar uploads reales | Crear módulo `storage` con `POST /uploads` (FastAPI `UploadFile`) → S3/boto3 → devolver URL. Las URLs se siguen guardando como `string` en los modelos existentes |
| Nuevo rol | (a) Añadir literal en `User.role`. (b) Custom claim Firebase. (c) `require_roles("nuevo_rol")` en endpoints. (d) Página + ruta protegida en `App.tsx`. (e) Item en `HOME_BY_ROLE` de `Layout.tsx` |
| Nueva traducción | Agregar fila en `*_translations`. UI: copiar locale en `frontend/src/locales/<xx>/common.json` y registrar en `i18n.ts` |
| Webhook Zoom para attendance | Endpoint nuevo en `live_sessions/router.py` que recibe payload Zoom y rellena `LiveSession.attendance` JSON |

---

## 14. Cómo orientarse rápido (para nuevo dev)

1. Lee `HANDOFF.md` (mapa).
2. `make demo` y entra con los 4 botones.
3. Lee `MANUAL.md` (este folder) — entiende los procesos operativos.
4. Hojea `FLUJOGRAMAS.md` para la vista visual.
5. Abre `backend/app/main.py` para ver todos los routers; `App.tsx` para ver todas las rutas.
6. Para entender un dominio puntual: lee `models.py` → `schemas.py` → `services.py` → `router.py` (en ese orden).
7. Si algo en UI no funciona: copia el `rid=...` del footer/console y `grep` en logs backend.
