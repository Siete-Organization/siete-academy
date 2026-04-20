import { useEffect, useMemo, useState } from "react";
import { useTranslation } from "react-i18next";
import { api } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Input, Textarea } from "@/components/ui/input";

const STAGES = [
  "applying",
  "siete_interview",
  "siete_test",
  "approved",
  "presented",
  "placed",
  "rejected",
] as const;
type Stage = (typeof STAGES)[number];

interface Candidate {
  id: number;
  user_id: number;
  cohort_id: number | null;
  stage: Stage;
  summary: string | null;
  portfolio_url: string | null;
  notes: string | null;
  updated_at: string;
}

interface EventOut {
  id: number;
  event_type: string;
  data: Record<string, unknown>;
  actor_id: number | null;
  created_at: string;
}

interface CandidateDetail extends Candidate {
  user_name: string | null;
  user_email: string | null;
  events: EventOut[];
}

export function AdminPlacement() {
  const { t, i18n } = useTranslation();
  const [candidates, setCandidates] = useState<Candidate[]>([]);
  const [selectedId, setSelectedId] = useState<number | null>(null);
  const [detail, setDetail] = useState<CandidateDetail | null>(null);
  const [note, setNote] = useState("");

  const load = async () => {
    const { data } = await api.get<Candidate[]>("/placement/candidates");
    setCandidates(data);
  };
  useEffect(() => {
    void load();
  }, []);

  useEffect(() => {
    if (selectedId == null) {
      setDetail(null);
      return;
    }
    const controller = new AbortController();
    void (async () => {
      try {
        const { data } = await api.get<CandidateDetail>(
          `/placement/candidates/${selectedId}`,
          { signal: controller.signal },
        );
        setDetail(data);
        setNote(data.notes || "");
      } catch (err) {
        if ((err as { code?: string })?.code !== "ERR_CANCELED") throw err;
      }
    })();
    return () => controller.abort();
  }, [selectedId]);

  const grouped = useMemo(() => {
    const g: Record<Stage, Candidate[]> = Object.fromEntries(
      STAGES.map((s) => [s, [] as Candidate[]]),
    ) as Record<Stage, Candidate[]>;
    for (const c of candidates) g[c.stage]?.push(c);
    return g;
  }, [candidates]);

  const moveTo = async (stage: Stage) => {
    if (!detail) return;
    await api.patch(`/placement/candidates/${detail.id}/stage`, { stage });
    await load();
  };

  const saveProfile = async () => {
    if (!detail) return;
    await api.patch(`/placement/candidates/${detail.id}`, {
      notes: note,
      summary: detail.summary,
      portfolio_url: detail.portfolio_url,
    });
    await load();
  };

  return (
    <div className="container-editorial py-12">
      <header className="mb-10">
        <p className="num-label">Admin · placement</p>
        <h1 className="font-display text-display-md mt-3">{t("placement.title")}</h1>
      </header>

      <div className="overflow-x-auto pb-4">
        <div className="grid grid-flow-col auto-cols-[minmax(220px,1fr)] gap-4 min-w-full">
          {STAGES.map((stage) => (
            <section key={stage} className="border border-bone bg-paper/80 rounded-md">
              <header className="px-4 py-3 border-b border-bone flex items-baseline justify-between">
                <p className="num-label">{t(`placement.stages.${stage}` as never)}</p>
                <span className="font-mono text-xs text-ink-faint tabular-nums">
                  {grouped[stage]?.length ?? 0}
                </span>
              </header>
              <ol className="p-2 space-y-2 min-h-[240px]">
                {(grouped[stage] ?? []).map((c) => (
                  <li key={c.id}>
                    <button
                      onClick={() => setSelectedId(c.id)}
                      className={`w-full text-left p-3 rounded border text-sm ${
                        selectedId === c.id
                          ? "border-ember bg-ember-ghost"
                          : "border-bone hover:bg-paper-tint"
                      }`}
                    >
                      <p className="font-display text-base leading-tight">
                        Candidate #{c.id}
                      </p>
                      <p className="text-xs text-ink-muted mt-1">
                        user {c.user_id} · {new Date(c.updated_at).toLocaleDateString(i18n.language)}
                      </p>
                    </button>
                  </li>
                ))}
              </ol>
            </section>
          ))}
        </div>
      </div>

      {detail && (
        <aside className="mt-14 border-t-2 border-ink pt-10 grid grid-cols-1 lg:grid-cols-[1fr_320px] gap-10">
          <div className="space-y-6">
            <header>
              <p className="num-label">{t("placement.candidate")} #{detail.id}</p>
              <h2 className="font-display text-display-md mt-2">
                {detail.user_name || `User ${detail.user_id}`}
              </h2>
              <p className="text-sm text-ink-muted">{detail.user_email || "—"}</p>
            </header>

            <div className="space-y-3">
              <label>
                <span className="num-label mb-1 block">{t("placement.summary")}</span>
                <Textarea
                  value={detail.summary || ""}
                  onChange={(e) => setDetail({ ...detail, summary: e.target.value })}
                />
              </label>
              <label>
                <span className="num-label mb-1 block">{t("placement.portfolio")}</span>
                <Input
                  value={detail.portfolio_url || ""}
                  onChange={(e) => setDetail({ ...detail, portfolio_url: e.target.value })}
                />
              </label>
              <label>
                <span className="num-label mb-1 block">{t("placement.addNote")}</span>
                <Textarea value={note} onChange={(e) => setNote(e.target.value)} />
              </label>
              <Button onClick={saveProfile}>{t("common.save")}</Button>
            </div>

            <div className="hairline pt-4">
              <p className="num-label mb-2">{t("placement.moveTo")}</p>
              <div className="flex flex-wrap gap-2">
                {STAGES.filter((s) => s !== detail.stage).map((s) => (
                  <Button key={s} size="sm" variant="outline" onClick={() => moveTo(s)}>
                    {t(`placement.stages.${s}` as never)}
                  </Button>
                ))}
              </div>
            </div>
          </div>

          <div className="border-l border-bone pl-6">
            <p className="num-label mb-3">Timeline</p>
            <ol className="space-y-3 text-sm">
              {detail.events.map((e) => (
                <li key={e.id} className="grid grid-cols-[60px_1fr] gap-2">
                  <span className="font-mono text-[10px] text-ink-faint tabular-nums">
                    {new Date(e.created_at).toLocaleDateString(i18n.language, {
                      day: "2-digit",
                      month: "short",
                    })}
                  </span>
                  <div>
                    <p className="font-medium">{e.event_type.replace(/_/g, " ")}</p>
                    {Object.keys(e.data || {}).length > 0 && (
                      <p className="text-xs text-ink-muted font-mono mt-0.5">
                        {JSON.stringify(e.data)}
                      </p>
                    )}
                  </div>
                </li>
              ))}
            </ol>
          </div>
        </aside>
      )}
    </div>
  );
}
