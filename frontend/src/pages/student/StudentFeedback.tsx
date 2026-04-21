import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { api } from "@/lib/api";

interface ReviewOut {
  id: number;
  score: number;
  feedback: string;
  attachment_url: string | null;
  approved_at: string;
}

interface SubmissionOut {
  id: number;
  assessment_id: number;
  payload: Record<string, unknown>;
  file_url: string | null;
  status: string;
  auto_score: number | null;
  submitted_at: string;
}

interface SubmissionWithReview {
  submission: SubmissionOut;
  assessment_title: string;
  review: ReviewOut | null;
}

interface TeacherNote {
  id: number;
  teacher_id: number;
  teacher_name: string | null;
  student_id: number;
  student_name: string | null;
  body: string;
  attachment_kind: string | null;
  attachment_url: string | null;
  created_at: string;
}

const ATTACHMENT_ICONS: Record<string, string> = {
  pdf: "📄",
  ppt: "📊",
  video: "🎞",
  doc: "📝",
  link: "🔗",
};

export function StudentFeedback() {
  const { t, i18n } = useTranslation();
  const [items, setItems] = useState<SubmissionWithReview[] | null>(null);
  const [notes, setNotes] = useState<TeacherNote[]>([]);

  useEffect(() => {
    void (async () => {
      const [s, n] = await Promise.all([
        api.get<SubmissionWithReview[]>("/assessments/submissions/me/with-reviews"),
        api.get<TeacherNote[]>("/teacher/notes/me"),
      ]);
      setItems(s.data);
      setNotes(n.data);
    })();
  }, []);

  if (items === null) {
    return <div className="container-editorial py-24 text-ink-muted">{t("common.loading")}</div>;
  }

  if (items.length === 0 && notes.length === 0) {
    return (
      <div className="container-editorial py-28 max-w-2xl">
        <p className="num-label">Sin entregas</p>
        <h1 className="font-display text-display-lg mt-4 text-balance">
          Cuando entregues una prueba o te escriba un profesor, aparecerá aquí.
        </h1>
        <p className="text-ink-soft mt-6 leading-relaxed">{t("common.empty")}</p>
      </div>
    );
  }

  return (
    <div className="container-editorial py-16 md:py-24 space-y-12">
      <header>
        <p className="num-label">Seguimiento</p>
        <h1 className="font-display text-display-lg mt-4 text-balance">
          {t("feedback.title")}
        </h1>
      </header>

      {notes.length > 0 && (
        <section className="space-y-5">
          <div className="flex items-baseline justify-between">
            <p className="num-label">{t("feedback.directNotes")}</p>
            <p className="text-xs text-ink-muted font-mono">{notes.length}</p>
          </div>
          <ol className="border-y border-bone divide-y divide-bone">
            {notes.map((n) => (
              <li key={n.id} className="py-6 grid grid-cols-12 gap-4">
                <div className="col-span-2 md:col-span-1 font-mono text-[10px] text-ink-faint tabular-nums pt-1">
                  ✉
                </div>
                <div className="col-span-10 md:col-span-11 space-y-2">
                  <div className="flex items-baseline justify-between gap-4">
                    <p className="text-sm font-semibold text-ink">
                      {n.teacher_name || "Profesor"}
                    </p>
                    <p className="font-mono text-[10px] uppercase tracking-[0.14em] text-ink-muted">
                      {new Date(n.created_at).toLocaleString(i18n.language, {
                        dateStyle: "medium",
                        timeStyle: "short",
                      })}
                    </p>
                  </div>
                  <p className="whitespace-pre-wrap text-[15px] leading-relaxed text-ink-soft">
                    {n.body}
                  </p>
                  {n.attachment_url && (
                    <a
                      href={n.attachment_url}
                      target="_blank"
                      rel="noreferrer"
                      className="inline-flex items-baseline gap-2 text-sm text-ember hover:underline underline-offset-4"
                    >
                      <span>{ATTACHMENT_ICONS[n.attachment_kind || "link"] || "🔗"}</span>
                      {t("feedback.attachment")} ↗
                    </a>
                  )}
                </div>
              </li>
            ))}
          </ol>
        </section>
      )}

      {items.length > 0 && (
        <section className="space-y-5">
          <p className="num-label">{t("feedback.submissionsTitle")}</p>
          <ol className="border-y border-bone divide-y divide-bone">
            {items.map((it, idx) => {
          const s = it.submission;
          const r = it.review;
          const statusLabel =
            s.status === "reviewed"
              ? t("feedback.reviewed")
              : s.status === "auto_graded"
                ? t("feedback.autoGraded")
                : t("feedback.pending");
          return (
            <li key={s.id} className="py-8 grid grid-cols-12 gap-6">
              <span className="col-span-1 font-mono text-xs text-ink-faint tabular-nums">
                {String(idx + 1).padStart(2, "0")}
              </span>
              <div className="col-span-11 md:col-span-8 space-y-3">
                <div className="flex items-baseline justify-between gap-4">
                  <h2 className="font-display text-2xl text-balance">{it.assessment_title}</h2>
                  <span className="num-label whitespace-nowrap">{statusLabel}</span>
                </div>
                <p className="font-mono text-[11px] uppercase tracking-[0.14em] text-ink-muted">
                  {new Date(s.submitted_at).toLocaleString(i18n.language, {
                    dateStyle: "medium",
                    timeStyle: "short",
                  })}
                </p>
                {r ? (
                  <article className="mt-3 border-l-2 border-ember pl-5 py-1 space-y-2">
                    <p className="num-label text-ember">{t("feedback.teacherNote")}</p>
                    <p className="whitespace-pre-wrap text-[15px] leading-relaxed text-ink-soft">
                      {r.feedback}
                    </p>
                    {r.attachment_url && (
                      <a
                        className="inline-block text-sm text-ember hover:underline underline-offset-4"
                        href={r.attachment_url}
                        target="_blank"
                        rel="noreferrer"
                      >
                        {t("feedback.attachment")} ↗
                      </a>
                    )}
                  </article>
                ) : s.status === "auto_graded" ? (
                  <p className="text-sm text-ink-muted italic">
                    Calificación automática — sin feedback escrito.
                  </p>
                ) : (
                  <p className="text-sm text-ink-muted italic">{t("feedback.pending")}…</p>
                )}
              </div>
              <aside className="col-span-12 md:col-span-3 md:text-right space-y-2 md:border-l md:border-bone md:pl-6">
                <p className="num-label">{t("feedback.score")}</p>
                <p className="font-display text-5xl tabular-nums">
                  {r?.score ?? s.auto_score ?? "—"}
                  <span className="text-ink-faint text-2xl">/100</span>
                </p>
              </aside>
            </li>
          );
        })}
          </ol>
        </section>
      )}
    </div>
  );
}
