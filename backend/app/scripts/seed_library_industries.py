"""Seed: 10 tarjetas de industria (Documento Maestro Parte II v0.1).

Material de consulta transversal, no evaluado. Estructura fija de 8 campos
por tarjeta. Solo locale "es" en v1 (en/pt se agregan cuando la cohorte 1
piloto los pida).

Idempotente: re-ejecutable. Si la tarjeta existe, actualiza el contenido del
locale es; si no, la crea.

Uso:
    cd backend && .venv/bin/python -m app.scripts.seed_library_industries
"""
from __future__ import annotations

from app.core.database import SessionLocal
from app.core.logging import configure_logging, get_logger
from app.modules.audit import models as _audit  # noqa: F401
from app.modules.library import models as _library  # noqa: F401
from app.modules.library.models import IndustryCard, IndustryCardTranslation
from app.modules.users import models as _users  # noqa: F401

configure_logging()
log = get_logger("seed_library_industries")


# Cada entry transcribe literal del doc (líneas 1421-1795 del Documento Maestro).
# Orden = orden del doc. Tags son etiquetas funcionales para futuros filtros.
INDUSTRIES: list[dict] = [
    {
        "slug": "retail-cpg",
        "order_index": 1,
        "name": "Retail y consumo masivo",
        "tags": ["b2c", "b2b2c", "alta-estacionalidad", "margen-bajo"],
        "examples": [
            "Falabella (Chile/regional)",
            "Cencosud (Chile/regional)",
            "Walmart México",
            "Alicorp (Perú — consumo masivo)",
            "Grupo Éxito (Colombia)",
            "Carozzi (Chile — alimentos)",
        ],
        "what_is": (
            "Venta de productos de uso frecuente al consumidor final, directo "
            "(retailers) o a través de tiendas minoristas (marcas de consumo "
            "masivo o CPG — Consumer Packaged Goods). Una de las industrias "
            "más grandes y maduras de LATAM, con márgenes históricamente "
            "ajustados y competencia intensa."
        ),
        "how_makes_money": (
            "Márgenes brutos bajos (8-25% típicamente) compensados por volumen. "
            "En retail, la clave es la rotación de inventario; en CPG, la "
            "distribución y presencia en góndola. Ambas dependen crudamente de "
            "la eficiencia operativa y la gestión de la cadena."
        ),
        "what_sells": (
            "Alimentos, bebidas, productos de limpieza, cuidado personal, ropa, "
            "electrodomésticos, productos para el hogar. Cada vez más, también "
            "experiencia (omnicanal, delivery, loyalty)."
        ),
        "sells_to": (
            "B2C (consumidor final) o B2B2C (a través de supermercados, "
            "distribuidores, mayoristas). Las grandes cadenas son también "
            "plataforma de venta para marcas más chicas."
        ),
        "buys_to_operate": (
            "- Sistemas de gestión de inventario y cadena de suministro.\n"
            "- Software de análisis de ventas y forecasting de demanda.\n"
            "- Plataformas de e-commerce y pagos.\n"
            "- Soluciones de logística y última milla.\n"
            "- Plataformas de marketing y CRM (fidelización).\n"
            "- Servicios financieros: factoring, leasing, seguros de inventario.\n"
            "- Consultoría de expansión regional y apertura de tiendas."
        ),
        "dynamics": (
            "Fuerte estacionalidad (Navidad/Día de Madre concentran 40%+ de "
            "ventas anuales en muchos segmentos), presión creciente del "
            "e-commerce sobre tiendas físicas, sensibilidad a tipo de cambio "
            "(muchos productos importados), creciente demanda de trazabilidad "
            "y sostenibilidad."
        ),
        "deepen_in": (
            "McKinsey State of the Latin American Consumer (reporte anual). "
            "Nielsen IQ — reports por país. HBR — How Retail Chains Win in "
            "Emerging Markets. [VERIFICAR última edición]"
        ),
    },
    {
        "slug": "logistica-transporte",
        "order_index": 2,
        "name": "Logística y transporte",
        "tags": ["b2b", "margen-bajo", "volumen", "regulado"],
        "examples": [
            "Pedidos Ya (regional)",
            "Rappi (regional — también fintech)",
            "DHL Express LATAM",
            "99minutos (México, startup B2B)",
            "Traxión (México — transporte de carga)",
        ],
        "what_is": (
            "Movimiento de mercadería y personas dentro de y entre países. "
            "Incluye transporte terrestre, aéreo, marítimo, última milla, "
            "depósitos (warehousing), freight forwarding y distribución. En "
            "LATAM, la infraestructura desigual entre países hace que la "
            "eficiencia logística sea un diferenciador clave de competitividad."
        ),
        "how_makes_money": (
            "Márgenes típicamente bajos (5-15%), modelo de volumen y escala. "
            "Rentabilidad depende de utilización de flota/capacidad, ruteo "
            "eficiente y gestión de combustible. Pricing por peso, volumen, "
            "distancia o servicio (express vs estándar)."
        ),
        "what_sells": (
            "Servicios de transporte de carga (B2B dominante) y de pasajeros "
            "(B2C), almacenaje, distribución última milla, gestión aduanera, "
            "freight forwarding internacional."
        ),
        "sells_to": (
            "B2B principalmente (empresas de todos los sectores que necesitan "
            "mover producto). Operadores de última milla venden también a "
            "e-commerce y marketplaces. Algunos jugadores B2C (pasajeros, "
            "mudanzas)."
        ),
        "buys_to_operate": (
            "- Flota (vehículos, contenedores, aeronaves) y mantenimiento.\n"
            "- Combustible (componente de costo mayor — sensible a precio del petróleo).\n"
            "- Software de ruteo, TMS (Transportation Management System), WMS (Warehouse Management System).\n"
            "- Telemetría, GPS, IoT para monitoreo de flota.\n"
            "- Seguros de carga y flota.\n"
            "- Servicios aduaneros y de compliance regulatorio.\n"
            "- Personal — choferes, operarios de depósito (alta rotación, costo creciente)."
        ),
        "dynamics": (
            "Alta volatilidad por precio del combustible, fuerte presión del "
            "e-commerce (explosión de última milla en LATAM post-pandemia), "
            "regulación aduanera cambiante por país, creciente demanda de "
            "trazabilidad y entregas rápidas, presión por decarbonización "
            "(flotas eléctricas empezando)."
        ),
        "deepen_in": (
            "Banco Mundial Logistics Performance Index (LPI, bianual por país). "
            "CEPAL — reports sobre infraestructura logística en LATAM. [VERIFICAR]"
        ),
    },
    {
        "slug": "tech-software",
        "order_index": 3,
        "name": "Tecnología / Software (SaaS, hardware, servicios TI)",
        "tags": ["b2b", "saas", "margen-alto", "talento-intensivo"],
        "examples": [
            "Globant (Argentina, servicios TI a escala global)",
            "Nubank (Brasil — fintech SaaS)",
            "Kueski (México)",
            "Rappi (colombiana — plataforma)",
            "Auth0 (Argentina — adquirida por Okta)",
        ],
        "what_is": (
            "Empresas que desarrollan o distribuyen soluciones tecnológicas. "
            "Se divide en 3 grandes grupos: software (SaaS, on-premise, "
            "aplicaciones), hardware (equipos, dispositivos, infraestructura) "
            "y servicios TI (implementación, consultoría tech, desarrollo a "
            "medida). En LATAM, el sector ha crecido a tasas de 15-20% anual "
            "en la última década — es la industria con mayor velocidad de "
            "adopción de modelos B2B modernos."
        ),
        "how_makes_money": (
            "Varía fuerte por subsegmento:\n"
            "- SaaS B2B: modelo de suscripción (MRR/ARR), márgenes brutos altos (70-85%), pero CAC elevado y payback largo (12-24 meses típico).\n"
            "- Hardware: márgenes bajos (10-25%), ciclo de venta más lineal.\n"
            "- Servicios TI: facturación por hora, proyecto o retainer. Márgenes medios (25-45%), depende del talento."
        ),
        "what_sells": (
            "Desde plataformas SaaS y licencias, hasta servidores, "
            "integraciones, ciberseguridad, AI/ML, datos y analítica, hasta "
            "desarrollo a medida y staff augmentation."
        ),
        "sells_to": (
            "B2B dominantemente (otras empresas lo usan para operar) aunque "
            "hay subsegmentos B2C (apps de consumidor). En LATAM, muchas tech "
            "venden al exterior (servicios TI a EE.UU./Europa) — es uno de "
            "los sectores más exportadores de servicios."
        ),
        "buys_to_operate": (
            "- Talento: es la variable #1 de costo. Desarrolladores, data engineers, product managers (competencia feroz por talento local + remoto global).\n"
            "- Infraestructura cloud (AWS, Azure, GCP — subcontratada casi siempre).\n"
            "- Herramientas internas: CRM, marketing automation, HR tech, finance software, analytics.\n"
            "- Servicios profesionales: legal, contable, marketing.\n"
            "- Espacios de trabajo, beneficios para empleados (para retención)."
        ),
        "dynamics": (
            "Competencia global (empresas gringas venden al mismo cliente "
            "LATAM), presión por adoptar AI, ciclos de fundraising (muchas "
            "tech dependen de capital de riesgo), alta rotación de talento "
            "(tenure promedio 18-24 meses), creciente regulación de datos "
            "(LGPD Brasil, ley de protección de datos Chile/Colombia)."
        ),
        "deepen_in": (
            "LAVCA (Latin American Venture Capital Association) — reports "
            "anuales. KPMG Tech Landscape LATAM. SaaStr.com (artículos de "
            "industria). Distributed State of LATAM Tech. [VERIFICAR]"
        ),
    },
    {
        "slug": "servicios-financieros",
        "order_index": 4,
        "name": "Servicios financieros (banca, seguros, fintech)",
        "tags": ["b2b", "b2c", "regulado", "datos-sensibles"],
        "examples": [
            "Nubank (Brasil — el neobanco más grande del mundo fuera de China)",
            "Mercado Pago (regional)",
            "Ualá (Argentina)",
            "Banco de Crédito del Perú (BCP)",
            "Itaú Unibanco (Brasil)",
            "Rappi Pay",
        ],
        "what_is": (
            "Empresas que mueven, gestionan o protegen dinero. Incluye banca "
            "tradicional (retail y corporativa), seguros (generales, vida, "
            "salud), fintech (pagos, lending, neobancos, crypto, WealthTech, "
            "InsurTech), gestoras de activos y casas de bolsa. Es una de las "
            "industrias más reguladas y más grandes por ingresos en LATAM."
        ),
        "how_makes_money": (
            "- Banca: spread de tasas (préstamos - depósitos), comisiones, trading.\n"
            "- Seguros: primas - siniestros (floating invertido).\n"
            "- Fintech: comisiones de transacción (pagos), tasas de interés (lending), suscripciones (wealthtech)."
        ),
        "what_sells": (
            "Préstamos personales y corporativos, tarjetas de crédito, cuentas "
            "corrientes, seguros (auto, salud, vida, empresariales), productos "
            "de inversión, procesamiento de pagos, remesas."
        ),
        "sells_to": (
            "Mix de B2C (banca retail, seguros individuales) y B2B (banca "
            "corporativa, seguros empresariales, pagos para comercios, fintech "
            "infrastructure). Algunos jugadores son B2B2C (venden a empresas "
            "que revenden al consumidor final)."
        ),
        "buys_to_operate": (
            "- Core banking / plataformas de pagos (muchas veces subcontratadas o licenciadas — mercado gigante).\n"
            "- Ciberseguridad, fraud prevention y AML (anti-lavado) — requisito regulatorio.\n"
            "- Datos y credit scoring — especialmente crítico en LATAM donde hay mucha población sin historial formal.\n"
            "- CRM y automatización de marketing (competencia por captación es feroz).\n"
            "- Consultoría legal y regulatoria (cambios constantes de normativa).\n"
            "- Software de riesgo y compliance.\n"
            "- Infraestructura cloud con alta disponibilidad y certificaciones (ISO 27001, PCI-DSS, SOC 2)."
        ),
        "dynamics": (
            "Regulación pesada y cambiante (bancos centrales, "
            "superintendencias), competencia creciente entre banca tradicional "
            "y fintech (dinámica \"banks vs neobanks\"), inclusión financiera "
            "como tendencia (LATAM tiene ~30% de adultos sin cuenta bancaria "
            "según Banco Mundial), impulso fuerte de open banking en México, "
            "Brasil, Colombia, Chile."
        ),
        "deepen_in": (
            "FELABAN (Federación Latinoamericana de Bancos) — reports "
            "regionales. Banco Mundial Global Findex (inclusión financiera). "
            "CB Insights State of Fintech LATAM. LAVCA reports sectoriales. "
            "[VERIFICAR última edición]"
        ),
    },
    {
        "slug": "consultoria",
        "order_index": 5,
        "name": "Consultoría (gestión, tributaria, legal, RRHH, tecnológica)",
        "tags": ["b2b", "alto-ticket", "relacional", "talento-senior"],
        "examples": [
            "Deloitte LATAM",
            "PwC regional",
            "KPMG",
            "EY",
            "McKinsey LATAM",
            "Accenture LATAM",
            "Quint (estratégica mexicana)",
            "PLATAFORMAS (boutiques tributarias en Perú y Chile)",
        ],
        "what_is": (
            "Servicios profesionales de alto valor agregado donde la venta es "
            "fundamentalmente conocimiento experto aplicado al problema del "
            "cliente. Se subdivide en:\n"
            "- Consultoría estratégica / de gestión: McKinsey, BCG, Bain, boutiques locales.\n"
            "- Consultoría tributaria y legal: PwC, Deloitte, KPMG, EY + estudios legales.\n"
            "- Consultoría tecnológica: Accenture, Deloitte Digital, Globant, IBM Consulting, firmas locales.\n"
            "- Consultoría de RRHH y compensaciones: Mercer, Korn Ferry, locales."
        ),
        "how_makes_money": (
            "Facturación por hora, por proyecto (fee fijo), o por retainer "
            "(mensualidad continua). Márgenes altos (30-50% en firmas "
            "establecidas) pero intensivo en talento senior. La pirámide "
            "típica: pocos partners (muy caros, traen el negocio), muchos "
            "senior/juniors (ejecutan). Utilización (% horas facturables del "
            "consultor) es el KPI principal."
        ),
        "what_sells": (
            "Diagnósticos, estrategia, implementación, optimización de "
            "procesos, defensa legal, planeamiento tributario, evaluaciones, "
            "due diligence, rediseños organizacionales, implementaciones "
            "tecnológicas."
        ),
        "sells_to": (
            "Casi exclusivamente B2B. Clientes típicos: directorios de "
            "empresas grandes, CFOs, CHROs, legal counsels, CEOs de "
            "mid-market, gobiernos (procesos licitados). Interlocutores son "
            "casi siempre decisores senior con presupuesto propio."
        ),
        "buys_to_operate": (
            "- Talento senior (la variable dominante de costo — socios ganan 6-7 dígitos USD anuales en firmas grandes).\n"
            "- Herramientas de colaboración, project management, análisis de datos.\n"
            "- Software vertical específico (SAP, Oracle para consultorías que implementan ERPs).\n"
            "- Espacios de oficina premium (el entorno vende).\n"
            "- Suscripciones a bases de datos, reports, benchmarks (acceso a información).\n"
            "- Servicios de marketing B2B y content (cómo posicionan su expertise)."
        ),
        "dynamics": (
            "Sensible a ciclos económicos (en crisis se corta consultoría "
            "primero), venta relacional (las cuentas se ganan por confianza, "
            "no por licitación fría), estacionalidad marcada (cierre fiscal "
            "concentra trabajo tributario; planeamiento anual concentra "
            "gestión), presión creciente de consultoras boutique "
            "especializadas contra las Big Four y MBB."
        ),
        "deepen_in": (
            "Consulting Magazine — rankings anuales. Vault Guide to "
            "Consulting. HBR The Consulting Industry Transformation. [VERIFICAR]"
        ),
    },
    {
        "slug": "manufactura",
        "order_index": 6,
        "name": "Manufactura",
        "tags": ["b2b", "b2c", "capital-intensivo", "export-driven"],
        "examples": [
            "Grupo Bimbo (México — alimentos)",
            "Embraer (Brasil — aeroespacial)",
            "Cemex (México — cementera regional)",
            "Gerdau (Brasil — acero)",
            "Techint (Argentina — industrial diversificado)",
        ],
        "what_is": (
            "Empresas que producen bienes físicos a partir de materias primas "
            "e insumos — desde alimentos procesados y textiles hasta "
            "automotriz, farmacéutica, metalurgia y química. Es la columna "
            "industrial de países como México (fuerte por cercanía a EE.UU. "
            "y T-MEC) y Brasil. En otros LATAM, segmentos más específicos "
            "(textil en Perú, vinos en Argentina/Chile)."
        ),
        "how_makes_money": (
            "Modelo de volumen con márgenes medios (15-30%), dependiente de "
            "eficiencia de planta, utilización de capacidad (OEE — Overall "
            "Equipment Effectiveness) y control de costos de materia prima. "
            "Rentabilidad muy sensible a tipo de cambio (insumos importados "
            "vs ventas locales/exportadas)."
        ),
        "what_sells": (
            "Productos físicos de todo tipo — productos terminados para "
            "consumidor (B2C) o componentes/insumos para otras industrias "
            "(B2B). Cada vez más empresas manufactureras venden también "
            "servicios alrededor del producto (mantenimiento, garantías "
            "extendidas, servitization)."
        ),
        "sells_to": (
            "Mix: B2B industrial (proveedores de partes, ingredientes, "
            "insumos) o B2C (productos terminados — típicamente vía "
            "retailers). Muchas manufactureras LATAM exportan a EE.UU., "
            "Europa o Asia."
        ),
        "buys_to_operate": (
            "- Materia prima e insumos (40-60% del costo).\n"
            "- Maquinaria y equipamiento industrial (inversión periódica grande).\n"
            "- Software de planificación (ERP — SAP domina en empresas grandes, pero hay mercado grande para alternativas mid-market).\n"
            "- MES (Manufacturing Execution Systems), mantenimiento predictivo, IoT industrial.\n"
            "- Servicios de logística (para movimiento de insumos y producto terminado).\n"
            "- Energía (componente de costo importante, especialmente en industrias intensivas como metalurgia).\n"
            "- Consultoría de mejora continua (Lean, Six Sigma), compliance ambiental, automatización."
        ),
        "dynamics": (
            "Muy sensible a tipo de cambio y precios de commodities. Presión "
            "por adopción de Industria 4.0 (automatización, IoT, AI en "
            "planta). Transición energética forzada por regulación en países "
            "como Chile, Brasil. Nearshoring de EE.UU. hacia México "
            "beneficiando a manufactura mexicana. Envejecimiento de la fuerza "
            "laboral industrial es un desafío real."
        ),
        "deepen_in": (
            "CEPAL — reports sobre manufactura y productividad. OCDE "
            "Manufacturing Outlook. Deloitte Global Manufacturing "
            "Competitiveness Index. [VERIFICAR]"
        ),
    },
    {
        "slug": "mineria-energia",
        "order_index": 7,
        "name": "Minería y energía",
        "tags": ["b2b", "commodities", "regulado", "capital-intensivo"],
        "examples": [
            "Codelco (Chile — cobre, estatal)",
            "Vale (Brasil — hierro)",
            "Petrobras (Brasil — petróleo/gas)",
            "YPF (Argentina)",
            "SQM (Chile — litio)",
            "Southern Copper (regional)",
        ],
        "what_is": (
            "Extracción y procesamiento de recursos naturales. LATAM es una "
            "potencia mundial en minería (cobre en Chile y Perú, litio en "
            "Argentina/Chile/Bolivia — el \"triángulo del litio\", hierro en "
            "Brasil) y en energía (gas en Argentina, petróleo en Brasil, "
            "hidroelectricidad en múltiples países). Generan una porción "
            "significativa del PIB y exportaciones regionales."
        ),
        "how_makes_money": (
            "- Minería: extracción → procesamiento → venta internacional, con márgenes altamente correlacionados al precio internacional de commodities (hay ciclos de 5-10 años de boom/caída).\n"
            "- Energía: venta regulada de electricidad, gas y combustibles, con márgenes estables pero bajos; empresas integradas (que combinan generación + distribución) tienen márgenes mejores."
        ),
        "what_sells": (
            "Minerales (cobre, oro, plata, litio, hierro), combustibles "
            "(petróleo crudo, gas natural, derivados), electricidad "
            "(generación, transmisión, distribución), y cada vez más energías "
            "renovables (solar, eólica — boom en Chile, Argentina, Brasil)."
        ),
        "sells_to": (
            "Dominantemente B2B, con exportación internacional fuerte. "
            "Minería vende a refinadoras y manufactureras globales. Energía "
            "vende a distribuidoras, industria y consumidor final (regulado)."
        ),
        "buys_to_operate": (
            "- Maquinaria pesada (camiones mineros, perforadoras, palas — inversiones de millones de USD por unidad).\n"
            "- Equipamiento industrial especializado y repuestos.\n"
            "- Servicios de ingeniería y consultoría técnica (muy intensivos).\n"
            "- Software de planificación de mina, modelado geológico, simulación.\n"
            "- Servicios ambientales y de compliance regulatorio (pesado en ambos sectores).\n"
            "- Mantenimiento, monitoreo predictivo, IoT.\n"
            "- Logística especializada (transporte de minerales, combustibles).\n"
            "- Energía, agua, y todos los servicios habilitantes."
        ),
        "dynamics": (
            "Ciclos largos de precios de commodities dictan inversión y "
            "expansión. Presión regulatoria ambiental creciente (licencias "
            "sociales, conflictos con comunidades). Transición energética "
            "reordena prioridades: caída gradual de carbón e hidrocarburos, "
            "subida del litio, cobre y energías renovables. Alta intensidad "
            "de capital y horizonte largo de proyectos (5-10 años de lead "
            "time para una mina nueva)."
        ),
        "deepen_in": (
            "SNL Metals & Mining / S&P Global reports. Wood Mackenzie LATAM "
            "Energy Outlook. CEPAL Recursos Naturales y Desarrollo. [VERIFICAR]"
        ),
    },
    {
        "slug": "agroindustria",
        "order_index": 8,
        "name": "Agroindustria",
        "tags": ["b2b", "commodities", "export-driven", "clima-sensible"],
        "examples": [
            "JBS (Brasil — carne)",
            "Bunge (regional)",
            "Cresud (Argentina)",
            "Camposol (Perú — frutas)",
            "Viña Concha y Toro (Chile)",
        ],
        "what_is": (
            "Producción, procesamiento, distribución y exportación de "
            "productos agropecuarios. LATAM es una potencia agrícola global — "
            "Brasil y Argentina lideran soja, carne y granos; Perú y Chile en "
            "frutas y hortalizas exportables; México en productos tropicales. "
            "Un sector muy presente en el PIB de varios países (Brasil >20% "
            "combinando upstream y downstream)."
        ),
        "how_makes_money": (
            "- Producción primaria: rendimiento por hectárea × precio internacional - costos de producción. Márgenes muy variables (negativos en malas cosechas, altos en buenas).\n"
            "- Procesamiento/industrialización: margen de transformación agregado (moler trigo, empacar fruta, procesar carne).\n"
            "- Exportación: margen de comercialización + logística + hedging de tipo de cambio."
        ),
        "what_sells": (
            "Commodities (soja, maíz, trigo, carne), productos frescos "
            "(frutas, hortalizas, flores), alimentos procesados, productos "
            "lácteos, bebidas (vino, cerveza), proteínas animales."
        ),
        "sells_to": (
            "B2B en toda la cadena: traders internacionales (Cargill, Bunge, "
            "ADM), industrias de alimentos, distribuidores, retailers. El "
            "consumidor final llega al producto vía supermercado o retail."
        ),
        "buys_to_operate": (
            "- Semillas, fertilizantes, agroquímicos (inputs dominantes — mercado gigante para Bayer, Syngenta, Corteva).\n"
            "- Maquinaria agrícola (tractores, cosechadoras — John Deere, AGCO dominan).\n"
            "- AgTech: software de gestión de campo, sensores IoT, imágenes satelitales, drones, precision agriculture.\n"
            "- Servicios financieros específicos: crédito de campaña, seguros agrícolas, coberturas de precio (hedging).\n"
            "- Logística especializada (cadena de frío, transporte bulk).\n"
            "- Certificaciones (orgánico, comercio justo, trazabilidad) cada vez más exigidas por importadores."
        ),
        "dynamics": (
            "Sensibilidad extrema al clima (sequías, heladas, inundaciones — "
            "cada vez más presentes por cambio climático). Precios "
            "internacionales volátiles. Regulación ambiental creciente "
            "(deforestación, uso de agroquímicos). Tendencia fuerte de "
            "adopción de AgTech (los productores están entre los más "
            "tech-hungry del mundo actualmente). Exportación altamente "
            "dependiente de logística y puertos eficientes."
        ),
        "deepen_in": (
            "FAO (Organización para la Alimentación y la Agricultura) — datos "
            "por país. USDA Foreign Agricultural Service — reports sobre "
            "LATAM. AgFunder reports. [VERIFICAR última edición]"
        ),
    },
    {
        "slug": "marketing-medios",
        "order_index": 9,
        "name": "Marketing, medios y publicidad",
        "tags": ["b2b", "talento-intensivo", "alta-rotacion", "disrupcion-ia"],
        "examples": [
            "Grupo Gallup (regional)",
            "Ogilvy LATAM",
            "Publicis",
            "Grupo Globo (Brasil — medios tradicionales)",
            "Grupo Clarín (Argentina)",
            "TelevisaUnivision (México)",
        ],
        "what_is": (
            "Industria que ayuda a otras empresas a captar clientes y "
            "construir marca. Incluye agencias de publicidad y marketing "
            "digital, medios tradicionales (TV, radio, prensa, revistas) y "
            "medios digitales (portales, plataformas, creadores de "
            "contenido). La transformación digital reordenó el sector — "
            "medios tradicionales siguen existiendo pero perdiendo share, "
            "mientras que digital y performance crecen."
        ),
        "how_makes_money": (
            "- Agencias: fee fijo + comisiones por medios + retainers mensuales. Márgenes medios (15-30%), dependientes de talento.\n"
            "- Medios: venta de espacios publicitarios (impresiones, clicks, CPM/CPC). Márgenes altos en digital cuando hay escala, bajos o negativos en medios tradicionales en decline.\n"
            "- Plataformas (Meta, Google): comisión por transacción publicitaria, márgenes altísimos por la escala."
        ),
        "what_sells": (
            "Estrategia de marca, campañas creativas, producción audiovisual, "
            "gestión de redes sociales, SEO/SEM, compra programática, "
            "planeamiento de medios, publishing, influencer marketing, "
            "analytics, branding corporativo, eventos."
        ),
        "sells_to": (
            "Casi exclusivamente B2B. Clientes son empresas de todos los "
            "sectores — retail y consumo masivo son los mayores gastadores, "
            "pero fintech y tech están creciendo fuerte. Interlocutores: "
            "CMOs, Brand Managers, Directores de Marketing."
        ),
        "buys_to_operate": (
            "- Talento: creativos, community managers, performance specialists, data analysts. Muy alta rotación.\n"
            "- Herramientas: plataformas de gestión (Hubspot, Marketo, Active Campaign), creativos (Adobe Creative Suite, Figma), analytics (GA4, Looker), social media management (Hootsuite, Buffer).\n"
            "- Compra de medios: presupuestos de clientes se canalizan a Meta/Google/TikTok (las agencias son intermediarias).\n"
            "- Producción audiovisual: estudios, talento, equipos, locaciones.\n"
            "- Servicios profesionales: legal (contratos con talentos, derechos de imagen), contable.\n"
            "- Espacios de trabajo."
        ),
        "dynamics": (
            "Disrupción acelerada por AI generativa (DALL-E, Midjourney, "
            "ChatGPT) que cambia cómo se produce contenido. Consolidación de "
            "plataformas (Meta, Google, TikTok capturan ~60% del gasto "
            "digital en LATAM). Creadores de contenido tomando parte del "
            "mercado. Regulación creciente sobre privacidad de datos y "
            "menores. Polarización política afecta presupuesto corporativo "
            "(empresas temen controversia)."
        ),
        "deepen_in": (
            "IAB LATAM (Interactive Advertising Bureau) — reports regionales. "
            "Kantar Media. eMarketer LATAM Digital Ad Spending. [VERIFICAR]"
        ),
    },
    {
        "slug": "salud-farmaceutica",
        "order_index": 10,
        "name": "Salud y farmacéutica (incluye distribución)",
        "tags": ["b2b", "regulado", "ticket-alto", "ciclo-largo"],
        "examples": [
            "DKT (regional, distribuidor)",
            "Marzam (México, distribuidor)",
            "Drogueria del Sur (Colombia)",
            "Drogueria La Sante",
            "Bagó (Argentina, regional)",
            "Roemmers",
            "Eurofarma (Brasil, regional)",
            "Genfar (Colombia)",
            "Andreani Pharma (Argentina — logística especializada)",
            "Mavi (México — logística especializada)",
        ],
        "what_is": (
            "Tres modalidades superpuestas en LATAM: (1) laboratorios "
            "productores (Roche, Bayer, Sanofi, Boehringer + locales como "
            "Bagó, Roemmers, Genfar) — venden medicamentos a distribuidores "
            "y a cadenas. (2) Distribuidores farmacéuticos (DKT, Marzam, "
            "Drogueria La Sante, Drogueria del Norte, Eurofarma distribución) "
            "— compran a laboratorios, venden a farmacias minoristas y "
            "hospitales. (3) Cadenas de farmacias y hospitales — venden al "
            "usuario final. Outbound B2B suele apuntar a (1) y (2), no a la "
            "cadena minorista."
        ),
        "how_makes_money": (
            "Tickets desde USD 30K-150K anuales para SaaS de gestión / "
            "trazabilidad / distribución. Implementaciones largas (3-12 "
            "meses según complejidad de integración con ERP existente — SAP "
            "es estándar). Ciclos de compra 3-6 meses típicos por la "
            "combinación de stakeholders + due diligence regulatoria."
        ),
        "what_sells": (
            "Medicamentos (laboratorios), distribución y logística "
            "especializada (distribuidores), software de trazabilidad / "
            "gestión / cadena de frío / cumplimiento regulatorio (vendors "
            "B2B que apuntan a la cadena)."
        ),
        "sells_to": (
            "VP de Operaciones o Director de Cadena de Suministro suelen ser "
            "los KDM operativos. Gerente de Cumplimiento Regulatorio es "
            "co-decisor casi siempre — y a veces disparador único del proceso "
            "cuando hay presión regulatoria activa. CFO valida ticket. En "
            "distribuidores grandes, el COO decide. En laboratorios, suele "
            "entrar el Director Médico para validar componentes técnicos."
        ),
        "buys_to_operate": (
            "Drivers de compra: cumplimiento regulatorio (COFEPRIS México, "
            "INVIMA Colombia, DIGEMID Perú, ANMAT Argentina, ANVISA Brasil) "
            "— driver #1 desde 2023, y creciente. Trazabilidad obligatoria "
            "(seriación, retiros de mercado). Cadena de frío (sensores IoT + "
            "alertas) en biológicos y vacunas. Eficiencia operativa (control "
            "de inventario en tiempo real, integración con ERP). Reducción "
            "de pérdidas por vencimientos.\n\n"
            "Frenos: aversión a interrumpir la operación — un fallo de 1 día "
            "en distribución farmacéutica afecta abastecimiento crítico. "
            "Inversión en sistemas legacy (SAP + Oracle + planillas Excel) "
            "que llevan años configurados. Resistencia regulatoria a cambios "
            "sin validación previa. Burocracia interna — comités de "
            "aprobación de cambios de proveedor que toman semanas."
        ),
        "dynamics": (
            "Menos estacional que retail. Pero sí hay ciclos de auditoría "
            "regulatoria (auditorías sorpresa de COFEPRIS/INVIMA/DIGEMID "
            "típicamente concentradas en Q2 y Q4) y picos de stock antes de "
            "cierre fiscal. Compras grandes suelen aprobarse Q1 (presupuesto "
            "fresco) o Q4 (uso de partidas remanentes).\n\n"
            "Vocabulario / KPIs típicos: trazabilidad de lotes, seriación, "
            "cadena de frío, retiros de mercado (recall management), DSO "
            "(days sales outstanding) en distribuidores, OTIF "
            "(on-time-in-full delivery), inventory turn, expiry rate (% de "
            "mercadería por vencer), compliance score, validación regulatoria.\n\n"
            "Señales de timing: auditorías recientes con observaciones "
            "(= dolor activo). Multas o sanciones públicas. Anuncio de "
            "expansión a nuevo país (= necesita compliance del nuevo "
            "regulador). Nuevo Gerente de Cumplimiento contratado. Inversión "
            "/ ronda de capital reciente. Cambio en regulación regional (ej. "
            "nueva exigencia de seriación en Perú DIGEMID 2024-2025 disparó "
            "ola de proyectos)."
        ),
        "deepen_in": (
            "ALAFARPE (Asociación Latinoamericana de Industrias "
            "Farmacéuticas) — reports regionales. IQVIA LATAM Pharma "
            "Outlook. Cámaras nacionales (CILFA Argentina, AMIIF México, "
            "Asinfar Colombia). Organismos regulatorios oficiales (COFEPRIS, "
            "INVIMA, DIGEMID, ANMAT, ANVISA). [VERIFICAR]"
        ),
    },
]


