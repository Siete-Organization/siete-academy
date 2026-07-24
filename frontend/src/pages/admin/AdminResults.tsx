import { useEffect, useMemo, useState, type ReactNode } from "react";
import { useTranslation } from "react-i18next";
import { api } from "@/lib/api";
import { cn } from "@/lib/utils";
import { BackLink } from "@/components/BackLink";
import { LoadError } from "@/components/LoadError";

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

interface ReviewQuestion {
  id: string;
  prompt: string | null;
  type: string;
  student_answer: string | null;
  correct_answer: string | null;
  is_correct: boolean;
}

interface ReviewSubmission {
  submission_id: number;
  assessment_id: number;
  assessment_title: string;
  assessment_type: string;
  submitted_at: string | null;
  status: string;
  auto_score: number | null;
  video_url: string | null;
  questions: ReviewQuestion[];
}

interface ReviewTarget {
  userId: number;
  studentLabel: string;
  moduleId: number;
  moduleLabel: string;
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
  const [loadFailed, setLoadFailed] = useState(false);
  const [retryKey, setRetryKey] = useState(0);

  useEffect(() => {
    setLoadFailed(false);
    void (async () => {
      try {
        const { data } = await api.get<Cohort[]>("/cohorts");
        setCohorts(data);
        if (data.length > 0 && selectedId === null) {
          setSelectedId(data[0].id);
        }
      } catch {
        setLoadFailed(true);
      }
    })();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [retryKey]);

  useEffect(() => {
    if (selectedId === null) {
      setResults(null);
      return;
    }
    setLoading(true);
    setLoadFailed(false);
    void (async () => {
      try {
        const { data } = await api.get<CohortResults>("/grading/results", {
          params: { cohort_id: selectedId, locale: i18n.language.slice(0, 2) },
        });
        setResults(data);
      } catch {
        setLoadFailed(true);
      } finally {
        setLoading(false);
      }
    })();
  }, [selectedId, i18n.language, retryKey]);

  const moduleHeaders = results?.modules ?? [];

  return (
    <div className="container-editorial py-16 space-y-12">
      <BackLink to="/admin">{t("nav.admin")}</BackLink>
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
              {loadFailed ? "—" : t("adminResults.noCohorts")}
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

      {loadFailed && <LoadError onRetry={() => setRetryKey((k) => k + 1)} />}

      {loading && <p className="text-ink-muted">{t("common.loading")}</p>}

      {!loading && !loadFailed && results && results.students.length === 0 && (
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
  const [review, setReview] = useState<ReviewTarget | null>(null);

  return (
    <>
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
              {sortedModules.map((m, idx) => {
                const mr = s.modules.find((x) => x.module_id === m.id);
                return (
                  <ModuleCells
                    key={m.id}
                    mr={mr ?? null}
                    t={t}
                    onView={() =>
                      setReview({
                        userId: s.user_id,
                        studentLabel: s.name || s.email,
                        moduleId: m.id,
                        moduleLabel: t("adminResults.moduleN", { n: idx + 1 }),
                      })
                    }
                  />
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
    {review && (
      <ReviewModal target={review} t={t} onClose={() => setReview(null)} />
    )}
    </>
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

function ModuleCells({
  mr,
  t,
  onView,
}: {
  mr: ModuleResult | null;
  t: (key: string, options?: Record<string, unknown>) => string;
  onView: () => void;
}) {
  const hasSubmissions =
    mr !== null &&
    (mr.capa_1_avg !== null ||
      mr.capa_2_score !== null ||
      mr.capa_2_mcq !== null ||
      mr.capa_1_scores.some((v) => v !== null));
  return (
    <>
      <ScoreCell value={mr?.capa_1_avg ?? null} subtle />
      <ScoreCell value={mr?.capa_2_score ?? null}>
        {hasSubmissions && (
          <button
            type="button"
            onClick={onView}
            className="block mx-auto mt-1 text-[10px] uppercase tracking-[0.12em] text-ink-muted underline underline-offset-2 hover:text-ink"
          >
            {t("adminResults.viewTest")}
          </button>
        )}
      </ScoreCell>
    </>
  );
}

function ReviewModal({
  target,
  t,
  onClose,
}: {
  target: ReviewTarget;
  t: (key: string, options?: Record<string, unknown>) => string;
  onClose: () => void;
}) {
  const [subs, setSubs] = useState<ReviewSubmission[] | null>(null);
  const [loadFailed, setLoadFailed] = useState(false);
  const [retryKey, setRetryKey] = useState(0);

  useEffect(() => {
    setLoadFailed(false);
    void (async () => {
      try {
        const { data } = await api.get<ReviewSubmission[]>(
          "/grading/submissions/review",
          { params: { user_id: target.userId, module_id: target.moduleId } },
        );
        setSubs(data);
      } catch {
        setLoadFailed(true);
      }
    })();
  }, [target.userId, target.moduleId, retryKey]);

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [onClose]);

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-ink/60 p-4"
      onClick={onClose}
    >
      <div
        className="w-full max-w-2xl max-h-[85vh] overflow-y-auto bg-paper border border-bone"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="sticky top-0 flex items-start justify-between gap-4 bg-paper border-b border-bone px-6 py-4">
          <div>
            <p className="num-label">{target.moduleLabel}</p>
            <h2 className="font-display text-xl mt-1">{target.studentLabel}</h2>
          </div>
          <button
            type="button"
            onClick={onClose}
            aria-label={t("common.close")}
            className="text-ink-muted hover:text-ink text-xl leading-none px-2 py-1"
          >
            ✕
          </button>
        </div>

        <div className="px-6 py-5 space-y-8">
          {loadFailed && (
            <LoadError onRetry={() => setRetryKey((k) => k + 1)} />
          )}
          {!loadFailed && subs === null && (
            <p className="text-ink-muted text-sm">{t("common.loading")}</p>
          )}
          {subs !== null && subs.length === 0 && (
            <p className="text-ink-muted text-sm">
              {t("adminResults.reviewEmpty")}
            </p>
          )}
          {subs?.map((sub) => (
            <section key={sub.submission_id} className="space-y-4">
              <header className="flex flex-wrap items-baseline justify-between gap-2 border-b border-bone pb-2">
                <h3 className="font-medium text-ink">{sub.assessment_title}</h3>
                <p className="text-xs text-ink-muted tabular-nums">
                  {sub.auto_score !== null && (
                    <span className={cn("font-semibold mr-3", scoreTone(sub.auto_score))}>
                      {sub.auto_score.toFixed(1)}
                    </span>
                  )}
                  {sub.submitted_at &&
                    new Date(sub.submitted_at).toLocaleDateString()}
                </p>
              </header>
              {sub.video_url && (
                <a
                  href={sub.video_url}
                  target="_blank"
                  rel="noreferrer"
                  className="inline-block text-sm underline underline-offset-2 text-ink-muted hover:text-ink"
                >
                  {t("adminResults.reviewVideo")}
                </a>
              )}
              <ol className="space-y-4">
                {sub.questions.map((q, i) => (
                  <li key={q.id ?? i} className="text-sm">
                    <p className="font-medium text-ink">
                      {i + 1}. {q.prompt}
                    </p>
                    <p
                      className={cn(
                        "mt-1",
                        q.is_correct ? "text-emerald-700" : "text-rose-700",
                      )}
                    >
                      {q.is_correct ? "✓" : "✗"}{" "}
                      <span className="text-ink-muted">
                        {t("adminResults.reviewStudentAnswer")}:
                      </span>{" "}
                      {q.student_answer ?? t("adminResults.reviewNoAnswer")}
                    </p>
                    {!q.is_correct && (
                      <p className="mt-0.5 text-ink-muted">
                        {t("adminResults.reviewCorrectAnswer")}:{" "}
                        <span className="text-ink">{q.correct_answer}</span>
                      </p>
                    )}
                  </li>
                ))}
              </ol>
            </section>
          ))}
        </div>
      </div>
    </div>
  );
}

function ScoreCell({
  value,
  bold = false,
  subtle = false,
  children,
}: {
  value: number | null;
  bold?: boolean;
  subtle?: boolean;
  children?: ReactNode;
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
      {children}
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
