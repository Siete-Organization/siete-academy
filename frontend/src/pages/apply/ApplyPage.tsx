import { useEffect, useMemo, useState } from "react";
import { useTranslation } from "react-i18next";
import { useLocation } from "react-router-dom";
import axios from "axios";
import PhoneInput from "react-phone-number-input";
import "react-phone-number-input/style.css";
import { api } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Input, Textarea } from "@/components/ui/input";

interface OpenPrompt {
  id: string;
  title: string;
  prompt: string;
  min_words: number;
  max_words: number;
}

interface McqChoice {
  id: string;
  text: string;
}

interface McqQuestion {
  id: string;
  section: "excel" | "logic" | "business" | "comprehension";
  prompt: string;
  choices: McqChoice[];
}

interface AdmissionRules {
  mcq_total_pass_pct: number;
  mcq_excel_pass_pct: number;
  seconds_per_question: number;
  min_completion_minutes: number;
}

interface AdmissionData {
  locale: string;
  open_prompts: OpenPrompt[];
  comprehension_text: string;
  mcq: McqQuestion[];
  rules: AdmissionRules;
}

interface ApplicationResponse {
  id: number;
  status: string;
  auto_decision: string | null;
  mcq_score: number | null;
  mcq_excel_score: number | null;
}

const SECTION_LABEL: Record<McqQuestion["section"], string> = {
  excel: "Excel y BBDD",
  logic: "Lógica y números",
  business: "Lectura de negocio",
  comprehension: "Comprensión de texto",
};

function wordCount(s: string): number {
  return s.trim().split(/\s+/).filter(Boolean).length;
}

function shuffle<T>(arr: T[]): T[] {
  const out = [...arr];
  for (let i = out.length - 1; i > 0; i -= 1) {
    const j = Math.floor(Math.random() * (i + 1));
    [out[i], out[j]] = [out[j], out[i]];
  }
  return out;
}

