"""Rich seed for local demo.

Creates enough data so that an admin/teacher/student/recruiter can log in
(via dev bypass) and exercise every screen of the product. Idempotent — safe
to re-run. Reads-first so it only inserts missing rows.

Usage:
    cd backend && .venv/bin/python -m app.scripts.seed
    # or
    make seed
"""

from __future__ import annotations

from datetime import UTC, date, datetime, timedelta

from app.core.database import Base, SessionLocal, engine
from app.core.logging import configure_logging, get_logger
from app.modules.applications.models import Application
from app.modules.applications import models as _apps  # noqa: F401
from app.modules.assessments.models import AIReview, Assessment, Submission, TeacherReview
from app.modules.assessments import models as _assess  # noqa: F401
from app.modules.audit import models as _audit  # noqa: F401
from app.modules.certificates import models as _certs  # noqa: F401
from app.modules.cohorts.models import Cohort, ModuleWindow
from app.modules.cohorts import models as _cohorts  # noqa: F401
from app.modules.courses.models import (
    Course,
    CourseTranslation,
    Lesson,
    LessonTranslation,
    Module,
    ModuleTranslation,
)
from app.modules.courses import models as _courses  # noqa: F401
from app.modules.enrollment.models import Enrollment
from app.modules.enrollment import models as _enroll  # noqa: F401
from app.modules.live_sessions.models import LiveSession
from app.modules.live_sessions import models as _live  # noqa: F401
from app.modules.placement.models import PlacementCandidate, PlacementEvent
from app.modules.placement import models as _place  # noqa: F401
from app.modules.users.models import User
from app.modules.users import models as _users  # noqa: F401

configure_logging()
log = get_logger("seed")


def _ensure_schema() -> None:
    Base.metadata.create_all(engine)


def _upsert(db, model, *, lookup: dict, defaults: dict | None = None):
    instance = db.query(model).filter_by(**lookup).first()
    if instance:
        return instance, False
    data = {**lookup, **(defaults or {})}
    instance = model(**data)
    db.add(instance)
    db.commit()
    db.refresh(instance)
    return instance, True


def seed_users(db) -> dict[str, User]:
    specs = [
        ("admin@siete.com", "Admin Siete", "admin", "seed-admin"),
        ("teacher@siete.com", "Mariana López", "teacher", "seed-teacher"),
        ("student@siete.com", "Luis Carrillo", "student", "seed-student"),
        ("recruiter@siete.com", "HR Cliente", "recruiter", "seed-recruiter"),
        ("camila@example.com", "Camila Reyes", "student", "seed-student-2"),
        ("diego@example.com", "Diego Pereira", "student", "seed-student-3"),
    ]
    created_users: list[User] = []
    for email, name, role, uid in specs:
        u, created = _upsert(
            db,
            User,
            lookup={"email": email},
            defaults={"firebase_uid": uid, "display_name": name, "role": role, "locale": "es"},
        )
        created_users.append(u)
        if created:
            log.info("seed.user", extra={"email": email, "role": role})
    by_email = {u.email: u for u in created_users}
    return {
        "admin": by_email["admin@siete.com"],
        "teacher": by_email["teacher@siete.com"],
        "student": by_email["student@siete.com"],
        "recruiter": by_email["recruiter@siete.com"],
        "camila": by_email["camila@example.com"],
        "diego": by_email["diego@example.com"],
    }


