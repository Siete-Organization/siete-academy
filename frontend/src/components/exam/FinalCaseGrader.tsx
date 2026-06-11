import { useEffect, useMemo, useState } from "react";
import { useTranslation } from "react-i18next";
import { api } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/input";

/**
 * Calificación híbrida por ítem de la Prueba Final (Capa 3).
 * El profesor puntúa respuestas cortas (/max), tablas (/max) y la rúbrica de
 * video (15 dims × 0-2 = /30). El backend computa la nota del caso y del video;
 * acá mostramos un preview en vivo. MCQ ya viene autocalificado.
 */

interface ShortAnswer {
  id: string;
  topic?: string;
  prompt: string;
  rubric?: string;
  max_points?: number;
}
interface CaseTable {
  id: string;
  topic?: string;
  prompt: string;
  rubric?: string;
  max_points?: number;
}
interface VideoDim {
  id: number | string;
  label: string;
}
interface FinalConfig {
  questions?: unknown[];
  short_answers?: ShortAnswer[];
  tables?: CaseTable[];
  video_rubric?: { max_total?: number; dimensions?: VideoDim[] };
}

const clamp = (v: number, max: number) => Math.max(0, Math.min(max, v));

export function FinalCaseGrader({
  submissionId,
  assessmentId,
  payload,
  mcqAutoScore,
  onSubmitted,
}: {
  submissionId: number;
  assessmentId: number;
  payload: Record<string, unknown>;
  mcqAutoScore: number | null;
  onSubmitted: () => void;
}) {
  const { t } = useTranslation();
  const [config, setConfig] = useState<FinalConfig | null>(null);
  const [shortScores, setShortScores] = useState<Record<string, number>>({});
  const [tableScores, setTableScores] = useState<Record<string, number>>({});
  const [videoScores, setVideoScores] = useState<Record<string, number>>({});
  const [feedback, setFeedback] = useState("");
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    let active = true;
    void (async () => {
      const { data } = await api.get<{ config: FinalConfig }>(
        `/assessments/${assessmentId}`,
      );
      if (active) setConfig(data.config);
    })();
    return () => {
      active = false;
    };
  }, [assessmentId]);

  const shortAnswers = config?.short_answers ?? [];
  const tables = config?.tables ?? [];
  const videoDims = config?.video_rubric?.dimensions ?? [];
  const videoMax = config?.video_rubric?.max_total ?? 30;
  const mcqCount = config?.questions?.length ?? 0;

  const studentShort = (payload.short_answers as Record<string, string>) ?? {};
  const studentTables = (payload.tables as Record<string, unknown>) ?? {};

  const { casePct, videoPct, finalPct } = useMemo(() => {
    const shortMax = shortAnswers.reduce((s, a) => s + (a.max_points ?? 2), 0);
    const tableMax = tables.reduce((s, a) => s + (a.max_points ?? 0), 0);
    const mcqHits = Math.round(((mcqAutoScore ?? 0) / 100) * mcqCount);
    const shortPts = Object.values(shortScores).reduce((s, v) => s + v, 0);
    const tablePts = Object.values(tableScores).reduce((s, v) => s + v, 0);
    const caseMax = mcqCount + shortMax + tableMax;
    const cPct = caseMax > 0 ? ((mcqHits + shortPts + tablePts) / caseMax) * 100 : 0;
    const vPts = Object.values(videoScores).reduce((s, v) => s + v, 0);
    const vPct = videoMax > 0 ? (vPts / videoMax) * 100 : 0;
    return {
      casePct: Math.round(cPct * 100) / 100,
      videoPct: Math.round(vPct * 100) / 100,
      finalPct: Math.round((cPct * 0.7 + vPct * 0.3) * 100) / 100,
    };
  }, [shortAnswers, tables, shortScores, tableScores, videoScores, videoMax, mcqAutoScore, mcqCount]);

  const submit = async () => {
    setSubmitting(true);
    try {
      await api.post(`/assessments/submissions/${submissionId}/review`, {
        score: finalPct,
        feedback,
        details: {
          short_answers: shortScores,
          tables: tableScores,
          video_rubric: videoScores,
        },
      });
      onSubmitted();
    } finally {
      setSubmitting(false);
    }
  };

  if (!config) return <p className="num-label">{t("common.loading")}</p>;

  return (
    <div className="space-y-8">
      <div className="grid grid-cols-3 gap-4 border border-bone rounded-md p-5 bg-paper-tint">
        <Metric label={t("teacher.gradeCase")} value={casePct} />
        <Metric label={t("teacher.gradeVideo")} value={videoPct} />
        <Metric label={t("teacher.gradeFinal")} value={finalPct} accent />
      </div>

      {shortAnswers.length > 0 && (
        <section className="space-y-4">
          <p className="num-label">{t("teacher.gradeShort")}</p>
          {shortAnswers.map((sa) => (
            <ItemRow
              key={sa.id}
              topic={sa.topic}
              prompt={sa.prompt}
              rubric={sa.rubric}
              answer={studentShort[sa.id]}
              max={sa.max_points ?? 2}
              value={shortScores[sa.id] ?? 0}
              onChange={(v) =>
                setShortScores((p) => ({ ...p, [sa.id]: clamp(v, sa.max_points ?? 2) }))
              }
            />
          ))}
        </section>
      )}

      {tables.length > 0 && (
        <section className="space-y-4">
          <p className="num-label">{t("teacher.gradeTables")}</p>
          {tables.map((tb) => (
            <ItemRow
              key={tb.id}
              topic={tb.topic}
              prompt={tb.prompt}
              rubric={tb.rubric}
              answer={JSON.stringify(studentTables[tb.id] ?? null)}
              max={tb.max_points ?? 0}
              value={tableScores[tb.id] ?? 0}
              onChange={(v) =>
                setTableScores((p) => ({ ...p, [tb.id]: clamp(v, tb.max_points ?? 0) }))
              }
            />
          ))}
        </section>
      )}

      {videoDims.length > 0 && (
        <section className="space-y-3">
          <p className="num-label">{t("teacher.gradeVideoRubric")}</p>
          <div className="space-y-2">
            {videoDims.map((d) => (
              <div
                key={String(d.id)}
                className="grid grid-cols-[1fr_auto] gap-3 items-center text-sm border-b border-bone pb-2"
              >
                <span>
                  <span className="font-mono text-ink-faint mr-2">{String(d.id)}.</span>
                  {d.label}
                </span>
                <NumberInput
                  max={2}
                  value={videoScores[String(d.id)] ?? 0}
                  onChange={(v) =>
                    setVideoScores((p) => ({ ...p, [String(d.id)]: clamp(v, 2) }))
                  }
                />
              </div>
            ))}
          </div>
        </section>
      )}

      <label className="block">
        <span className="num-label mb-2 block">{t("teacher.feedback")}</span>
        <Textarea
          value={feedback}
          onChange={(e) => setFeedback(e.target.value)}
          placeholder={t("teacher.feedbackPlaceholder")}
        />
      </label>

      <Button onClick={submit} disabled={!feedback.trim() || submitting} size="lg" variant="ember">
        {t("teacher.approve")} <span aria-hidden>→</span>
      </Button>
    </div>
  );
}