export function ApplyPage() {
  const { t } = useTranslation();
  const location = useLocation();
  const notInvited = Boolean(
    (location.state as { notInvited?: boolean } | null)?.notInvited,
  );
  const [admissionData, setAdmissionData] = useState<AdmissionData | null>(null);
  const [loadError, setLoadError] = useState<string | null>(null);
  const [startedAt, setStartedAt] = useState<string | null>(null);

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [linkedinUrl, setLinkedinUrl] = useState("");
  const [country, setCountry] = useState("");
  const [locale, setLocale] = useState<"es" | "en" | "pt">("es");
  const [openAnswers, setOpenAnswers] = useState<Record<string, string>>({});
  const [mcqAnswers, setMcqAnswers] = useState<Record<string, string>>({});
  const [videoUrl, setVideoUrl] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState<ApplicationResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  // Fetch admission content on mount. started_at se setea cuando llega el payload.
  useEffect(() => {
    void (async () => {
      try {
        const { data } = await api.get<AdmissionData>("/admission/questions");
        setAdmissionData(data);
        setStartedAt(new Date().toISOString());
      } catch {
        setLoadError(t("apply.loadError"));
      }
    })();
  }, [t]);

  // Order de MCQ + opciones se randomiza UNA vez por sesión cuando llega la data.
  const shuffledMcq = useMemo(() => {
    if (!admissionData) return [];
    return shuffle(admissionData.mcq).map((q) => ({
      ...q,
      choices: shuffle(q.choices),
    }));
  }, [admissionData]);

  const openAnswersValid = useMemo(() => {
    if (!admissionData) return false;
    return admissionData.open_prompts.every((p) => {
      const wc = wordCount(openAnswers[p.id] || "");
      return wc >= p.min_words && wc <= p.max_words;
    });
  }, [openAnswers, admissionData]);

  const mcqAllAnswered = useMemo(() => {
    if (!admissionData) return false;
    return admissionData.mcq.every((q) => Boolean(mcqAnswers[q.id]));
  }, [mcqAnswers, admissionData]);

  const canSubmit = Boolean(
    name &&
      email &&
      linkedinUrl &&
      country &&
      videoUrl &&
      openAnswersValid &&
      mcqAllAnswered &&
      !submitting &&
      admissionData,
  );

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSubmitting(true);
    try {
      const { data } = await api.post<ApplicationResponse>("/applications", {
        applicant_name: name,
        applicant_email: email,
        applicant_phone: phone || null,
        linkedin_url: linkedinUrl,
        country,
        locale,
        video_url: videoUrl,
        started_at: startedAt,
        answers: (admissionData?.open_prompts ?? []).map((p) => ({
          question_id: p.id,
          text: openAnswers[p.id] || "",
        })),
        mcq_answers: mcqAnswers,
      });
      setResult(data);
    } catch (err: unknown) {
      let message: string = t("common.error");
      if (axios.isAxiosError(err)) {
        const detail = err.response?.data?.detail;
        if (Array.isArray(detail) && detail[0]?.msg) message = String(detail[0].msg);
        else if (typeof detail === "string") message = detail;
        else message = err.message;
      } else if (err instanceof Error) {
        message = err.message;
      }
      setError(message);
    } finally {
      setSubmitting(false);
    }
  };

  if (result) return <ResultView result={result} t={t} />;

  if (loadError) {
    return (
      <div className="container-editorial py-32 max-w-2xl">
        <p className="num-label text-ember">error</p>
        <p className="text-ink mt-4">{loadError}</p>
      </div>
    );
  }

  if (!admissionData) {
    return (
      <div className="container-editorial py-32 max-w-2xl">
        <p className="num-label">{t("common.loading")}</p>
      </div>
    );
  }

  return (
    <div className="container-editorial py-16 md:py-24">
      {notInvited && (
        <div className="mb-10 border-l-2 border-ember bg-ember/5 pl-5 py-4">
          <p className="num-label text-ember">acceso restringido</p>
          <p className="text-sm text-ink mt-2 leading-relaxed max-w-2xl">
            Tu cuenta todavía no está aprobada. Empieza por aplicar acá abajo; te
            avisaremos por email cuando puedas ingresar.
          </p>
        </div>
      )}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-12">
        <header className="lg:col-span-4 lg:sticky lg:top-24 h-max">
          <p className="num-label">Aplicación · cohorte 001</p>
          <h1 className="font-display text-display-lg mt-4 text-balance">
            {t("apply.title")}
          </h1>
          <p className="text-ink-soft mt-6 text-pretty leading-relaxed">
            {t("apply.subtitle")}
          </p>
          <div className="hairline mt-10 pt-6 space-y-3 text-sm text-ink-muted">
            <p>
              <span className="num-label mr-2">i</span>
              Tres preguntas escritas con límite estricto de palabras.
            </p>
            <p>
              <span className="num-label mr-2">ii</span>
              {`${admissionData.mcq.length} preguntas de opción múltiple — sin volver atrás recomendado.`}
            </p>
            <p>
              <span className="num-label mr-2">iii</span>
              Tiempo estimado: ~70 minutos.
            </p>
            <p>
              <span className="num-label mr-2">iv</span>
              Resultado de Etapa 1 al instante al enviar.
            </p>
          </div>
        </header>

        <form onSubmit={handleSubmit} className="lg:col-span-8 space-y-14">
          <Fieldset number="01" title={t("apply.section01")}>
            <Field label={t("apply.name")} required>
              <Input value={name} onChange={(e) => setName(e.target.value)} required />
            </Field>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <Field label={t("apply.email")} required>
                <Input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                />
              </Field>
              <Field label={t("apply.phone")}>
                <PhoneInput
                  international
                  defaultCountry="PE"
                  value={phone}
                  onChange={(v) => setPhone(v ?? "")}
                  className="phone-input"
                />
              </Field>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <Field label={t("apply.linkedin")} required>
                <Input
                  type="url"
                  value={linkedinUrl}
                  onChange={(e) => setLinkedinUrl(e.target.value)}
                  placeholder="https://www.linkedin.com/in/..."
                  required
                />
              </Field>
              <Field label={t("apply.country")} required>
                <Input
                  value={country}
                  onChange={(e) => setCountry(e.target.value)}
                  placeholder={t("apply.countryPlaceholder")}
                  required
                />
              </Field>
            </div>
            <Field label={t("apply.locale")}>
              <div className="flex gap-6 pt-1 font-mono text-xs uppercase tracking-[0.18em]">
                {(["es", "en", "pt"] as const).map((l) => (
                  <button
                    key={l}
                    type="button"
                    onClick={() => setLocale(l)}
                    className={`pb-1 transition-colors ${
                      locale === l
                        ? "text-ink border-b border-ink"
                        : "text-ink-faint hover:text-ink"
                    }`}
                  >
                    {l === "es" ? "Español" : l === "en" ? "English" : "Português"}
                  </button>
                ))}
              </div>
            </Field>
          </Fieldset>

          <Fieldset number="02" title={t("apply.section02")}>
            <p className="text-sm text-ink-soft -mt-4">{t("apply.section02Intro")}</p>
            {admissionData.open_prompts.map((p, idx) => (
              <Field
                key={p.id}
                number={`02.${idx + 1}`}
                label={p.title}
                required
              >
                <p className="text-sm text-ink-soft mb-3 leading-relaxed">
                  {p.prompt}
                </p>
                <Textarea
                  value={openAnswers[p.id] || ""}
                  onChange={(e) =>
                    setOpenAnswers({ ...openAnswers, [p.id]: e.target.value })
                  }
                  rows={6}
                  placeholder={t("apply.openAnswerPlaceholder")}
                />
                <WordRangeCounter
                  text={openAnswers[p.id] || ""}
                  min={p.min_words}
                  max={p.max_words}
                  t={t}
                />
              </Field>
            ))}
          </Fieldset>

          <Fieldset number="03" title={t("apply.section03")}>
            <div className="border border-bone rounded-md p-5 bg-paper-warm/40">
              <p className="num-label mb-2">{t("apply.comprehensionTextTitle")}</p>
              <p className="text-sm text-ink-soft whitespace-pre-line leading-relaxed">
                {admissionData.comprehension_text}
              </p>
            </div>
            <p className="text-sm text-ink-soft -mt-4">{t("apply.section03Intro")}</p>
            <McqProgress
              answered={Object.keys(mcqAnswers).length}
              total={admissionData.mcq.length}
              t={t}
            />
            <ol className="space-y-6">
              {shuffledMcq.map((q, idx) => (
                <McqItem
                  key={q.id}
                  q={q}
                  idx={idx}
                  value={mcqAnswers[q.id]}
                  onSelect={(choiceId) =>
                    setMcqAnswers({ ...mcqAnswers, [q.id]: choiceId })
                  }
                />
              ))}
            </ol>
          </Fieldset>

          <Fieldset number="04" title={t("apply.section04")}>
            <Field label={t("apply.video")} required>
              <Input
                type="url"
                value={videoUrl}
                onChange={(e) => setVideoUrl(e.target.value)}
                placeholder="https://loom.com/..."
                required
              />
              <p className="text-xs text-ink-muted mt-2 leading-relaxed">
                {t("apply.videoHint")}
              </p>
            </Field>
          </Fieldset>

          {error && (
            <p className="text-ember border-l-2 border-ember pl-4 text-sm">{error}</p>
          )}

          <div className="flex items-start gap-6 pt-4 hairline pt-10 flex-wrap">
            <Button type="submit" disabled={!canSubmit} size="lg" variant="ember">
              {submitting ? "Enviando…" : t("apply.submit")} <span aria-hidden>→</span>
            </Button>
            <p className="text-xs text-ink-muted max-w-md">
              {canSubmit
                ? t("apply.submitReady")
                : t("apply.submitIncomplete")}
            </p>
          </div>
        </form>
      </div>
    </div>
  );
}

