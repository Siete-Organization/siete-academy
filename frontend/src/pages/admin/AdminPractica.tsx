import { useEffect, useMemo, useState } from "react";
import { useTranslation } from "react-i18next";
import { api } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Input, Textarea } from "@/components/ui/input";

interface Candidate {
  id: number;
  user_id: number;
  stage: string;
  entered_stage_at: string;
  monthly_usd: number | null;
  country_deel_ok: boolean;
  assigned_manager_id: number | null;
  notes: string | null;
  created_at: string;
  updated_at: string;
}

interface StageEvent {
  id: number;
  from_stage: string | null;
  to_stage: string;
  reason: string | null;
  actor_id: number | null;
  created_at: string;
}

interface CandidateDetail extends Candidate {
  events: StageEvent[];
}

interface StageDefinition {
  key: string;
  label: string;
  compensation: string;
  duration_weeks: string;
}

const STAGE_FILTERS: { value: string; label: string }[] = [
  { value: "", label: "Todos" },
  { value: "e1_invited", label: "E1 invitado" },
  { value: "e1_active", label: "E1 activo" },
  { value: "e2_active", label: "E2 (USD 400)" },
  { value: "e3_t2_active", label: "T2" },
  { value: "e3_t1_active", label: "T1" },
  { value: "closed_camino_b", label: "Camino B" },
  { value: "declined", label: "Declinó" },
];

const PAID_STAGES = new Set(["e2_active", "e3_t2_active", "e3_t1_active"]);

