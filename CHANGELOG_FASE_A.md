# Changelog — Fase A (iteración sobre feedback)

Registro de todo lo agregado/cambiado entre `Checkpoint — Fase 0 lista para pruebas locales`
(`6445dbd`) y el handoff al equipo técnico. Orden cronológico inverso: lo más reciente arriba.

Objetivo: que el equipo que reciba el repo entienda el **por qué** de cada cambio, no solo
el qué. Los detalles mecánicos están en el diff de git.

---

## Ronda 2 — post-testeo del equipo

### Slack community por cohorte
**Contexto:** el cliente quiere que el alumno, al ser enrolado, reciba un link para unirse
al canal de Slack de su cohorte. Y si pierde el email, el link debe estar disponible en su
perfil.

**Cambios:**
- `Cohort.slack_invite_url: str | None` (nueva columna)
- `PATCH /cohorts/{id}` — nuevo endpoint para editar (incluye campo slack)
- `GET /enrollment/me` enriquecido: ahora incluye `cohort_name` y `slack_invite_url`
- `backend/app/modules/enrollment/router.py::_send_welcome_email` — nueva función. Dispara al
  crear un enrollment. Email en idioma del alumno, incluye link de Slack si existe.
- Admin UI: `/admin/cohorts` → al seleccionar cohorte aparece tarjeta "Comunidad Slack"
  editable.
- Student UI: banner "Únete a tu comunidad en Slack" en dashboard + bloque en `/account`.

**Pendiente (Fase 1):** reemplazar URL por integración con Slack API
(`SLACK_BOT_TOKEN` + `conversations.invite`). Hook: `_send_welcome_email`.

### Comentarios directos del profesor al alumno
**Contexto:** el profesor necesita dar feedback puntual (o compartir recursos) a un alumno
sin que esté atado a una submission.

**Cambios:**
- Nuevo modelo `TeacherNote` en `backend/app/modules/teacher/models.py`:
  `id, teacher_id, student_id, body, attachment_kind, attachment_url, created_at`
- Endpoints en `/teacher/notes`:
  - `POST /teacher/notes` — crear (teacher/admin)
  - `GET /teacher/notes/student/{id}` — listar notas para un alumno (teacher/admin)
  - `GET /teacher/notes/me` — listar notas recibidas (cualquier role)
  - `DELETE /teacher/notes/{id}` — borrar (autor o admin)
- Admin UI (`/teacher`): botón pill azul **"✉ Enviar comentario"** por alumno en la tabla.
  Modal con textarea + tipos de adjunto (link/pdf/ppt/video/doc) + URL + enviar.
- Student UI (`/student/feedback`): nueva sección **"Comentarios del profesor"** arriba
  del listado de entregas.

### Gestión de alumnos por cohorte (AdminCohorts)
**Contexto:** el admin debe poder asignar/mover alumnos entre cohortes y tener múltiples
cohortes simultáneas.

**Cambios:**
- `GET /enrollment/by-cohort/{id}` — nuevo endpoint (admin): devuelve enrollments con
  datos enriquecidos del alumno
- `PATCH /enrollment/{id}` — mover de cohorte (valida unique(user_id, cohort_id))
- `DELETE /enrollment/{id}` — desasignar
- `GET /users?role=student` — filtro por role agregado
- Admin UI: al seleccionar cohorte en `/admin/cohorts` aparece tabla "Alumnos de la cohorte"
  con: avance, estado, mover-a (dropdown), quitar. Dropdown "Agregar alumno" para enrolar.
- **Segunda cohorte sembrada** ("SDR 002 — Julio 2026", vacía) para probar mover entre
  cohortes desde el seed.

### Rebrand final — matcheando wearesiete.com real
**Contexto:** primera pasada usé la opción 1 del PDF (Cool Steel `#406E8E`). Después bajé
el CSS real de `wearesiete.com` y descubrí que usan la opción 3 (System Blue `#007AFF`).

