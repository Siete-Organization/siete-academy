# Instrucciones de producción de video — Siete Academy

> **Qué es esto.** El estándar único para armar **todos los videos del curso** en HeyGen
> Studio, semana a semana. Si seguís este documento, los 12 videos del piloto (4 semanas ×
> 3 videos) salen con el **mismo formato, la misma identidad visual, subtítulos legibles, el
> avatar lo más humano posible y un ambiente académico, limpio y profesional**.
>
> Léelo una vez completo. Después usá el **Checklist de salida** (al final) para cada video.
>
> Fuente de marca: `tools/brand/` (Brandbook_Siete.pdf, fuentes, logos) + `tools/brand/guia_brand.css`.
> Config técnica de HeyGen: `tools/heygen_defaults.json`.

---

## 0. Principio rector

**Académico pero relajado. Limpio pero con marca. Formal sin ser acartonado.**

Siete es una empresa de identidad relajada: cercana, directa, que tutea al alumno. Pero esto
es **un curso que se paga y que certifica**, así que la factura visual tiene que sentirse
profesional. La regla para resolver cualquier duda de diseño:

> Si un detalle distrae del mensaje o "se ve a IA barata", se quita. Si aporta claridad y se
> ve cuidado, se queda. **Menos elementos, mejor ejecutados.**

---

## 1. Formato unificado de video

Cada **semana** tiene 3 videos, siempre en el mismo orden y con la misma anatomía. No se
cambia la estructura entre semanas: lo único que cambia es el contenido.

| Video | Archivo fuente | Duración objetivo | Rol |
| --- | --- | --- | --- |
| **Intro** | `semXX/intro.md` | 2:30 – 3:30 | Mapa de la semana: qué vas a poder hacer + cómo usar el material |
| **Contenido 1** | `semXX/contenido_1.md` | 7:30 – 8:30 | Primera mitad de bloques + 1 ejercicio resuelto en vivo |
| **Contenido 2** | `semXX/contenido_2.md` | 8:00 – 9:30 | Segunda mitad + 1 ejercicio en vivo + síntesis + puente a la semana siguiente |

### 1.1 Anatomía interna (la misma en las 4 semanas)

Los `.md` ya traen los segmentos marcados. Respetá este orden en pantalla:

1. **Gancho (~15-20s):** una sola idea fuerte. Es el único lugar donde se permite **un dato
   numérico de impacto** (ej. "en más de un tercio de los casos no compran nada"). El resto
   del video va sin estadísticas duras.
2. **Contexto / puente (~30s):** qué cubre el video.
3. **Bloques de contenido:** cada concepto con su `[SLIDE: ...]`.
4. **Ejercicio en vivo** (solo en Contenido 1 y 2): caso → pregunta → pausa → respuesta.
5. **Síntesis** (solo en Contenido 2): recap numerado.
6. **Puente a la guía** ("Complementa este contenido con las guías adjuntas…") y **puente
   al siguiente video / semana**.

### 1.2 De dónde sacar el texto a pegar

- El **`.md`** es la fuente con marcas `[SLIDE:]`, frontmatter y bibliografía.
- El **`_studio_kit_sXX.md`** (uno por semana) trae el **texto narrado limpio**, ya sin
  marcas ni markdown, listo para pegar en el script del avatar.
- La sección **"Fuentes de este video"** del `.md` **NO se narra**: va a la pestaña de
  Bibliografía en la plataforma.

> **Si una semana no tiene `_studio_kit`,** generalo antes de grabar: copiá solo el texto
> hablado de cada `.md` (sin `[SLIDE:]`, sin títulos, sin frontmatter, sin "Fuentes"),
> respetando que cada ítem enumerado ("Uno…", "Dos…") quede en su propio párrafo.

### 1.3 Ritmo de narración

- **Pausa de ~0.5s entre ítems enumerados** ("Uno… [pause] Dos… [pause]"). Usá el botón
  **Pause** de Studio. Hoy el conteo se acelera y se pierde.
- **Pausa de ~1s** antes de revelar la respuesta de cada ejercicio ("*[Pausa breve]*" en el
  guion).
- Velocidad de voz: **1.0** (la default). No acelerar para "que entre en X minutos".

### 1.4 Pronunciación de siglas (Brand Glossary)

Activá el Brand Glossary **"Video Agent Pronunciation"** (id `0e3e834da76f4f988fac667e40fcbbaf`,
parámetro `brand_voice_id` en la API). Afecta **solo el audio**, no los subtítulos:

| Sigla | Se pronuncia |
| --- | --- |
| B2B | "bi tu bi" (no "bi dos be") |
| B2C | "bi tu ci" |
| SDR | "es di ar" |
| LOB | "el ou bi" (no "lob") |
| AE | "ei i" |
| MQL / SQL | "eme cu ele" / "ese cu ele" |
| ICP | "i ci pi" |
| CRM | "ci ar eme" |

> Si aparece una sigla nueva en una semana, agregala al glosario antes de renderizar.

---

## 2. Identidad de marca en pantalla

### 2.1 Paleta (única, sin colores fuera de esta lista)