function McqItem({
  q,
  idx,
  value,
  onSelect,
}: {
  q: McqQuestion;
  idx: number;
  value: string | undefined;
  onSelect: (choiceId: string) => void;
}) {
  return (
    <li className="border border-bone rounded-md p-5 space-y-4 bg-paper">
      <div className="flex items-baseline justify-between gap-4">
        <p className="num-label">
          {String(idx + 1).padStart(2, "0")} · {SECTION_LABEL[q.section]}
        </p>
        {value && <span className="text-xs font-mono text-ember">✓</span>}
      </div>
      <p className="text-sm leading-relaxed whitespace-pre-line">{q.prompt}</p>
      <div className="space-y-2">
        {q.choices.map((c) => (
          <label
            key={c.id}
            className="flex items-start gap-3 text-sm cursor-pointer hover:bg-paper-tint p-2 -mx-2 rounded"
          >
            <input
              type="radio"
              name={q.id}
              checked={value === c.id}
              onChange={() => onSelect(c.id)}
              className="mt-1"
            />
            <span className="leading-relaxed">{c.text}</span>
          </label>
        ))}
      </div>
    </li>
  );
}

function McqProgress({
  answered,
  total,
  t,
}: {
  answered: number;
  total: number;
  t: (k: string, opts?: Record<string, unknown>) => string;
}) {
  const pct = total ? Math.round((answered / total) * 100) : 0;
  return (
    <div className="sticky top-4 z-10 bg-paper/95 backdrop-blur border border-bone rounded-md px-4 py-3 flex items-center gap-3 -mt-2">
      <span className="num-label tabular-nums">
        {t("apply.mcqProgress", { answered, total })}
      </span>
      <div className="flex-1 h-1 bg-bone rounded-full overflow-hidden">
        <div
          className="h-full bg-ink transition-all"
          style={{ width: `${pct}%` }}
        />
      </div>
      <span className="font-mono text-[10px] tabular-nums text-ink-muted">
        {pct}%
      </span>
    </div>
  );
}

