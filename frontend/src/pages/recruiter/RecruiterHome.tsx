import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { api } from "@/lib/api";

function buildInterviewMailto({
  name,
  email,
  subject,
  body,
}: {
  name: string | null;
  email: string;
  subject: string;
  body: string;
}): string {
  const params = new URLSearchParams({ subject, body });
  const label = name ? `${name} <${email}>` : email;
  return `mailto:${encodeURIComponent(label)}?${params.toString()}`;
}

interface RecruiterCandidate {
  id: number;
  user_name: string | null;
  user_email: string | null;
  cohort_id: number | null;
  stage: string;
  summary: string | null;
  portfolio_url: string | null;
  approved_at: string | null;
}

export function RecruiterHome() {
  const { t, i18n } = useTranslation();
  const [list, setList] = useState<RecruiterCandidate[] | null>(null);

  useEffect(() => {
    void (async () => {
      const { data } = await api.get<RecruiterCandidate[]>("/placement/recruiter/candidates");
      setList(data);
    })();
  }, []);

  if (list === null) {
    return <div className="container-editorial py-24 text-ink-muted">{t("common.loading")}</div>;
  }

  return (
    <div className="container-editorial py-16 md:py-24 space-y-12">
      <header>
        <p className="num-label">Siete · Talento</p>
        <h1 className="font-display text-display-lg mt-4 text-balance">
          {t("recruiter.title")}
        </h1>
        <p className="text-ink-soft mt-3 max-w-2xl">{t("recruiter.subtitle")}</p>
      </header>

      {list.length === 0 ? (
        <p className="text-ink-muted">{t("common.empty")}</p>
      ) : (
        <ol className="border-y border-bone divide-y divide-bone">
          {list.map((c, i) => (
            <li key={c.id} className="py-8 grid grid-cols-12 gap-4 items-baseline">
              <span className="col-span-1 font-mono text-xs text-ink-faint tabular-nums">
                {String(i + 1).padStart(2, "0")}
              </span>
              <div className="col-span-12 md:col-span-7">
                <h2 className="font-display text-2xl">{c.user_name || `Candidate #${c.id}`}</h2>
                <p className="font-mono text-[10px] uppercase tracking-[0.16em] text-ink-muted mt-2">
                  {t(`placement.stages.${c.stage}` as never)} · cohorte #{c.cohort_id ?? "—"}
                </p>
                {c.summary && (
                  <p className="text-ink-soft mt-3 text-pretty leading-relaxed">{c.summary}</p>
                )}
              </div>
              <aside className="col-span-12 md:col-span-4 md:text-right space-y-2">
                {c.approved_at && (
                  <p className="num-label">
                    {t("recruiter.approvedOn")}{" "}
                    {new Date(c.approved_at).toLocaleDateString(i18n.language)}
                  </p>
                )}
                {c.portfolio_url && (
                  <a
                    className="block text-ember hover:underline underline-offset-4 text-sm"
                    href={c.portfolio_url}
                    target="_blank"
                    rel="noreferrer"
                  >
                    {t("recruiter.viewProfile")} ↗
                  </a>
                )}
                {c.user_email && (
                  <a
                    className="inline-block mt-2 px-3 py-1.5 border border-ink text-ink text-xs uppercase tracking-[0.14em] font-mono hover:bg-ink hover:text-paper transition-colors"
                    href={buildInterviewMailto({
                      name: c.user_name,
                      email: c.user_email,
                      subject: t("recruiter.interviewSubject"),
                      body: t("recruiter.interviewBody", {
                        name: (c.user_name || "").split(" ")[0] || "",
                      }),
                    })}
                  >
                    {t("recruiter.scheduleInterview")} →
                  </a>
                )}
              </aside>
            </li>
          ))}
        </ol>
      )}
    </div>
  );
}
