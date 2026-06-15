import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { api } from "@/lib/api";
import { BackLink } from "@/components/BackLink";
import { ExamRunner, type ExamAssessment } from "@/components/exam/ExamRunner";

/** Vista admin/profesor: previsualiza un assessment tal como lo ve el alumno (solo lectura). */
export function AdminAssessmentPreview() {
  const { t } = useTranslation();
  const { assessmentId } = useParams();
  const [assessment, setAssessment] = useState<ExamAssessment | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!assessmentId) return;
    const controller = new AbortController();
    void (async () => {
      try {
        const { data } = await api.get<ExamAssessment>(
          `/assessments/${assessmentId}`,
          { signal: controller.signal },
        );
        setAssessment(data);
      } catch (err) {
        if ((err as { code?: string })?.code === "ERR_CANCELED") return;
        setError(t("common.error"));
      }
    })();
    return () => controller.abort();
  }, [assessmentId, t]);

  return (
    <div className="container-editorial py-16 md:py-24 max-w-3xl">
      <BackLink to="/admin/course">{t("exam.back")}</BackLink>
      <p className="num-label mt-6 text-ember">{t("exam.previewKicker")}</p>
      <h1 className="font-display text-display-md mt-3 mb-2 text-balance">
        {assessment?.title ?? t("exam.previewTitle")}
      </h1>
      {assessment && (
        <p className="num-label mb-10">
          {assessment.type} · {t("exam.passingScore", { score: assessment.passing_score })}
        </p>
      )}
      {error && (
        <p className="text-ember border-l-2 border-ember pl-4 text-sm">{error}</p>
      )}
      {!error && !assessment && <p className="num-label">{t("common.loading")}</p>}
      {assessment && <ExamRunner assessment={assessment} preview answerKey />}
    </div>
  );
}
