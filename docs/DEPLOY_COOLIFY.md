# Deploy a Coolify — Siete Academy

> Runbook end-to-end para llevar el repo a producción en `siete.com/academy`.
> Hermanos: [`MANUAL.md`](MANUAL.md) (proceso) · [`ARQUITECTURA.md`](ARQUITECTURA.md) (técnico) · raíz [`NEXT_STEPS_PROD.md`](../NEXT_STEPS_PROD.md) (la versión "humana" original).
>
> **Tiempo:** ≈ 6–8 h de trabajo + esperas DNS/TLS. **Orden importa** — no saltees pasos.
>
> **Antes de empezar lee la sección [§ 0 Pitfalls de Coolify](#0--pitfalls-conocidos-de-coolify-leer-primero)** — son trampas que ya golpearon a otro repo de Siete (`AI-SDR`) en producción real.

---

## 0 · Pitfalls conocidos de Coolify (leer primero)

### 0.1 Auto-deploy dispara solo en **push directo a `main`**

Coolify **no** despliega cuando se mergea un PR vía la UI de GitHub (lo registró el equipo el 2026-04-21 con `AI-SDR`). Si haces "Squash & merge" en GitHub, Coolify se queda dormido hasta que alguien empuje un commit directo.

**Workflow correcto (mantener):**

```bash
git checkout main
git pull
git merge --ff-only <feature-branch>
git push origin main          # ← este es el que despierta Coolify
```

> Si por política tu equipo merge desde la UI, después tienes que hacer un push trivial (`git commit --allow-empty -m "trigger deploy" && git push origin main`) o gatillarlo manual desde el panel de Coolify (botón "Redeploy").

### 0.2 El entrypoint puede **tragarse fallas de Alembic**

Patrón frecuente y peligroso:

```bash
alembic upgrade head || echo "WARNING: migration failed"  # ← MAL silencioso
```

Si la migración falla, el contenedor no crashea, la API arranca con **schema viejo**, y empiezan a aparecer 500s "column does not exist". Esto pasó en `AI-SDR` con la columna `search_learnings`.

**Regla para Siete Academy:** el entrypoint de `api` **debe** tronar si `alembic upgrade head` falla. Si te preocupa downtime durante incidentes de DB, separa **migraciones** del **arranque** (ver [§ 4.2](#42-entrypoint-de-api-recomendado)).

### 0.3 Otros que vale recordar

- **Coolify usa el `Dockerfile` que está en el path del repo**, no `docker-compose.yml`. El compose sirve solo para dev local.
- **Healthcheck de Coolify** se basa en HTTP; si tu app tarda > 30 s en arrancar, ajusta el `start_period`.
- **Volúmenes de Postgres**: si recreas el servicio sin proteger el volumen, **pierdes data**. Marca el volumen como persistente.
- **Logs Coolify se rotan**. Para retención larga, conecta Loki/Datadog.

---

## 1 · Prerrequisitos (qué necesitas antes de empezar)

| Cosa | Para qué | Dónde |
|---|---|---|
| VPS Hetzner (≥ 4 GB RAM) con Coolify instalado | Orquestación | Panel Hetzner; si Coolify no está, `curl -fsSL https://cdn.coollabs.io/coolify/install.sh \| bash` |
| Acceso SSH al VPS | Backup/debug puntual | Panel Hetzner → SSH key |
| Repo en GitHub privado: `Siete-Organization/siete-academy` | Coolify lo clona | `gh repo create Siete-Organization/siete-academy --private --source=. --push` |
| Dominio `siete.com` con DNS gestionable (Cloudflare ideal) | TLS + routing | Cloudflare DNS |
| Proyecto Firebase (`siete-academy`) | Auth real | console.firebase.google.com |
| Cuenta SMTP (Resend recomendado) | Emails transaccionales | resend.com |
| `ANTHROPIC_API_KEY` | Scoring + drafts | console.anthropic.com |
| Acceso Webflow | Agregar link "Academy" en navbar | tu cuenta Webflow |

---

## 2 · Hardening del repo antes del primer deploy

Los `Dockerfile` que están **hoy** en el repo (`backend/Dockerfile`, `frontend/Dockerfile`) son de **desarrollo**:

- `frontend/Dockerfile` arranca `npm run dev` (Vite dev server con HMR) — **no servir esto en prod**.
- `backend/Dockerfile` no corre migraciones, ni usa `gunicorn`, ni se compila multi-stage.

Antes del primer deploy hay que reemplazarlos. Estas son las versiones de producción.

### 2.1 `backend/Dockerfile` — versión prod (multi-stage, non-root)

```dockerfile
# ---------- builder ----------
FROM python:3.12-slim AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && pip install --prefix=/install -r requirements.txt

# ---------- runtime ----------
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/install/bin:$PATH" \
    PYTHONPATH="/app"

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 curl \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --create-home --uid 1001 siete

WORKDIR /app
COPY --from=builder /install /install
COPY --chown=siete:siete . .

USER siete

EXPOSE 8000

# Healthcheck honest: golpea /health con timeout corto
HEALTHCHECK --interval=15s --timeout=5s --start-period=20s --retries=4 \
  CMD curl -fsS http://127.0.0.1:8000/health || exit 1

CMD ["sh", "deploy/entrypoint-api.sh"]
```

### 2.2 `frontend/Dockerfile` — versión prod (Caddy sirviendo el build)

```dockerfile
# ---------- builder ----------
FROM node:20-alpine AS builder
WORKDIR /app

# Las VITE_* deben estar disponibles en el build (Vite las inlinea en el bundle)
ARG VITE_API_BASE_URL
ARG VITE_FIREBASE_API_KEY
ARG VITE_FIREBASE_AUTH_DOMAIN
ARG VITE_FIREBASE_PROJECT_ID
ARG VITE_FIREBASE_STORAGE_BUCKET
ARG VITE_FIREBASE_MESSAGING_SENDER_ID
ARG VITE_FIREBASE_APP_ID

ENV VITE_API_BASE_URL=$VITE_API_BASE_URL \
    VITE_FIREBASE_API_KEY=$VITE_FIREBASE_API_KEY \
    VITE_FIREBASE_AUTH_DOMAIN=$VITE_FIREBASE_AUTH_DOMAIN \
    VITE_FIREBASE_PROJECT_ID=$VITE_FIREBASE_PROJECT_ID \
    VITE_FIREBASE_STORAGE_BUCKET=$VITE_FIREBASE_STORAGE_BUCKET \
    VITE_FIREBASE_MESSAGING_SENDER_ID=$VITE_FIREBASE_MESSAGING_SENDER_ID \
    VITE_FIREBASE_APP_ID=$VITE_FIREBASE_APP_ID

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build       # genera /app/dist

# ---------- runtime ----------
FROM caddy:2-alpine

COPY --from=builder /app/dist /usr/share/caddy
COPY deploy/Caddyfile /etc/caddy/Caddyfile

EXPOSE 80
HEALTHCHECK --interval=15s --timeout=5s --start-period=10s --retries=3 \
  CMD wget -qO- http://127.0.0.1/ || exit 1
```

### 2.3 `deploy/Caddyfile` (frontend SPA)

```caddyfile
:80 {
    encode zstd gzip

    # SPA fallback: todo lo desconocido cae a index.html
    handle {
        try_files {path} /index.html
        root * /usr/share/caddy
        file_server
    }

    header {
        Strict-Transport-Security "max-age=31536000; includeSubDomains"
        X-Content-Type-Options "nosniff"
        X-Frame-Options "DENY"
        Referrer-Policy "strict-origin-when-cross-origin"
        # Si llamas APIs de terceros (Firebase, Anthropic), ajusta CSP:
        Content-Security-Policy "default-src 'self'; img-src 'self' data: https:; script-src 'self' 'unsafe-inline' https://apis.google.com https://www.gstatic.com; connect-src 'self' https://*.googleapis.com https://*.firebaseio.com https://identitytoolkit.googleapis.com; frame-src https://www.youtube-nocookie.com https://drive.google.com; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com data:;"
    }
}
```

### 2.4 `deploy/entrypoint-api.sh` (backend)

```bash
#!/usr/bin/env sh
set -euo pipefail

echo "[entrypoint] running alembic upgrade head"
alembic upgrade head    # ← SIN `|| echo`. Si falla, el contenedor crashea.

echo "[entrypoint] starting gunicorn"
exec gunicorn app.main:app \
    --workers ${WEB_CONCURRENCY:-3} \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000 \
    --access-logfile - \
    --error-logfile - \
    --timeout 60 \
    --keep-alive 5
```

> Hazlo ejecutable: `chmod +x deploy/entrypoint-api.sh`. Y agrega `gunicorn` a `backend/requirements.txt` si no está.

### 2.5 `deploy/entrypoint-worker.sh` (Celery worker)

```bash
#!/usr/bin/env sh
set -euo pipefail

# IMPORTANTE: el worker NO corre migraciones. Solo `api` lo hace.
echo "[entrypoint] starting celery worker"
exec celery -A app.core.celery_app.celery_app worker \
    --loglevel=info \
    --concurrency=${CELERY_CONCURRENCY:-2}
```

---

## 3 · Crear el proyecto y servicios en Coolify

En Coolify → **+ New Project** → nombre `siete-academy`.

Dentro del proyecto, crear **5 resources**:

| Nombre | Tipo | Notas |
|---|---|---|
| `postgres` | Database → **PostgreSQL 16** | Volumen persistente. Anota credenciales generadas. |
| `redis` | Database → **Redis 7** | Persistencia opcional. |
| `api` | Application → **Dockerfile** (Git source) | Repo `Siete-Organization/siete-academy`, branch `main`, Dockerfile path `backend/Dockerfile`, **build context `/` (raíz del repo)**. Port `8000`. |
| `worker` | Application → **Dockerfile** | **Mismo repo, Dockerfile y build context que `api`**. Override `Custom Start Command` → `/usr/local/bin/entrypoint-worker.sh`. Sin port expuesto. |
| `frontend` | Application → **Dockerfile** | Dockerfile path `frontend/Dockerfile`, **build context `/` (raíz del repo)**. Port `80`. |

> ⚠️ **Build context = raíz del repo** (NO la subcarpeta). Los Dockerfiles de prod usan paths como `backend/requirements.txt` y `deploy/entrypoint-api.sh` que solo resuelven con la raíz como context.

**Conectar Git source:** Coolify → Sources → GitHub App → instalar en la org `Siete-Organization` → seleccionar `siete-academy`.

> El `docker-compose.yml` del repo es **solo para dev local** y debe ignorarse en Coolify. Crea cada resource como Application from Dockerfile.

---

## 4 · Variables de entorno

> Pegar en Coolify → cada Application → tab **Environment Variables**. Marca como **Build-time** las que necesite Vite.

### 4.1 `api` y `worker` (mismas vars excepto donde se indica)

| Var | Valor | Notas |
|---|---|---|
| `APP_ENV` | `production` | Activa root_path, valida bypass dev OFF. |
| `APP_SECRET_KEY` | `openssl rand -hex 32` | Único por entorno. |
| `PUBLIC_BASE_URL` | `https://siete.com` | Usado en links de email. |
| `ALLOWED_ORIGINS` | `https://siete.com` | Coma-separados si hay más. |
| `DATABASE_URL` | `postgresql+psycopg://siete:<pwd>@<postgres-internal-host>:5432/siete_academy` | Usa el host **interno** que Coolify expone (suele ser el nombre del recurso). |
| `REDIS_URL` | `redis://<redis-internal-host>:6379/0` | Igual: host interno. |
| `DEV_AUTH_BYPASS` | `false` | El código ya rechaza el bypass si esto es false o si APP_ENV != development. |
| `CELERY_ALWAYS_EAGER` | `false` | El worker recoge tasks reales. |
| `FIREBASE_CREDENTIALS_JSON` | `<service account JSON en una sola línea>` | Generado en Firebase → Service accounts → Generate new private key. |
| `FIREBASE_PROJECT_ID` | `siete-academy` | |
| `ANTHROPIC_API_KEY` | `sk-ant-…` | Si lo dejas vacío, el pipeline AI degrada silenciosamente (no rompe). |
| `ANTHROPIC_MODEL` | `claude-opus-4-7` | |
| `SMTP_HOST` | `smtp.resend.com` | |
| `SMTP_PORT` | `587` | |
| `SMTP_USER` | `resend` | Para Resend, literalmente "resend". |
| `SMTP_PASSWORD` | `re_…` | API key de Resend. |
| `SMTP_FROM` | `"Siete Academy <academy@siete.com>"` | Dominio debe estar verificado en Resend. |
| `WEB_CONCURRENCY` | `3` | Solo `api`. Workers gunicorn. |
| `CELERY_CONCURRENCY` | `2` | Solo `worker`. |

### 4.2 `frontend` (todas son **Build-time** porque Vite las inlinea)

| Var | Valor |
|---|---|
| `VITE_API_BASE_URL` | `/api/academy` |
| `VITE_FIREBASE_API_KEY` | `<de Firebase Web App>` |
| `VITE_FIREBASE_AUTH_DOMAIN` | `siete-academy.firebaseapp.com` |
| `VITE_FIREBASE_PROJECT_ID` | `siete-academy` |
| `VITE_FIREBASE_STORAGE_BUCKET` | `siete-academy.appspot.com` |
| `VITE_FIREBASE_MESSAGING_SENDER_ID` | `<…>` |
| `VITE_FIREBASE_APP_ID` | `1:…:web:…` |

> ⚠️ **Cambio en VITE_*** ⇒ requiere **rebuild**, no solo redeploy. Dispara un build manual en Coolify después de actualizarlas.

### 4.3 `postgres` y `redis`

Coolify gestiona credenciales. Anota:

- Postgres host interno (algo como `postgres-xxxx` o el nombre que le pongas)
- Postgres user/password/db
- Redis host interno

Y úsalos para construir `DATABASE_URL` y `REDIS_URL` arriba.

---

## 5 · Primer deploy

### 5.1 Push del hardening al repo

```bash
git add backend/Dockerfile frontend/Dockerfile deploy/
git commit -m "chore(deploy): prod Dockerfiles + entrypoints + Caddyfile"
git push origin main      # ← push DIRECTO. Coolify dispara desde aquí.
```

### 5.2 Orden de despliegue en Coolify

Importante por dependencias:

1. **`postgres`** → Deploy. Espera healthy.
2. **`redis`** → Deploy. Espera running.
3. **`api`** → Deploy. El entrypoint corre `alembic upgrade head` antes de gunicorn. Si la migración falla, el log lo dirá y el contenedor reiniciará — **eso es bueno** (no queremos schema viejo silencioso).
4. **`worker`** → Deploy. No toca DB schema, solo encola/desencola.
5. **`frontend`** → Deploy. Caddy sirve el `dist`.

### 5.3 Validación post-deploy

```bash
# 1. Health backend (vía Coolify → terminal del servicio api)
curl -fsS http://127.0.0.1:8000/health
# → {"status":"ok","env":"production"}

# 2. DB schema al día
alembic current
# → debe coincidir con el último versions/<hash>

# 3. Worker conectado
# Logs del servicio worker deben mostrar:
#   [tasks] . app.modules.applications.tasks.notify_submitted
#   [tasks] . app.modules.notifications.tasks.send_email_task
#   ...
#   celery@... ready.

# 4. Frontend sirve assets
curl -I http://127.0.0.1/
# → 200 OK, content-type: text/html
```

### 5.4 Crear primer admin

```bash
# Opción A: vía Firebase + promoción manual en DB
# 1. En Firebase console → Authentication → Users → Add user (email + password temporal)
# 2. El user logea una vez al frontend → backend lo provisiona como `student` por default
# 3. Promover a admin desde la terminal del servicio api:
python -c "
from app.core.database import SessionLocal
from app.modules.users.models import User
db = SessionLocal()
u = db.query(User).filter_by(email='cesar@siete.com').first()
u.role = 'admin'
db.commit()
print('promoted:', u.email, '→', u.role)
"

# Opción B: setear el custom claim en Firebase para que llegue como admin desde el primer login
python -c "
import firebase_admin
from firebase_admin import auth, credentials
import json, os
firebase_admin.initialize_app(credentials.Certificate(json.loads(os.environ['FIREBASE_CREDENTIALS_JSON'])))
auth.set_custom_user_claims('<firebase-uid>', {'role': 'admin'})
"
```

> No corras `python -m app.scripts.seed` en producción — borra y recrea data demo. Es solo para dev.

---

## 6 · Routing público: `siete.com/academy/*`

El frontend Webflow sigue sirviendo `siete.com`. Hay que enrutar dos paths a Coolify:

- `siete.com/academy/*` → frontend Coolify
- `siete.com/api/academy/*` → backend Coolify

### 6.1 Recomendado: Cloudflare Worker (path-based)

1. Cloudflare → DNS de `siete.com` (debe estar bajo Cloudflare, naranja la nube).
2. Crear hostnames internos en Coolify: el panel asigna automáticamente o configuras `app-academy.siete-coolify.com` (frontend) y `api-academy.siete-coolify.com` (api). Activa Let's Encrypt en cada uno.
3. Cloudflare → Workers & Pages → Create Worker:

```js
export default {
  async fetch(request) {
    const url = new URL(request.url);
    const isApi = url.pathname.startsWith("/api/academy");
    const isApp = url.pathname.startsWith("/academy");

    if (!isApi && !isApp) {
      // todo lo demás (incl. /) sigue yendo a Webflow
      return fetch(request);
    }

    const target = isApi
      ? "https://api-academy.siete-coolify.com"
      : "https://app-academy.siete-coolify.com";

    // strip /academy del path para el frontend (Caddy sirve / como root)
    const upstreamPath = isApp
      ? (url.pathname.replace(/^\/academy/, "") || "/")
      : url.pathname; // /api/academy/... lo deja igual; FastAPI usa root_path

    const upstream = new URL(upstreamPath + url.search, target);
    const init = {
      method: request.method,
      headers: request.headers,
      body: ["GET", "HEAD"].includes(request.method) ? undefined : request.body,
      redirect: "manual",
    };
    return fetch(upstream.toString(), init);
  },
};
```

4. Worker → Routes → Add Route → `siete.com/*` → este worker.

> **Importante para FastAPI:** el backend usa `root_path="/api/academy"` cuando `APP_ENV != development` (`backend/app/main.py:31`). El Worker pasa la URL **completa** sin strip — FastAPI ya sabe que su prefix es `/api/academy/`.

### 6.2 Alternativa más simple: subdominio

Si Cloudflare Worker te complica:

- DNS `app.siete.com` → IP Hetzner / Coolify (frontend)
- DNS `api.siete.com` → IP Hetzner / Coolify (api)
- Cambia `VITE_API_BASE_URL=https://api.siete.com`
- Cambia `root_path` del backend (en `main.py`) o eliminalo si vas a `api.siete.com/`
- Actualiza `ALLOWED_ORIGINS=https://app.siete.com`

Esto evita el Worker pero rompe la URL "siete.com/academy" del cliente. Decisión de marca.

### 6.3 Link en Webflow

Designer → Navbar → agregar item:
- Label: `Academy`
- Link: `/academy`
- Publish.

---

## 7 · Healthchecks y observabilidad

### 7.1 Coolify health

Coolify ya hace HTTP healthcheck por defecto. Configura por servicio:

| Servicio | Path | Expected |
|---|---|---|
| `api` | `/health` | `200` con `{"status":"ok"}` |
| `frontend` | `/` | `200` con HTML |
| `worker` | (sin HTTP) usa `tcp` o `process` check | proceso `celery` vivo |

### 7.2 Uptime externo

UptimeRobot (gratis):

- `https://siete.com/api/academy/health` → cada 5 min
- `https://siete.com/academy/` → cada 5 min
- Alerta por email si 2 checks consecutivos fallan.

### 7.3 Logs

- Coolify rota logs automáticamente. Para retención larga, conecta Loki o Datadog vía Docker logging driver.
- Backend ya emite **JSON estructurado** con `rid=<16-chars>`. Cualquier agregador parsea sin config extra.
- Para correlacionar un bug reportado por usuario: pídele el `rid` que el frontend imprime → busca en logs `api`.

### 7.4 Errores

Sentry (opcional pero recomendado en piloto):

- Backend: `pip install sentry-sdk[fastapi]` + `sentry_sdk.init(...)` en `app/main.py`.
- Frontend: `npm i @sentry/react` + init en `main.tsx` con `VITE_SENTRY_DSN`.

---

## 8 · Migraciones, backups y rollback

### 8.1 Migraciones futuras

1. En dev local: cambias modelos → `alembic revision --autogenerate -m "agrega columna X"` → revisas el archivo en `backend/alembic/versions/`.
2. Commit + push. Coolify rebuilds `api`.
3. Entrypoint corre `alembic upgrade head` antes de servir → si falla, **el contenedor crashea** (deliberado).
4. Si crashea: revisa logs Coolify → corrige migración → push otra vez.

### 8.2 Backup de Postgres

Coolify → servicio `postgres` → tab Backups → habilitar backup diario a S3 (o local + descarga manual semanal).

Manual antes de migración riesgosa:

```bash
# desde la terminal del servicio postgres en Coolify
pg_dump -U siete siete_academy > /tmp/backup-$(date +%Y%m%d).sql
# luego scp al host externo
```

### 8.3 Rollback

Coolify guarda los últimos N deploys. Para revertir:

1. Servicio `api` → Deployments → seleccionar deploy anterior → "Redeploy".
2. **Si la migración nueva ya cambió schema**, hay que `alembic downgrade -1` antes:
   ```bash
   # terminal del servicio api (en el deploy nuevo, antes de revertir)
   alembic downgrade -1
   ```
3. Después redespliega la versión anterior.

> Mantén la regla: **una migración por commit**. Hace los rollbacks puntuales.

---

## 9 · Seguridad mínima

| Check | Cómo |
|---|---|
| `DEV_AUTH_BYPASS=false` en prod | El código rechaza el header `X-Dev-User` igual si `APP_ENV != development`, pero es defensa en profundidad |
| HTTPS en todos los hostnames | Coolify activa Let's Encrypt automático |
| Headers de seguridad | Caddyfile (§ 2.3) ya los añade |
| Secretos sin commitear | `.env` está en `.gitignore`. Confirma `git ls-files .env` vacío |
| Rate limit sano | `POST /applications` 5/h/IP; `/certificates/verify` 30/min/IP (ya en código) |
| Firebase con Authorized domains | Solo `siete.com` y dominios staging |
| Postgres no expuesto público | Coolify no abre el puerto 5432 al mundo por default; verifica |

---

## 10 · Smoke test post-deploy (15 min, hacerlo siempre)

```
[ ] curl https://siete.com/academy/                  → 200 (HTML)
[ ] curl https://siete.com/api/academy/health        → 200 {"status":"ok","env":"production"}
[ ] Abrir https://siete.com/academy/login            → ves botón "Continuar con Google"
[ ] Login con cuenta admin real                      → cae en /admin
[ ] /admin/applications carga                        → DB conectada
[ ] /admin/cohorts crear cohorte de prueba           → INSERT funciona
[ ] /apply (incógnito) enviar postulación dummy      → llegó email de acuse (Resend dashboard)
[ ] Logs de `worker` muestran que la task corrió     → Celery + Redis OK
[ ] Si pusiste ANTHROPIC_API_KEY: en logs `worker` ves `ai.score_completed` para esa app
[ ] /verify/<código-falso>                           → 404 (rate limit no se activa con 1 hit)
[ ] Cambiar idioma a EN/PT en el header              → toda la UI reacciona
```

Si alguno falla, **no abras el flujo a usuarios reales** — corrige primero.

---

## 11 · Checklist final del go-live

```
[ ] Pitfalls leídos (§ 0). Workflow de push directo entendido.
[ ] Dockerfiles prod commiteados (§ 2). entrypoint-api.sh ejecutable.
[ ] gunicorn agregado a requirements.txt.
[ ] Repo en GitHub privado, Coolify GitHub App instalada.
[ ] 5 servicios Coolify creados y configurados.
[ ] Variables de entorno completas en api/worker/frontend.
[ ] postgres con volumen persistente + backup diario activo.
[ ] alembic upgrade head corrió limpio en primer deploy.
[ ] Primer usuario admin promovido (vía DB o custom claim Firebase).
[ ] DNS + Cloudflare Worker activos. siete.com/academy responde.
[ ] Link "Academy" agregado a navbar Webflow.
[ ] Smoke test § 10 pasó completo.
[ ] UptimeRobot monitoreando /health.
[ ] (Opcional) Sentry capturando errores.
[ ] Plantilla de email de invitación lista.
[ ] Plan de monitoreo durante primeras 48h: tú revisas Coolify logs cada 4 h.
```

---

## 12 · Troubleshooting rápido

| Síntoma | Diagnóstico | Fix |
|---|---|---|
| `api` reinicia en loop | Log dice `alembic.util.exc.CommandError` | Migración rota. Arregla y push directo a `main` |
| 500s con `column does not exist` | Migración se "saltó" | Confirma logs del último deploy. Verifica que entrypoint **NO** tenga `\|\| echo` (§ 0.2) |
| Login funciona pero `GET /auth/me` da 401 | Token Firebase no se valida | Revisa `FIREBASE_CREDENTIALS_JSON` (debe ser JSON válido en una línea) y `FIREBASE_PROJECT_ID` |
| 403 al hacer cualquier cosa de admin | Tu user no tiene `role=admin` | Promueve en DB (§ 5.4) o setea custom claim |
| Email nunca llega | `SMTP_HOST` vacío → stub silencioso | Setea SMTP_*. Logs backend deben mostrar `email.sent` no `email.stubbed` |
| Drafts Claude no se generan | `ANTHROPIC_API_KEY` vacío | Setear; pipeline degrada silenciosamente cuando falta — es feature, no bug |
| CORS error desde `siete.com` | `ALLOWED_ORIGINS` no incluye el origin | Añadir y redeploy api |
| Rebuild no toma el cambio de `VITE_*` | Vite las inlinea en build | Forzar rebuild manual en Coolify |
| Cambio mergeado por PR no desplegó | § 0.1 — Coolify ignora merges UI | `git push origin main` directo o redeploy manual |
| Worker no toma tasks | Redis URL mal o `CELERY_ALWAYS_EAGER=true` | Verifica `REDIS_URL` y que la flag esté `false` en worker |

---

## 13 · Lo que conviene hacer **después** del go-live

- Sentry SDK ya activo y triando errores diarios.
- Backups Postgres testeados (restaurar en staging).
- CI con GitHub Actions: `make test` antes de cualquier merge a `main`.
- Métrica de costo Anthropic: query semanal sobre `ai_call_logs` (`SUM(duration_ms)`, `COUNT`).
- Plan de rotación de secretos (Firebase service account, Anthropic key) cada 90 días.
- Documentar el handoff operativo al equipo de Comercial (quién aprueba aplicaciones, quién califica, SLA de respuesta).

---

**Cuando estés listo para ejecutar este runbook**, empieza por la § 0 (pitfalls) y la § 2 (hardening de Dockerfiles). Lo demás es seguir el orden y validar cada paso con su entregable.