def seed_applications(db) -> None:
    if db.query(Application).count() > 0:
        return

    # Respuestas más realistas (≥100 palabras) — en vez de filler text.
    answer_set_strong_es = {
        "why_sales": (
            "Quiero trabajar en ventas porque es el único rol donde mi resultado depende "
            "directamente de qué tanto entiendo al otro. Soy curiosa por naturaleza, me "
            "obsesiona entender qué hace que una persona diga que sí. Hice prospección a "
            "frío durante tres años en una inmobiliaria de Bogotá y aprendí que un buen "
            "SDR no vende: hace preguntas precisas, escucha más de lo que habla, y toma "
            "la llamada que nadie quiere tomar. Ya perdí la vergüenza al teléfono, pero "
            "me faltan las metodologías y las herramientas para escalar eso en B2B tech. "
            "Siete Academy es el siguiente paso lógico."
        ),
        "achievement": (
            "El último trimestre de 2025 cerré 14 reuniones calificadas en 8 semanas "
            "vendiendo un SaaS de logística que nadie conocía en Colombia. Sin playbook, "
            "sin lista de prospects, sin CRM. Construí una base de 400 leads scrapeando "
            "LinkedIn y cruzando con info pública de empresas. De ahí saqué 14 meetings, "
            "de los cuales 6 se convirtieron en deals. Lo más orgulloso no es el número: "
            "es que documenté cada objeción real que escuché y se volvió el primer "
            "playbook que tuvo el equipo comercial cuando entró el segundo SDR."
        ),
        "hours_per_week": (
            "Puedo dedicar 25 horas a la semana al programa. Actualmente trabajo "
            "part-time en una agencia como community manager (lunes a jueves medio día, "
            "unas 20h/sem) y uso las mañanas temprano y los fines de semana para "
            "estudiar. Ya bloqueé en mi calendario todas las sesiones en vivo de los 8 "
            "módulos. En las semanas con entregas grandes puedo estirar a 30-35h, pero "
            "prefiero comprometerme con 25 de forma sostenida que prometer 40 y no "
            "cumplir. Vivo con mis papás, no tengo hijos, puedo reasignar tiempo."
        ),
    }

    answer_set_medium_es = {
        "why_sales": (
            "Siempre me llamó la atención cómo las grandes compañías generan ingresos "
            "sin que uno los vea trabajar. En los últimos años me di cuenta de que el "
            "motor es el equipo comercial, y específicamente los SDR son los que abren "
            "el embudo. Me gusta conversar con extraños, tengo buena tolerancia a la "
            "frustración, y soy obsesiva con hacer seguimiento. Quiero pasar de mi rol "
            "actual en atención al cliente a algo que pague mejor y que tenga una curva "
            "de crecimiento clara. Ventas B2B es el camino que más me motiva de los "
            "que exploré, por eso estoy aplicando."
        ),
        "achievement": (
            "En mi trabajo actual de atención al cliente ayudé a bajar el tiempo de "
            "respuesta promedio de 4 horas a 40 minutos en un trimestre. Fue un mix "
            "entre ordenar el backlog de tickets, crear macros para los 20 casos más "
            "frecuentes, y entrenar al resto del equipo a categorizar bien los tickets "
            "desde el principio. Mi jefa me dio un bono y me pidió que ayudara a "
            "escribir el proceso para los nuevos ingresos. Lo que más rescato es que "
            "aprendí a medir, no solo a ejecutar. Antes trabajaba duro; ahora trabajo "
            "duro Y llevo métricas."
        ),
        "hours_per_week": (
            "Puedo dedicar entre 15 y 20 horas por semana. Trabajo full-time de lunes a "
            "viernes en un horario fijo (9 a 6) y tengo los fines de semana y las "
            "noches libres. Me comprometo a las sesiones en vivo porque son pocas y ya "
            "hablé con mi pareja para organizar el tiempo. Soy consciente de que 20 "
            "horas es el mínimo que debo dedicarle para aprovechar el programa, no "
            "pienso hacer esto a medias. Si algo no me permite cumplir, aviso antes "
            "con una semana de anticipación, no el mismo día."
        ),
    }

    answer_set_weak_es = {
        "why_sales": (
            "La verdad es que no sé mucho de ventas pero me interesa aprender. Vi a "
            "Siete Academy en LinkedIn y me llamó la atención el programa. Creo que "
            "tengo buena comunicación y no me da miedo hablar con gente nueva. Quiero "
            "tener más ingresos y una carrera que crezca rápido. En mi trabajo actual "
            "ya me aburrí y quiero un cambio. Además siento que las ventas son el "
            "futuro y con la IA todo el mundo dice que es un skill importante. Por eso "
            "estoy aplicando, espero poder entrar al programa y dar lo mejor de mí "
            "durante las semanas que dure el curso y todo lo que sigue después."
        ),
        "achievement": (
            "En mi trabajo anterior me dieron el empleado del mes una vez porque "
            "llegaba temprano y no faltaba. Creo que eso dice mucho de mí como persona. "
            "También en la universidad saqué el tercer lugar en un concurso de "
            "emprendimiento donde presentamos una app de comida saludable. No ganamos "
            "pero nos fue bien para ser la primera vez. Me gusta trabajar en equipo y "
            "soy responsable con los tiempos. Soy bastante estructurado y me gusta "
            "hacer listas de pendientes para no olvidar nada durante el día. Eso me "
            "ha ayudado mucho en todos los trabajos que he tenido."
        ),
        "hours_per_week": (
            "Tengo bastante tiempo disponible. No estoy trabajando ahorita, salí hace "
            "dos meses del trabajo anterior y estoy en búsqueda activa. Puedo dedicar "
            "40 horas o más si es necesario. No tengo hijos ni otras responsabilidades "
            "grandes ahorita. Estoy 100% disponible para lo que el programa pida. "
            "Vivo con mis papás y no tengo que pagar renta, así que puedo enfocarme "
            "solo en esto. Si me dan la oportunidad voy a meterle con todo porque "
            "necesito volver a tener trabajo pronto y creo que esto me puede abrir "
            "puertas importantes en el mundo B2B."
        ),
    }

    apps = [
        Application(
            applicant_name="Sofía Martínez",
            applicant_email="sofia.m@example.com",
            applicant_phone="+57 300 555 1212",
            linkedin_url="https://www.linkedin.com/in/sofia-martinez-demo",
            country="Colombia",
            locale="es",
            answers=answer_set_strong_es,
            video_url="https://loom.com/share/demo-sofia",
            status="submitted",
        ),
        Application(
            applicant_name="Rodrigo Castro",
            applicant_email="rodrigo.c@example.com",
            applicant_phone="+52 55 2345 6789",
            linkedin_url="https://www.linkedin.com/in/rodrigo-castro-demo",
            country="México",
            locale="es",
            answers=answer_set_medium_es,
            video_url="https://loom.com/share/demo-rodrigo",
            ai_score=78,
            ai_notes=(
                "Comunicación clara, motivación genuina. "
                "Banderas: dice 20h/sem pero trabaja full-time — validar."
            ),
            status="under_review",
        ),
        Application(
            applicant_name="Valentina Ríos",
            applicant_email="valentina.rios@example.com",
            applicant_phone="+54 11 5678 4321",
            linkedin_url="https://www.linkedin.com/in/valentina-rios-demo",
            country="Argentina",
            locale="es",
            answers=answer_set_strong_es,
            video_url="https://loom.com/share/demo-valentina",
            ai_score=86,
            ai_notes=(
                "Perfil SDR maduro. Storytelling sólido, métricas reales. "
                "Fuerte ajuste cultural — asignable a cohorte senior."
            ),
            status="under_review",
        ),
        Application(
            applicant_name="Joaquín Salazar",
            applicant_email="joaquin.s@example.com",
            applicant_phone="+56 9 8765 4321",
            linkedin_url="https://www.linkedin.com/in/joaquin-salazar-demo",
            country="Chile",
            locale="es",
            answers=answer_set_medium_es,
            video_url="https://loom.com/share/demo-joaquin",
            status="submitted",
        ),
        Application(
            applicant_name="Isabela Fernandes",
            applicant_email="isabela.f@example.com",
            applicant_phone="+55 11 94567 8901",
            linkedin_url="https://www.linkedin.com/in/isabela-fernandes-demo",
            country="Brasil",
            locale="pt",
            answers={
                "why_sales": (
                    "Quero trabalhar em vendas porque é o único papel onde o resultado "
                    "depende do quanto entendo o outro. Passei três anos fazendo "
                    "prospecção B2C em um banco em São Paulo, aprendi que um bom SDR "
                    "pergunta mais do que fala. Já perdi o medo do telefone. Agora "
                    "quero metodologia real para escalar em tech — por isso o Siete "
                    "Academy faz sentido: é específico, tem mentoria humana e treina "
                    "para colocação real em agências e SaaS. Minha meta é sair do "
                    "programa com pipeline construído, não só com conhecimento teórico."
                ),
                "achievement": (
                    "No último trimestre levei o NPS do meu esquadrão de 42 para 68 em "
                    "dez semanas — reestruturei o script de atendimento, implementei "
                    "um check-list de qualificação antes da ligação e treinei três "
                    "colegas novos. A gerente transformou meu processo em padrão. "
                    "Aprendi que medir importa mais do que fazer bonito. Já estou "
                    "acostumada a ter metas semanais, ownership dos meus números e "
                    "feedback direto. Quero levar isso para um ambiente B2B tech."
                ),
                "hours_per_week": (
                    "Posso dedicar 22-25 horas por semana ao programa. Trabalho "
                    "meio-expediente de manhã (20h/sem) e uso as tardes de três dias "
                    "da semana mais os sábados. Minhas sessões ao vivo já estão "
                    "bloqueadas no calendário. Moro com minha família, não tenho "
                    "filhos, consigo reorganizar meu tempo facilmente para entregar "
                    "as atividades antes do prazo."
                ),
            },
            video_url="https://loom.com/share/demo-isabela",
            ai_score=82,
            ai_notes=(
                "Perfil sólido en PT-BR. Evidencia cuantitativa, experiencia previa "
                "relevante. Considerar cohorte PT-BR si hay cupo."
            ),
            status="under_review",
        ),
        Application(
            applicant_name="Mateo Acosta",
            applicant_email="mateo.a@example.com",
            applicant_phone="+51 999 888 777",
            linkedin_url="https://www.linkedin.com/in/mateo-acosta-demo",
            country="Perú",
            locale="es",
            answers=answer_set_weak_es,
            video_url="https://loom.com/share/demo-mateo",
            ai_score=42,
            ai_notes=(
                "Respuestas genéricas, sin métricas concretas. Disponibilidad "
                "40h/sem pero sin trabajo ni ingresos: riesgo de abandono si "
                "consigue empleo mid-programa. Recomendado: entrevista o reject."
            ),
            status="under_review",
        ),
        Application(
            applicant_name="Emily Carter",
            applicant_email="emily.c@example.com",
            applicant_phone="+1 415 555 0199",
            linkedin_url="https://www.linkedin.com/in/emily-carter-demo",
            country="United States",
            locale="en",
            answers={
                "why_sales": (
                    "I want to work in sales because it's the only role where my "
                    "output is directly tied to how well I understand the other "
                    "person. I spent two years doing inbound support for a B2B SaaS "
                    "and saw the AE team make numbers I didn't make. I got tired of "
                    "being on the receiving end of the conversation and started "
                    "running discovery calls myself last quarter. I closed two small "
                    "deals and realized this is what I want full-time. I'm applying "
                    "to Siete Academy because I want structured methodology and real "
                    "coaching, not just Udemy courses and hoping it sticks."
                ),
                "achievement": (
                    "Last year I rebuilt our support macros from scratch after "
                    "auditing 200 of our worst-rated tickets. I identified that 60% "
                    "of bad ratings came from 4 specific issue types with unclear "
                    "canned responses. I rewrote the top 20 macros, A/B tested them "
                    "with two teammates for a month, and the CSAT moved from 4.1 to "
                    "4.6 team-wide. My manager asked me to own onboarding for new "
                    "support hires after that. I took ownership of the problem, "
                    "measured the change, and made the fix durable."
                ),
                "hours_per_week": (
                    "I can dedicate 25 hours per week. I work 30 hours weekly at my "
                    "current role (contract, flexible schedule) and have mornings and "
                    "weekends free. I've already blocked all eight live sessions on "
                    "my calendar. I'd rather commit to 25 sustainably than promise "
                    "40 and burn out. I live alone, no kids, no major time "
                    "constraints aside from work."
                ),
            },
            video_url="https://loom.com/share/demo-emily",
            status="submitted",
        ),
        Application(
            applicant_name="Ana Lucía Vega",
            applicant_email="ana.vega@example.com",
            applicant_phone="+593 99 888 7766",
            linkedin_url="https://www.linkedin.com/in/ana-vega-demo",
            country="Ecuador",
            locale="es",
            answers=answer_set_medium_es,
            video_url="https://loom.com/share/demo-ana",
            ai_score=71,
            ai_notes=(
                "Sólida en fundamentos. Poca exposición a B2B tech pero alta "
                "motivación. Entrevista recomendada para validar ajuste."
            ),
            status="under_review",
        ),
    ]
    for a in apps:
        db.add(a)
    db.commit()
    log.info("seed.applications", extra={"count": len(apps)})


