import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { api } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Input, Textarea } from "@/components/ui/input";

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
  const { t } = useTranslation();
  const [pending, setPending] = useState<Submission[]>([]);
  const [selected, setSelected] = useState<Submission | null>(null);
  const [aiDraft, setAiDraft] = useState<AIReview | null>(null);
  const [feedback, setFeedback] = useState("");
  const [score, setScore] = useState<number>(70);
  const [attachmentUrl, setAttachmentUrl] = useState("");

  const load = async () => {
    const { data } = await api.get<Submission[]>("/assessments/submissions/pending");
    setPending(data);
    if (data.length) setSelected(data[0]);
    else setSelected(null);
  };

  useEffect(() => {
    void load();
  }, []);

  useEffect(() => {
    if (!selected) {
      setAiDraft(null);
      setFeedback("");
      setScore(70);
      setAttachmentUrl("");
      return;
    }
    void (async () => {
      try {
        const { data } = await api.get<AIReview | null>(
          `/ai-review/submission/${selected.id}`,
        );
        setAiDraft(data);
      } catch {
        setAiDraft(null);
      }
    })();
  }, [selected]);

  const submitReview = async () => {
    if (!selected) return;
    await api.post(`/assessments/submissions/${selected.id}/review`, {
      score,
      feedback,
      attachment_url: attachmentUrl || null,
    });
    setFeedback("");
    setScore(70);
    setAttachmentUrl("");
    setSelected(null);
    setAiDraft(null);
    await load();
  };

  if (pending.length === 0) {
    return (
      <div className="container-editorial py-32 max-w-2xl">
        <p className="num-label">Cola vacía</p>
        <h1 className="font-display text-display-lg mt-4 text-balance">Todo al día.</h1>
        <p className="text-ink-soft mt-5 leading-relaxed">{t("teacher.noPending")}</p>
      </div>
    );
  }

  return (
    <div className="container-editorial py-16">
      <header className="mb-12">
        <p className="num-label">Profesor</p>
        <h1 className="font-display text-display-md mt-3">{t("teacher.reviewQueue")}</h1>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-[340px_1fr] gap-12">
        <aside>
          <p className="num-label mb-4">{pending.length} pendientes</p>
          <ol className="divide-y divide-bone border-y border-bone">
            {pending.map((s, i) => (
              <li key={s.id}>
                <button
                  onClick={() => setSelected(s)}
                  className={`w-full text-left py-5 grid grid-cols-12 gap-3 items-baseline transition-colors ${
                    selected?.id === s.id ? "bg-paper-tint" : "hover:bg-paper-tint/60"
                  }`}
                >
                  <span className="col-span-2 font-mono text-[10px] text-ink-faint tabular-nums">
                    {String(i + 1).padStart(3, "0")}
                  </span>
                  <div className="col-span-10">
                    <p className="font-display text-lg">Entrega #{s.id}</p>
                    <p className="text-xs text-ink-muted mt-0.5 font-mono">
                      user {s.user_id} · {new Date(s.submitted_at).toLocaleDateString()}
                    </p>
                  </div>
                </button>
              </li>
            ))}
          </ol>
        </aside>

        {selected && (
          <article className="space-y-10">
            <header className="hairline pt-6">
              <p className="num-label">Entrega</p>
              <h2 className="font-display text-display-md mt-3">#{selected.id}</h2>
              <p className="font-mono text-xs text-ink-muted mt-2">
                user {selected.user_id} · {new Date(selected.submitted_at).toLocaleString()}
              </p>
            </header>

            <section>
              <p className="num-label mb-3">Payload</p>
              <pre className="bg-paper-tint border border-bone p-5 rounded-md text-xs leading-relaxed overflow-auto max-h-96 font-mono">
                {JSON.stringify(selected.payload, null, 2)}
              </pre>
              {selected.file_url && (
                <a
                  href={selected.file_url}
                  target="_blank"
                  rel="noreferrer"
                  className="inline-block mt-4 text-ember hover:underline underline-offset-4 text-sm"
                >
                  Archivo adjunto del alumno ↗
                </a>
              )}
            </section>

            {aiDraft && (
              <section className="border border-bone bg-paper-tint/60 rounded-md p-5 space-y-3">
                <div className="flex items-baseline justify-between">
                  <p className="num-label text-ember">{t("teacher.aiDraft")}</p>
                  {aiDraft.score_suggestion !== null && (
                    <p className="font-mono text-xs text-ink-muted">
                      sugerido: {aiDraft.score_suggestion.toFixed(0)}/100
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
                    placeholder="Sé específico. Sé honesto. Ayúdalo a mejorar."
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
