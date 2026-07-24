import { useEffect, useMemo, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { api } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { BackLink } from "@/components/BackLink";
import { LoadError } from "@/components/LoadError";

const RESOURCE_ICONS: Record<string, string> = {
  pdf: "📄",
  ppt: "📊",
  video: "🎞",
  doc: "📝",
  link: "🔗",
};

type StepKey = "video" | "avatar" | "presentation" | "material" | "exam";

interface PresentationBlock {
  title: string;
  bullets?: string[];
  source?: string;
}

interface Lesson {
  id: number;
  order_index: number;
  kind: "video" | "reading";
  youtube_id: string | null;
  video_url: string | null;
  duration_seconds: number | null;
  avatar_audio_url: string | null;
  avatar_script: string | null;
  presentation_url: string | null;
  presentation_blocks: PresentationBlock[] | null;
  title: string;
  body: string | null;
}

interface McqChoice {
  id: string;
  text: string;
}

interface McqQuestion {
  id: string;
  type: "single" | "multi" | "match";
  prompt: string;
  choices?: McqChoice[];
  left?: McqChoice[];
  right?: McqChoice[];
  correct: string[] | Record<string, string>;
  explanation?: string;
}

interface Assessment {
  id: number;
  type: string;
  title: string;
  config: { questions?: McqQuestion[]; rules?: Record<string, unknown> } & Record<
    string,
    unknown
  >;
  passing_score: number;
}

interface ModuleResource {
  id: number;
  module_id: number;
  lesson_id: number | null;
  kind: "pdf" | "ppt" | "video" | "doc" | "link";
  title: string;
  url: string;
  order_index: number;
}

interface SubmissionResult {
  id: number;
  auto_score: number | null;
  status: string;
}

export function ModulePage() {
  const { moduleId } = useParams();
  const { t, i18n } = useTranslation();
  const [lessons, setLessons] = useState<Lesson[]>([]);
  const [selectedLesson, setSelectedLesson] = useState<Lesson | null>(null);
  const [assessment, setAssessment] = useState<Assessment | null>(null);
  const [resources, setResources] = useState<ModuleResource[]>([]);
  const [activeStep, setActiveStep] = useState<StepKey>("video");
  const [completedSteps, setCompletedSteps] = useState<Set<StepKey>>(new Set());
  const [loadFailed, setLoadFailed] = useState(false);
  const [retryKey, setRetryKey] = useState(0);

  useEffect(() => {
    if (!moduleId) return;
    const controller = new AbortController();
    setLoadFailed(false);
    void (async () => {
      try {
        const { data } = await api.get<Lesson[]>(
          `/courses/modules/${moduleId}/lessons`,
          {
            params: { locale: i18n.language.slice(0, 2) },
            signal: controller.signal,
          },
        );
        setLessons(data);
        setSelectedLesson((prev) => {
          if (prev && data.some((l) => l.id === prev.id)) {
            return data.find((l) => l.id === prev.id) ?? data[0] ?? null;
          }
          return data[0] ?? null;
        });
      } catch (err) {
        if ((err as { code?: string })?.code !== "ERR_CANCELED") setLoadFailed(true);
      }
    })();
    return () => controller.abort();
  }, [moduleId, i18n.language, retryKey]);

  useEffect(() => {
    if (!selectedLesson) {
      setAssessment(null);
      setResources([]);
      return;
    }
    const controller = new AbortController();
    setActiveStep("video");
    setCompletedSteps(new Set());
    void (async () => {
      try {
        const [r, a] = await Promise.all([
          api.get<ModuleResource[]>(
            `/courses/lessons/${selectedLesson.id}/resources`,
            { signal: controller.signal },
          ),
          api.get<Assessment[]>(`/assessments/lesson/${selectedLesson.id}`, {
            signal: controller.signal,
          }),
        ]);
        setResources(r.data);
        setAssessment(a.data[0] ?? null);
      } catch (err) {
        if ((err as { code?: string })?.code !== "ERR_CANCELED") throw err;
      }
    })();
    return () => controller.abort();
  }, [selectedLesson?.id]);

  const stepAvailability = useMemo(() => {
    if (!selectedLesson) {
      return { video: false, avatar: false, presentation: false, material: false, exam: false };
    }
    return {
      video: Boolean(selectedLesson.video_url || selectedLesson.youtube_id),
      avatar: Boolean(selectedLesson.avatar_audio_url || selectedLesson.avatar_script),
      presentation: Boolean(
        selectedLesson.presentation_url ||
          (selectedLesson.presentation_blocks && selectedLesson.presentation_blocks.length > 0) ||
          selectedLesson.body,
      ),
      material: resources.length > 0,
      exam: Boolean(assessment),
    };
  }, [selectedLesson, resources, assessment]);

  const stepsOrder: StepKey[] = ["video", "avatar", "presentation", "material", "exam"];

  const isStepUnlocked = (step: StepKey): boolean => {
    const idx = stepsOrder.indexOf(step);
    if (idx === 0) return true;
    for (let i = 0; i < idx; i += 1) {
      const prev = stepsOrder[i];
      if (stepAvailability[prev] && !completedSteps.has(prev)) return false;
    }
    return true;
  };

  const markStepComplete = (step: StepKey) => {
    setCompletedSteps((prev) => {
      const next = new Set(prev);
      next.add(step);
      return next;
    });
    const idx = stepsOrder.indexOf(step);
    for (let i = idx + 1; i < stepsOrder.length; i += 1) {
      if (stepAvailability[stepsOrder[i]]) {
        setActiveStep(stepsOrder[i]);
        return;
      }
    }
  };

  if (loadFailed) {
    return (
      <div className="container-editorial py-12">
        <BackLink to="/student" className="mb-8">{t("nav.myProgress")}</BackLink>
        <LoadError onRetry={() => setRetryKey((k) => k + 1)} />
      </div>
    );
  }

  return (
    <div className="container-editorial py-12">
      <BackLink to="/student" className="mb-8">{t("nav.myProgress")}</BackLink>
      <div className="grid grid-cols-1 lg:grid-cols-[280px_1fr] gap-12">
      <aside className="lg:sticky lg:top-24 h-max space-y-8">
        <div>
          <p className="num-label mb-4">Lecciones</p>
          <ol className="space-y-0.5">
            {lessons.map((l, i) => (
              <li key={l.id}>
                <button
                  onClick={() => setSelectedLesson(l)}
                  className={`w-full text-left py-2.5 px-3 -mx-3 rounded grid grid-cols-[24px_1fr] gap-2 items-baseline transition-colors ${
                    selectedLesson?.id === l.id
                      ? "bg-ink text-paper"
                      : "hover:bg-paper-tint"
                  }`}
                >
                  <span
                    className={`font-mono text-[10px] tabular-nums ${
                      selectedLesson?.id === l.id ? "text-paper/60" : "text-ink-faint"
                    }`}
                  >
                    {l.kind === "reading" ? "📖" : String(i + 1).padStart(2, "0")}
                  </span>
                  <span className="text-sm leading-tight">{l.title}</span>
                </button>
              </li>
            ))}
          </ol>
        </div>
        <div className="hairline pt-6 space-y-2">
          <p className="num-label mb-2">{t("exam.evaluations")}</p>
          <Link
            to={`/student/module/${moduleId}/exam`}
            className="block text-sm py-2 px-3 -mx-3 rounded hover:bg-paper-tint transition-colors"
          >
            → {t("exam.moduleTitle")}
          </Link>
          <Link
            to="/student/final"
            className="block text-sm py-2 px-3 -mx-3 rounded hover:bg-paper-tint transition-colors"
          >
            → {t("exam.finalTitle")}
          </Link>
        </div>
      </aside>

      <main>
        {selectedLesson ? (
          <article className="space-y-8">
            <header>
              <p className="num-label">
                {`${t("student.lesson")} ${String(selectedLesson.order_index + 1).padStart(2, "0")}`}
              </p>
              <h1 className="font-display text-display-md mt-3 text-balance">
                {selectedLesson.title}
              </h1>
            </header>

            <StepNav
              steps={stepsOrder}
              availability={stepAvailability}
              completed={completedSteps}
              active={activeStep}
              isUnlocked={isStepUnlocked}
              onSelect={(s) => setActiveStep(s)}
              t={t}
            />

            <section className="space-y-6">
              {activeStep === "video" && (
                <VideoStep
                  lesson={selectedLesson}
                  onComplete={() => markStepComplete("video")}
                  t={t}
                />
              )}
              {activeStep === "avatar" && (
                <AvatarStep
                  lesson={selectedLesson}
                  onComplete={() => markStepComplete("avatar")}
                  t={t}
                />
              )}
              {activeStep === "presentation" && (
                <PresentationStep
                  lesson={selectedLesson}
                  onComplete={() => markStepComplete("presentation")}
                  t={t}
                />
              )}
              {activeStep === "material" && (
                <MaterialStep
                  resources={resources}
                  onComplete={() => markStepComplete("material")}
                  t={t}
                />
              )}
              {activeStep === "exam" && assessment && (
                <ExamStep
                  assessment={assessment}
                  onComplete={() => {
                    markStepComplete("exam");
                    void markLessonComplete(selectedLesson.id);
                  }}
                  t={t}
                />
              )}
            </section>
          </article>
        ) : (
          <p className="text-ink-muted">{t("common.loading")}</p>
        )}
      </main>
      </div>
    </div>
  );
}

function StepNav({
  steps,
  availability,
  completed,
  active,
  isUnlocked,
  onSelect,
  t,
}: {
  steps: StepKey[];
  availability: Record<StepKey, boolean>;
  completed: Set<StepKey>;
  active: StepKey;
  isUnlocked: (s: StepKey) => boolean;
  onSelect: (s: StepKey) => void;
  t: (k: string) => string;
}) {
  const labels: Record<StepKey, string> = {
    video: t("student.stepVideo"),
    avatar: t("student.stepAvatar"),
    presentation: t("student.stepPresentation"),
    material: t("student.stepMaterial"),
    exam: t("student.stepExam"),
  };
  return (
    <ol className="grid grid-cols-5 gap-1 border-y border-bone py-3 text-xs font-mono uppercase tracking-[0.14em]">
      {steps.map((s, i) => {
        const present = availability[s];
        const isDone = completed.has(s);
        const isActive = s === active;
        const unlocked = isUnlocked(s);
        const clickable = present && unlocked;
        return (
          <li key={s}>
            <button
              disabled={!clickable}
              onClick={() => clickable && onSelect(s)}
              className={`w-full text-left py-2 px-2 rounded transition-colors flex flex-col gap-1 ${
                isActive
                  ? "bg-ink text-paper"
                  : isDone
                  ? "bg-paper-tint text-ink"
                  : clickable
                  ? "hover:bg-paper-tint text-ink-soft"
                  : "text-ink-faint cursor-not-allowed"
              }`}
              title={
                !present
                  ? t("student.stepNoContent")
                  : !unlocked
                  ? t("student.stepLocked")
                  : ""
              }
            >
              <span className="text-[10px] tabular-nums">
                {String(i + 1).padStart(2, "0")} {isDone ? "✓" : ""}
              </span>
              <span className="text-[11px] tracking-normal normal-case">
                {labels[s]}
              </span>
            </button>
          </li>
        );
      })}
    </ol>
  );
}

function VideoStep({
  lesson,
  onComplete,
  t,
}: {
  lesson: Lesson;
  onComplete: () => void;
  t: (k: string) => string;
}) {
  if (!lesson.video_url && !lesson.youtube_id) {
    return <p className="text-ink-muted">{t("student.stepNoContent")}</p>;
  }
  return (
    <div className="space-y-4">
      <div className="aspect-video border border-bone shadow-frame overflow-hidden rounded-md bg-black">
        {lesson.video_url ? (
          <video
            className="w-full h-full"
            src={lesson.video_url}
            controls
            controlsList="nodownload"
            playsInline
          />
        ) : (
          <iframe
            className="w-full h-full"
            src={`https://www.youtube-nocookie.com/embed/${lesson.youtube_id}?rel=0&modestbranding=1`}
            title={lesson.title}
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowFullScreen
          />
        )}
      </div>
      <Button variant="outline" onClick={onComplete}>
        {t("student.stepNext")} →
      </Button>
    </div>
  );
}

function AvatarStep({
  lesson,
  onComplete,
  t,
}: {
  lesson: Lesson;
  onComplete: () => void;
  t: (k: string) => string;
}) {
  if (!lesson.avatar_audio_url && !lesson.avatar_script) {
    return <p className="text-ink-muted">{t("student.stepNoContent")}</p>;
  }
  return (
    <div className="space-y-4">
      <div className="flex items-start gap-4 border border-bone rounded-md p-6 bg-paper-tint">
        <div className="w-16 h-16 rounded-full bg-ink/10 flex items-center justify-center text-2xl shrink-0">
          🤖
        </div>
        <div className="flex-1 space-y-3">
          {lesson.avatar_audio_url ? (
            <audio controls src={lesson.avatar_audio_url} className="w-full">
              {t("student.avatarPlayPrompt")}
            </audio>
          ) : (
            <p className="text-xs font-mono uppercase tracking-[0.14em] text-ink-muted">
              {t("student.avatarPlayPrompt")} ({t("student.stepNoContent")})
            </p>
          )}
          {lesson.avatar_script && (
            <p className="text-sm text-ink-soft whitespace-pre-line leading-relaxed">
              {lesson.avatar_script}
            </p>
          )}
        </div>
      </div>
      <Button variant="outline" onClick={onComplete}>
        {t("student.stepNext")} →
      </Button>
    </div>
  );
}

function PresentationStep({
  lesson,
  onComplete,
  t,
}: {
  lesson: Lesson;
  onComplete: () => void;
  t: (k: string) => string;
}) {
  const hasBlocks = lesson.presentation_blocks && lesson.presentation_blocks.length > 0;
  const hasUrl = Boolean(lesson.presentation_url);
  const hasBody = Boolean(lesson.body);
  if (!hasBlocks && !hasUrl && !hasBody) {
    return <p className="text-ink-muted">{t("student.stepNoContent")}</p>;
  }
  return (
    <div className="space-y-4">
      {hasUrl && (
        <a
          href={lesson.presentation_url!}
          target="_blank"
          rel="noreferrer"
          className="inline-flex items-center gap-2 text-sm text-ember hover:underline"
        >
          📊 {t("student.stepPresentation")} ↗
        </a>
      )}
      {hasBlocks && (
        <ol className="space-y-4">
          {lesson.presentation_blocks!.map((b, i) => (
            <li
              key={i}
              className="border border-bone rounded-md p-5 bg-paper space-y-3"
            >
              <p className="font-mono text-[10px] uppercase tracking-[0.14em] text-ink-faint">
                {String(i + 1).padStart(2, "0")}
              </p>
              <h3 className="font-display text-lg">{b.title}</h3>
              {b.bullets && (
                <ul className="list-disc pl-5 space-y-1 text-sm text-ink-soft">
                  {b.bullets.map((bl, j) => (
                    <li key={j}>{bl}</li>
                  ))}
                </ul>
              )}
              {b.source && (
                <p className="text-[11px] font-mono text-ink-faint">
                  Fuente: {b.source}
                </p>
              )}
            </li>
          ))}
        </ol>
      )}
      {!hasBlocks && hasBody && (
        <div className="prose prose-lg max-w-none text-ink-soft leading-relaxed whitespace-pre-line">
          {lesson.body}
        </div>
      )}
      <Button variant="outline" onClick={onComplete}>
        {t("student.stepNext")} →
      </Button>
    </div>
  );
}

function MaterialStep({
  resources,
  onComplete,
  t,
}: {
  resources: ModuleResource[];
  onComplete: () => void;
  t: (k: string) => string;
}) {
  if (resources.length === 0) {
    return <p className="text-ink-muted">{t("student.stepNoContent")}</p>;
  }
  return (
    <div className="space-y-4">
      <ul className="space-y-2">
        {resources.map((r) => (
          <li key={r.id}>
            <a
              href={r.url}
              target="_blank"
              rel="noreferrer"
              className="flex items-baseline gap-3 text-sm text-ink-soft hover:text-ember transition-colors border border-bone rounded-md px-4 py-3"
            >
              <span>{RESOURCE_ICONS[r.kind] || "🔗"}</span>
              <span className="leading-tight truncate flex-1">{r.title}</span>
              <span className="font-mono text-[10px] uppercase tracking-[0.14em] text-ink-faint">
                {r.kind}
              </span>
            </a>
          </li>
        ))}
      </ul>
      <Button variant="outline" onClick={onComplete}>
        {t("student.stepNext")} →
      </Button>
    </div>
  );
}

function ExamStep({
  assessment,
  onComplete,
  t,
}: {
  assessment: Assessment;
  onComplete: () => void;
  t: (k: string, opts?: Record<string, unknown>) => string;
}) {
  const questions = assessment.config.questions ?? [];
  const [answers, setAnswers] = useState<Record<string, unknown>>({});
  const [result, setResult] = useState<SubmissionResult | null>(null);
  const [submitting, setSubmitting] = useState(false);

  const submit = async () => {
    setSubmitting(true);
    try {
      const { data } = await api.post<SubmissionResult>(
        "/assessments/submissions",
        { assessment_id: assessment.id, payload: { answers } },
      );
      setResult(data);
      if ((data.auto_score ?? 0) >= assessment.passing_score) {
        onComplete();
      }
    } finally {
      setSubmitting(false);
    }
  };

  if (questions.length === 0) {
    return <p className="text-ink-muted">{t("student.stepNoContent")}</p>;
  }

  if (result) {
    return (
      <ExamReview
        questions={questions}
        answers={answers}
        result={result}
        passing={assessment.passing_score}
        t={t}
      />
    );
  }

  return (
    <div className="space-y-6">
      <p className="text-sm text-ink-muted">{assessment.title}</p>
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
              onChange={(v) => setAnswers((prev) => ({ ...prev, [q.id]: v }))}
            />
          </li>
        ))}
      </ol>
      <Button onClick={submit} disabled={submitting}>
        {t("student.examSubmit")}
      </Button>
    </div>
  );
}