| Uso | Color | HEX |
| --- | --- | --- |
| Fondo principal | Blanco | `#FFFFFF` |
| Texto / títulos | Negro | `#000000` |
| Texto cuerpo (casi negro) | Tinta | `#0A0A0A` |
| **Acento primario** | System Blue | `#007AFF` |
| **Acento secundario / fondos suaves** | Glacial Sky | `#8FBDFF` |
| Fondo suave de slide | Glacial bg | `#EEF5FF` |
| Texto secundario / notas | Gris suave | `#5B6470` |
| Divisores sutiles | Línea | `#E3E8EF` |

**Regla:** fondo blanco o glacial muy claro, texto negro, **un solo** acento azul por slide
para resaltar lo importante. Nada de degradados llamativos, sombras duras ni colores ajenos
a la paleta.

### 2.2 Tipografía

- **Montserrat** en todo (está en `tools/brand/fonts/`). Subila como fuente custom en Studio
  si HeyGen lo permite; si no, elegí la más cercana (Montserrat / Poppins / Inter).
- Pesos: **Black/Bold** para títulos de slide, **Medium/Regular** para el cuerpo.
- Jerarquía por slide: **1 título** (grande, negro) + **2-4 bullets** máximo (cuerpo). Nunca
  un párrafo largo en pantalla.

### 2.3 Logo

- Usar los assets de `tools/brand/assets/` y `tools/brand/logos siete/`.
- Logo **discreto**, esquina superior o inferior, tamaño chico (~26px de alto equivalente).
  `logo-black.png` sobre fondo claro; `logo-white.png` solo si el fondo es oscuro.
- No animar el logo. No ponerlo encima del avatar.

### 2.4 Slides: criterios de diseño

- **Fondo:** blanco o `#EEF5FF`. Consistente en todo el video.
- **Acento de barra:** una línea/barra `#007AFF` corta bajo el título (igual que las guías PDF).
- **Iconos:** estilo lineal simple, monocromo (negro o azul), **todos del mismo set**. Si un
  concepto tiene N elementos (las 5 etapas, los roles), **mostrar los N completos** —no
  algunos— y **sin que se corten** (ver §5, regla de safe zone).
- **Tablas/comparaciones:** encabezado negro con texto blanco, filas alternadas con `#EEF5FF`
  (mismo lenguaje que las guías).
- **Una idea por slide.** Si un bloque tiene mucho, dividilo en 2 slides.

---

## 3. Avatar lo más real y humano posible

> El detalle de avatar + reglas de gráficos sobre pantalla vive en su propio documento,
> **`_INSTRUCCIONES_IA_HEYGEN.md`** (bloque único, pegable en la IA de HeyGen para cada video).
> Acá va el resumen.

- **El avatar es Nico, nuestro CEO** — su **rostro y su voz**, recreados con **Seedance 2.0**.
  Ya **no** se usa "Liam" ni avatares de stock. El **mismo asset de Nico en los 12 videos**
  (misma persona, mismo set, misma ropa/encuadre): consistencia total.
- **Voz:** la voz de Nico (clonada), español neutro LATAM, cálida, velocidad 1.0. Si todavía
  no está la clonada, usar una voz ES LATAM masculina cálida como provisional — **nunca**
  inglés ni acento marcado. (El viejo `voice_id` "Warm Tutor (MX)" de `heygen_defaults.json`
  figuraba con `language: English`: ese es el bug que motivó el mal acento — no reutilizarlo.)
- **Movimiento natural:** gestos/expresividad **media** (no la máxima: exagera y se ve falso).
  Parpadeo y manos relajadas, sin loops. Mirada a cámara.
- **Encuadre:** plano medio (de pecho hacia arriba), avatar **descentrado a un lado** dejando
  espacio para la slide al otro lado (layout presentador + contenido).
- **Nada se atraviesa por delante del avatar.** Ningún objeto, ícono, texto o animación cruza
  sobre su cuerpo o su cara — los gráficos van en su zona, separados. (Regla de oro del doc de
  IA de HeyGen; cero excepciones.)

> Realismo ≠ recargado. Un avatar sobrio, bien iluminado, con gesto moderado y voz cálida en
> español se ve mucho más humano que uno con gestos al máximo y efectos encima.

---

## 4. Ambiente: académico, limpio, profesional (y relajado)

El "set" donde vive el avatar y las slides debe transmitir aula moderna, no oficina corporativa
fría ni fondo de stock genérico.

- **Fondo del avatar:** liso o con **profundidad muy sutil** (un estudio claro desenfocado, o
  un color sólido de la paleta). Preferencia: blanco/gris muy claro o `#EEF5FF`. Evitá fondos
  con logos ajenos, plantas de stock o gradientes saturados.
- **Coherencia presentador + slide:** el mismo fondo y paleta en avatar y slides, para que se
  sienta **un solo espacio**, no dos capas pegadas.
