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
          {t("home.eyebrow")}
        </p>
        <h1
          className="font-display text-display-xl mt-6 max-w-5xl text-balance animate-fade-up"
          style={{ animationDelay: "140ms" }}
        >
          {t("home.heroLine1")}
          <br />
          <span className="relative inline-block">
            {t("home.heroLine2")}
            <span
              className="absolute inset-x-0 -bottom-2 h-[3px] bg-ember origin-left animate-stroke-in"
              style={{ animationDelay: "900ms" }}
            />
          </span>
        </h1>

        <div
          className="grid grid-cols-1 md:grid-cols-12 gap-8 mt-14 animate-fade-up"
          style={{ animationDelay: "300ms" }}
        >
          <p className="md:col-span-7 text-lg text-ink-soft leading-relaxed text-pretty">
            {t("home.heroPitch")}
          </p>
          <aside className="md:col-span-4 md:col-start-9 border-l-2 border-ember pl-6 flex flex-col gap-3">
            <p className="eyebrow">{t("home.whatToExpect")}</p>
            {(t("home.expectList", { returnObjects: true }) as string[]).map((item, i) => (
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
            <Button size="lg" variant="ember">
              {t("home.ctaApply")}
              <span aria-hidden>→</span>
            </Button>
          </Link>
          <p className="font-mono text-xs text-ink-muted">{t("home.ctaFine")}</p>
        </div>
      </section>

      {/* Curriculum preview */}
      <section className="hairline pt-16 pb-24">
        <div className="flex items-baseline justify-between mb-10">
          <h2 className="font-display text-display-md">{t("home.curriculumTitle")}</h2>
          <p className="num-label">{t("home.curriculumMeta")}</p>
        </div>

        <ol className="divide-y divide-bone border-y border-bone">
          {(t("home.modules", { returnObjects: true }) as {
            n: string;
            t: string;
            d: string;
            w: string;
          }[]).map((m) => (
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
          {(t("home.stats", { returnObjects: true }) as { k: string; v: string }[]).map((s) => (
            <div key={s.k} className="flex flex-col">
              <span className="font-display text-5xl tabular-nums font-black">{s.k}</span>
              <span className="text-xs text-ink-muted mt-3 max-w-[16ch]">{s.v}</span>
            </div>
          ))}
        </div>
      </section>

      {/* CTA */}
      <section className="hairline py-20">
        <div className="flex flex-col md:flex-row items-start md:items-end justify-between gap-8">
          <div>
            <p className="eyebrow">{t("home.finalEyebrow")}</p>
            <p className="font-display text-display-md mt-3 max-w-2xl text-balance font-bold">
              {t("home.finalTagline")}
            </p>
          </div>
          <Link to="/apply">
            <Button size="lg" variant="ember">
              {t("home.ctaApply")} <span aria-hidden>→</span>
            </Button>
          </Link>
        </div>
      </section>
    </div>
  );
}
