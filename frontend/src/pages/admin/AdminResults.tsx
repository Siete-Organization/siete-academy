import { useEffect, useMemo, useState } from "react";
import { useTranslation } from "react-i18next";
import { api } from "@/lib/api";
import { cn } from "@/lib/utils";

interface Cohort {
  id: number;
  name: string;
  status: string;
}

interface ModuleHeader {
  id: number;
  title: string | null;
  order_index: number;
}

interface ModuleResult {
  module_id: number;
  module_title: string | null;
  order_index: number;
  capa_1_scores: (number | null)[];
  capa_1_avg: number | null;
  capa_2_mcq: number | null;
  capa_2_video: number | null;
  capa_2_score: number | null;
}

interface FinalResult {
  case: number | null;
  video: number | null;
  score: number | null;
}

interface StudentResult {
  user_id: number;
  name: string | null;
  email: string;
  modules: ModuleResult[];
  final: FinalResult;
  course_total: number | null;
  status: "distinction" | "basic" | "failing" | "in_progress";
}

interface CohortResults {
  cohort_id: number;
  modules: ModuleHeader[];
  students: StudentResult[];
}

const STATUS_STYLES: Record<StudentResult["status"], string> = {
  distinction: "bg-emerald-50 text-emerald-900 border-emerald-200",
  basic: "bg-amber-50 text-amber-900 border-amber-200",
  failing: "bg-rose-50 text-rose-900 border-rose-200",
  in_progress: "bg-bone/50 text-ink-muted border-bone",
};

export function AdminResults() {
  const { t, i18n } = useTranslation();
  const [cohorts, setCohorts] = useState<Cohort[]>([]);
  const [selectedId, setSelectedId] = useState<number | null>(null);
  const [results, setResults] = useState<CohortResults | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    void (async () => {
      const { data } = await api.get<Cohort[]>("/cohorts");
      setCohorts(data);
      if (data.length > 0 && selectedId === null) {
        setSelectedId(data[0].id);
      }
    })();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    if (selectedId === null) {
      setResults(null);
      return;
    }
    setLoading(true);
    void (async () => {
      try {
        const { data } = await api.get<CohortResults>("/grading/results", {
          params: { cohort_id: selectedId, locale: i18n.language.slice(0, 2) },
        });
        setResults(data);
      } finally {
        setLoading(false);
      }
    })();
  }, [selectedId, i18n.language]);

  const moduleHeaders = results?.modules ?? [];

  return (
    <div className="container-editorial py-16 space-y-12">
      <header>
        <p className="num-label">{t("adminResults.eyebrow")}</p>
        <h1 className="font-display text-display-md mt-3">
          {t("adminResults.title")}
        </h1>
      </header>

      <section className="flex flex-wrap items-end gap-6">
        <div>
          <label className="num-label block mb-2">
            {t("adminResults.selectCohort")}
          </label>
          {cohorts.length === 0 ? (
            <p className="text-ink-muted text-sm">
              {t("adminResults.noCohorts")}
            </p>
          ) : (
            <select
              value={selectedId ?? ""}
              onChange={(e) => setSelectedId(Number(e.target.value))}
              className="border border-bone bg-paper px-3 py-2 text-sm"
            >
              {cohorts.map((c) => (
                <option key={c.id} value={c.id}>
                  {c.name}
                </option>
              ))}
            </select>
          )}
        </div>

        <Legend />
      </section>

      {loading && <p className="text-ink-muted">{t("common.loading")}</p>}

      {!loading && results && results.students.length === 0 && (
        <p className="text-ink-muted">{t("adminResults.noStudents")}</p>
      )}

      {!loading && results && results.students.length > 0 && (
        <ResultsTable
          modules={moduleHeaders}
          students={results.students}
          t={t}
        />
      )}
    </div>
  );
}

function Legend() {
  const { t } = useTranslation();
  const items: { label: string; cls: string }[] = [
    { label: t("adminResults.legendDistinction"), cls: scoreTone(90) },
    { label: t("adminResults.legendBasic"), cls: scoreTone(70) },
    { label: t("adminResults.legendBelow"), cls: scoreTone(50) },
    { label: t("adminResults.legendMissing"), cls: scoreTone(null) },
  ];
  return (
    <div>
      <p className="num-label mb-2">{t("adminResults.legendTitle")}</p>
      <div className="flex flex-wrap gap-3">
        {items.map((it) => (
          <span
            key={it.label}
            className={cn(
              "text-xs px-2 py-1 border tabular-nums",
              it.cls,
            )}
          >
            {it.label}
          </span>
        ))}
      </div>
    </div>
  );
}