def seed_course(db) -> dict[int, Module]:
    course, _ = _upsert(db, Course, lookup={"slug": "sdr-fundamentals"})
    if not course.translations:
        course.translations = [
            CourseTranslation(locale="es", title="Fundamentos SDR", description="Programa base de ocho semanas."),
            CourseTranslation(locale="en", title="SDR Fundamentals", description="Core eight-week program."),
            CourseTranslation(locale="pt", title="Fundamentos SDR", description="Programa base de oito semanas."),
        ]
        db.commit()

    modules_spec = [
        (
            0,
            "modelos-de-negocio",
            {"es": "Modelos de negocio", "en": "Business models", "pt": "Modelos de negócio"},
            {"es": "Cómo se gana dinero en B2B.", "en": "How money is made in B2B.", "pt": "Como se ganha dinheiro em B2B."},
        ),
        (
            1,
            "icp",
            {"es": "Ideal Customer Profile", "en": "Ideal Customer Profile", "pt": "Ideal Customer Profile"},
            {"es": "Del buyer persona al ICP utilitario.", "en": "From persona to practical ICP.", "pt": "Do persona ao ICP prático."},
        ),
        (
            2,
            "metodologia-sdr",
            {"es": "Metodología SDR", "en": "SDR methodology", "pt": "Metodologia SDR"},
            {"es": "Cadencias, discovery, qualification.", "en": "Cadences, discovery, qualification.", "pt": "Cadências, discovery, qualification."},
        ),
        (
            3,
            "herramientas-y-cold-calling",
            {"es": "Herramientas & Cold Calling", "en": "Tooling & Cold Calling", "pt": "Ferramentas & Cold Calling"},
            {"es": "Stack real + tu primera llamada en vivo.", "en": "Real stack + your first live call.", "pt": "Stack real + sua primeira ligação."},
        ),
    ]

    mods: dict[int, Module] = {}
    LESSON_VIDEOS = ["LXb3EKWsInQ", "pN-Z2kDpL6Q"]

    for order, slug, titles, summaries in modules_spec:
        m, created = _upsert(
            db,
            Module,
            lookup={"course_id": course.id, "slug": slug},
            defaults={"order_index": order},
        )
        if created or not m.translations:
            for loc, t in titles.items():
                m.translations.append(
                    ModuleTranslation(locale=loc, title=t, summary=summaries[loc])
                )
            db.commit()
        mods[order] = m

        if not m.lessons:
            for idx, yid in enumerate(LESSON_VIDEOS):
                le = Lesson(
                    module_id=m.id,
                    order_index=idx,
                    kind="video",
                    youtube_id=yid,
                    duration_seconds=600 + idx * 120,
                )
                le.translations.extend(
                    [
                        LessonTranslation(
                            locale="es",
                            title=f"Lección {idx + 1}: {titles['es']}",
                            body=f"Video guía de la lección {idx + 1}. Toma notas y haz los ejercicios al final.",
                        ),
                        LessonTranslation(
                            locale="en",
                            title=f"Lesson {idx + 1}: {titles['en']}",
                            body=f"Guide video for lesson {idx + 1}. Take notes and do the exercises.",
                        ),
                        LessonTranslation(
                            locale="pt",
                            title=f"Aula {idx + 1}: {titles['pt']}",
                            body=f"Vídeo guia da aula {idx + 1}. Tome notas e faça os exercícios.",
                        ),
                    ]
                )
                db.add(le)
            manual_idx = len(LESSON_VIDEOS)
            manual = Lesson(
                module_id=m.id,
                order_index=manual_idx,
                kind="reading",
                youtube_id=None,
                duration_seconds=None,
            )
            manual_body = {
                "es": (
                    f"# Manual — {titles['es']}\n\n"
                    "## Introducción\n\n"
                    f"{summaries['es']} Este material complementa las lecciones en video y "
                    "te sirve como referencia durante y después del módulo.\n\n"
                    "## Marco conceptual\n\n"
                    "1. **Contexto**: entiende por qué este tema es crítico para un SDR moderno.\n"
                    "2. **Principios**: las tres ideas centrales que debes interiorizar antes de hacer cold outreach.\n"
                    "3. **Aplicación**: cómo se ve esto en la práctica, con ejemplos reales.\n\n"
                    "## Checklist de dominio\n\n"
                    "- [ ] Puedes explicarle este tema a alguien en 60 segundos.\n"
                    "- [ ] Tienes un ejemplo concreto de tu experiencia donde aplica.\n"
                    "- [ ] Identificas cuándo este concepto NO aplica.\n\n"
                    "## Cierre\n\n"
                    "Este manual es tuyo para consultar cuando estés en una llamada "
                    "o preparando una cadencia. No lo descargues — vuelve aquí cuando lo necesites."
                ),
                "en": (
                    f"# Handbook — {titles['en']}\n\n"
                    "## Intro\n\n"
                    f"{summaries['en']} This material complements the video lessons and "
                    "serves as a reference during and after the module.\n\n"
                    "## Framework\n\n"
                    "1. **Context**: why this matters for a modern SDR.\n"
                    "2. **Principles**: the three core ideas to internalize before any cold outreach.\n"
                    "3. **Applied**: real examples of what this looks like in practice.\n\n"
                    "## Mastery checklist\n\n"
                    "- [ ] You can explain this topic to someone in 60 seconds.\n"
                    "- [ ] You have a concrete example from your own experience.\n"
                    "- [ ] You can identify when this concept does NOT apply.\n\n"
                    "## Wrap\n\n"
                    "Use this handbook during calls or when planning cadences. "
                    "Don't download — come back here when you need it."
                ),
                "pt": (
                    f"# Manual — {titles['pt']}\n\n"
                    "## Introdução\n\n"
                    f"{summaries['pt']} Este material complementa as aulas em vídeo e "
                    "serve como referência durante e depois do módulo.\n\n"
                    "## Enquadramento\n\n"
                    "1. **Contexto**: por que isso importa para um SDR moderno.\n"
                    "2. **Princípios**: as três ideias centrais para interiorizar antes de qualquer outreach.\n"
                    "3. **Aplicado**: como isso aparece na prática, com exemplos reais.\n\n"
                    "## Checklist de domínio\n\n"
                    "- [ ] Consegue explicar este tema em 60 segundos.\n"
                    "- [ ] Tem um exemplo concreto da sua experiência.\n"
                    "- [ ] Identifica quando este conceito NÃO se aplica.\n\n"
                    "## Fecho\n\n"
                    "Este manual é seu para consultar. Não baixe — volte aqui quando precisar."
                ),
            }
            manual_titles = {
                "es": f"Manual — {titles['es']}",
                "en": f"Handbook — {titles['en']}",
                "pt": f"Manual — {titles['pt']}",
            }
            for loc in ("es", "en", "pt"):
                manual.translations.append(
                    LessonTranslation(
                        locale=loc,
                        title=manual_titles[loc],
                        body=manual_body[loc],
                    )
                )
            db.add(manual)
            db.commit()
        if created:
            log.info("seed.module", extra={"slug": slug})

    return mods


