# Instrucciones para la IA de HeyGen — bloque único para TODOS los videos

> **Para qué sirve.** Este es el **prompt maestro** que se le pega a la IA de HeyGen (o se
> sigue a mano en Studio) **en cada uno de los videos del curso**, sin cambiarlo. El objetivo
> es que los **12 videos del piloto** (y los que vengan) salgan **visualmente idénticos**:
> mismo avatar, mismo encuadre, mismas reglas de gráficos, mismos subtítulos, mismo ritmo.
>
> Lo único que cambia de un video a otro es **(a) el texto narrado** (del
> `_studio_kit_sXX.md` de cada semana) y **(b) el contenido de las slides** (los `[SLIDE: …]`
> del guion). **Todo lo demás es fijo.**
>
> Acompaña a `_INSTRUCCIONES_PRODUCCION_VIDEO.md` (el estándar general). Si algo choca, manda
> este documento para lo relativo al **avatar y a los gráficos sobre pantalla**.

---

## 0. El avatar: Nico (CEO)

- **El avatar es Nico ** Se usa su **rostro y su voz** como base.
- El avatar se **recrea con Seedance 2.0** (a partir del material de referencia de Nico:
  rostro y muestra de voz). **Ya no se usa "Liam"** ni ningún avatar de stock.
- **El mismo asset de avatar de Nico se usa en los 12 videos.** No se cambia de avatar, de
  peinado, de ropa ni de encuadre entre videos. Consistencia total: tiene que parecer la
  misma persona, en el mismo set, grabada el mismo día.
- **Voz:** la voz de Nico (clonada). Español neutro LATAM, tono cálido y cercano, velocidad
  normal (1.0). Si la voz clonada todavía no está lista, usar una voz ES LATAM masculina,
  cálida, como provisional — **nunca** una voz en inglés ni con acento marcado.
- Realismo: gesto **natural y moderado** (parpadeo, micro-movimientos, manos relajadas).
  Ni rígido ni sobreactuado. Mirada a cámara.

---

## 1. LA REGLA DE ORO: nada se atraviesa por delante del avatar

**Ningún objeto, gráfico, ícono, texto, animación ni transición puede pasar POR DELANTE del
avatar ni cruzar sobre su cuerpo o su cara. Nunca. En ningún video.**

- Los gráficos viven en **su propia zona**, al lado del avatar (layout presentador + panel de
  contenido). El avatar ocupa un lado del cuadro; las slides/íconos, el otro. **No se
  superponen.**
- Nada de elementos que "vuelan" entrando o saliendo por encima del avatar, ni lower-thirds
  que le tapen el torso, ni partículas/figuras animadas sobre él.
- Las transiciones entre slides ocurren **en la zona de contenido**, no sobre el avatar.
- El **logo** va en una esquina, chico y fijo — **no** sobre el avatar.
- Los **subtítulos** van en la banda inferior, en su zona segura — **no** sobre la cara ni el
  cuerpo del avatar (ver §4).

> Si una plantilla de HeyGen trae animaciones que cruzan al presentador, **se desactivan**.
> Antes esto se marcó como el principal defecto ("queda raro, se ve a IA"). Cero excepciones.

---

## 2. Lo que es FIJO en todos los videos (no se toca entre videos)

- **Avatar:** Nico, mismo asset, mismo encuadre (plano medio, de pecho hacia arriba),
  **descentrado a un lado** dejando libre el otro lado para el contenido.
- **Fondo:** estudio claro y limpio, liso o con profundidad muy sutil. Blanco / gris muy claro
  / `#EEF5FF`. El **mismo fondo en los 12 videos**. Sin fondos de stock, sin plantas, sin
  logos ajenos, sin gradientes saturados.
- **Paleta:** Negro `#000000`, Blanco `#FFFFFF`, Glacial Sky `#8FBDFF`, System Blue `#007AFF`
  (acento). Un solo acento azul por slide. Nada fuera de esta paleta.
- **Tipografía:** Montserrat (Black/Bold para títulos, Medium/Regular para cuerpo).
- **Estilo de slide:** 1 título + máx. 2-4 bullets, barra de acento azul corta bajo el título,
  íconos lineales monocromos del **mismo set**, tablas con encabezado negro y filas alternadas
  `#EEF5FF`. (Mismo lenguaje visual que las guías PDF de la marca.)
- **Subtítulos:** estilo, tamaño y posición idénticos en todos los videos (§4).
- **Encuadre y resolución:** 1920×1080, 16:9.

## 3. Lo que CAMBIA por video (lo único)

1. **El texto narrado:** copiar del `_studio_kit_sXX.md` de la semana correspondiente (texto ya
   limpio, sin marcas). Cada ítem enumerado ("Uno… Dos…") en su propio párrafo, con **Pause
   ~0.5s** entre ítems y **~1s** antes de revelar la respuesta de cada ejercicio.
2. **El contenido de las slides:** según los `[SLIDE: …]` del guion `.md`. Si un concepto tiene
   N elementos (las 5 etapas, los roles), mostrar **los N completos** y **sin que se corten**
   (respetar la zona segura del §4).

