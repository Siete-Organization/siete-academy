import { useMemo, useState } from "react";
import { useTranslation } from "react-i18next";
import { api } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Input, Textarea } from "@/components/ui/input";

/**
 * Runner de examen reusable para Capa 2 (prueba de módulo) y Capa 3 (prueba final).
 *
 * - MCQ se autocalifican en el backend (single/multi/match).
 * - capa_2 / final_test piden además una URL de video (narrado / defensa) que va
 *   a la cola de revisión del profesor.
 * - El caso final suma respuestas cortas + tablas (capturadas acá; el profesor
 *   las califica en PR 2). El MCQ del caso ya da nota automática.
 * - `preview` = solo lectura (vista admin/profesor), sin enviar.
 *
 * NOTA(deuda): las micropruebas de lección en ModulePage tienen su propio runner
 * inline. Se unifican con este componente en un PR de limpieza posterior.
 */

export interface ExamChoice {
  id: string;
  text: string;
}

export interface ExamQuestion {
  id: string;
  type: "single" | "multi" | "match";
  prompt: string;
  choices?: ExamChoice[];
  left?: ExamChoice[];
  right?: ExamChoice[];
  correct?: string[] | Record<string, string>;
  explanation?: string;
}

export interface ShortAnswer {
  id: string;
  topic?: string;
  prompt: string;
  max_words?: number;
}

export interface ClassificationRow {
  id: string;
  label: string;
}

export interface TableOption {
  id: string;
  label?: string;
  text?: string;
}

export interface ExamTable {
  id: string;
  topic?: string;
  prompt: string;
  rows?: ClassificationRow[];
  options?: TableOption[];
  expected_sequence?: unknown[];
}

export interface ExamAssessment {
  id: number;
  type: string;
  title: string;
  passing_score: number;
  config: {
    questions?: ExamQuestion[];
    short_answers?: ShortAnswer[];
    tables?: ExamTable[];
    case_brief?: Record<string, unknown>;
    rules?: Record<string, unknown>;
  } & Record<string, unknown>;
}

interface SubmissionResult {
  id: number;
  auto_score: number | null;
  status: string;
}

const SEQ_CHANNELS = ["email", "telefono", "whatsapp", "linkedin"];

function requiresVideo(type: string): boolean {
  return type === "capa_2" || type === "final_test";
}

/** Réplica client-side de `_question_is_correct` del backend. Solo para el
 * preview con clave de respuestas (admin/profesor); el grading real vive server. */
function isAnswerCorrect(q: ExamQuestion, given: unknown): boolean {
  if (given === undefined || given === null) return false;
  const correct = q.correct;
  if (q.type === "single") {
    if (Array.isArray(correct)) {
      return correct.length === 1 && String(given) === String(correct[0]);
    }
    return String(given) === String(correct);
  }
  if (q.type === "multi") {
    if (!Array.isArray(correct) || !Array.isArray(given)) return false;
    const a = [...correct].map(String).sort();
    const b = [...(given as unknown[])].map(String).sort();
    return a.length === b.length && a.every((x, i) => x === b[i]);
  }
  if (q.type === "match") {
    if (typeof correct !== "object" || correct === null || Array.isArray(correct)) return false;
    if (typeof given !== "object" || given === null) return false;
    const c = correct as Record<string, string>;
    const g = given as Record<string, string>;
    const ck = Object.keys(c);
    if (ck.length !== Object.keys(g).length) return false;
    return ck.every((k) => String(c[k]) === String(g[k]));
  }
  return false;
}