def seed_assessments(db, mods: dict[int, Module]) -> dict[int, list[Assessment]]:
    out: dict[int, list[Assessment]] = {0: [], 1: [], 2: [], 3: []}
    specs = [
        (
            0, "mcq", "Quiz — Modelos de negocio",
            {
                "questions": [
                    {"id": "q1", "prompt": "¿Cuál es el principal driver de valor en un SaaS B2B?",
                     "options": {"a": "NPS", "b": "MRR recurrente", "c": "Tráfico web"}},
                    {"id": "q2", "prompt": "¿Qué significa ACV?",
                     "options": {"a": "Average Contract Value", "b": "Annual Customer Volume", "c": "Acquired Client Value"}},
                    {"id": "q3", "prompt": "¿Qué es un 'freemium motion'?",
                     "options": {"a": "Cobrar por usuario", "b": "Tier gratis con conversión a paga", "c": "Descuento anual"}},
                ],
                "correct_answers": {"q1": "b", "q2": "a", "q3": "b"},
            },
        ),
        (
            1, "written", "Entrega — Define un ICP para una PyME fintech",
            {"prompt": (
                "Nuestro cliente es una fintech B2B latinoamericana con ticket promedio $12k/año. "
                "Define en 200-300 palabras un ICP accionable: industria, tamaño, rol del buyer, "
                "señales de intent, exclusiones."
            )},
        ),
        (
            2, "prospection_db", "Entrega — Base de 50 prospects segmentados",
            {"instructions": (
                "Sube un CSV con 50 prospects que cumplan el ICP del módulo 1. Columnas: company, "
                "employees, industry, contact_name, title, linkedin_url, source_signal."
            )},
        ),
        (
            3, "cold_call_video", "Entrega — Graba un cold call role-play de 90 segundos",
            {
                "scenario": (
                    "El prospect es Head of Sales en una empresa SaaS Serie A (~50 empleados). "
                    "Acaban de levantar ronda. Objetivo: conseguir discovery de 20 min."
                ),
                "rubric": [
                    "Apertura clara y permiso",
                    "Pregunta de dolor específica",
                    "Manejo de objeción 'no tengo tiempo'",
                    "Cierre con CTA concreto",
                ],
            },
        ),
        (
            3, "team_exercise", "Ejercicio en equipo (sesión en vivo)",
            {
                "brief": (
                    "En grupos de 3, construyan una cadencia de 8 toques (email + LinkedIn + teléfono) "
                    "para el ICP definido en módulo 1."
                ),
                "deliverable": "Documento compartido con la cadencia.",
            },
        ),
    ]

    if db.query(Assessment).count() == 0:
        for order, type_, title, config in specs:
            a = Assessment(
                module_id=mods[order].id,
                type=type_, title=title, config=config, passing_score=70.0,
            )
            db.add(a)
            out[order].append(a)
        db.commit()
        log.info("seed.assessments", extra={"count": sum(len(v) for v in out.values())})
    else:
        for order, m in mods.items():
            out[order] = db.query(Assessment).filter_by(module_id=m.id).all()
    return out


