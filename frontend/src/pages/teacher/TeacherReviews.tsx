import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { api } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Input, Textarea } from "@/components/ui/input";

interface PendingReview {
  submission_id: number;
  assessment_id: number;
  assessment_title: string;
  assessment_type: string;
  module_id: number | null;
  module_title: string | null;
  user_id: number;
  user_name: string | null;
  user_email: string | null;
  submitted_at: string;
  has_file: boolean;
  cohort_id: number | null;
}

interface Submission {
  id: number;
  assessment_id: number;
  user_id: number;
  payload: Record<string, unknown>;
  file_url: string | null;
  status: string;
  auto_score: number | null;
  submitted_at: string;
}

interface AIReview {
  id: number;
  submission_id: number;
  draft_feedback: string;
  score_suggestion: number | null;
  model_used: string;
}

export function TeacherReviews() {
  const { t, i18n } = useTranslation();
  const [pending, setPending] = useState<PendingReview[]>([]);
  const [selected, setSelected] = useState<PendingReview | null>(null);
  const [detail, setDetail] = useState<Submission | null>(null);
  const [aiDraft, setAiDraft] = useState<AIReview | null>(null);
  const [feedback, setFeedback] = useState("");
  const [score, setScore] = useState<number>(70);
  const [attachmentUrl, setAttachmentUrl] = useState("");

  const [query, setQuery] = useState("");
  const [assessmentFilter, setAssessmentFilter] = useState<number | "all">("all");
  const [studentFilter, setStudentFilter] = useState<number | "all">("all");

  const load = async () => {
    const { data } = await api.get<PendingReview[]>("/teacher/pending");
    setPending(data);
    if (data.length) setSelected((prev) => prev ?? data[0]);
    else setSelected(null);
  };

  useEffect(() => {
    void load();
  }, []);

  useEffect(() => {
    if (!selected) {
      setDetail(null);
      setAiDraft(null);
      setFeedback("");
      setScore(70);
      setAttachmentUrl("");
      return;
    }
    void (async () => {
      try {
        const [subRes, draftRes] = await Promise.all([
          api.get<Submission[]>("/assessments/submissions/pending"),
          api.get<AIReview | null>(`/ai-review/submission/${selected.submission_id}`),
        ]);
        const match = subRes.data.find((s) => s.id === selected.submission_id) || null;
        setDetail(match);
        setAiDraft(draftRes.data);
      } catch {
        setDetail(null);
        setAiDraft(null);
      }
    })();
  }, [selected]);

  const assessmentOptions = useMemo(() => {
    const map = new Map<number, string>();
    pending.forEach((p) => map.set(p.assessment_id, p.assessment_title));
    return Array.from(map.entries()).map(([id, title]) => ({ id, title }));
  }, [pending]);

  const studentOptions = useMemo(() => {
    const map = new Map<number, string>();
    pending.forEach((p) =>
      map.set(p.user_id, p.user_name || p.user_email || `user #${p.user_id}`),
    );
    return Array.from(map.entries()).map(([id, name]) => ({ id, name }));
  }, [pending]);

  const filtered = useMemo(() => {
    const needle = query.trim().toLowerCase();
    return pending.filter((p) => {
      if (assessmentFilter !== "all" && p.assessment_id !== assessmentFilter) return false;
      if (studentFilter !== "all" && p.user_id !== studentFilter) return false;
      if (!needle) return true;
      const haystack =
        (p.user_name || "") +
        " " +
        (p.user_email || "") +
        " " +
        p.assessment_title +
        " " +
        (p.module_title || "");
      return haystack.toLowerCase().includes(needle);
    });
  }, [pending, query, assessmentFilter, studentFilter]);

  const submitReview = async () => {
    if (!selected) return;
    await api.post(`/assessments/submissions/${selected.submission_id}/review`, {
      score,
      feedback,
      attachment_url: attachmentUrl || null,
    });
    setFeedback("");
    setScore(70);
    setAttachmentUrl("");
    setSelected(null);
    setDetail(null);
    setAiDraft(null);
    await load();
  };

  return (
    <div className="container-editorial py-16">
      <header className="mb-8 flex items-end justify-between gap-4 flex-wrap">
        <div>
          <p className="num-label">Profesor</p>
          <h1 className="font-display text-display-md mt-3">{t("teacher.reviewQueue")}</h1>
          <p className="text-sm text-ink-muted mt-2">
            {t("teacher.totalPending", { count: pending.length })}
          </p>
        </div>
        <Link
          to="/teacher"
          className="text-xs uppercase tracking-[0.14em] font-mono text-ink-muted hover:text-ink transition-colors"
        >
          ← {t("teacher.backToDashboard")}
        </Link>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-[360px_1fr] gap-12">
        <aside className="space-y-4">
          <Input
            placeholder={t("teacher.searchPlaceholder")}
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />

          <div className="grid grid-cols-1 gap-2">
            <select
              value={assessmentFilter}
              onChange={(e) =>
                setAssessmentFilter(e.target.value === "all" ? "all" : Number(e.target.value))
              }
              className="border-b border-bone-strong py-2 text-sm bg-transparent focus:outline-none focus:border-ink"
            >
              <option value="all">{t("teacher.filterAllAssessments")}</option>
              {assessmentOptions.map((a) => (
                <option key={a.id} value={a.id}>
                  {a.title}
                </option>
              ))}
            </select>
            <select
              value={studentFilter}
              onChange={(e) =>
                setStudentFilter(e.target.value === "all" ? "all" : Number(e.target.value))
              }
              className="border-b border-bone-strong py-2 text-sm bg-transparent focus:outline-none focus:border-ink"
            >
              <option value="all">{t("teacher.filterAllStudents")}</option>
              {studentOptions.map((s) => (
                <option key={s.id} value={s.id}>
                  {s.name}
                </option>
              ))}
            </select>
          </div>

          {pending.length === 0 ? (
            <p className="text-ink-muted text-sm py-6">{t("teacher.noPending")}</p>
          ) : filtered.length === 0 ? (
            <p className="text-ink-muted text-sm py-6">{t("teacher.noMatches")}</p>
          ) : (
            <ol className="divide-y divide-bone border-y border-bone max-h-[600px] overflow-y-auto">
              {filtered.map((p, i) => (
                <li key={p.submission_id}>
                  <button
                    onClick={() => setSelected(p)}
                    className={`w-full text-left py-4 px-2 grid grid-cols-12 gap-2 items-baseline transition-colors ${
                      selected?.submission_id === p.submission_id
                        ? "bg-paper-tint"
                        : "hover:bg-paper-tint/60"
                    }`}
                  >
                    <span className="col-span-2 font-mono text-[10px] text-ink-faint tabular-nums">
                      {String(i + 1).padStart(3, "0")}
                    </span>
                    <div className="col-span-10">
                      <p className="font-medium text-ink text-sm truncate">
                        {p.user_name || p.user_email || `user #${p.user_id}`}
                      </p>
                      <p className="text-xs text-ink-soft mt-0.5 truncate">
                        {p.assessment_title}
                      </p>
                      <p className="text-[10px] text-ink-faint mt-1 font-mono uppercase tracking-[0.12em]">
                        {p.assessment_type.replace(/_/g, " ")}
                        {p.module_title ? ` · ${p.module_title}` : ""} ·{" "}
                        {new Date(p.submitted_at).toLocaleDateString(i18n.language)}
                      </p>
                    </div>
                  </button>
                </li>
              ))}
            </ol>
          )}
        </aside>

        {selected && (
          <article className="space-y-10">
            <header className="hairline pt-6">
              <p className="num-label">{t("teacher.delivery")}</p>
              <h2 className="font-display text-display-md mt-3">
                {selected.assessment_title}
              </h2>
              <p className="font-mono text-xs text-ink-muted mt-3">
                {selected.user_name || selected.user_email} ·{" "}
                {selected.module_title || "—"} ·{" "}
                {new Date(selected.submitted_at).toLocaleString(i18n.language)}
              </p>
            </header>

            {detail && (
              <section>
                <p className="num-label mb-3">Payload</p>
                <pre className="bg-paper-tint border border-bone p-5 rounded-md text-xs leading-relaxed overflow-auto max-h-96 font-mono">
                  {JSON.stringify(detail.payload, null, 2)}
                </pre>
                {detail.file_url && (
                  <a
                    href={detail.file_url}
                    target="_blank"
                    rel="noreferrer"
                    className="inline-block mt-4 text-ember hover:underline underline-offset-4 text-sm"
                  >
                    {t("teacher.studentFile")} ↗
                  </a>
                )}
              </section>
            )}

            {aiDraft && (
              <section className="border border-bone bg-paper-tint/60 rounded-md p-5 space-y-3">
                <div className="flex items-baseline justify-between">
                  <p className="num-label text-ember">{t("teacher.aiDraft")}</p>
                  {aiDraft.score_suggestion !== null && (
                    <p className="font-mono text-xs text-ink-muted">
                      {t("teacher.suggested")}: {aiDraft.score_suggestion.toFixed(0)}/100
                    </p>
                  )}
                </div>
                <p className="whitespace-pre-wrap text-sm leading-relaxed text-ink-soft">
                  {aiDraft.draft_feedback}
                </p>
                <div className="flex gap-3 pt-2">
                  <Button
                    size="sm"
                    variant="outline"
                    onClick={() => {
                      setFeedback(aiDraft.draft_feedback);
                      if (aiDraft.score_suggestion !== null) {
                        setScore(Math.round(aiDraft.score_suggestion));
                      }
                    }}
                  >
                    {t("teacher.useDraft")}
                  </Button>
                </div>
              </section>
            )}

            <section className="hairline pt-6 space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-[140px_1fr] gap-6">
                <label>
                  <span className="num-label mb-2 block">{t("teacher.score")}</span>
                  <input
                    type="number"
                    min={0}
                    max={100}
                    value={score}
                    onChange={(e) => setScore(Number(e.target.value))}
                    className="w-full font-display text-4xl tabular-nums bg-transparent border-0 border-b border-bone-strong focus:border-ink focus:outline-none pb-1"
                  />
                  <span className="text-ink-faint text-xs">/ 100</span>
                </label>
                <label>
                  <span className="num-label mb-2 block">{t("teacher.feedback")}</span>
                  <Textarea
                    value={feedback}
                    onChange={(e) => setFeedback(e.target.value)}
                    placeholder={t("teacher.feedbackPlaceholder")}
                  />
                </label>
              </div>

              <label className="block">
                <span className="num-label mb-2 block">{t("teacher.attachment")}</span>
                <Input
                  type="url"
                  value={attachmentUrl}
                  onChange={(e) => setAttachmentUrl(e.target.value)}
                  placeholder="https://drive.google.com/... · https://loom.com/..."
                />
                <span className="text-xs text-ink-muted mt-1 block">
                  {t("teacher.attachmentHint")}
                </span>
              </label>

              <Button
                onClick={submitReview}
                disabled={!feedback.trim()}
                size="lg"
                variant="ember"
              >
                {t("teacher.approve")} <span aria-hidden>→</span>
              </Button>
            </section>
          </article>
        )}
      </div>
    </div>
  );
}
