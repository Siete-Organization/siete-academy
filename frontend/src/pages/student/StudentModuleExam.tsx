import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { api } from "@/lib/api";
import { BackLink } from "@/components/BackLink";
import { ExamRunner, type ExamAssessment } from "@/components/exam/ExamRunner";

/** Prueba de módulo (Capa 2): MCQ + video narrado. Una por módulo (lesson_id NULL). */
export function StudentModuleExam() {
  const { t } = useTranslation();
  const { moduleId } = useParams();
  const [assessment, setAssessment] = useState<ExamAssessment | null>(null);
  const [state, setState] = useState<"loading" | "none" | "ready" | "error">("loading");

  useEffect(() => {
    if (!moduleId) return;
    const controller = new AbortController();
    void (async () => {
      try {
        const { data } = await api.get<ExamAssessment[]>(
          `/assessments/module/${moduleId}`,
          { signal: controller.signal },
        );
        const capa2 = data.find((a) => a.type === "capa_2");
        if (!capa2) {
          setState("none");
          return;
        }
        setAssessment(capa2);
        setState("ready");
      } catch (err) {
        if ((err as { code?: string })?.code === "ERR_CANCELED") return;
        setState("error");
      }
    })();
    return () => controller.abort();
  }, [moduleId]);

  return (
    <div className="container-editorial py-16 md:py-24 max-w-3xl">
      <BackLink to={`/student/module/${moduleId}`}>{t("exam.back")}</BackLink>
      <p className="num-label mt-6">{t("exam.moduleKicker")}</p>
      <h1 className="font-display text-display-md mt-3 mb-10 text-balance">
        {assessment?.title ?? t("exam.moduleTitle")}
      </h1>
      {state === "loading" && <p className="num-label">{t("common.loading")}</p>}
      {state === "none" && <p className="text-ink-soft">{t("exam.moduleUnavailable")}</p>}
      {state === "error" && (
        <p className="text-ember border-l-2 border-ember pl-4 text-sm">{t("common.error")}</p>
      )}
      {state === "ready" && assessment && <ExamRunner assessment={assessment} />}
    </div>
  );
}