def seed_cohort(db, mods: dict[int, Module]) -> Cohort:
    cohort, created = _upsert(
        db,
        Cohort,
        lookup={"name": "SDR 001 — Mayo 2026"},
        defaults={
            "locale": "es",
            "start_date": date(2026, 5, 1),
            "end_date": date(2026, 6, 30),
            "status": "in_progress",
            "max_students": 15,
        },
    )
    now = datetime.now(UTC).replace(tzinfo=None)
    window_specs = [
        (0, now - timedelta(days=3), now + timedelta(days=11), now + timedelta(days=10)),
        (1, now + timedelta(days=14), now + timedelta(days=28), now + timedelta(days=27)),
        (2, now + timedelta(days=28), now + timedelta(days=42), now + timedelta(days=41)),
        (3, now + timedelta(days=42), now + timedelta(days=56), now + timedelta(days=55)),
    ]
    for order, opens, closes, live_at in window_specs:
        _upsert(
            db,
            ModuleWindow,
            lookup={"cohort_id": cohort.id, "module_id": mods[order].id},
            defaults={"opens_at": opens, "closes_at": closes, "live_session_at": live_at},
        )
    if created:
        log.info("seed.cohort", extra={"cohort_name": cohort.name})
    return cohort


def seed_live_sessions(db, cohort: Cohort) -> None:
    windows = db.query(ModuleWindow).filter_by(cohort_id=cohort.id).all()
    for w in windows:
        _upsert(
            db,
            LiveSession,
            lookup={"module_window_id": w.id},
            defaults={
                "title": f"Sesión en vivo — Módulo {w.module_id}",
                "zoom_url": "https://us06web.zoom.us/j/88888888888?pwd=demo-siete-academy",
                "recording_url": None,
            },
        )
    log.info("seed.live_sessions", extra={"count": len(windows)})


