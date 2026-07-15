# Descarga de b-roll (Pexels) para los videos del curso

Workflow para conseguir el video stock (b-roll) que rellena los bloques de contenido
de cada video del curso, sin tocar el presupuesto de HeyGen.

> **Por qué Pexels y no el b-roll de HeyGen.** La API de Pexels es **gratis** y la
> licencia permite **uso comercial sin atribución**. El b-roll de HeyGen, en cambio,
> consume créditos del wallet (solo 1 gratis). Componiendo con Pexels + ffmpeg, HeyGen
> queda únicamente para el avatar (~$4/min sobre el ~45% del tiempo). Ver
> `guiones_videos/v2/_INSTRUCCIONES_PRODUCCION_VIDEO.md` (formato "presentador por tramos").

## Inputs

- `PEXELS_API_KEY` en `.env` (ya está). Gratis: 200 req/hora, 20.000/mes.
- Un **plan** JSON con los temas a buscar: lista de `{slug, query, count, ...}`.
  Ejemplo: `tools/broll_plan_m1.json` (Módulo 1).

## Herramienta

`tools/pexels_fetch.py` — busca, filtra y baja. Es determinista; lo editorial (qué
buscar) va en el plan, no en el tool.

- Filtra a **landscape (16:9), ≥1920×1080, duración 4–30s** (cutaways).
- **Verifica la resolución REAL con ffprobe**: Pexels a veces sirve 720p bajo una URL
  llamada "...1080..."; el tool detecta eso y sube al archivo más grande (UHD) hasta
  conseguir ≥1080p de verdad.
- Lleva `.tmp/broll/_manifest.json` (id, query, autor, url) → **no re-baja** lo ya
  bajado y deja registro de fuentes.

## Paso a paso

1. **Armar el plan** del módulo (uno por módulo). Queries en **inglés** (rinden mucho
   más en Pexels). 2–3 clips por tema alcanzan; el b-roll se reutiliza entre videos.
   Temas típicos: reunión/comité, equipo, llamada (SDR), datos en pantalla, oficina,
   acuerdo/handshake, persona pensando, teclado/outbound.

2. **Dry-run** (no baja nada, confirma que cada query trae suficientes resultados):
   ```
   python tools/pexels_fetch.py --plan tools/broll_plan_mX.json --dry-run
   ```
   Si algún tema dice "solo N/objetivo", afinar la query o subir `max_duration`.

3. **Descargar**:
   ```
   python tools/pexels_fetch.py --plan tools/broll_plan_mX.json
   ```
   Salida en `.tmp/broll/<slug>/<id>.mp4`. Un clip suelto: `--query "..." --slug nombre --count 3`.

4. **Revisar** los clips a ojo (carpeta `.tmp/broll/`) y descartar los que no peguen con
   el tono (oficina moderna, limpio, gente real). Borrar un .mp4 no rompe el manifest.

## Notas / aprendizajes

- **Resolución real ≠ metadata** en Pexels (clips viejos). Por eso el tool verifica con
  ffprobe; nunca confiar solo en el nombre del archivo.
- `.tmp/broll/` es desechable (regenerable desde el plan + manifest). No commitear.
- La licencia Pexels no exige crédito en los videos; el manifest guarda el autor igual,
  por las dudas y para no repetir clips entre módulos.
