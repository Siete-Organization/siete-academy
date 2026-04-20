import { Link } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { Button } from "@/components/ui/button";

export function HomePage() {
  const { t } = useTranslation();
  return (
    <div className="container-editorial relative">
      {/* Hero */}
      <section className="pt-20 pb-28 md:pt-32 md:pb-40 relative">
        <p className="num-label animate-fade-up" style={{ animationDelay: "60ms" }}>
          № 001 · cohorte mayo 2026
        </p>
        <h1
          className="font-display text-display-xl mt-6 max-w-5xl text-balance animate-fade-up"
          style={{ animationDelay: "140ms" }}
        >
          La formación <em className="italic font-light">SDR</em> que siempre
          <br />
          debió <span className="relative inline-block">
            existir
            <span
              className="absolute inset-x-0 -bottom-2 h-[3px] bg-ember origin-left animate-stroke-in"
              style={{ animationDelay: "900ms" }}
            />
          </span>
          .
        </h1>

        <div
          className="grid grid-cols-1 md:grid-cols-12 gap-8 mt-14 animate-fade-up"
          style={{ animationDelay: "300ms" }}
        >
          <p className="md:col-span-7 text-lg text-ink-soft leading-relaxed text-pretty">
            Hecho por <strong className="font-semibold">Siete</strong> — la agencia de prospección
            que ha enviado más de <span className="font-mono">4.2M</span> de emails
            profesionales en LatAm. Formamos SDRs durante ocho semanas con contenido
            on-demand, sesiones en vivo, ejercicios en equipo, y un examen práctico real
            frente al equipo comercial de Siete. Los que pasan, se colocan.
          </p>
          <aside className="md:col-span-4 md:col-start-9 border-l border-bone pl-6 flex flex-col gap-3">
            <p className="eyebrow">Qué esperar</p>
            {[
              "4 módulos · 2 semanas c/u",
              "3h en vivo al cierre de cada módulo",
              "Ejercicios en equipo breakout",
              "Examen práctico en Siete",
              "Placement con clientes reales",
            ].map((item, i) => (
              <div key={item} className="flex items-baseline gap-3 text-[13px]">
                <span className="font-mono text-[10px] text-ink-faint tabular-nums">
                  {String(i + 1).padStart(2, "0")}
                </span>
                <span className="text-ink-soft">{item}</span>
              </div>
            ))}
          </aside>
        </div>

        <div
          className="flex flex-wrap items-center gap-5 mt-16 animate-fade-up"
          style={{ animationDelay: "460ms" }}
        >
          <Link to="/apply">
            <Button size="lg">
              Aplica a la cohorte
              <span aria-hidden>→</span>
            </Button>
          </Link>
          <p className="font-mono text-xs text-ink-muted">
            Filtrado personal · 100% gratis · plazas limitadas
          </p>
        </div>
      </section>

      {/* Curriculum preview */}
      <section className="hairline pt-16 pb-24">
        <div className="flex items-baseline justify-between mb-10">
          <h2 className="font-display text-display-md">El currículum</h2>
          <p className="num-label">4 módulos · 8 semanas</p>
        </div>

        <ol className="divide-y divide-bone border-y border-bone">
          {[
            {
              n: "01",
              t: "Modelos de negocio",
              d: "Cómo se gana dinero en B2B. Recurring vs. transaccional, pricing, funding, métricas.",
              w: "semana 1–2",
            },
            {
              n: "02",
              t: "Ideal Customer Profile",
              d: "Del buyer persona al ICP utilitario. Segmentación por señales reales, no por intuición.",
              w: "semana 3–4",
            },
            {
              n: "03",
              t: "Metodología SDR",
              d: "Cadencias, discovery, qualification frameworks, manejo de respuestas y seguimiento.",
              w: "semana 5–6",
            },
            {
              n: "04",
              t: "Herramientas & Cold Calling",
              d: "Stack técnico real de prospección. Tu primera llamada frente al equipo de Siete.",
              w: "semana 7–8",
            },
          ].map((m) => (
            <li key={m.n} className="grid grid-cols-12 gap-4 py-7 group">
              <span className="col-span-1 font-mono text-xs text-ink-faint tabular-nums mt-1">
                {m.n}
              </span>
              <div className="col-span-12 md:col-span-7 -mt-1">
                <h3 className="font-display text-2xl group-hover:text-ember transition-colors">
                  {m.t}
                </h3>
                <p className="text-ink-soft mt-2 text-pretty">{m.d}</p>
              </div>
              <span className="hidden md:block col-span-4 text-right num-label mt-2">{m.w}</span>
            </li>
          ))}
        </ol>
      </section>

      {/* Social / numbers */}
      <section className="py-24">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-y-12 gap-x-8">
          {[
            { k: "4.2M", v: "emails profesionales enviados" },
            { k: "180+", v: "clientes B2B activos" },
            { k: "70/30", v: "on-demand vs. en vivo" },
            { k: "0 $", v: "costo para la cohorte 001" },
          ].map((s) => (
            <div key={s.k} className="flex flex-col">
              <span className="font-display text-5xl tracking-editorial tabular-nums">{s.k}</span>
              <span className="text-xs text-ink-muted mt-3 max-w-[16ch]">{s.v}</span>
            </div>
          ))}
        </div>
      </section>

      {/* CTA */}
      <section className="hairline py-20">
        <div className="flex flex-col md:flex-row items-start md:items-end justify-between gap-8">
          <div>
            <p className="eyebrow">Aplicaciones abiertas</p>
            <p className="font-display text-display-md mt-3 max-w-2xl text-balance">
              Si crees que tienes lo que se necesita, <em>demuéstralo.</em>
            </p>
          </div>
          <Link to="/apply">
            <Button size="lg" variant="ember">
              Aplicar ahora <span aria-hidden>→</span>
            </Button>
          </Link>
        </div>
      </section>
    </div>
  );
}