def seed_enrollments(db, users: dict[str, User], cohort: Cohort) -> None:
    for role_key, progress in (("student", 40.0), ("camila", 75.0), ("diego", 100.0)):
        u = users[role_key]
        _upsert(
            db,
            Enrollment,
            lookup={"user_id": u.id, "cohort_id": cohort.id},
            defaults={
                "status": "active" if progress < 100 else "completed",
                "progress_pct": progress,
            },
        )
    log.info("seed.enrollments", extra={"count": 3})


def seed_submissions_and_reviews(
    db, users: dict[str, User], assessments: dict[int, list[Assessment]]
) -> None:
    if db.query(Submission).count() > 0:
        return
    mcq = assessments[0][0]
    written = assessments[1][0]

    s1 = Submission(
        assessment_id=mcq.id,
        user_id=users["student"].id,
        payload={"answers": {"q1": "b", "q2": "a", "q3": "b"}},
        status="auto_graded",
        auto_score=100.0,
    )
    s2 = Submission(
        assessment_id=written.id,
        user_id=users["camila"].id,
        payload={"text": (
            "ICP propuesto: Fintech B2B LatAm serie A con 50-200 empleados. Buyer: Head of Finance "
            "o CFO. Industria: retail digital, logística, salud privada. Señales: acaban de levantar "
            "ronda, están contratando finance ops. Excluye: empresas con más de 3 años sin "
            "crecimiento de head-count."
        )},
        status="reviewed",
    )
    s3 = Submission(
        assessment_id=written.id,
        user_id=users["diego"].id,
        payload={"text": "Pymes de 10-50 empleados. Venta por relación. Hablar con el dueño."},
        status="pending_review",
    )
    db.add_all([s1, s2, s3])
    db.commit()
    db.refresh(s2)
    db.refresh(s3)

    review = TeacherReview(
        submission_id=s2.id,
        teacher_id=users["teacher"].id,
        score=82.0,
        feedback=(
            "Muy buen nivel de especificidad. Dos mejoras:\n\n"
            "1. Las señales están bien pero son genéricas — piensa en cómo las detectas en la "
            "práctica (LinkedIn Sales Nav? Crunchbase? scraping?).\n\n"
            "2. La exclusión de '3 años sin crecimiento' es arbitraria. Justifícala o retírala."
        ),
        attachment_url="https://drive.google.com/file/d/demo-icp-review-notes/view",
    )
    db.add(review)

    ai = AIReview(
        submission_id=s3.id,
        draft_feedback=(
            "Diagnóstico: respuesta muy corta (25 palabras contra objetivo de 200-300). "
            "No define industrias, ni señales de intent, ni exclusiones. \"Venta por relación\" no "
            "es un ICP, es una táctica.\n\n"
            "Sugerencia al alumno:\n"
            "- Pedirle que reescriba con el framework del módulo (industria + tamaño + rol + señal).\n"
            "- Mostrarle el ejemplo de Camila como referencia.\n\n"
            "Score sugerido: 35/100 — no aprueba."
        ),
        score_suggestion=35.0,
        model_used="claude-opus-4-7",
    )
    db.add(ai)
    db.commit()
    log.info(
        "seed.submissions_and_reviews",
        extra={"submissions": 3, "reviews": 1, "ai_drafts": 1},
    )


