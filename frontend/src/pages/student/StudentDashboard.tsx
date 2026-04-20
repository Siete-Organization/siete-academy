import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { Link } from "react-router-dom";
import { api } from "@/lib/api";
import { useAuth } from "@/lib/auth-context";

interface Enrollment {
  id: number;
  cohort_id: number;
  status: string;
  progress_pct: number;
}

interface ModuleWindow {
  id: number;
  cohort_id: number;
  module_id: number;
  opens_at: string;
  closes_at: string;
  live_session_at: string | null;
}

export function StudentDashboard() {
  const { t, i18n } = useTranslation();
  const { me } = useAuth();
  const [enrollments, setEnrollments] = useState<Enrollment[] | null>(null);
  const [windowsByCohort, setWindowsByCohort] = useState<Record<number, ModuleWindow[]>>({});

  useEffect(() => {
    const controller = new AbortController();
    void (async () => {
      try {
        const { data } = await api.get<Enrollment[]>("/enrollment/me", {
          signal: controller.signal,
        });
        setEnrollments(data);
        // Paralelizamos todos los windows y hacemos un solo setState
        const pairs = await Promise.all(
          data.map(async (e) => {
            const res = await api.get<ModuleWindow[]>(
              `/cohorts/${e.cohort_id}/windows`,
              { signal: controller.signal },
            );
            return [e.cohort_id, res.data] as const;
          }),
        );
        setWindowsByCohort(Object.fromEntries(pairs));
      } catch (err) {
        // Abortos al desmontar no son errores
        if ((err as { code?: string })?.code !== "ERR_CANCELED") throw err;
      }
    })();
    return () => controller.abort();
  }, []);

  if (enrollments === null) {
    return <div className="container-editorial py-24 text-ink-muted">{t("common.loading")}</div>;
  }

  if (enrollments.length === 0) {
    return (
      <div className="container-editorial py-28 max-w-2xl">
        <p className="num-label">Pendiente</p>
        <h1 className="font-display text-display-lg mt-4 text-balance">
          Aún no tienes una cohorte asignada.
        </h1>
        <p className="text-ink-soft mt-6 leading-relaxed">
          {t("student.noEnrollments")} Te avisaremos por email apenas tu cupo esté listo.
        </p>
      </div>
    );
  }

  return (
    <div className="container-editorial py-16 md:py-24 space-y-16">
      <header>
        <p className="num-label">
          Bienvenido, {me?.display_name?.split(" ")[0] || "estudiante"}
        </p>
        <h1 className="font-display text-display-lg mt-4 text-balance">
          Tu <em className="italic font-light">progreso</em>.
        </h1>
      </header>

      {enrollments.map((e) => {
        const windows = windowsByCohort[e.cohort_id] || [];
        return (
          <section key={e.id} className="space-y-8">
            <div className="flex items-end justify-between hairline pt-8">
              <div>
                <p className="eyebrow">Cohorte #{String(e.cohort_id).padStart(3, "0")}</p>
                <h2 className="font-display text-display-md mt-2">8 semanas · 4 módulos</h2>
              </div>
              <div className="text-right">
                <p className="num-label mb-1">progreso</p>
                <p className="font-display text-4xl tabular-nums">
                  {e.progress_pct.toFixed(0)}
                  <span className="text-ink-faint text-2xl">%</span>
                </p>
              </div>
            </div>

            <ol className="divide-y divide-bone border-y border-bone">
              {windows.map((w, idx) => {
                const now = new Date();
                const opens = new Date(w.opens_at);
                const closes = new Date(w.closes_at);
                const isOpen = now >= opens && now <= closes;
                const isPast = now > closes;
                return (
                  <li
                    key={w.id}
                    className="grid grid-cols-12 gap-4 py-6 group items-baseline"
                  >
                    <span className="col-span-2 md:col-span-1 font-mono text-xs text-ink-faint tabular-nums">
                      {String(idx + 1).padStart(2, "0")}
                    </span>
                    <div className="col-span-10 md:col-span-6">
                      <h3 className="font-display text-2xl group-hover:text-ember transition-colors">
                        {t("student.module")} {String(idx + 1).padStart(2, "0")}
                      </h3>
                      <p className="font-mono text-[11px] uppercase tracking-[0.14em] text-ink-muted mt-2">
                        {opens.toLocaleDateString(i18n.language, {
                          day: "2-digit",
                          month: "short",
                        })}{" "}
                        →{" "}
                        {closes.toLocaleDateString(i18n.language, {
                          day: "2-digit",
                          month: "short",
                        })}
                      </p>
                      {w.live_session_at && (
                        <p className="text-xs mt-2 text-ink-soft">
                          <span className="text-ember font-medium mr-1.5">●</span>
                          {t("student.liveSession")}:{" "}
                          <span className="font-mono">
                            {new Date(w.live_session_at).toLocaleString(i18n.language, {
                              weekday: "short",
                              day: "2-digit",
                              month: "short",
                              hour: "2-digit",
                              minute: "2-digit",
                            })}
                          </span>
                        </p>
                      )}
                    </div>
                    <div className="col-span-12 md:col-span-5 md:text-right">
                      <StatusChip open={isOpen} past={isPast} />
                      {isOpen && (
                        <Link
                          to={`/student/module/${w.module_id}`}
                          className="ml-4 font-mono text-xs uppercase tracking-[0.14em] text-ink hover:text-ember transition-colors"
                        >
                          entrar →
                        </Link>
                      )}
                    </div>
                  </li>
                );
              })}
            </ol>
          </section>
        );
      })}
    </div>
  );
}

function StatusChip({ open, past }: { open: boolean; past: boolean }) {
  const { label, cls } = open
    ? { label: "En curso", cls: "border-ember text-ember bg-ember-ghost" }
    : past
      ? { label: "Cerrado", cls: "border-bone text-ink-faint" }
      : { label: "Próximo", cls: "border-bone text-ink-muted" };
  return (
    <span
      className={`inline-flex items-center px-2.5 py-1 border rounded-xs font-mono text-[10px] uppercase tracking-[0.18em] ${cls}`}
    >
      {label}
    </span>
  );
}