function Metric({ label, value, accent }: { label: string; value: number; accent?: boolean }) {
  return (
    <div>
      <p className="num-label">{label}</p>
      <p className={`font-display text-3xl tabular-nums mt-1 ${accent ? "text-ember" : ""}`}>
        {value}%
      </p>
    </div>
  );
}

function ItemRow({
  topic,
  prompt,
  rubric,
  answer,
  max,
  value,
  onChange,
}: {
  topic?: string;
  prompt: string;
  rubric?: string;
  answer?: string;
  max: number;
  value: number;
  onChange: (v: number) => void;
}) {
  return (
    <div className="border border-bone rounded-md p-4 space-y-2">
      <div className="flex items-start justify-between gap-4">
        <div className="space-y-1">
          {topic && <p className="num-label">{topic}</p>}
          <p className="text-sm leading-relaxed">{prompt}</p>
        </div>
        <NumberInput max={max} value={value} onChange={onChange} />
      </div>
      <p className="text-sm text-ink whitespace-pre-line bg-paper-tint border border-bone rounded p-3">
        {answer || "—"}
      </p>
      {rubric && (
        <p className="text-xs text-ink-muted leading-relaxed">{rubric}</p>
      )}
    </div>
  );
}

function NumberInput({
  max,
  value,
  onChange,
}: {
  max: number;
  value: number;
  onChange: (v: number) => void;
}) {
  return (
    <span className="inline-flex items-baseline gap-1 font-mono">
      <input
        type="number"
        min={0}
        max={max}
        value={value}
        onChange={(e) => onChange(Number(e.target.value))}
        className="w-14 text-right tabular-nums bg-transparent border-0 border-b border-bone-strong focus:border-ink focus:outline-none"
      />
      <span className="text-ink-faint text-xs">/ {max}</span>
    </span>
  );
}
