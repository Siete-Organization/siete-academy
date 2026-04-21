import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { api } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Input, Textarea } from "@/components/ui/input";

interface CohortStats {
  cohort_id: number;
  cohort_name: string;
  status: string;
  students_count: number;
  avg_progress_pct: number;
  pending_reviews: number;
}

interface StudentStats {
  user_id: number;
  user_name: string | null;
  user_email: string;
  cohort_id: number;
  cohort_name: string;
  progress_pct: number;
  lessons_completed: number;
  avg_score: number | null;
  last_activity_at: string | null;
  has_certificate: boolean;
}

interface Dashboard {
  pending_reviews: number;
  cohorts: CohortStats[];
  students: StudentStats[];
}

export function TeacherHome() {
  const { t, i18n } = useTranslation();
  const [data, setData] = useState<Dashboard | null>(null);
  const [cohortFilter, setCohortFilter] = useState<number | "all">("all");
  const [issuing, setIssuing] = useState<number | null>(null);
  const [noteTarget, setNoteTarget] = useState<StudentStats | null>(null);

  const loadDashboard = async () => {
    const { data } = await api.get<Dashboard>("/teacher/dashboard");
    setData(data);
  };

  useEffect(() => {
    void loadDashboard();
  }, []);

  const issueCertificate = async (s: StudentStats) => {
    if (s.has_certificate) return;
    setIssuing(s.user_id);
    try {
      await api.post("/certificates/issue", {
        user_id: s.user_id,
        cohort_id: s.cohort_id,
      });
      await loadDashboard();
    } catch (err) {
      const detail =
        (err as { response?: { data?: { detail?: string } } }).response?.data?.detail ||
        t("common.error");
      window.alert(detail);
    } finally {
      setIssuing(null);
    }
  };

  const filteredStudents = useMemo(() => {
    if (!data) return [];
    if (cohortFilter === "all") return data.students;
    return data.students.filter((s) => s.cohort_id === cohortFilter);
  }, [data, cohortFilter]);

  if (!data) {
    return <div className="container-editorial py-24 text-ink-muted">{t("common.loading")}</div>;
  }

  return (
    <div className="container-editorial py-16 md:py-20 space-y-14">
      <header className="flex items-end justify-between flex-wrap gap-6">
        <div>
          <p className="num-label">{t("teacherHome.eyebrow")}</p>
          <h1 className="font-display text-display-lg mt-4 text-balance">
            {t("teacherHome.title")}
          </h1>
          <p className="text-ink-soft mt-4 max-w-2xl">{t("teacherHome.subtitle")}</p>
        </div>
        <Link
          to="/teacher/reviews"
          className="inline-flex items-center gap-3 px-5 py-3 bg-ink text-paper hover:bg-ember transition-colors font-mono text-xs uppercase tracking-[0.14em]"
        >
          <span className="text-2xl font-display leading-none tabular-nums">
            {data.pending_reviews}
          </span>
          <span>{t("teacherHome.goToQueue")}</span>
          <span aria-hidden>→</span>
        </Link>
      </header>

      <section className="space-y-4">
        <p className="num-label">{t("teacherHome.byCohort")}</p>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {data.cohorts.map((c) => (
            <article
              key={c.cohort_id}
              className="border border-bone p-5 rounded-xs space-y-3 bg-paper-warm/40"
            >
              <div className="flex items-baseline justify-between gap-2">
                <div>
                  <p className="num-label">{t(`admin.status.${c.status}` as never, c.status)}</p>
                  <h2 className="font-display text-xl mt-1">{c.cohort_name}</h2>
                </div>
                <span className="font-display text-4xl tabular-nums">
                  {c.avg_progress_pct.toFixed(0)}
                  <span className="text-ink-faint text-xl">%</span>
                </span>
              </div>
              <div className="grid grid-cols-2 gap-3 text-sm pt-2 hairline">
                <Metric
                  label={t("teacherHome.students")}
                  value={String(c.students_count)}
                />
                <Metric
                  label={t("teacherHome.pending")}
                  value={String(c.pending_reviews)}
                  highlight={c.pending_reviews > 0}
                />
              </div>
            </article>
          ))}
          {data.cohorts.length === 0 && (
            <p className="text-ink-muted text-sm">{t("teacherHome.noCohorts")}</p>
          )}
        </div>
      </section>

      <section className="space-y-4">
        <div className="flex items-end justify-between flex-wrap gap-3">
          <p className="num-label">{t("teacherHome.byStudent")}</p>
          <div className="flex gap-2 flex-wrap">
            <button
              onClick={() => setCohortFilter("all")}
              className={chipCls(cohortFilter === "all")}
            >
              {t("teacherHome.allCohorts")}
            </button>
            {data.cohorts.map((c) => (
              <button
                key={c.cohort_id}
                onClick={() => setCohortFilter(c.cohort_id)}
                className={chipCls(cohortFilter === c.cohort_id)}
              >
                {c.cohort_name}
              </button>
            ))}
          </div>
        </div>

        <div className="border border-bone rounded-xs overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="bg-paper-tint border-b border-bone">
              <tr className="text-left font-mono text-[10px] uppercase tracking-[0.14em] text-ink-muted">
                <th className="px-4 py-3 font-medium">{t("teacherHome.colStudent")}</th>
                <th className="px-4 py-3 font-medium">{t("teacherHome.colCohort")}</th>
                <th className="px-4 py-3 font-medium text-right">{t("teacherHome.colProgress")}</th>
                <th className="px-4 py-3 font-medium text-right">{t("teacherHome.colLessons")}</th>
                <th className="px-4 py-3 font-medium text-right">{t("teacherHome.colScore")}</th>
                <th className="px-4 py-3 font-medium">{t("teacherHome.colActivity")}</th>
                <th className="px-4 py-3 font-medium text-right">{t("teacherHome.colCertificate")}</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-bone">
              {filteredStudents.map((s) => (
                <tr key={`${s.user_id}-${s.cohort_id}`} className="hover:bg-paper-tint/60">
                  <td className="px-4 py-3">
                    <p className="font-medium text-ink">
                      {s.user_name || s.user_email.split("@")[0]}
                    </p>
                    <p className="text-xs text-ink-muted">{s.user_email}</p>
                    <button
                      onClick={() => setNoteTarget(s)}
                      className="mt-2 inline-flex items-center gap-1.5 bg-ember text-paper hover:bg-ember-soft rounded-full px-3 py-1 text-[11px] font-semibold tracking-tight transition-colors"
                    >
                      <span aria-hidden>✉</span>
                      {t("teacherHome.sendNote")}
                    </button>
                  </td>
                  <td className="px-4 py-3 text-ink-soft font-mono text-xs">
                    {s.cohort_name}
                  </td>
                  <td className="px-4 py-3 text-right">
                    <ProgressBar value={s.progress_pct} />
                  </td>
                  <td className="px-4 py-3 text-right tabular-nums font-mono">
                    {s.lessons_completed}
                  </td>
                  <td className="px-4 py-3 text-right tabular-nums font-mono">
                    {s.avg_score !== null ? `${s.avg_score.toFixed(0)}` : "—"}
                  </td>
                  <td className="px-4 py-3 text-ink-muted font-mono text-xs">
                    {s.last_activity_at
                      ? new Date(s.last_activity_at).toLocaleDateString(i18n.language, {
                          day: "2-digit",
                          month: "short",
                        })
                      : "—"}
                  </td>
                  <td className="px-4 py-3 text-right">
                    {s.has_certificate ? (
                      <span className="inline-flex items-center gap-1 text-moss font-mono text-[10px] uppercase tracking-[0.14em]">
                        ✓ {t("teacherHome.certIssued")}
                      </span>
                    ) : s.progress_pct >= 100 ? (
                      <button
                        disabled={issuing === s.user_id}
                        onClick={() => issueCertificate(s)}
                        className="text-[10px] uppercase tracking-[0.14em] font-mono px-2.5 py-1 border border-ink text-ink hover:bg-ink hover:text-paper transition-colors disabled:opacity-50"
                      >
                        {issuing === s.user_id
                          ? t("teacherHome.issuing")
                          : t("teacherHome.issueCert")}
                      </button>
                    ) : (
                      <span className="text-ink-faint text-[10px] font-mono uppercase tracking-[0.14em]">
                        {t("teacherHome.notYet")}
                      </span>
                    )}
                  </td>
                </tr>
              ))}
              {filteredStudents.length === 0 && (
                <tr>
                  <td
                    colSpan={7}
                    className="px-4 py-8 text-center text-ink-muted text-sm"
                  >
                    {t("teacherHome.noStudents")}
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </section>

      {noteTarget && (
        <SendNoteDialog
          student={noteTarget}
          onClose={() => setNoteTarget(null)}
        />
      )}
    </div>
  );
}

const ATTACHMENT_KINDS: {
  value: "pdf" | "ppt" | "video" | "doc" | "link";
  icon: string;
  label: string;
}[] = [
  { value: "link", icon: "🔗", label: "Link" },
  { value: "pdf", icon: "📄", label: "PDF" },
  { value: "ppt", icon: "📊", label: "PPT" },
  { value: "video", icon: "🎞", label: "Video" },
  { value: "doc", icon: "📝", label: "Doc" },
];

function SendNoteDialog({
  student,
  onClose,
}: {
  student: StudentStats;
  onClose: () => void;
}) {
  const { t } = useTranslation();
  const [body, setBody] = useState("");
  const [attachmentKind, setAttachmentKind] = useState<
    "pdf" | "ppt" | "video" | "doc" | "link"
  >("link");
  const [attachmentUrl, setAttachmentUrl] = useState("");
  const [sending, setSending] = useState(false);
  const [sent, setSent] = useState(false);

  useEffect(() => {
    const onEsc = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    document.addEventListener("keydown", onEsc);
    return () => document.removeEventListener("keydown", onEsc);
  }, [onClose]);

  const handleSend = async () => {
    if (!body.trim()) return;
    setSending(true);
    try {
      await api.post("/teacher/notes", {
        student_id: student.user_id,
        body: body.trim(),
        attachment_kind: attachmentUrl ? attachmentKind : null,
        attachment_url: attachmentUrl || null,
      });
      setSent(true);
      setTimeout(onClose, 900);
    } finally {
      setSending(false);
    }
  };

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-ink/40 backdrop-blur-sm p-4"
      onClick={onClose}
    >
      <div
        className="bg-paper border border-bone rounded-xs max-w-xl w-full p-8 space-y-6 shadow-lift"
        onClick={(e) => e.stopPropagation()}
      >
        <header>
          <p className="num-label">{t("teacherHome.noteTo")}</p>
          <h2 className="font-display text-2xl mt-2 font-bold">
            {student.user_name || student.user_email.split("@")[0]}
          </h2>
          <p className="text-xs text-ink-muted">{student.user_email}</p>
        </header>

        <label className="block">
          <span className="num-label mb-2 block">{t("teacherHome.noteBody")}</span>
          <Textarea
            value={body}
            onChange={(e) => setBody(e.target.value)}
            rows={5}
            placeholder={t("teacherHome.notePlaceholder")}
            autoFocus
          />
        </label>

        <div className="space-y-2">
          <span className="num-label block">{t("teacherHome.attachmentOptional")}</span>
          <div className="flex gap-2 flex-wrap">
            {ATTACHMENT_KINDS.map((k) => (
              <button
                key={k.value}
                type="button"
                onClick={() => setAttachmentKind(k.value)}
                className={`px-3 py-1.5 border text-xs uppercase tracking-[0.14em] font-mono transition-colors rounded-full ${
                  attachmentKind === k.value
                    ? "border-ink bg-ink text-paper"
                    : "border-bone text-ink-muted hover:border-ink"
                }`}
              >
                {k.icon} {k.label}
              </button>
            ))}
          </div>
          <Input
            type="url"
            value={attachmentUrl}
            onChange={(e) => setAttachmentUrl(e.target.value)}
            placeholder="https://drive.google.com/... · https://loom.com/..."
          />
          <p className="text-[11px] text-ink-muted">
            {t("teacherHome.attachmentHint")}
          </p>
        </div>

        {sent && (
          <p className="text-moss text-sm border-l-2 border-moss pl-3">
            {t("teacherHome.noteSent")}
          </p>
        )}

        <div className="flex items-center gap-3 hairline pt-5">
          <Button
            variant="ember"
            onClick={handleSend}
            disabled={sending || sent || !body.trim()}
          >
            {sending ? "…" : sent ? "✓" : t("teacherHome.sendNow")}
          </Button>
          <button
            type="button"
            onClick={onClose}
            className="text-xs uppercase tracking-[0.14em] font-mono text-ink-muted hover:text-ink"
          >
            {t("common.cancel")}
          </button>
        </div>
      </div>
    </div>
  );
}

function Metric({
  label,
  value,
  highlight,
}: {
  label: string;
  value: string;
  highlight?: boolean;
}) {
  return (
    <div>
      <p className="num-label">{label}</p>
      <p
        className={`font-display text-2xl tabular-nums mt-1 ${
          highlight ? "text-ember" : "text-ink"
        }`}
      >
        {value}
      </p>
    </div>
  );
}

function ProgressBar({ value }: { value: number }) {
  const pct = Math.max(0, Math.min(100, value));
  return (
    <div className="flex items-center gap-2 justify-end">
      <div className="w-24 h-1 bg-bone relative overflow-hidden">
        <div
          className={`absolute inset-y-0 left-0 ${pct === 100 ? "bg-moss" : "bg-ink"}`}
          style={{ width: `${pct}%` }}
        />
      </div>
      <span className="font-mono text-[11px] text-ink-muted tabular-nums w-10 text-right">
        {pct.toFixed(0)}%
      </span>
    </div>
  );
}

function chipCls(active: boolean): string {
  return (
    "px-3 py-1.5 border text-xs uppercase tracking-[0.14em] font-mono transition-colors " +
    (active
      ? "border-ink bg-ink text-paper"
      : "border-bone text-ink-muted hover:border-ink hover:text-ink")
  );
}