def seed_placement(db, users: dict[str, User], cohort: Cohort) -> None:
    if db.query(PlacementCandidate).count() > 0:
        return
    specs = [
        (users["student"], "applying", "Terminando módulo 1. Sólido en modelos de negocio."),
        (users["camila"], "siete_interview", "Primera entrevista con equipo comercial agendada."),
        (users["diego"], "siete_test", "Pasó entrevista. Toma la prueba práctica el viernes."),
    ]
    for user, stage, summary in specs:
        c = PlacementCandidate(
            user_id=user.id,
            cohort_id=cohort.id,
            stage=stage,
            summary=summary,
            portfolio_url=f"https://linkedin.com/in/{user.email.split('@')[0]}",
        )
        db.add(c)
        db.flush()
        db.add(
            PlacementEvent(
                candidate_id=c.id,
                event_type="created",
                data={"cohort_id": cohort.id},
                actor_id=users["admin"].id,
            )
        )
        if stage != "applying":
            db.add(
                PlacementEvent(
                    candidate_id=c.id,
                    event_type="stage_changed",
                    data={"from": "applying", "to": stage},
                    actor_id=users["admin"].id,
                )
            )
    db.commit()
    log.info("seed.placement", extra={"count": len(specs)})


def seed_approved_grad(db, users: dict[str, User], cohort: Cohort) -> None:
    grad, _ = _upsert(
        db,
        User,
        lookup={"email": "valeria@example.com"},
        defaults={
            "firebase_uid": "seed-grad-valeria",
            "display_name": "Valeria Ortiz",
            "role": "student",
            "locale": "es",
        },
    )
    _upsert(
        db,
        Enrollment,
        lookup={"user_id": grad.id, "cohort_id": cohort.id},
        defaults={
            "status": "completed",
            "progress_pct": 100.0,
            "completed_at": datetime.now(UTC).replace(tzinfo=None),
        },
    )
    if db.query(PlacementCandidate).filter_by(user_id=grad.id).first():
        return
    c = PlacementCandidate(
        user_id=grad.id,
        cohort_id=cohort.id,
        stage="approved",
        summary=(
            "Graduada con distinción (92/100). Fuerte en discovery y manejo de objeciones. "
            "Background en BDR de SaaS 1 año."
        ),
        portfolio_url="https://linkedin.com/in/valeria-ortiz-demo",
    )
    db.add(c)
    db.flush()
    for event_type, data in [
        ("created", {"cohort_id": cohort.id}),
        ("stage_changed", {"from": "applying", "to": "siete_interview"}),
        ("stage_changed", {"from": "siete_interview", "to": "siete_test"}),
        ("stage_changed", {"from": "siete_test", "to": "approved"}),
    ]:
        db.add(
            PlacementEvent(
                candidate_id=c.id,
                event_type=event_type,
                data=data,
                actor_id=users["admin"].id,
            )
        )
    db.commit()
    log.info("seed.approved_grad", extra={"email": grad.email})


def seed_certificate(db, users: dict[str, User], cohort: Cohort) -> None:
    from app.modules.certificates.services import issue_if_eligible

    issue_if_eligible(db, user_id=users["diego"].id, cohort_id=cohort.id)


def run() -> None:
    _ensure_schema()
    db = SessionLocal()
    try:
        users = seed_users(db)
        seed_applications(db)
        mods = seed_course(db)
        assessments = seed_assessments(db, mods)
        cohort = seed_cohort(db, mods)
        seed_live_sessions(db, cohort)
        seed_enrollments(db, users, cohort)
        seed_submissions_and_reviews(db, users, assessments)
        seed_placement(db, users, cohort)
        seed_approved_grad(db, users, cohort)
        seed_certificate(db, users, cohort)
        log.info("seed.done")
    finally:
        db.close()


if __name__ == "__main__":
    run()