TRANSLATABLE_FIELDS = (
    "name",
    "what_is",
    "how_makes_money",
    "what_sells",
    "sells_to",
    "buys_to_operate",
    "dynamics",
    "deepen_in",
)


def _upsert(db, entry: dict) -> IndustryCard:
    card = (
        db.query(IndustryCard).filter(IndustryCard.slug == entry["slug"]).first()
    )
    if card is None:
        card = IndustryCard(
            slug=entry["slug"],
            order_index=entry["order_index"],
            examples=entry.get("examples"),
            tags=entry.get("tags"),
        )
        db.add(card)
        db.flush()
    else:
        card.order_index = entry["order_index"]
        card.examples = entry.get("examples")
        card.tags = entry.get("tags")

    es = next((t for t in card.translations if t.locale == "es"), None)
    payload = {f: entry.get(f) for f in TRANSLATABLE_FIELDS}
    if es is None:
        db.add(IndustryCardTranslation(industry_card_id=card.id, locale="es", **payload))
    else:
        for f, v in payload.items():
            setattr(es, f, v)
    return card


def run() -> None:
    with SessionLocal() as db:
        for entry in INDUSTRIES:
            _upsert(db, entry)
        db.commit()
        total = db.query(IndustryCard).count()
        log.info("seed_library_industries.done", extra={"total": total})


if __name__ == "__main__":
    run()