function QuestionInput({
  q,
  value,
  onChange,
}: {
  q: McqQuestion;
  value: unknown;
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
                checked={checked}
                onChange={() => {
                  const next = checked
                    ? selected.filter((x) => x !== c.id)
                    : [...selected, c.id];
                  onChange(next);
                }}
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

function ExamReview({
  questions,
  answers,
  result,
  passing,
  t,
}: {
  questions: McqQuestion[];
  answers: Record<string, unknown>;
  result: SubmissionResult;
  passing: number;
  t: (k: string, opts?: Record<string, unknown>) => string;
}) {
  const score = result.auto_score ?? 0;
  const passed = score >= passing;
  return (
    <div className="space-y-6">
      <div
        className={`border rounded-md p-5 ${passed ? "border-ember/40 bg-ember/5" : "border-bone bg-paper-tint"}`}
      >
        <p className="font-display text-2xl">{t("student.examScore", { score })}</p>
        <p className="text-sm text-ink-soft mt-1">
          {passed
            ? t("student.examPass", { passing })
            : t("student.examFail", { passing })}
        </p>
      </div>
      <ol className="space-y-4">
        {questions.map((q, i) => {
          const given = answers[q.id];
          const isCorrect = checkAnswer(q, given);
          return (
            <li
              key={q.id}
              className={`border rounded-md p-5 space-y-3 ${
                isCorrect ? "border-ember/30" : "border-bone"
              }`}
            >
              <p className="font-mono text-[10px] uppercase tracking-[0.14em] text-ink-faint">
                {String(i + 1).padStart(2, "0")} · {isCorrect ? "✓" : "✗"}
              </p>
              <p className="text-sm leading-relaxed">{q.prompt}</p>
              <div className="text-xs space-y-1">
                <p className="text-ink-muted">
                  <span className="font-mono uppercase tracking-[0.14em] mr-2">
                    {t("student.examYourAnswer")}:
                  </span>
                  {formatAnswer(q, given)}
                </p>
                <p className="text-ink-muted">
                  <span className="font-mono uppercase tracking-[0.14em] mr-2">
                    {t("student.examCorrect")}:
                  </span>
                  {formatAnswer(q, q.correct)}
                </p>
              </div>
              {q.explanation && (
                <p className="text-sm text-ink-soft border-t border-bone pt-3">
                  <span className="font-mono text-[10px] uppercase tracking-[0.14em] text-ink-faint mr-2">
                    {t("student.examExplanation")}:
                  </span>
                  {q.explanation}
                </p>
              )}
            </li>
          );
        })}
      </ol>
    </div>
  );
}

function checkAnswer(q: McqQuestion, given: unknown): boolean {
  if (given === undefined || given === null) return false;
  if (q.type === "single") {
    const correct = Array.isArray(q.correct) ? q.correct[0] : q.correct;
    return String(given) === String(correct);
  }
  if (q.type === "multi") {
    if (!Array.isArray(given) || !Array.isArray(q.correct)) return false;
    const a = [...given].map(String).sort();
    const b = [...(q.correct as string[])].map(String).sort();
    return a.length === b.length && a.every((x, i) => x === b[i]);
  }
  if (q.type === "match") {
    if (typeof given !== "object" || typeof q.correct !== "object" || Array.isArray(q.correct)) {
      return false;
    }
    const g = given as Record<string, string>;
    const c = q.correct as Record<string, string>;
    const gKeys = Object.keys(g);
    const cKeys = Object.keys(c);
    if (gKeys.length !== cKeys.length) return false;
    return cKeys.every((k) => String(g[k]) === String(c[k]));
  }
  return false;
}

function formatAnswer(q: McqQuestion, ans: unknown): string {
  if (ans === undefined || ans === null) return "—";
  if (q.type === "single") {
    const id = Array.isArray(ans) ? ans[0] : ans;
    const choice = (q.choices ?? []).find((c) => c.id === String(id));
    return choice ? `${choice.id}. ${choice.text}` : String(id);
  }
  if (q.type === "multi") {
    const ids = Array.isArray(ans) ? ans : [];
    return ids.map((id) => {
      const c = (q.choices ?? []).find((x) => x.id === String(id));
      return c ? `${c.id}` : String(id);
    }).join(", ") || "—";
  }
  if (q.type === "match") {
    if (typeof ans !== "object") return "—";
    const pairs = Object.entries(ans as Record<string, string>);
    return pairs.map(([l, r]) => `${l}→${r}`).join(", ") || "—";
  }
  return "—";
}

async function markLessonComplete(lessonId: number) {
  try {
    const { data: enrollments } = await api.get<{ id: number }[]>("/enrollment/me");
    const enrollment = enrollments[0];
    if (!enrollment) return;
    await api.post(`/enrollment/${enrollment.id}/progress`, {
      lesson_id: lessonId,
      watched_pct: 100,
      completed: true,
    });
  } catch {
    // No enrollment yet (admin/teacher preview) — silently ignore.
  }
}
