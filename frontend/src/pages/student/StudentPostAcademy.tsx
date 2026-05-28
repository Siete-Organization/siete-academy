import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { api } from "@/lib/api";

interface StageDefinition {
  key: string;
  label: string;
  compensation: string;
  duration_weeks: string;
  summary: string;
  criteria: string[];
  decision_rule?: string;
}

interface MyStatus {
  id: number;
  user_id: number;
  stage: string;
  entered_stage_at: string;
  monthly_usd: number | null;
  country_deel_ok: boolean;
  notes: string | null;
  events?: StageEvent[];
}

interface StageEvent {
  id: number;
  from_stage: string | null;
  to_stage: string;
  reason: string | null;
  created_at: string;
}

export function StudentPostAcademy() {
  const { t } = useTranslation();
  const [stages, setStages] = useState<StageDefinition[]>([]);
  const [me, setMe] = useState<MyStatus | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    void (async () => {
      try {
        const [s, m] = await Promise.all([
          api.get<{ stages: StageDefinition[] }>("/practica/stages"),
          api.get<MyStatus | null>("/practica/me"),
        ]);
        setStages(s.data.stages);
        setMe(m.data);
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  if (loading) {
    return (
      <div className="container-editorial py-24 text-ink-muted">
        {t("common.loading")}
      </div>
    );
  }

  return (
    <div className="container-editorial py-16 md:py-20 space-y-12">
      <header>
        <p className="num-label">{t("postAcademy.eyebrow")}</p>
        <h1 className="font-display text-display-lg mt-4 text-balance">
          {t("postAcademy.title")}
        </h1>
        <p className="text-ink-soft mt-6 max-w-2xl leading-relaxed">
          {t("postAcademy.intro")}
        </p>
      </header>

      {me ? <CurrentStatusCard me={me} stages={stages} t={t} /> : <NotInvitedNotice t={t} />}

      <section className="space-y-6">
        <p className="num-label">{t("postAcademy.fullPath")}</p>
        <ol className="space-y-4">
          {stages.map((s, idx) => (
            <StageRow
              key={s.key}
              stage={s}
              idx={idx}
              isCurrent={me?.stage === s.key}
              t={t}
            />
          ))}
        </ol>
      </section>
    </div>
  );
}

function CurrentStatusCard({
  me,
  stages,
  t,
}: {
  me: MyStatus;
  stages: StageDefinition[];
  t: (k: string, opts?: Record<string, unknown>) => string;
}) {
  const current = stages.find((s) => s.key === me.stage);
  const enteredDate = new Date(me.entered_stage_at).toLocaleDateString();
  return (
    <section className="border border-ember/30 bg-ember/5 rounded-md p-6 space-y-3">
      <p className="num-label text-ember">{t("postAcademy.yourStage")}</p>
      <h2 className="font-display text-3xl text-balance">
        {current?.label ?? me.stage}
      </h2>
      <div className="flex flex-wrap gap-x-8 gap-y-2 text-sm text-ink-soft">
        <span>
          <span className="font-mono text-[10px] uppercase tracking-[0.14em] text-ink-faint mr-2">
            {t("postAcademy.since")}
          </span>
          {enteredDate}
        </span>
        {me.monthly_usd !== null && (
          <span>
            <span className="font-mono text-[10px] uppercase tracking-[0.14em] text-ink-faint mr-2">
              {t("postAcademy.compensation")}
            </span>
            USD {me.monthly_usd}/mes
          </span>
        )}
        {!me.country_deel_ok && (
          <span className="text-ember">{t("postAcademy.deelIneligible")}</span>
        )}
      </div>
      {current?.summary && (
        <p className="text-sm text-ink-soft leading-relaxed">{current.summary}</p>
      )}
    </section>
  );
}

function NotInvitedNotice({
  t,
}: {
  t: (k: string, opts?: Record<string, unknown>) => string;
}) {
  return (
    <section className="border border-bone rounded-md p-6 bg-paper-tint space-y-2">
      <p className="num-label">{t("postAcademy.notInvited")}</p>
      <p className="text-sm text-ink-soft leading-relaxed max-w-2xl">
        {t("postAcademy.notInvitedBody")}
      </p>
    </section>
  );
}

function StageRow({
  stage,
  idx,
  isCurrent,
  t,
}: {
  stage: StageDefinition;
  idx: number;
  isCurrent: boolean;
  t: (k: string, opts?: Record<string, unknown>) => string;
}) {
  return (
    <li
      className={`border rounded-md p-5 transition-colors ${
        isCurrent ? "border-ember bg-ember/5" : "border-bone bg-paper"
      }`}
    >
      <div className="grid grid-cols-12 gap-4 items-baseline">
        <span className="col-span-1 font-mono text-[10px] tabular-nums text-ink-faint">
          {String(idx + 1).padStart(2, "0")}
        </span>
        <div className="col-span-11 md:col-span-8 space-y-1">
          <h3
            className={`font-display text-2xl ${isCurrent ? "text-ember" : ""}`}
          >
            {stage.label}
          </h3>
          <p className="text-sm text-ink-soft leading-relaxed">{stage.summary}</p>
        </div>
        <div className="col-span-12 md:col-span-3 md:text-right space-y-1 text-xs">
          <p className="font-mono uppercase tracking-[0.14em] text-ink-muted">
            {stage.compensation}
          </p>
          {stage.duration_weeks !== "—" && (
            <p className="text-ink-faint">
              {stage.duration_weeks} {t("postAcademy.weeksShort")}
            </p>
          )}
        </div>
      </div>

      {stage.criteria.length > 0 && (
        <div className="mt-4 pt-4 border-t border-bone">
          <p className="num-label mb-2">{t("postAcademy.criteria")}</p>
          <ul className="space-y-1.5 text-sm text-ink-soft">
            {stage.criteria.map((c, i) => (
              <li key={i} className="flex gap-2">
                <span className="text-ink-faint">·</span>
                <span>{c}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {stage.decision_rule && (
        <div className="mt-3 text-xs text-ink-muted italic leading-relaxed">
          <span className="font-mono text-[10px] uppercase tracking-[0.14em] text-ink-faint mr-2 not-italic">
            {t("postAcademy.decisionRule")}
          </span>
          {stage.decision_rule}
        </div>
      )}
    </li>
  );
}
