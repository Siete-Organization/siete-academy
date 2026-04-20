import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { api } from "@/lib/api";

type CountsByStatus = Record<string, number>;

export function AdminAnalytics() {
  const { t } = useTranslation();
  const [metrics, setMetrics] = useState<{
    applications: number;
    applicationsByStatus: CountsByStatus;
    pendingReviews: number;
    candidates: number;
    candidatesByStage: CountsByStatus;
  } | null>(null);

  useEffect(() => {
    void (async () => {
      const [apps, pending, candidates] = await Promise.all([
        api.get<Array<{ status: string }>>("/applications"),
        api.get<unknown[]>("/assessments/submissions/pending"),
        api.get<Array<{ stage: string }>>("/placement/candidates"),
      ]);
      const countsBy = <T extends { [k: string]: unknown }>(
        arr: T[],
        key: keyof T,
      ): CountsByStatus =>
        arr.reduce<CountsByStatus>((acc, row) => {
          const k = String(row[key]);
          acc[k] = (acc[k] || 0) + 1;
          return acc;
        }, {});

      setMetrics({
        applications: apps.data.length,
        applicationsByStatus: countsBy(apps.data, "status"),
        pendingReviews: pending.data.length,
        candidates: candidates.data.length,
        candidatesByStage: countsBy(candidates.data, "stage"),
      });
    })();
  }, []);

  if (!metrics) {
    return <div className="container-editorial py-24 text-ink-muted">{t("common.loading")}</div>;
  }

  const placed = metrics.candidatesByStage["placed"] || 0;
  const approved = metrics.candidatesByStage["approved"] || 0;

  const kpis = [
    { label: t("analytics.applications"), value: metrics.applications },
    { label: t("analytics.pendingReviews"), value: metrics.pendingReviews },
    { label: t("analytics.graduates"), value: approved + placed },
    { label: t("analytics.placed"), value: placed },
  ];

  return (
    <div className="container-editorial py-16 md:py-24 space-y-14">
      <header>
        <p className="num-label">Admin</p>
        <h1 className="font-display text-display-lg mt-3">{t("analytics.title")}</h1>
      </header>

      <section className="grid grid-cols-2 md:grid-cols-4 gap-y-10 gap-x-6 hairline pt-10">
        {kpis.map((k) => (
          <div key={k.label}>
            <p className="num-label">{k.label}</p>
            <p className="font-display text-5xl tabular-nums mt-2">{k.value}</p>
          </div>
        ))}
      </section>

      <section className="grid grid-cols-1 md:grid-cols-2 gap-12 hairline pt-10">
        <div>
          <p className="num-label mb-4">Aplicaciones por estado</p>
          <StatusBars counts={metrics.applicationsByStatus} />
        </div>
        <div>
          <p className="num-label mb-4">Candidatos por etapa</p>
          <StatusBars counts={metrics.candidatesByStage} />
        </div>
      </section>
    </div>
  );
}

function StatusBars({ counts }: { counts: Record<string, number> }) {
  const total = Object.values(counts).reduce((s, n) => s + n, 0) || 1;
  const entries = Object.entries(counts).sort(([, a], [, b]) => b - a);
  if (entries.length === 0) return <p className="text-ink-muted text-sm">—</p>;
  return (
    <ol className="space-y-3">
      {entries.map(([k, n]) => {
        const pct = Math.round((n / total) * 100);
        return (
          <li key={k} className="grid grid-cols-[140px_1fr_60px] gap-3 items-center">
            <span className="text-sm text-ink-soft truncate">{k}</span>
            <span className="h-1 bg-bone overflow-hidden">
              <span
                className="block h-full bg-ink"
                style={{ width: `${pct}%` }}
              />
            </span>
            <span className="font-mono text-xs tabular-nums text-right">
              {n} · {pct}%
            </span>
          </li>
        );
      })}
    </ol>
  );
}