---

## 4. Subtítulos (idénticos en todos los videos)

- **Siempre activados.** Fuente Montserrat (o sans cercana), peso Medium/Semibold.
- **Tamaño grande:** ~4-5% del alto del cuadro (≈ 44-52 px en 1080p). Legible en celular.
- **Contraste:** texto **blanco** sobre **caja/banda negra semitransparente** (~70% opacidad),
  o blanco con borde/sombra marcada.
- **Posición:** banda **inferior centrada**, dentro de la zona segura (margen ~5-7% en los 4
  bordes). **No** pisar avatar, logo, bullets ni íconos.
- **Longitud:** máx. **2 líneas**, ~40 caracteres por línea, sincronizados con el habla.
- **Misma posición y estilo exactos en los 12 videos.**

---

## 5. Pronunciación (Brand Glossary)

Activar el Brand Glossary **"Video Agent Pronunciation"** (id
`0e3e834da76f4f988fac667e40fcbbaf`). Afecta solo el audio, no los subtítulos:
B2B = "bi tu bi" · B2C = "bi tu ci" · SDR = "es di ar" · LOB = "el ou bi" · AE = "ei i" ·
MQL/SQL = "eme cu ele"/"ese cu ele" · ICP = "i ci pi" · CRM = "ci ar eme".
Si aparece una sigla nueva en una semana, agregarla antes de renderizar.

---

## 6. PROMPT MAESTRO — pegar tal cual en la IA de HeyGen (en cada video)

```
Armá este video con estas reglas, que son las mismas para TODOS los videos del curso (tienen que quedar visualmente idénticos):

AVATAR
- Usá el avatar de Nico (nuestro CEO): su rostro y su voz, recreados con Seedance 2.0. Es el mismo avatar en todos los videos.
- Voz en español neutro LATAM, cálida y cercana, velocidad normal. Nunca en inglés ni con acento marcado.
- Gesto natural y moderado, mirada a cámara. Plano medio (de pecho hacia arriba), avatar ubicado a un lado del cuadro.

REGLA INNEGOCIABLE
- NINGÚN objeto, ícono, texto, animación ni transición puede pasar POR DELANTE del avatar ni cruzar sobre su cuerpo o su cara. Los gráficos van SIEMPRE en su propia zona, al lado del avatar, sin superponerse. Si la plantilla trae animaciones que cruzan al presentador, desactivalas.

ESCENA (fija en todos los videos)
- Fondo de estudio claro y limpio (blanco / gris muy claro / #EEF5FF), liso o con profundidad muy sutil. El mismo fondo siempre. Sin fondos de stock ni gradientes saturados.
- Paleta: negro #000000, blanco #FFFFFF, Glacial Sky #8FBDFF y System Blue #007AFF como único acento. Tipografía Montserrat.
- Slides: 1 título + máximo 2-4 bullets, barra de acento azul corta bajo el título, íconos lineales monocromos del mismo set. Si un concepto tiene varios elementos, mostralos TODOS y completos, sin que se corten.
- Logo chico y fijo en una esquina, nunca sobre el avatar.

SUBTÍTULOS (idénticos en todos los videos)
- Siempre activados. Texto blanco grande (legible en celular) sobre banda negra semitransparente, en la franja inferior dentro de la zona segura. Máximo 2 líneas, ~40 caracteres por línea, sincronizados con el habla. No deben tapar al avatar, al logo ni a los gráficos.

RITMO
- Pausá ~0,5 s entre cada ítem cuando el narrador enumera ("Uno… Dos… Tres…").
- Pausá ~1 s antes de revelar la respuesta de cada ejercicio.

PRONUNCIACIÓN
- Activá el Brand Glossary de pronunciación: B2B="bi tu bi", B2C="bi tu ci", SDR="es di ar", LOB="el ou bi", AE="ei i", MQL/SQL, ICP, CRM. Afecta solo el audio, no los subtítulos.

SALIDA
- 1920×1080, 16:9.

El texto a narrar y el contenido de las slides te los paso aparte (son lo único que cambia entre videos).
```

---

## 7. Checklist específico de este documento (por video)

- [ ] Avatar = Nico (Seedance 2.0), mismo asset/encuadre que los demás videos.
- [ ] Voz de Nico (o provisional ES LATAM cálida), **no** inglés.
- [ ] **Cero elementos cruzando por delante del avatar.**
- [ ] Gráficos en su zona, sin superponerse al avatar.
- [ ] Fondo, paleta, tipografía y estilo de slide idénticos a los otros videos.
- [ ] Subtítulos blancos sobre banda, franja inferior, sin tapar nada, mismo estilo siempre.
- [ ] Íconos completos (los N), sin cortarse.
- [ ] Pausas (enumeraciones y respuestas) aplicadas.
- [ ] Brand Glossary de pronunciación activo.
- [ ] Render 1920×1080 y revisión final en celular.
