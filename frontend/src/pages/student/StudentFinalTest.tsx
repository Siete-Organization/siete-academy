import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { api } from "@/lib/api";
import { BackLink } from "@/components/BackLink";
import { ExamRunner, type ExamAssessment } from "@/components/exam/ExamRunner";

export function StudentFinalTest() {
  const { t } = useTranslation();
  const [assessment, setAssessment] = useState<ExamAssessment | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const controller = new AbortController();
    void (async () => {
      try {
        const { data } = await api.get<ExamAssessment>("/assessments/final", {
          signal: controller.signal,
        });
        setAssessment(data);
      } catch (err) {
        if ((err as { code?: string })?.code === "ERR_CANCELED") return;
        setError(t("exam.finalUnavailable"));
      }
    })();
    return () => controller.abort();
  }, [t]);

  return (
    <div className="container-editorial py-16 md:py-24 max-w-3xl">
      <BackLink to="/student">{t("exam.back")}</BackLink>
      <p className="num-label mt-6">{t("exam.finalKicker")}</p>
      <h1 className="font-display text-display-lg mt-3 mb-10 text-balance">
        {assessment?.title ?? t("exam.finalTitle")}
      </h1>
      {error && (
        <p className="text-ember border-l-2 border-ember pl-4 text-sm">{error}</p>
      )}
      {!error && !assessment && <p className="num-label">{t("common.loading")}</p>}
      {assessment && <ExamRunner assessment={assessment} />}
    </div>
  );
}