**Cambios:**
- `tailwind.config.js`: tokens `paper/ink/bone/ember/sky` apuntan a valores extraídos del
  stylesheet de producción por frecuencia de uso (`#000` 1060x, `#007aff` 509x,
  `#f5f5f7` 470x, `#dbdbdb` 113x, `#8fbdff` 77x).
- Fonts: solo Montserrat (300-900) + JetBrains Mono. Quitado Space Grotesk y Fraunces.
- `Button`: `rounded-full` (pill shape, matchea `border-radius: 33px` del site).
  `font-semibold` por default. Variants ember ahora usan hover a `ember-soft` en vez de
  `ember/90`.
- `index.css`: selection color ahora azul (`rgb(0 122 255 / 0.25)`); gradients de fondo
  tiñeron a sky/ember. Quitado el grain/noise del paper warm — diseño más limpio.

**Titular rebrand:** "Te formamos SDR. Te contratamos." (es/en/pt). Nótese cambio de
posicionamiento: antes era "las agencias te contratan" (Siete como puente) → ahora "te
contratamos" (Siete contrata directo). Esto **contradice** el flujo del reclutador externo
en `/recruiter` — pendiente decidir si se alinea la narrativa.

### Aprobar/rechazar aplicaciones realista
**Contexto:** solo había 2 aplicantes sembrados → la pantalla se veía vacía. Y el admin
detalle no mostraba LinkedIn/país (agregados en Ronda 1 pero no surfaceados).

**Cambios:**
- Seed: 8 aplicantes con perfiles diferenciados (fuerte/medio/débil), 3 con score
  Claude pre-sembrado, variados por país (CO/MX/AR/CL/BR/PE/US/EC) y locale (es/en/pt).
- `AdminApplications.tsx` ahora hace `GET /applications/{id}` al seleccionar (el list
  endpoint devuelve shape liviano sin `answers`/`video_url`/etc.) — **bug fix**.
- Muestra LinkedIn + país + notas admin previas en el detalle.

---

## Ronda 1 — primer feedback del usuario

Esta ronda está completamente reflejada en el commit
`4876ef7 · Feedback round 1: UX por rol, rebrand 2026, admin editor de curso`. Resumen
de los 12 cambios organizados por rol:

### Global
- **Logo "Siete /academy" → dashboard por rol** cuando el usuario está autenticado.
  Antes siempre iba a `/` (landing marketing).
- **Language selector: banderitas 🇪🇸 🇺🇸 🇧🇷** con grayscale para inactivos.
  Antes: texto `es · en · pt`.
- **Avatar/menú cuenta** al final del nav (todos los roles): dropdown con "Mi cuenta" +
  "Cerrar sesión" + nombre + email + role. Incluye foto_url si está seteada.

### Alumno
- **Tabs nuevos:** Mi Progreso · Feedback Profesor · Calendario (quitado Certificado).
- **`/account`** (todos los roles, no solo alumno) — editable: display_name, photo_url.
  Email read-only. Password: nota "se gestiona via Google".
- **`/student/calendar`** — nueva página con sesiones en vivo + ventanas + grabaciones,
  agregado-cruzadamente de todas las cohortes del alumno.
- **Manuales/lecturas** dentro de módulos — `Lesson.kind: "video" | "reading"`. Los
  reading son markdown inline renderizado con `user-select: none` y `@media print {
  display: none }`. No descargables.
- **Material de apoyo por módulo** — nuevo modelo `ModuleResource` (pdf/ppt/video/doc/link,
  URL-based). Admin los agrega, alumno los ve en sidebar del módulo.
- **Botón compartir en LinkedIn + copiar link** en dashboard — referral a la red del
  alumno. Usa LinkedIn share intent URL.

### Profesor
- **`/teacher` es ahora un dashboard**, no la cola de revisiones directamente.
  Endpoint nuevo: `GET /teacher/dashboard` con stats por cohorte + tabla completa de
  alumnos (progreso, lecciones completadas, nota promedio, última actividad, certificado).