- **Iluminación:** cálida y pareja, sin sombras duras. Sensación de "bien grabado".
- **Tono relajado pero formal:** lenguaje cercano (tutea, "vamos al contenido", "prestaste
  atención"), pero composición ordenada, tipografía cuidada y cero elementos chillones. Es la
  identidad de Siete: cercanía con factura prolija.
- **Transiciones:** cortes simples o fundidos suaves entre slides. Nada de transiciones 3D,
  giros ni zooms bruscos.

---

## 5. Subtítulos legibles en todos los slides y videos

Los subtítulos van **siempre activados** (accesibilidad + se consume mucho en silencio).

- **Fuente:** Montserrat (o la sans más cercana), **peso Medium/Semibold**.
- **Tamaño:** grande, legible en móvil. ~**4-5% del alto del cuadro** (≈ 44-52 px en 1080p).
- **Color:** texto **blanco `#FFFFFF`** con **caja/banda semitransparente negra** detrás
  (opacidad ~70%), **o** texto blanco con borde/sombra marcada. Nunca texto sin contraste
  sobre la slide.
- **Posición:** **banda inferior centrada**, dentro de la **safe zone** (margen del ~5-7% en
  los 4 bordes). Que **no pise** el logo, ni los bullets de la slide, ni se corte abajo.
- **Longitud:** **máximo 2 líneas**, ~**40 caracteres por línea**. Frases cortas, sincronizadas
  con el habla (no bloques largos que adelanten al narrador).
- **Consistencia:** misma posición, tamaño y estilo en **los 3 videos de las 4 semanas**.
- **Sin solापmiento:** revisá que en los slides con iconos/tablas los subtítulos no tapen
  contenido. Si chocan, subí ligeramente la banda o bajá el contenido del slide, no achiques
  el subtítulo.

> Regla de oro de legibilidad: si tenés que entrecerrar los ojos para leerlo en el celular,
> está mal. Más grande, más contraste, menos texto por pantalla.

---

## 6. Proceso por semana (repetible)

Para cada `semXX`:

1. Abrí `semXX/_studio_kit_sXX.md` (o generalo desde los `.md`, §1.2).
2. Creá el proyecto en Studio con el **mismo template/escena base** que las demás semanas
   (avatar, fondo, layout, estilo de slide y subtítulos idénticos).
3. Activá el **Brand Glossary** de pronunciación (§1.4).
4. Pegá el texto de cada video; insertá las **pausas** (§1.3).
5. Armá las slides siguiendo los `[SLIDE: ...]` del `.md`, con la **paleta y tipografía** de §2.
6. Confirmá **avatar humano** (§3), **ambiente** (§4) y **subtítulos** (§5).
7. Pasá el **Checklist de salida** antes de renderizar.
8. Render en **1920×1080** (16:9).

---

## 7. Checklist de salida (por cada video, antes de renderizar)

**Formato**
- [ ] Estructura correcta: gancho → contexto → bloques → (ejercicio) → (síntesis) → puentes.
- [ ] Duración dentro del rango del tipo de video (§1).
- [ ] Texto pegado = `_studio_kit` (sin marcas, sin "Fuentes" narradas).
- [ ] Pausas entre ítems enumerados y antes de cada respuesta de ejercicio.

**Marca**
- [ ] Solo colores de la paleta (§2.1); fondo blanco/glacial; un acento azul por slide.
- [ ] Montserrat; 1 título + máx. 2-4 bullets por slide.
- [ ] Logo discreto, sin animar, fuera del avatar.
- [ ] Iconos completos (los N elementos), mismo set, **sin cortarse**.

**Avatar y ambiente**
- [ ] Avatar lo más realista disponible; gesto moderado; mirada a cámara.
- [ ] **Sin overlays/animaciones encima del avatar.**
- [ ] Voz en **español LATAM** (no inglés), cálida, velocidad 1.0.
- [ ] Fondo limpio y coherente entre avatar y slides; iluminación pareja.

**Subtítulos**
- [ ] Activados, blancos con caja/sombra, grandes (≈44-52px @1080p).
- [ ] Banda inferior en safe zone; máx. 2 líneas / ~40 car. por línea.
- [ ] No tapan logo, bullets ni iconos; misma posición en todos los videos.

**Pronunciación**
- [ ] Brand Glossary activo: B2B, B2C, SDR, LOB, AE, MQL/SQL, ICP, CRM suenan bien.

**Salida**
- [ ] Render 1920×1080, 16:9.
- [ ] Revisión final en móvil (legibilidad de subtítulos y slides).

---

## 8. Errores ya detectados a no repetir (del feedback del líder, Módulo 1)

- Buying cycle / lifecycle mostrados con **iconos faltantes** → mostrar siempre los **5 completos**.
- **Iconos cortados** cerca del min 1:00 → respetar safe zone (§5).
- **"Cuadritos" raros** (~seg 18 de la intro) → quitar esa animación del template.
- **Animaciones encima del avatar** → eliminadas (§3, §7).
- Slide del **"customer lifecycle de Siete" de ~14 etapas** y el encuadre "cómo te ven a ti"
  → **no deben aparecer**. El ciclo de vida del prospecto es **Prospect → MQL → SQL →
  Opportunity → Customer** y termina en Customer (lo posterior a la firma es Atención al Cliente).
