import { useState } from "react";
import { useTranslation } from "react-i18next";
import axios from "axios";
import { api } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Input, Textarea } from "@/components/ui/input";

const QUESTION_IDS = ["why_sales", "achievement", "hours_per_week"] as const;
type QuestionId = (typeof QUESTION_IDS)[number];

function wordCount(s: string): number {
  return s.trim().split(/\s+/).filter(Boolean).length;
}

export function ApplyPage() {
  const { t } = useTranslation();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [locale, setLocale] = useState<"es" | "en" | "pt">("es");
  const [answers, setAnswers] = useState<Record<QuestionId, string>>({
    why_sales: "",
    achievement: "",
    hours_per_week: "",
  });
  const [videoUrl, setVideoUrl] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [done, setDone] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const allQuestionsValid = QUESTION_IDS.every((q) => wordCount(answers[q]) >= 100);
  const canSubmit = name && email && videoUrl && allQuestionsValid && !submitting;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSubmitting(true);
    try {
      await api.post("/applications", {
        applicant_name: name,
        applicant_email: email,
        applicant_phone: phone || null,
        locale,
        video_url: videoUrl,
        answers: QUESTION_IDS.map((qid) => ({ question_id: qid, text: answers[qid] })),
      });
      setDone(true);
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

  if (done) {
    return (
      <div className="container-editorial py-32 max-w-2xl">
        <p className="num-label">№ 001 / acuse de recibo</p>
        <h1 className="font-display text-display-lg mt-5 text-balance">
          Tu aplicación está en nuestra mesa.
        </h1>
        <p className="text-ink-soft text-lg mt-6 leading-relaxed">
          Vamos a leer cada palabra, ver tu video, y decidir con calma. Si seguimos
          contigo, recibirás un email con los siguientes pasos en un plazo máximo de
          siete días.
        </p>
      </div>
    );
  }

  return (
    <div className="container-editorial py-16 md:py-24">
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
              Respondes en tu idioma.
            </p>
            <p>
              <span className="num-label mr-2">ii</span>
              Mínimo 100 palabras por pregunta.
            </p>
            <p>
              <span className="num-label mr-2">iii</span>
              Video corto (1–2 min) vendiéndote.
            </p>
            <p>
              <span className="num-label mr-2">iv</span>
              Humano + IA revisan tu aplicación.
            </p>
          </div>
        </header>

        <form onSubmit={handleSubmit} className="lg:col-span-8 space-y-14">
          <Fieldset number="01" title="Sobre ti">
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
                <Input value={phone} onChange={(e) => setPhone(e.target.value)} />
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

          <Fieldset number="02" title="Tres preguntas">
            {QUESTION_IDS.map((qid, idx) => (
              <Field
                key={qid}
                number={`02.${idx + 1}`}
                label={t(`apply.question${idx + 1}` as never)}
                required
              >
                <Textarea
                  value={answers[qid]}
                  onChange={(e) => setAnswers({ ...answers, [qid]: e.target.value })}
                  placeholder="Tómate tu tiempo. Cuéntanos lo que los formularios no muestran."
                  required
                />
                <WordCounter text={answers[qid]} />
              </Field>
            ))}
          </Fieldset>

          <Fieldset number="03" title="Tu video">
            <Field label={t("apply.video")} required>
              <Input
                type="url"
                value={videoUrl}
                onChange={(e) => setVideoUrl(e.target.value)}
                placeholder="https://loom.com/..."
                required
              />
              <p className="text-xs text-ink-muted mt-2 leading-relaxed">
                Véndete como lo harías en una llamada en frío. No nos mandes un CV en video.
              </p>
            </Field>
          </Fieldset>

          {error && (
            <p className="text-ember border-l-2 border-ember pl-4 text-sm">{error}</p>
          )}

          <div className="flex items-center gap-6 pt-4 hairline pt-10">
            <Button type="submit" disabled={!canSubmit} size="lg" variant="ember">
              {submitting ? "Enviando…" : t("apply.submit")} <span aria-hidden>→</span>
            </Button>
            <p className="text-xs text-ink-muted">
              Al enviar aceptas que revisemos tu aplicación con cariño.
            </p>
          </div>
        </form>
      </div>
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

function WordCounter({ text }: { text: string }) {
  const n = wordCount(text);
  const ok = n >= 100;
  const pct = Math.min(100, (n / 100) * 100);
  return (
    <div className="flex items-center gap-3 mt-3">
      <div className="flex-1 h-px bg-bone relative overflow-hidden">
        <div
          className={`absolute inset-y-0 left-0 transition-all duration-500 ${
            ok ? "bg-moss" : "bg-ink/40"
          }`}
          style={{ width: `${pct}%` }}
        />
      </div>
      <span
        className={`font-mono text-[11px] tabular-nums ${
          ok ? "text-moss" : "text-ink-faint"
        }`}
      >
        {n}/100
      </span>
    </div>
  );
}
