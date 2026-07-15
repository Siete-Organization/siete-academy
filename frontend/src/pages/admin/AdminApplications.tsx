import { useEffect, useMemo, useState } from "react";
import { useTranslation } from "react-i18next";
import { api } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/input";
import { BackLink } from "@/components/BackLink";

interface Application {
  id: number;
  applicant_name: string;
  applicant_email: string;
  applicant_phone: string | null;
  linkedin_url: string | null;
  country: string | null;
  locale: string;
  answers: Record<string, string>;
  video_url: string | null;
  started_at: string | null;
  mcq_answers: Record<string, string> | null;
  mcq_score: number | null;
  mcq_excel_score: number | null;
  auto_decision: AutoDecision | null;
  ai_score: number | null;
  ai_notes: string | null;
  status: string;
  admin_notes: string | null;
  created_at: string;
}

type AutoDecision =
  | "passed_stage_1"
  | "rejected_text"
  | "rejected_mcq_excel"
  | "rejected_mcq_total"
  | "rejected_speed";

const AUTO_DECISION_FILTERS: { value: "" | "passed" | "rejected"; label: string }[] = [
  { value: "", label: "Todas" },
  { value: "passed", label: "Pasaron Etapa 1" },
  { value: "rejected", label: "Auto-descartadas" },
];

interface OpenPrompt {
  id: string;
  title: string;
}