export function ExamRunner({
  assessment,
  preview = false,
  answerKey = false,
  onPassed,
}: {
  assessment: ExamAssessment;
  preview?: boolean;
  /** Preview con clave de respuestas: habilita inputs y permite calcular la nota
   * MCQ localmente (vista admin/profesor para testear la puntuación). */
  answerKey?: boolean;
  onPassed?: () => void;
}) {
  const { t } = useTranslation();
  const cfg = assessment.config ?? {};
  const questions = useMemo(() => cfg.questions ?? [], [cfg.questions]);
  const shortAnswers = useMemo(() => cfg.short_answers ?? [], [cfg.short_answers]);
  const tables = useMemo(() => cfg.tables ?? [], [cfg.tables]);
  const needsVideo = requiresVideo(assessment.type);
  // En preview normal todo es solo-lectura. Con answerKey (admin testeando la
  // nota) habilitamos los inputs sin enviar nada al backend.
  const inputsDisabled = preview && !answerKey;

  const [answers, setAnswers] = useState<Record<string, unknown>>({});
  const [shortText, setShortText] = useState<Record<string, string>>({});
  const [tableData, setTableData] = useState<Record<string, unknown>>({});
  const [videoUrl, setVideoUrl] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState<SubmissionResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [localGraded, setLocalGraded] = useState(false);

  const localScore = useMemo(() => {
    if (questions.length === 0) return 0;
    const hits = questions.filter((q) => isAnswerCorrect(q, answers[q.id])).length;
    return Math.round((hits / questions.length) * 10000) / 100;
  }, [questions, answers]);
  const localHits = useMemo(
    () => questions.filter((q) => isAnswerCorrect(q, answers[q.id])).length,
    [questions, answers],
  );

  const canSubmit =
    !preview &&
    !submitting &&
    questions.every((q) => answers[q.id] !== undefined) &&
    (!needsVideo || Boolean(videoUrl));

  const submit = async () => {
    setError(null);
    setSubmitting(true);
    try {
      const { data } = await api.post<SubmissionResult>("/assessments/submissions", {
        assessment_id: assessment.id,
        payload: {
          answers,
          short_answers: shortText,
          tables: tableData,
          video_url: videoUrl || null,
        },
        file_url: videoUrl || null,
      });
      setResult(data);
      if (
        !needsVideo &&
        (data.auto_score ?? 0) >= assessment.passing_score &&
        onPassed
      ) {
        onPassed();
      }
    } catch {
      setError(t("common.error"));
    } finally {
      setSubmitting(false);
    }
  };

  if (result) {
    return <ResultPanel result={result} needsVideo={needsVideo} assessment={assessment} t={t} />;
  }

  return (
    <div className="space-y-8">
      {cfg.case_brief ? <CaseBrief brief={cfg.case_brief} t={t} /> : null}

      {questions.length > 0 && (
        <Section title={t("exam.mcqSection")}>
          <ol className="space-y-6">
            {questions.map((q, i) => (
              <li key={q.id} className="border border-bone rounded-md p-5 space-y-4">
                <p className="font-mono text-[10px] uppercase tracking-[0.14em] text-ink-faint">
                  {String(i + 1).padStart(2, "0")} / {questions.length}
                </p>
                <p className="text-sm leading-relaxed">{q.prompt}</p>
                <QuestionInput
                  q={q}
                  value={answers[q.id]}
                  disabled={inputsDisabled}
                  onChange={(v) => setAnswers((p) => ({ ...p, [q.id]: v }))}
                />
                {answerKey && localGraded && (
                  <QuestionFeedback q={q} given={answers[q.id]} t={t} />
                )}
              </li>
            ))}
          </ol>
        </Section>
      )}

      {shortAnswers.length > 0 && (
        <Section title={t("exam.shortSection")}>
          <div className="space-y-6">
            {shortAnswers.map((sa) => (
              <div key={sa.id} className="border border-bone rounded-md p-5 space-y-3">
                {sa.topic && <p className="num-label">{sa.topic}</p>}
                <p className="text-sm leading-relaxed">{sa.prompt}</p>
                <Textarea
                  rows={4}
                  disabled={inputsDisabled}
                  value={shortText[sa.id] ?? ""}
                  onChange={(e) =>
                    setShortText((p) => ({ ...p, [sa.id]: e.target.value }))
                  }
                />
              </div>
            ))}
          </div>
        </Section>
      )}

      {tables.length > 0 && (
        <Section title={t("exam.tablesSection")}>
          <div className="space-y-6">
            {tables.map((tbl) => (
              <TableInput
                key={tbl.id}
                table={tbl}
                value={tableData[tbl.id]}
                disabled={inputsDisabled}
                onChange={(v) => setTableData((p) => ({ ...p, [tbl.id]: v }))}
                t={t}
              />
            ))}
          </div>
        </Section>
      )}

      {needsVideo && (
        <Section title={t("exam.videoSection")}>
          <p className="text-sm text-ink-soft mb-3">{t("exam.videoHint")}</p>
          <Input
            type="url"
            disabled={inputsDisabled}
            value={videoUrl}
            placeholder="https://loom.com/..."
            onChange={(e) => setVideoUrl(e.target.value)}
          />
        </Section>
      )}

      {error && (
        <p className="text-ember border-l-2 border-ember pl-4 text-sm">{error}</p>
      )}

      {!preview && (
        <div className="flex items-center gap-4 hairline pt-6">
          <Button onClick={submit} disabled={!canSubmit} variant="ember">
            {submitting ? t("common.loading") : t("exam.submit")}
          </Button>
          {needsVideo && (
            <p className="text-xs text-ink-muted">{t("exam.videoReviewNote")}</p>
          )}
        </div>
      )}
      {preview && answerKey && (
        <div className="space-y-4 hairline pt-6">
          <div className="flex items-center gap-4">
            <Button onClick={() => setLocalGraded(true)} variant="ember">
              {t("exam.calculateScore")}
            </Button>
            <p className="text-xs text-ink-muted">{t("exam.answerKeyNote")}</p>
          </div>
          {localGraded && questions.length > 0 && (
            <div className="border border-ember/40 bg-ember/5 rounded-md p-6">
              <p className="font-display text-2xl">
                {t("exam.score", { score: localScore })}
              </p>
              <p className="text-sm text-ink-soft mt-1">
                {t("exam.mcqHits", { hits: localHits, total: questions.length })}
              </p>
            </div>
          )}
        </div>
      )}
      {preview && !answerKey && (
        <p className="num-label text-ember hairline pt-6">{t("exam.previewMode")}</p>
      )}
    </div>
  );
}