export function AdminPractica() {
  const { t } = useTranslation();
  const [candidates, setCandidates] = useState<Candidate[]>([]);
  const [stages, setStages] = useState<Record<string, StageDefinition>>({});
  const [selected, setSelected] = useState<CandidateDetail | null>(null);
  const [filter, setFilter] = useState("");
  const [inviteOpen, setInviteOpen] = useState(false);

  const load = async () => {
    const { data } = await api.get<Candidate[]>("/practica/candidates");
    setCandidates(data);
  };

  useEffect(() => {
    void load();
    void (async () => {
      const { data } = await api.get<{ stages: StageDefinition[] }>(
        "/practica/stages",
      );
      setStages(Object.fromEntries(data.stages.map((s) => [s.key, s])));
    })();
  }, []);

  const filtered = useMemo(
    () => (filter ? candidates.filter((c) => c.stage === filter) : candidates),
    [filter, candidates],
  );

  const selectRow = async (row: Candidate) => {
    const { data } = await api.get<CandidateDetail>(
      `/practica/candidates/${row.id}`,
    );
    setSelected(data);
  };

  return (
    <div className="container-editorial py-16">
      <header className="mb-12 flex items-baseline justify-between gap-6 flex-wrap">
        <div>
          <p className="num-label">Admin · Post-Academy</p>
          <h1 className="font-display text-display-md mt-3">
            {t("adminPractica.title")}
          </h1>
        </div>
        <Button onClick={() => setInviteOpen(true)} variant="ember">
          + {t("adminPractica.invite")}
        </Button>
      </header>

      {inviteOpen && (
        <InviteForm
          onCancel={() => setInviteOpen(false)}
          onCreated={async () => {
            setInviteOpen(false);
            await load();
          }}
          t={t}
        />
      )}

      <div className="grid grid-cols-1 lg:grid-cols-[360px_1fr] gap-12 mt-8">
        <aside>
          <div className="flex flex-wrap gap-2 mb-4">
            {STAGE_FILTERS.map((f) => (
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
          <p className="num-label mb-4">{filtered.length} candidatos</p>
          <ol className="divide-y divide-bone border-y border-bone">
            {filtered.map((c, idx) => (
              <li key={c.id}>
                <button
                  onClick={() => void selectRow(c)}
                  className={`w-full text-left py-4 grid grid-cols-12 gap-3 items-baseline transition-colors ${
                    selected?.id === c.id
                      ? "bg-paper-tint"
                      : "hover:bg-paper-tint/60"
                  }`}
                >
                  <span className="col-span-2 font-mono text-[10px] text-ink-faint tabular-nums">
                    {String(idx + 1).padStart(3, "0")}
                  </span>
                  <div className="col-span-10">
                    <p className="text-sm">user #{c.user_id}</p>
                    <p className="text-[10px] font-mono uppercase tracking-[0.14em] text-ink-muted mt-1">
                      {stages[c.stage]?.label ?? c.stage}
                      {c.monthly_usd !== null && ` · USD ${c.monthly_usd}/mes`}
                    </p>
                  </div>
                </button>
              </li>
            ))}
          </ol>
        </aside>

        {selected ? (
          <CandidateDetailView
            candidate={selected}
            stages={stages}
            onUpdated={async () => {
              await load();
              const { data } = await api.get<CandidateDetail>(
                `/practica/candidates/${selected.id}`,
              );
              setSelected(data);
            }}
            t={t}
          />
        ) : (
          <p className="text-ink-muted text-sm">
            {t("adminPractica.selectCandidate")}
          </p>
        )}
      </div>
    </div>
  );
}

function InviteForm({
  onCancel,
  onCreated,
  t,
}: {
  onCancel: () => void;
  onCreated: () => Promise<void>;
  t: (k: string) => string;
}) {
  const [userId, setUserId] = useState("");
  const [deelOk, setDeelOk] = useState(true);
  const [notes, setNotes] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);

  const submit = async () => {
    setError(null);
    setSaving(true);
    try {
      await api.post("/practica/candidates", {
        user_id: Number(userId),
        country_deel_ok: deelOk,
        notes: notes || null,
      });
      setUserId("");
      setNotes("");
      await onCreated();
    } catch (err) {
      const e = err as { response?: { data?: { detail?: string } } };
      setError(e.response?.data?.detail ?? "error");
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="border border-bone bg-paper-warm/40 rounded-md p-5 space-y-4 mb-8">
      <p className="num-label">{t("adminPractica.inviteHint")}</p>
      <div className="grid grid-cols-1 md:grid-cols-[1fr_auto] gap-4 items-end">
        <label className="block">
          <span className="num-label mb-1 block">User ID</span>
          <Input
            type="number"
            value={userId}
            onChange={(e) => setUserId(e.target.value)}
            placeholder="42"
          />
        </label>
        <label className="flex items-center gap-2 text-sm pb-3">
          <input
            type="checkbox"
            checked={deelOk}
            onChange={(e) => setDeelOk(e.target.checked)}
          />
          {t("adminPractica.deelOk")}
        </label>
      </div>
      <label className="block">
        <span className="num-label mb-1 block">{t("adminPractica.notes")}</span>
        <Textarea
          value={notes}
          onChange={(e) => setNotes(e.target.value)}
          rows={2}
          placeholder={t("adminPractica.notesPlaceholder")}
        />
      </label>
      {error && (
        <p className="text-ember text-sm border-l-2 border-ember pl-3">{error}</p>
      )}
      <div className="flex gap-3">
        <Button onClick={submit} disabled={!userId || saving} variant="ember">
          {saving ? "…" : t("adminPractica.invite")}
        </Button>
        <button
          type="button"
          onClick={onCancel}
          className="text-xs uppercase tracking-[0.14em] font-mono text-ink-muted hover:text-ink"
        >
          {t("common.cancel")}
        </button>
      </div>
    </div>
  );
}

function CandidateDetailView({
  candidate,
  stages,
  onUpdated,
  t,
}: {
  candidate: CandidateDetail;
  stages: Record<string, StageDefinition>;
  onUpdated: () => Promise<void>;
  t: (k: string) => string;
}) {
  const current = stages[candidate.stage];
  return (
    <article className="space-y-10">
      <header className="hairline pt-6">
        <p className="num-label">user #{candidate.user_id}</p>
        <h2 className="font-display text-display-md mt-3">
          {current?.label ?? candidate.stage}
        </h2>
        <div className="mt-4 flex flex-wrap gap-x-8 gap-y-2 text-sm text-ink-muted">
          <span>
            <span className="text-ink-faint">{t("adminPractica.since")}</span>{" "}
            <span className="text-ink">
              {new Date(candidate.entered_stage_at).toLocaleDateString()}
            </span>
          </span>
          {candidate.monthly_usd !== null && (
            <span>
              <span className="text-ink-faint">{t("adminPractica.compensation")}</span>{" "}
              <span className="text-ink">USD {candidate.monthly_usd}/mes</span>
            </span>
          )}
          {!candidate.country_deel_ok && (
            <span className="text-ember">{t("adminPractica.deelIneligibleBadge")}</span>
          )}
        </div>
        {candidate.notes && (
          <p className="mt-4 text-sm text-ink-soft border-l-2 border-bone pl-4 italic leading-relaxed">
            {candidate.notes}
          </p>
        )}
      </header>

      <TransitionForm candidate={candidate} stages={stages} onUpdated={onUpdated} t={t} />

      <section className="hairline pt-6">
        <p className="num-label mb-4">{t("adminPractica.timeline")}</p>
        <ol className="space-y-3">
          {candidate.events.map((ev) => (
            <li key={ev.id} className="grid grid-cols-12 gap-4 text-sm">
              <span className="col-span-3 font-mono text-[10px] text-ink-faint">
                {new Date(ev.created_at).toLocaleString()}
              </span>
              <div className="col-span-9">
                <p>
                  <span className="font-mono text-[10px] uppercase tracking-[0.14em] text-ink-faint mr-2">
                    {ev.from_stage ? `${ev.from_stage} →` : "INIT →"}
                  </span>
                  <span className="font-medium">{ev.to_stage}</span>
                </p>
                {ev.reason && (
                  <p className="text-xs text-ink-muted mt-1">{ev.reason}</p>
                )}
              </div>
            </li>
          ))}
        </ol>
      </section>
    </article>
  );
}

function TransitionForm({
  candidate,
  stages,
  onUpdated,
  t,
}: {
  candidate: CandidateDetail;
  stages: Record<string, StageDefinition>;
  onUpdated: () => Promise<void>;
  t: (k: string) => string;
}) {
  const allowed = ALLOWED_TRANSITIONS[candidate.stage] ?? [];
  const [toStage, setToStage] = useState("");
  const [reason, setReason] = useState("");
  const [monthlyUsd, setMonthlyUsd] = useState("");
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const needsMonthly = PAID_STAGES.has(toStage);
  const canSubmit = Boolean(
    toStage && !saving && (!needsMonthly || monthlyUsd),
  );

  if (allowed.length === 0) {
    return (
      <section className="border border-bone rounded-md p-5 bg-paper-tint">
        <p className="text-sm text-ink-muted italic">
          {t("adminPractica.terminalStage")}
        </p>
      </section>
    );
  }

  const submit = async () => {
    setError(null);
    setSaving(true);
    try {
      await api.post(`/practica/candidates/${candidate.id}/transition`, {
        to_stage: toStage,
        reason: reason || null,
        monthly_usd: needsMonthly ? Number(monthlyUsd) : null,
      });
      setToStage("");
      setReason("");
      setMonthlyUsd("");
      await onUpdated();
    } catch (err) {
      const e = err as { response?: { data?: { detail?: string } } };
      setError(e.response?.data?.detail ?? "error");
    } finally {
      setSaving(false);
    }
  };

  return (
    <section className="border border-bone rounded-md p-5 bg-paper space-y-4">
      <p className="num-label">{t("adminPractica.transitionTo")}</p>
      <div className="flex flex-wrap gap-2">
        {allowed.map((s) => (
          <button
            key={s}
            onClick={() => setToStage(s)}
            className={`text-xs px-3 py-1.5 border rounded-xs transition-colors ${
              toStage === s
                ? "border-ink bg-ink text-paper"
                : "border-bone text-ink-soft hover:border-ink"
            }`}
          >
            {stages[s]?.label ?? s}
          </button>
        ))}
      </div>
      {toStage && (
        <>
          {needsMonthly && (
            <label className="block max-w-xs">
              <span className="num-label mb-1 block">USD/mes</span>
              <Input
                type="number"
                value={monthlyUsd}
                onChange={(e) => setMonthlyUsd(e.target.value)}
                placeholder="400"
              />
            </label>
          )}
          <label className="block">
            <span className="num-label mb-1 block">{t("adminPractica.reason")}</span>
            <Textarea
              value={reason}
              onChange={(e) => setReason(e.target.value)}
              rows={2}
              placeholder={t("adminPractica.reasonPlaceholder")}
            />
          </label>
          {error && (
            <p className="text-ember text-sm border-l-2 border-ember pl-3">
              {error}
            </p>
          )}
          <Button onClick={submit} disabled={!canSubmit} variant="ember">
            {saving ? "…" : t("adminPractica.confirmTransition")}
          </Button>
        </>
      )}
    </section>
  );
}

const ALLOWED_TRANSITIONS: Record<string, string[]> = {
  e1_invited: ["e1_active", "declined", "closed_camino_b"],
  e1_active: ["e2_active", "closed_camino_b"],
  e2_active: ["e3_t2_active", "closed_camino_b"],
  e3_t2_active: ["e3_t1_active", "closed_camino_b"],
  e3_t1_active: ["closed_camino_b"],
  closed_camino_b: [],
  declined: [],
};