export function AdminApplications() {
  const { t } = useTranslation();
  const [apps, setApps] = useState<Application[]>([]);
  const [selected, setSelected] = useState<Application | null>(null);
  const [loadingDetail, setLoadingDetail] = useState(false);
  const [notes, setNotes] = useState("");
  const [filter, setFilter] = useState<"" | "passed" | "rejected">("");
  const [promptTitles, setPromptTitles] = useState<Record<string, string>>({});

  const load = async () => {
    const { data } = await api.get<Application[]>("/applications");
    setApps(data);
  };

  useEffect(() => {
    void load();
    // Cargamos títulos de prompts para mostrar nombre legible en lugar del qid crudo.
    void (async () => {
      try {
        const { data } = await api.get<{ open_prompts: OpenPrompt[] }>(
          "/admission/questions",
        );
        setPromptTitles(
          Object.fromEntries(data.open_prompts.map((p) => [p.id, p.title])),
        );
      } catch {
        // Si falla, caemos al qid crudo. No bloquea la vista.
      }
    })();
  }, []);

  const filteredApps = useMemo(() => {
    if (!filter) return apps;
    if (filter === "passed") {
      return apps.filter((a) => a.auto_decision === "passed_stage_1");
    }
    return apps.filter((a) => a.auto_decision?.startsWith("rejected_"));
  }, [apps, filter]);

  // List view returns a lean shape (ApplicationListOut). Fetch the full detail
  // for the selected row so answers/video/linkedin/admin_notes are available.
  const selectRow = async (row: Application) => {
    setSelected(row);
    setNotes("");
    setLoadingDetail(true);
    try {
      const { data } = await api.get<Application>(`/applications/${row.id}`);
      setSelected(data);
      setNotes(data.admin_notes || "");
    } finally {
      setLoadingDetail(false);
    }
  };

  const review = async (status: "approved" | "rejected") => {
    if (!selected) return;
    await api.post(`/applications/${selected.id}/review`, {
      status,
      admin_notes: notes,
    });
    setNotes("");
    setSelected(null);
    await load();
  };

  const removeApplication = async () => {
    if (!selected) return;
    const ok = window.confirm(
      `¿Eliminar definitivamente la postulación de ${selected.applicant_name} (${selected.applicant_email})?\n\nEsto libera el email: la persona podrá volver a postular desde cero.`,
    );
    if (!ok) return;
    await api.delete(`/applications/${selected.id}`);
    setNotes("");
    setSelected(null);
    await load();
  };

  return (
    <div className="container-editorial py-16">
      <BackLink to="/admin" className="mb-8">{t("nav.admin")}</BackLink>
      <header className="mb-12">
        <p className="num-label">Admin · cohorte 001</p>
        <h1 className="font-display text-display-md mt-3">{t("admin.applications")}</h1>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-[400px_1fr] gap-12">
        <aside>
          <div className="flex items-center gap-2 mb-4 flex-wrap">
            {AUTO_DECISION_FILTERS.map((f) => (
              <button
                key={f.value}
                onClick={() => setFilter(f.value)}
                className={`text-[10px] font-mono uppercase tracking-[0.14em] px-2 py-1 border rounded-xs transition-colors ${
                  filter === f.value
                    ? "border-ink text-ink"
                    : "border-bone text-ink-muted hover:text-ink"
                }`}
              >
                {f.label}
              </button>
            ))}
          </div>
          <p className="num-label mb-4">{filteredApps.length} registros</p>
          <ol className="divide-y divide-bone border-y border-bone">
            {filteredApps.map((a, idx) => (
              <li key={a.id}>
                <button
                  onClick={() => void selectRow(a)}
                  className={`w-full text-left py-5 grid grid-cols-12 gap-3 items-baseline transition-colors ${
                    selected?.id === a.id ? "bg-paper-tint" : "hover:bg-paper-tint/60"
                  }`}
                >
                  <span className="col-span-2 font-mono text-[10px] text-ink-faint tabular-nums">
                    {String(idx + 1).padStart(3, "0")}
                  </span>
                  <div className="col-span-7">
                    <p className="font-display text-lg leading-tight">{a.applicant_name}</p>
                    <p className="text-xs text-ink-muted mt-0.5">{a.applicant_email}</p>
                    {a.auto_decision && (
                      <div className="mt-2">
                        <AutoDecisionBadge decision={a.auto_decision} />
                      </div>
                    )}
                  </div>
                  <div className="col-span-3 text-right space-y-1">
                    <StatusBadge status={a.status} />
                    {a.mcq_score !== null && (
                      <p className="font-mono text-[10px] text-ink-faint tabular-nums">
                        {a.mcq_score}% · ex {a.mcq_excel_score}%
                      </p>
                    )}
                  </div>
                </button>
              </li>
            ))}
          </ol>
        </aside>

        {selected ? (
          <article className="space-y-10">
            <header className="hairline pt-6">
              <p className="num-label">Aplicante</p>
              <h2 className="font-display text-display-md mt-3">{selected.applicant_name}</h2>
              <div className="mt-4 flex flex-wrap gap-x-8 gap-y-2 text-sm text-ink-muted">
                <span>{selected.applicant_email}</span>
                <span>{selected.applicant_phone || "—"}</span>
                {selected.country && (
                  <span className="inline-flex items-center gap-1.5">
                    <span className="text-ink-faint">País</span>
                    <span className="text-ink">{selected.country}</span>
                  </span>
                )}
                <span className="font-mono text-xs uppercase tracking-[0.14em]">
                  {selected.locale}
                </span>
                <span className="font-mono text-xs">
                  {new Date(selected.created_at).toLocaleDateString()}
                </span>
              </div>
              {selected.linkedin_url && (
                <a
                  href={selected.linkedin_url}
                  target="_blank"
                  rel="noreferrer"
                  className="inline-flex items-center gap-2 mt-3 text-sm text-ember hover:underline underline-offset-4"
                >
                  LinkedIn <span aria-hidden>↗</span>
                </a>
              )}
              {selected.admin_notes && (
                <div className="mt-4 text-xs font-mono uppercase tracking-[0.14em] text-ink-faint">
                  Notas previas
                  <p className="mt-1 font-sans normal-case tracking-normal text-sm text-ink-soft">
                    {selected.admin_notes}
                  </p>
                </div>
              )}
            </header>

            {loadingDetail && (
              <p className="text-xs text-ink-muted font-mono">Cargando detalle…</p>
            )}

            {selected.auto_decision && (
              <Stage1Summary application={selected} />
            )}

            <section className="space-y-7">
              {Object.entries(selected.answers || {}).map(([qid, text]) => (
                <div key={qid} className="grid grid-cols-12 gap-4">
                  <span className="col-span-2 num-label tabular-nums pt-1">
                    {qid}
                  </span>
                  <div className="col-span-10">
                    <p className="font-display text-xl text-ink-muted italic leading-snug">
                      {promptTitles[qid] || qid.replace(/_/g, " ")}
                    </p>
                    <WordCountInfo text={text} />
                    <p className="whitespace-pre-wrap text-[15px] mt-3 leading-relaxed text-ink-soft">
                      {text}
                    </p>
                  </div>
                </div>
              ))}
            </section>

            {selected.video_url && (
              <section className="hairline pt-6">
                <p className="num-label mb-3">Video</p>
                <a
                  href={selected.video_url}
                  target="_blank"
                  rel="noreferrer"
                  className="inline-flex items-center gap-2 text-ember hover:underline underline-offset-4"
                >
                  Ver video del aplicante <span aria-hidden>↗</span>
                </a>
              </section>
            )}

            {selected.ai_score !== null && (
              <section className="border-l-2 border-ember pl-5 py-1">
                <p className="num-label text-ember">análisis claude</p>
                <p className="font-display text-3xl tabular-nums mt-1">
                  {selected.ai_score}
                  <span className="text-ink-faint text-base">/100</span>
                </p>
                <p className="text-sm text-ink-soft mt-2 leading-relaxed">
                  {selected.ai_notes}
                </p>
              </section>
            )}

            <section className="hairline pt-6 space-y-4">
              <label className="block">
                <span className="num-label mb-2 block">Notas admin</span>
                <Textarea value={notes} onChange={(e) => setNotes(e.target.value)} />
              </label>
              <div className="flex gap-4 items-center flex-wrap">
                <Button onClick={() => review("approved")} variant="ember">
                  {t("admin.approve")}
                </Button>
                <Button onClick={() => review("rejected")} variant="outline">
                  {t("admin.reject")}
                </Button>
                <button
                  onClick={() => void removeApplication()}
                  className="ml-auto text-[11px] font-mono uppercase tracking-[0.14em] text-ink-faint hover:text-ember border-b border-transparent hover:border-ember transition-colors"
                >
                  Eliminar postulación
                </button>
              </div>
            </section>
          </article>
        ) : (
          <div className="text-ink-muted text-sm">Selecciona una aplicación para revisar.</div>
        )}
      </div>
    </div>
  );
}

