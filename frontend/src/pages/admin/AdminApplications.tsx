import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { api } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/input";

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
  ai_score: number | null;
  ai_notes: string | null;
  status: string;
  admin_notes: string | null;
  created_at: string;
}

export function AdminApplications() {
  const { t } = useTranslation();
  const [apps, setApps] = useState<Application[]>([]);
  const [selected, setSelected] = useState<Application | null>(null);
  const [loadingDetail, setLoadingDetail] = useState(false);
  const [notes, setNotes] = useState("");

  const load = async () => {
    const { data } = await api.get<Application[]>("/applications");
    setApps(data);
  };

  useEffect(() => {
    void load();
  }, []);

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

  return (
    <div className="container-editorial py-16">
      <header className="mb-12">
        <p className="num-label">Admin · cohorte 001</p>
        <h1 className="font-display text-display-md mt-3">{t("admin.applications")}</h1>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-[360px_1fr] gap-12">
        <aside>
          <p className="num-label mb-4">{apps.length} registros</p>
          <ol className="divide-y divide-bone border-y border-bone">
            {apps.map((a, idx) => (
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
                  </div>
                  <span className="col-span-3 text-right">
                    <StatusBadge status={a.status} />
                  </span>
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

            <section className="space-y-7">
              {Object.entries(selected.answers || {}).map(([qid, text], i) => (
                <div key={qid} className="grid grid-cols-12 gap-4">
                  <span className="col-span-2 num-label tabular-nums pt-1">
                    q.{String(i + 1).padStart(2, "0")}
                  </span>
                  <div className="col-span-10">
                    <p className="font-display text-xl text-ink-muted italic leading-snug">
                      {qid.replace(/_/g, " ")}
                    </p>
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
              <div className="flex gap-4">
                <Button onClick={() => review("approved")} variant="ember">
                  {t("admin.approve")}
                </Button>
                <Button onClick={() => review("rejected")} variant="outline">
                  {t("admin.reject")}
                </Button>
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