function QuestionFeedback({
  q,
  given,
  t,
}: {
  q: ExamQuestion;
  given: unknown;
  t: (k: string, opts?: Record<string, unknown>) => string;
}) {
  const correct = isAnswerCorrect(q, given);
  return (
    <div
      className={`text-xs border-l-2 pl-3 py-1 space-y-1 ${
        correct ? "border-ember text-ink-soft" : "border-ember/40 text-ink-soft"
      }`}
    >
      <p className="font-mono uppercase tracking-[0.14em] text-ember">
        {correct ? t("exam.questionCorrect") : t("exam.questionWrong")}
      </p>
      <p>
        <span className="font-medium">{t("exam.correctAnswer")}:</span>{" "}
        {formatCorrect(q.correct)}
      </p>
      {q.explanation && <p className="text-ink-muted">{q.explanation}</p>}
    </div>
  );
}

function formatCorrect(correct: ExamQuestion["correct"]): string {
  if (correct == null) return "—";
  if (Array.isArray(correct)) return correct.join(", ");
  if (typeof correct === "object") {
    return Object.entries(correct)
      .map(([k, v]) => `${k}→${v}`)
      .join(", ");
  }
  return String(correct);
}

function ResultPanel({
  result,
  needsVideo,
  assessment,
  t,
}: {
  result: SubmissionResult;
  needsVideo: boolean;
  assessment: ExamAssessment;
  t: (k: string, opts?: Record<string, unknown>) => string;
}) {
  // capa_2 / final: el MCQ ya autocalificó, pero la nota depende del video → en revisión.
  if (needsVideo) {
    return (
      <div className="border border-ember/40 bg-ember/5 rounded-md p-6 space-y-2">
        <p className="num-label text-ember">{t("exam.receivedTitle")}</p>
        <p className="text-sm text-ink leading-relaxed">{t("exam.receivedBody")}</p>
      </div>
    );
  }
  const score = result.auto_score ?? 0;
  const passed = score >= assessment.passing_score;
  return (
    <div
      className={`border rounded-md p-6 ${
        passed ? "border-ember/40 bg-ember/5" : "border-bone bg-paper-tint"
      }`}
    >
      <p className="font-display text-2xl">{t("exam.score", { score })}</p>
      <p className="text-sm text-ink-soft mt-1">
        {passed
          ? t("exam.pass", { passing: assessment.passing_score })
          : t("exam.fail", { passing: assessment.passing_score })}
      </p>
    </div>
  );
}

function CaseBrief({
  brief,
  t,
}: {
  brief: Record<string, unknown>;
  t: (k: string) => string;
}) {
  const title = typeof brief.title === "string" ? brief.title : "";
  const summary = typeof brief.summary === "string" ? brief.summary : "";
  return (
    <div className="border border-bone rounded-md p-5 bg-paper-warm/40 space-y-2">
      <p className="num-label">{t("exam.caseBrief")}</p>
      {title && <p className="font-display text-lg">{title}</p>}
      {summary && (
        <p className="text-sm text-ink-soft leading-relaxed whitespace-pre-line">
          {summary}
        </p>
      )}
    </div>
  );
}

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <section className="space-y-4">
      <p className="num-label">{title}</p>
      {children}
    </section>
  );
}

