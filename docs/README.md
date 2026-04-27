# Documentación funcional — Siete Academy

Tres documentos pensados para entender el proyecto de punta a punta sin tener que leer todo el código.

| Documento | Para quién | Qué contiene |
|---|---|---|
| [`MANUAL.md`](MANUAL.md) | equipo operativo + negocio | Proceso, usabilidad, recorridos paso a paso por rol, glosario. |
| [`FLUJOGRAMAS.md`](FLUJOGRAMAS.md) | todos | 14 diagramas Mermaid: arquitectura, ER, secuencias por rol, state machines, navegación. |
| [`ARQUITECTURA.md`](ARQUITECTURA.md) | equipo técnico | Stack, módulos backend, modelo de datos, endpoints, decisiones de diseño, deploy, puntos de extensión. |
| [`DEPLOY_COOLIFY.md`](DEPLOY_COOLIFY.md) | DevOps / responsable de deploy | Runbook end-to-end Coolify: Dockerfiles prod, entrypoints, env vars, routing Cloudflare, healthchecks, troubleshooting. |

Documentos hermanos en la raíz del repo:

- [`HANDOFF.md`](../HANDOFF.md) — mapa para el equipo que recibe el proyecto.
- [`RUNBOOK_LOCAL.md`](../RUNBOOK_LOCAL.md) — cómo correr la demo en local (`make demo`).
- [`POST_FEEDBACK.md`](../POST_FEEDBACK.md) — plan de fases A → B → C.
- [`NEXT_STEPS_PROD.md`](../NEXT_STEPS_PROD.md) — runbook con comandos para Fase B (infra prod).
- [`CHANGELOG_FASE_A.md`](../CHANGELOG_FASE_A.md) — histórico de cambios post-feedback del cliente.

> **Tip:** los flujogramas se renderizan automáticamente en GitHub/GitLab y en VS Code con la extensión "Markdown Preview Mermaid Support". Si necesitas editarlos visualmente, pega el bloque en <https://mermaid.live>.