function Stage1Summary({ application }: { application: Application }) {
  const decision = application.auto_decision;
  const completionMinutes =
    application.started_at
      ? Math.round(
          (new Date(application.created_at).getTime() -
            new Date(application.started_at).getTime()) /
            60000,
        )
      : null;
  return (
    <section className="border border-bone rounded-md p-5 bg-paper">
      <div className="flex items-baseline justify-between gap-4 flex-wrap">
        <div>
          <p className="num-label">Etapa 1 — Resultado automático</p>
          <div className="mt-2">
            {decision && <AutoDecisionBadge decision={decision} large />}
          </div>
        </div>
        {completionMinutes !== null && (
          <p className="font-mono text-xs text-ink-muted tabular-nums">
            Tomó {completionMinutes} min
          </p>
        )}
      </div>
      {(application.mcq_score !== null || application.mcq_excel_score !== null) && (
        <div className="mt-5 grid grid-cols-2 gap-4 max-w-md">
          <ScoreCell
            label="MCQ total"
            value={application.mcq_score}
            floor={60}
          />
          <ScoreCell
            label="Excel / BBDD"
            value={application.mcq_excel_score}
            floor={40}
          />
        </div>
      )}
    </section>
  );
}

function ScoreCell({
  label,
  value,
  floor,
}: {
  label: string;
  value: number | null;
  floor: number;
}) {
  if (value === null) return null;
  const passed = value >= floor;
  return (
    <div
      className={`border rounded-md p-3 ${passed ? "border-ember/40 bg-ember/5" : "border-bone bg-paper-tint"}`}
    >
      <p className="num-label">{label}</p>
      <p className="font-display text-3xl tabular-nums mt-1">{value}%</p>
      <p className="text-[10px] font-mono uppercase tracking-[0.14em] text-ink-faint mt-1">
        piso {floor}% {passed ? "✓" : "✗"}
      </p>
    </div>
  );
}

const AUTO_DECISION_COPY: Record<AutoDecision, { label: string; tone: "good" | "bad" }> = {
  passed_stage_1: { label: "Pasó Etapa 1", tone: "good" },
  rejected_text: { label: "Texto fuera de rango", tone: "bad" },
  rejected_mcq_excel: { label: "Excel < 40%", tone: "bad" },
  rejected_mcq_total: { label: "MCQ < 60%", tone: "bad" },
  rejected_speed: { label: "< 15 min", tone: "bad" },
};

function AutoDecisionBadge({
  decision,
  large,
}: {
  decision: AutoDecision;
  large?: boolean;
}) {
  const copy = AUTO_DECISION_COPY[decision];
  const base =
    copy.tone === "good"
      ? "border-moss bg-moss/10 text-moss"
      : "border-ember bg-ember/5 text-ember";
  return (
    <span
      className={`inline-block border font-mono uppercase tracking-[0.16em] rounded-xs ${base} ${
        large ? "px-3 py-1 text-xs" : "px-1.5 py-0.5 text-[9px]"
      }`}
    >
      {copy.label}
    </span>
  );
}

function WordCountInfo({ text }: { text: string }) {
  const wc = text.trim().split(/\s+/).filter(Boolean).length;
  return (
    <p className="font-mono text-[10px] tabular-nums text-ink-faint mt-1">
      {wc} palabras
    </p>
  );
}

function StatusBadge({ status }: { status: string }) {
  const map: Record<string, string> = {
    submitted: "border-bone text-ink-muted",
    under_review: "border-moss text-moss",
    approved: "border-moss bg-moss/10 text-moss",
    rejected: "border-ember text-ember",
  };
  return (
    <span
      className={`inline-block px-2 py-0.5 border font-mono text-[9px] uppercase tracking-[0.16em] rounded-xs ${map[status] || "border-bone text-ink-faint"}`}
    >
      {status}
    </span>
  );
}