function QuestionInput({
  q,
  value,
  disabled,
  onChange,
}: {
  q: ExamQuestion;
  value: unknown;
  disabled: boolean;
  onChange: (v: unknown) => void;
}) {
  if (q.type === "single") {
    return (
      <div className="space-y-2">
        {(q.choices ?? []).map((c) => (
          <label
            key={c.id}
            className="flex items-start gap-3 text-sm cursor-pointer hover:bg-paper-tint p-2 -mx-2 rounded"
          >
            <input
              type="radio"
              name={q.id}
              disabled={disabled}
              checked={value === c.id}
              onChange={() => onChange(c.id)}
              className="mt-1"
            />
            <span>{c.text}</span>
          </label>
        ))}
      </div>
    );
  }
  if (q.type === "multi") {
    const selected = (value as string[] | undefined) ?? [];
    return (
      <div className="space-y-2">
        {(q.choices ?? []).map((c) => {
          const checked = selected.includes(c.id);
          return (
            <label
              key={c.id}
              className="flex items-start gap-3 text-sm cursor-pointer hover:bg-paper-tint p-2 -mx-2 rounded"
            >
              <input
                type="checkbox"
                disabled={disabled}
                checked={checked}
                onChange={() =>
                  onChange(
                    checked
                      ? selected.filter((x) => x !== c.id)
                      : [...selected, c.id],
                  )
                }
                className="mt-1"
              />
              <span>{c.text}</span>
            </label>
          );
        })}
      </div>
    );
  }
  // match
  const pairs = (value as Record<string, string> | undefined) ?? {};
  return (
    <div className="space-y-2">
      {(q.left ?? []).map((l) => (
        <div key={l.id} className="grid grid-cols-[1fr_auto] gap-3 items-center text-sm">
          <span>
            <span className="font-mono text-ink-faint mr-2">{l.id}.</span>
            {l.text}
          </span>
          <select
            disabled={disabled}
            value={pairs[l.id] ?? ""}
            onChange={(e) => onChange({ ...pairs, [l.id]: e.target.value })}
            className="border border-bone rounded px-2 py-1 text-sm bg-paper"
          >
            <option value="">—</option>
            {(q.right ?? []).map((r) => (
              <option key={r.id} value={r.id}>
                {r.id}. {r.text}
              </option>
            ))}
          </select>
        </div>
      ))}
    </div>
  );
}

function TableInput({
  table,
  value,
  disabled,
  onChange,
  t,
}: {
  table: ExamTable;
  value: unknown;
  disabled: boolean;
  onChange: (v: unknown) => void;
  t: (k: string) => string;
}) {
  // Tabla de clasificación: cada fila → una opción.
  if (table.rows && table.options) {
    const picks = (value as Record<string, string> | undefined) ?? {};
    return (
      <div className="border border-bone rounded-md p-5 space-y-3">
        {table.topic && <p className="num-label">{table.topic}</p>}
        <p className="text-sm leading-relaxed">{table.prompt}</p>
        <div className="space-y-2">
          {table.rows.map((row) => (
            <div key={row.id} className="grid grid-cols-[1fr_auto] gap-3 items-center text-sm">
              <span>{row.label}</span>
              <select
                disabled={disabled}
                value={picks[row.id] ?? ""}
                onChange={(e) => onChange({ ...picks, [row.id]: e.target.value })}
                className="border border-bone rounded px-2 py-1 text-sm bg-paper"
              >
                <option value="">—</option>
                {(table.options ?? []).map((o) => (
                  <option key={o.id} value={o.id}>
                    {o.label ?? o.text ?? o.id}
                  </option>
                ))}
              </select>
            </div>
          ))}
        </div>
      </div>
    );
  }

  // Tabla de secuencia: N pasos con día / canal / propósito.
  const steps = Array.isArray(table.expected_sequence) ? table.expected_sequence.length : 6;
  const rows = (value as Array<Record<string, string>> | undefined) ?? [];
  const setRow = (i: number, patch: Record<string, string>) => {
    const next = [...rows];
    next[i] = { ...(next[i] ?? {}), ...patch };
    onChange(next);
  };
  return (
    <div className="border border-bone rounded-md p-5 space-y-3">
      {table.topic && <p className="num-label">{table.topic}</p>}
      <p className="text-sm leading-relaxed">{table.prompt}</p>
      <div className="space-y-2">
        {Array.from({ length: steps }).map((_, i) => (
          <div key={i} className="grid grid-cols-[auto_5rem_7rem_1fr] gap-2 items-center text-sm">
            <span className="font-mono text-ink-faint">{i + 1}</span>
            <Input
              type="number"
              disabled={disabled}
              placeholder={t("exam.seqDay")}
              value={rows[i]?.dia ?? ""}
              onChange={(e) => setRow(i, { dia: e.target.value })}
            />
            <select
              disabled={disabled}
              value={rows[i]?.canal ?? ""}
              onChange={(e) => setRow(i, { canal: e.target.value })}
              className="border border-bone rounded px-2 py-1 text-sm bg-paper"
            >
              <option value="">—</option>
              {SEQ_CHANNELS.map((c) => (
                <option key={c} value={c}>
                  {c}
                </option>
              ))}
            </select>
            <Input
              disabled={disabled}
              placeholder={t("exam.seqPurpose")}
              value={rows[i]?.proposito ?? ""}
              onChange={(e) => setRow(i, { proposito: e.target.value })}
            />
          </div>
        ))}
      </div>
    </div>
  );
}
