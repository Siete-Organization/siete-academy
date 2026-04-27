# Flujogramas — Siete Academy

> Diagramas en **Mermaid** (renderizables nativamente en GitHub, GitLab, VS Code, Obsidian, Notion).
> Si los abres en un visor que no soporta Mermaid, usa <https://mermaid.live> y pega el bloque.

Índice:

1. [Arquitectura general (C4 nivel 1)](#1-arquitectura-general-c4-nivel-1)
2. [Componentes internos del backend](#2-componentes-internos-del-backend)
3. [Modelo de datos (ER simplificado)](#3-modelo-de-datos-er-simplificado)
4. [Flujo del aspirante: postulación → decisión](#4-flujo-del-aspirante-postulación--decisión)
5. [Flujo del admin: aprobar aplicación → enrolar alumno](#5-flujo-del-admin-aprobar-aplicación--enrolar-alumno)
6. [Flujo del alumno: módulo → progreso → entrega](#6-flujo-del-alumno-módulo--progreso--entrega)
7. [Flujo del profesor: cola de revisiones → review](#7-flujo-del-profesor-cola-de-revisiones--review)
8. [Flujo de emisión y verificación de certificado](#8-flujo-de-emisión-y-verificación-de-certificado)
9. [Pipeline ATS de placement (state machine)](#9-pipeline-ats-de-placement-state-machine)
10. [Ciclo de vida de una aplicación (state diagram)](#10-ciclo-de-vida-de-una-aplicación-state-diagram)
11. [Ciclo de vida de un enrollment](#11-ciclo-de-vida-de-un-enrollment)
12. [Autenticación: dev bypass vs. Firebase](#12-autenticación-dev-bypass-vs-firebase)
13. [Pipeline AI (Claude scoring + drafts)](#13-pipeline-ai-claude-scoring--drafts)
14. [Mapa de navegación por rol](#14-mapa-de-navegación-por-rol)

---

## 1. Arquitectura general (C4 nivel 1)

```mermaid
graph TB
  subgraph Externos
    APP[Aspirante anónimo]
    STU[Alumno]
    TEA[Profesor]
    ADM[Admin]
    REC[Recruiter externo]
    PUB[Visitante público<br/>verifica certificado]
  end

  subgraph SieteAcademy["Siete Academy SPA + API"]
    FE[Frontend React + Vite<br/>siete.com/academy/*]
    BE[Backend FastAPI<br/>siete.com/api/academy/*]
    DB[(Postgres / SQLite)]
    RD[(Redis<br/>cache + Celery broker)]
    WK[Celery Worker<br/>emails + scoring]
  end

  subgraph Terceros
    FB[Firebase Auth]
    SMTP[SMTP Resend / Postmark]
    CL[Anthropic Claude API]
    YT[YouTube unlisted]
    ZM[Zoom]
    SL[Slack]
  end

  APP --> FE
  STU --> FE
  TEA --> FE
  ADM --> FE
  REC --> FE
  PUB --> FE

  FE -->|Bearer token JWT| BE
  BE --> DB
  BE --> RD
  BE -.->|enqueue| WK
  WK --> RD
  WK --> CL
  WK --> SMTP

  FE --> FB
  BE -.->|verify_id_token| FB
  FE --> YT
  STU -->|live session| ZM
  STU -->|comunidad| SL
```

---

## 2. Componentes internos del backend

```mermaid
graph LR
  subgraph Core
    cfg[core/config.py<br/>Settings]
    db[core/database.py<br/>SQLAlchemy]
    log[core/logging.py<br/>+ request_id]
    lim[core/limiter.py<br/>SlowAPI]
    fbm[core/firebase.py]
    cel[core/celery_app.py]
    pip[core/pipeline.py]
  end

  subgraph Modulos
    M_auth[auth]
    M_users[users]
    M_app[applications]
    M_coh[cohorts]
    M_cou[courses]
    M_enr[enrollment]
    M_ass[assessments]
    M_liv[live_sessions]
    M_pla[placement]
    M_cer[certificates]
    M_ai[ai_review]
    M_tea[teacher]
    M_not[notifications]
    M_aud[audit]
  end

  main[main.py FastAPI]
  main --> cfg
  main --> log
  main --> lim
  main --> M_auth
  main --> M_users
  main --> M_app
  main --> M_coh
  main --> M_cou
  main --> M_enr
  main --> M_ass
  main --> M_liv
  main --> M_pla
  main --> M_cer
  main --> M_ai
  main --> M_tea

  M_app -.->|ai score| M_ai
  M_ass -.->|ai draft| M_ai
  M_app --> M_not
  M_enr --> M_not
  M_cer --> M_not
  M_pla --> M_aud
  M_ai --> M_aud
```

---

## 3. Modelo de datos (ER simplificado)

```mermaid
erDiagram
  USERS ||--o{ ENROLLMENTS : "tiene"
  USERS ||--o{ APPLICATIONS : "revisa"
  USERS ||--o{ SUBMISSIONS : "entrega"
  USERS ||--o{ TEACHER_REVIEWS : "califica"
  USERS ||--o{ TEACHER_NOTES : "envía/recibe"
  USERS ||--o{ CERTIFICATES : "obtiene"
  USERS ||--o{ PLACEMENT_CANDIDATES : "es candidato"

  COHORTS ||--o{ ENROLLMENTS : "agrupa"
  COHORTS ||--o{ MODULE_WINDOWS : "abre"
  COHORTS ||--o{ CERTIFICATES : "emite"
  COHORTS ||--o{ PLACEMENT_CANDIDATES : "origina"

  COURSES ||--o{ COURSE_TRANSLATIONS : "es"
  COURSES ||--o{ MODULES : "contiene"
  MODULES ||--o{ MODULE_TRANSLATIONS : "es"
  MODULES ||--o{ LESSONS : "contiene"
  MODULES ||--o{ MODULE_RESOURCES : "tiene"
  MODULES ||--o{ ASSESSMENTS : "evalúa"
  MODULES ||--o{ MODULE_WINDOWS : "agendado en"
  LESSONS ||--o{ LESSON_TRANSLATIONS : "es"
  LESSONS ||--o{ LESSON_PROGRESS : "trackeado"

  ENROLLMENTS ||--o{ LESSON_PROGRESS : "registra"
  ASSESSMENTS ||--o{ SUBMISSIONS : "recibe"
  SUBMISSIONS ||--|| TEACHER_REVIEWS : "calificada"
  SUBMISSIONS ||--|| AI_REVIEWS : "borrador"

  MODULE_WINDOWS ||--|| LIVE_SESSIONS : "tiene"

  PLACEMENT_CANDIDATES ||--o{ PLACEMENT_EVENTS : "audita"

  USERS {
    int id PK
    string firebase_uid UK
    string email UK
    string role
    string locale
    json profile
  }

  COHORTS {
    int id PK
    string name UK
    date start_date
    date end_date
    string status
    int max_students
    string slack_invite_url
  }

  ENROLLMENTS {
    int id PK
    int user_id FK
    int cohort_id FK
    string status
    float progress_pct
    datetime completed_at
  }

  APPLICATIONS {
    int id PK
    string applicant_email
    string linkedin_url
    json answers
    string video_url
    int ai_score
    string status
    int reviewed_by_id FK
  }

  ASSESSMENTS {
    int id PK
    int module_id FK
    string type
    json config
    float passing_score
  }

  PLACEMENT_CANDIDATES {
    int id PK
    int user_id FK,UK
    int cohort_id FK
    string stage
  }
```

---

## 4. Flujo del aspirante: postulación → decisión

```mermaid
sequenceDiagram
  autonumber
  actor Asp as Aspirante
  participant FE as Frontend (/apply)
  participant API as Backend FastAPI
  participant DB as Postgres
  participant Q as Celery
  participant CL as Claude API
  participant MAIL as SMTP
  actor ADM as Admin

  Asp->>FE: Completa formulario (nombre, email, LinkedIn,<br/>3 respuestas ≥100 palabras, video URL)
  FE->>FE: Valida wordcount client-side
  FE->>API: POST /applications (rate-limit 5/h/IP)
  API->>DB: INSERT applications (status=submitted)
  API-->>FE: 201 ApplicationOut
  FE-->>Asp: Pantalla "Tu aplicación está en nuestra mesa"

  par Notificación
    API->>Q: notify_submitted(app_id)
    Q->>MAIL: Email acuse al aspirante
  and Scoring opcional
    API->>Q: score_application_task(app_id)
    Q->>CL: prompt scoring (si ANTHROPIC_API_KEY)
    CL-->>Q: score 0-100 + notes
    Q->>DB: UPDATE applications SET ai_score, ai_notes
  end

  Note over ADM: ...horas después...
  ADM->>FE: GET /admin/applications
  FE->>API: GET /applications?status=submitted
  ADM->>FE: Selecciona y revisa
  ADM->>FE: Aprobar / Rechazar + notas
  FE->>API: POST /applications/{id}/review
  API->>DB: UPDATE status, reviewed_by_id, reviewed_at
  API->>Q: notify_decision(app_id)
  Q->>MAIL: Email de decisión
```

---

## 5. Flujo del admin: aprobar aplicación → enrolar alumno

```mermaid
flowchart TD
  start([Aplicación aprobada]) --> exists{¿User existe<br/>con ese email?}
  exists -->|No| createUser[POST /users<br/>crear con role=student]
  exists -->|Sí| skipUser[Reutilizar User]
  createUser --> selectCohort
  skipUser --> selectCohort
  selectCohort[/Admin selecciona cohorte<br/>en /admin/cohorts/]
  selectCohort --> enroll[POST /enrollment<br/>user_id + cohort_id]
  enroll --> dup{¿Ya enrolado<br/>en esa cohorte?}
  dup -->|Sí| reuse[Devuelve enrollment existente]
  dup -->|No| persist[INSERT enrollments<br/>status=active, progress_pct=0]
  persist --> welcome[_send_welcome_email<br/>idioma del alumno + link Slack]
  welcome --> done([Alumno listo<br/>para entrar a /student])
  reuse --> done
```

---

## 6. Flujo del alumno: módulo → progreso → entrega

```mermaid
sequenceDiagram
  autonumber
  actor S as Student
  participant FE as Frontend
  participant API as Backend
  participant DB as DB
  participant Q as Celery
  participant CL as Claude

  S->>FE: GET /student
  FE->>API: GET /enrollment/me
  API->>DB: SELECT enrollments + cohort_name + slack_invite_url
  API-->>FE: lista cohortes
  FE->>API: GET /cohorts/{id}/windows (paralelo por cohorte)
  API-->>FE: ventanas de módulo

  S->>FE: Abre módulo dentro de su ventana
  FE->>API: GET /courses/{id} + /assessments/module/{id}
  API-->>FE: lecciones + recursos + pruebas

  loop Por cada lección completada
    FE->>API: POST /enrollment/{id}/progress<br/>{lesson_id, watched_pct, completed}
    API->>DB: UPSERT lesson_progress
    API->>DB: recalcula progress_pct (futuro hook)
    API-->>FE: LessonProgressOut
  end

  S->>FE: Submite MCQ
  FE->>API: POST /assessments/submissions
  alt type == mcq
    API->>DB: auto_score, status=auto_graded
  else otros tipos
    API->>DB: status=pending_review
    API->>Q: review_submission_task(s.id)
    Q->>CL: prompt borrador feedback
    CL-->>Q: draft_feedback + score_suggestion
    Q->>DB: INSERT ai_reviews
  end
  API-->>FE: SubmissionOut

  S->>FE: GET /student/feedback
  FE->>API: GET /assessments/submissions/me/with-reviews
  API-->>FE: submissions + assessment_title + review (LEFT JOIN)
  FE-->>S: lista con feedback humano (si existe)
```

---

## 7. Flujo del profesor: cola de revisiones → review

```mermaid
flowchart LR
  start([Teacher entra a /teacher/reviews]) --> fetch[GET /teacher/pending<br/>shape enriquecido]
  fetch --> filter{¿Filtra por<br/>alumno o entregable?}
  filter -->|Sí| narrow[Lista filtrada]
  filter -->|No| narrow[Lista completa]
  narrow --> select[Selecciona submission]
  select --> ai[GET /ai-review/submission/{id}]
  ai --> hasDraft{¿Existe AIReview?}
  hasDraft -->|Sí| showDraft[Muestra borrador Claude<br/>solo al profesor]
  hasDraft -->|No| empty[Sin borrador]
  showDraft --> grade[Profesor escribe feedback<br/>+ score + adjunto opcional]
  empty --> grade
  grade --> submit[POST /assessments/submissions/{id}/review]
  submit --> persist[INSERT/UPDATE teacher_reviews<br/>+ submission.status=reviewed]
  persist --> studentSees([Alumno ve la review<br/>en /student/feedback])
```

---

## 8. Flujo de emisión y verificación de certificado

```mermaid
flowchart TD
  subgraph Emisión["Emisión (admin/teacher)"]
    A[Alumno alcanza progress_pct == 100] --> B[Botón Emitir aparece<br/>en /teacher fila del alumno]
    B --> C[POST /certificates/issue<br/>user_id + cohort_id]
    C --> D{¿enrollment existe<br/>y progreso == 100?}
    D -->|No| E[422 Not eligible]
    D -->|Sí| F[INSERT certificates<br/>verification_code único]
    F --> G[email bilingüe al alumno<br/>con link de verificación]
  end

  subgraph Verificación["Verificación pública"]
    H[Cualquiera entra a /verify/CODE] --> I[GET /certificates/verify/CODE<br/>rate-limit 30/min/IP]
    I --> J{¿Existe?}
    J -->|No| K[404]
    J -->|Sí| L[Devuelve nombre + cohorte<br/>+ fecha de emisión]
  end

  G -.-> H
```

---

## 9. Pipeline ATS de placement (state machine)

```mermaid
stateDiagram-v2
  [*] --> applying : POST /placement/candidates
  applying --> siete_interview : PATCH stage
  siete_interview --> siete_test : pasa entrevista
  siete_test --> approved : pasa prueba
  siete_test --> rejected : no pasa
  approved --> presented : presentado a cliente
  presented --> placed : cliente lo contrata
  presented --> rejected : cliente lo rechaza
  approved --> rejected : por inactividad
  placed --> [*]
  rejected --> [*]

  note right of approved
    Visible al recruiter externo
    desde aquí en adelante
  end note

  note right of applying
    Cada cambio crea
    PlacementEvent auditable
  end note
```

---

## 10. Ciclo de vida de una aplicación (state diagram)

```mermaid
stateDiagram-v2
  [*] --> submitted : POST /applications (público)
  submitted --> under_review : admin abre / Claude scorea
  under_review --> approved : POST /applications/{id}/review
  under_review --> rejected : POST /applications/{id}/review
  submitted --> approved : admin aprueba directo
  submitted --> rejected : admin rechaza directo
  approved --> [*] : (manual) → User + Enrollment
  rejected --> [*]
```

---

## 11. Ciclo de vida de un enrollment

```mermaid
stateDiagram-v2
  [*] --> active : POST /enrollment
  active --> paused : admin PATCH status=paused
  paused --> active : admin PATCH status=active
  active --> dropped : admin PATCH status=dropped
  active --> completed : progress_pct == 100
  completed --> [*]
  dropped --> [*]
```

---

## 12. Autenticación: dev bypass vs. Firebase

```mermaid
flowchart TD
  req[Request entrante] --> hdr{Headers}
  hdr --> dev{X-Dev-User<br/>presente?}
  dev -->|Sí| envCheck{APP_ENV ==<br/>development<br/>+ dev_auth_bypass?}
  envCheck -->|Sí| lookup[SELECT user WHERE email=X-Dev-User]
  envCheck -->|No| reject401a[401 Unauthorized]
  lookup --> found{¿Existe?}
  found -->|Sí| ok1[CurrentUser claims=_dev]
  found -->|No| reject401b[401 'Run make seed first']

  dev -->|No| bearer{Authorization:<br/>Bearer ...?}
  bearer -->|No| reject401c[401 Missing bearer]
  bearer -->|Sí| verify[verify_id_token<br/>Firebase Admin SDK]
  verify --> bad{Token válido?}
  bad -->|No| reject401d[401 Invalid token]
  bad -->|Sí| up{¿User existe<br/>con firebase_uid?}
  up -->|No| provision[INSERT users<br/>con role del custom claim]
  provision --> ok2[CurrentUser claims=Firebase]
  up -->|Sí| ok2

  ok1 --> roles{require_roles<br/>matchea?}
  ok2 --> roles
  roles -->|Sí| handler[Handler ejecuta]
  roles -->|No| reject403[403 Forbidden]
```

---

## 13. Pipeline AI (Claude scoring + drafts)

```mermaid
sequenceDiagram
  autonumber
  participant ROUTE as Router (apps / assessments)
  participant Q as Celery
  participant CL as Claude API
  participant DB as DB
  participant LOG as ai_call_logs

  Note over ROUTE: Trigger A — Application submitted
  ROUTE->>Q: score_application_task(app_id)
  Q->>DB: SELECT application
  Q->>CL: prompt(answers, video_url, perfil) → score+notes
  alt Anthropic key vacío
    CL-->>Q: skipped (no-op)
  else con key
    CL-->>Q: {score: 0-100, notes: text}
    Q->>DB: UPDATE applications SET ai_score, ai_notes
  end
  Q->>LOG: INSERT ai_call_logs (purpose=app_score)

  Note over ROUTE: Trigger B — Submission con type != mcq
  ROUTE->>Q: review_submission_task(submission_id)
  Q->>DB: SELECT submission + assessment
  Q->>CL: prompt(payload, file_url, rubric)
  CL-->>Q: {draft_feedback, score_suggestion, model}
  Q->>DB: INSERT ai_reviews
  Q->>LOG: INSERT ai_call_logs (purpose=submission_draft)

  Note over LOG: Cada llamada queda auditada<br/>para revisar costo Anthropic
```

---

## 14. Mapa de navegación por rol

```mermaid
flowchart LR
  classDef pub fill:#fef3c7,stroke:#92400e
  classDef stu fill:#dbeafe,stroke:#1e40af
  classDef tea fill:#d1fae5,stroke:#065f46
  classDef adm fill:#fce7f3,stroke:#9d174d
  classDef rec fill:#ede9fe,stroke:#5b21b6

  Home["/ HomePage"]:::pub
  Apply["/apply"]:::pub
  Login["/login"]:::pub
  Verify["/verify/CODE"]:::pub

  Account["/account"]

  StuHome["/student"]:::stu
  StuMod["/student/module/:id"]:::stu
  StuFB["/student/feedback"]:::stu
  StuCal["/student/calendar"]:::stu
  StuCert["/student/certificate (legacy)"]:::stu

  TeaHome["/teacher"]:::tea
  TeaRev["/teacher/reviews"]:::tea

  AdmHome["/admin"]:::adm
  AdmApp["/admin/applications"]:::adm
  AdmCoh["/admin/cohorts"]:::adm
  AdmCou["/admin/course"]:::adm
  AdmPla["/admin/placement"]:::adm
  AdmAna["/admin/analytics"]:::adm

  RecHome["/recruiter"]:::rec

  Home --> Apply
  Home --> Login
  Login -->|student| StuHome
  Login -->|teacher| TeaHome
  Login -->|admin| AdmHome
  Login -->|recruiter| RecHome

  StuHome --> StuMod
  StuHome --> StuFB
  StuHome --> StuCal
  StuHome --> Account

  TeaHome --> TeaRev
  TeaHome --> Account

  AdmHome --> AdmApp
  AdmHome --> AdmCoh
  AdmHome --> AdmCou
  AdmHome --> AdmPla
  AdmHome --> AdmAna
  AdmHome --> Account

  RecHome --> Account

  AdmApp -.->|aprueba| AdmCoh
  AdmCoh -.->|enrola → email Slack| StuHome
  TeaRev -.->|review| StuFB
  TeaHome -.->|emite cert| Verify
```

---

## Apéndice — Cómo regenerar/editar estos diagramas

1. Cualquier vista en GitHub renderiza Mermaid de forma nativa.
2. Para editar visualmente: <https://mermaid.live> → pegar el bloque entre los \`\`\`mermaid \`\`\`.
3. VS Code: extensión **Markdown Preview Mermaid Support**.
4. Si agregas un módulo nuevo, recuerda actualizar al menos:
   - Diagrama 2 (componentes)
   - Diagrama 3 (modelo de datos) si introduces tabla nueva
   - Diagrama 14 (navegación) si añade ruta de UI