- **`/teacher/reviews`** — la vieja cola. Ahora con búsqueda libre + filtro por alumno +
  filtro por entregable. Endpoint nuevo `/teacher/pending` retorna shape enriquecido con
  nombre del alumno + título del entregable + módulo.
- **Botón "Emitir" certificado** por fila cuando `progress_pct == 100`. Dispara email
  al alumno con código de verificación.

### Admin
- **`/admin/course` — editor completo del curso:** CRUD módulos, lecciones, material de
  apoyo, pruebas.
  - `GET /courses/{course_id}/admin` — shape admin con todas las traducciones + lecciones
    + recursos anidados
  - `PATCH /courses/modules/{id}` — editar módulo (order + traducciones)
  - `PATCH /courses/lessons/{id}` + `DELETE` — editar/eliminar lección
  - CRUD resources (`/courses/modules/{id}/resources`, `/courses/resources/{id}`)
  - CRUD assessments (`POST /assessments`, `PATCH /assessments/{id}`,
    `DELETE /assessments/{id}`)
- **Assessments editor con JSON config textarea** — los 5 tipos (MCQ, written,
  prospection_db, cold_call_video, team_exercise) comparten schema pero tienen placeholders
  distintos. Cambio técnico: `Literal` en `AssessmentUpdate` + typescript types en el
  frontend.

### Reclutador
- **Botón "Agendar entrevista"** por candidato → abre `mailto:` con asunto y cuerpo
  pre-armados en el idioma del recluta. Requería exponer `user_email` en
  `CandidateRecruiterOut`.

### Formulario de aplicación
- **LinkedIn URL + país** obligatorios. Campos nuevos en `Application`:
  `linkedin_url: str`, `country: str`. Validado en schema (min/max length).

### Certificado
- **Fuera del nav del alumno** (queda la ruta `/student/certificate` viva por compatibilidad,
  pero no aparece en tabs).
- **Auto-email al emitir** — `backend/app/modules/certificates/services.py::_send_cert_email`.
  Mensaje bilingüe según locale del user.
- **Endpoint `/certificates/issue` acepta body** (antes query params) y permite
  role=teacher (antes solo admin).

### Rebrand 2026 (primera pasada — ajustada después en ronda 2)
Ver sección "Rebrand final" arriba para el estado definitivo.

---

## Decisiones que NO se tomaron y quedan abiertas

1. **¿Unificar aprobación + enrollment?** Hoy son dos acciones separadas. Puede simplificarse.
   Alternativa: añadir `cohort_id?: int` a `ApplicationReview`. Si status=approved y
   cohort_id presente, crear User + Enrollment automáticamente + disparar email de
   bienvenida (reutilizando `_send_welcome_email`).

2. **Narrativa de "te contratamos" vs. recruiter externo.** El hero dice "te contratamos"
   pero `/recruiter` sigue pensado para terceros contratando graduados. Debe unificarse la
   historia. Dos caminos:
   - Siete contrata a todos → eliminar `/recruiter` del scope.
   - Siete + partners contratan → reescribir copy del hero para reflejar ambos caminos.

3. **Upload real de archivos vs. URL-based.** Hoy todo es URL. Si deciden hacer upload,
   ver `HANDOFF.md` → sección "Decisiones de diseño" punto 2.

4. **Slack: URL o API.** Hoy URL. Si deciden API, hay que crear el workspace + cambiar
   `_send_welcome_email`. Ver `HANDOFF.md` → punto 9.

---

## Cómo auditar este changelog

Cada cambio mencionado aquí debe tener:

- Un commit asociado (`git log`)
- Archivos `.md` de documentación si afecta otro equipo
- Tests verdes en `make test`
- Al menos un render verificado en `make demo` con los 4 roles

Si alguno de los puntos no se cumple, el cambio se considera **no shipeado** y debe revisarse
antes de mergear a main.