function WordRangeCounter({
  text,
  min,
  max,
  t,
}: {
  text: string;
  min: number;
  max: number;
  t: (k: string, opts?: Record<string, unknown>) => string;
}) {
  const n = wordCount(text);
  const inRange = n >= min && n <= max;
  return (
    <div className="flex items-center justify-end mt-3">
      <span
        className={`font-mono text-[11px] tabular-nums ${
          inRange ? "text-ember" : "text-ink-faint"
        }`}
      >
        {t("apply.wordRange", { n, min, max })}
        {inRange && " ✓"}
      </span>
    </div>
  );
}

function ResultView({
  result,
  t,
}: {
  result: ApplicationResponse;
  t: (k: string, opts?: Record<string, unknown>) => string;
}) {
  const decision = result.auto_decision;
  const passed = decision === "passed_stage_1";
  const titleKey =
    decision === null
      ? "apply.resultPending"
      : passed
      ? "apply.resultPassed"
      : "apply.resultRejected";
  const bodyKey =
    decision === null
      ? "apply.resultPendingBody"
      : passed
      ? "apply.resultPassedBody"
      : `apply.reason_${decision}`;
  return (
    <div className="container-editorial py-32 max-w-2xl">
      <p className="num-label">№ {String(result.id).padStart(3, "0")} · acuse de recibo</p>
      <h1 className="font-display text-display-lg mt-5 text-balance">{t(titleKey)}</h1>
      <p className="text-ink-soft text-lg mt-6 leading-relaxed">{t(bodyKey)}</p>
      {result.mcq_score !== null && (
        <div className="hairline mt-10 pt-6 grid grid-cols-2 gap-4 max-w-sm">
          <div>
            <p className="num-label">{t("apply.scoreTotal")}</p>
            <p className="font-display text-3xl mt-2 tabular-nums">{result.mcq_score}%</p>
          </div>
          <div>
            <p className="num-label">{t("apply.scoreExcel")}</p>
            <p className="font-display text-3xl mt-2 tabular-nums">
              {result.mcq_excel_score}%
            </p>
          </div>
        </div>
      )}
    </div>
  );
}

function Fieldset({
  number,
  title,
  children,
}: {
  number: string;
  title: string;
  children: React.ReactNode;
}) {
  return (
    <fieldset className="space-y-8">
      <legend className="flex items-baseline gap-4 mb-2 w-full">
        <span className="num-label tabular-nums">{number}</span>
        <span className="font-display text-2xl tracking-editorial">{title}</span>
        <span className="flex-1 h-px bg-bone" />
      </legend>
      {children}
    </fieldset>
  );
}

function Field({
  label,
  children,
  number,
  required,
}: {
  label: string;
  children: React.ReactNode;
  number?: string;
  required?: boolean;
}) {
  return (
    <label className="block">
      <span className="flex items-baseline gap-2 mb-2">
        {number && <span className="num-label tabular-nums">{number}</span>}
        <span className="text-[13px] font-medium text-ink">{label}</span>
        {required && <span className="text-ember">*</span>}
      </span>
      {children}
    </label>
  );
}