function ResultsTable({
  modules,
  students,
  t,
}: {
  modules: ModuleHeader[];
  students: StudentResult[];
  t: (key: string, options?: Record<string, unknown>) => string;
}) {
  // Stable module order
  const sortedModules = useMemo(
    () => [...modules].sort((a, b) => a.order_index - b.order_index),
    [modules],
  );

  return (
    <div className="overflow-x-auto border border-bone">
      <table className="min-w-full text-sm">
        <thead className="bg-paper-tint">
          <tr className="border-b border-bone">
            <th className="sticky left-0 z-10 bg-paper-tint px-4 py-3 text-left num-label">
              {t("adminResults.colStudent")}
            </th>
            {sortedModules.map((m, idx) => (
              <th
                key={m.id}
                colSpan={2}
                className="px-3 py-3 text-center num-label border-l border-bone"
                title={m.title ?? ""}
              >
                {t("adminResults.moduleN", { n: idx + 1 })}
              </th>
            ))}
            <th className="px-3 py-3 text-center num-label border-l border-bone">
              {t("adminResults.colFinal")}
            </th>
            <th className="px-3 py-3 text-center num-label border-l border-bone">
              {t("adminResults.colCourse")}
            </th>
            <th className="px-3 py-3 text-left num-label border-l border-bone">
              {t("adminResults.colStatus")}
            </th>
          </tr>
          <tr className="border-b border-bone bg-paper-tint/60 text-[10px] uppercase tracking-[0.12em] text-ink-faint">
            <th className="sticky left-0 z-10 bg-paper-tint/60 px-4 py-2" />
            {sortedModules.map((m) => (
              <SubHeader key={m.id} t={t} />
            ))}
            <th className="px-3 py-2 border-l border-bone" />
            <th className="px-3 py-2 border-l border-bone" />
            <th className="px-3 py-2 border-l border-bone" />
          </tr>
        </thead>
        <tbody>
          {students.map((s) => (
            <tr key={s.user_id} className="border-b border-bone last:border-b-0">
              <td className="sticky left-0 z-10 bg-paper px-4 py-3">
                <div className="font-medium text-ink">{s.name || s.email}</div>
                <div className="text-xs text-ink-muted">{s.email}</div>
              </td>
              {sortedModules.map((m) => {
                const mr = s.modules.find((x) => x.module_id === m.id);
                return (
                  <ModuleCells key={m.id} mr={mr ?? null} />
                );
              })}
              <ScoreCell value={s.final.score} />
              <ScoreCell value={s.course_total} bold />
              <td className="px-3 py-3 border-l border-bone">
                <StatusBadge status={s.status} t={t} />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function SubHeader({
  t,
}: {
  t: (key: string, options?: Record<string, unknown>) => string;
}) {
  return (
    <>
      <th className="px-3 py-2 text-center border-l border-bone">
        {t("adminResults.colMicros")}
      </th>
      <th className="px-3 py-2 text-center">{t("adminResults.colModule")}</th>
    </>
  );
}

function ModuleCells({ mr }: { mr: ModuleResult | null }) {
  return (
    <>
      <ScoreCell value={mr?.capa_1_avg ?? null} subtle />
      <ScoreCell value={mr?.capa_2_score ?? null} />
    </>
  );
}

function ScoreCell({
  value,
  bold = false,
  subtle = false,
}: {
  value: number | null;
  bold?: boolean;
  subtle?: boolean;
}) {
  return (
    <td
      className={cn(
        "px-3 py-3 text-center tabular-nums border-l border-bone",
        scoreTone(value),
        bold && "font-semibold",
        subtle && "opacity-80",
      )}
    >
      {value === null ? "—" : value.toFixed(1)}
    </td>
  );
}

function StatusBadge({
  status,
  t,
}: {
  status: StudentResult["status"];
  t: (key: string, options?: Record<string, unknown>) => string;
}) {
  const labelKey: Record<StudentResult["status"], string> = {
    distinction: "adminResults.statusDistinction",
    basic: "adminResults.statusBasic",
    failing: "adminResults.statusFailing",
    in_progress: "adminResults.statusInProgress",
  };
  return (
    <span
      className={cn(
        "inline-block text-xs px-2 py-1 border tabular-nums",
        STATUS_STYLES[status],
      )}
    >
      {t(labelKey[status])}
    </span>
  );
}

function scoreTone(value: number | null): string {
  if (value === null) return "text-ink-faint";
  if (value >= 85) return "text-emerald-700";
  if (value >= 65) return "text-ink";
  return "text-rose-700";
}
