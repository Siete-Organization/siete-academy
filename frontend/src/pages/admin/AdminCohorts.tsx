import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { api } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

interface Cohort {
  id: number;
  name: string;
  locale: string;
  start_date: string;
  end_date: string;
  status: string;
  max_students: number;
}

interface ModuleWindow {
  id: number;
  cohort_id: number;
  module_id: number;
  opens_at: string;
  closes_at: string;
  live_session_at: string | null;
}

export function AdminCohorts() {
  const { t, i18n } = useTranslation();
  const [cohorts, setCohorts] = useState<Cohort[]>([]);
  const [form, setForm] = useState({
    name: "",
    start_date: "",
    end_date: "",
    locale: "es",
    max_students: 20,
  });
  const [selectedCohort, setSelectedCohort] = useState<Cohort | null>(null);
  const [windows, setWindows] = useState<ModuleWindow[]>([]);

  const loadCohorts = async () => {
    const { data } = await api.get<Cohort[]>("/cohorts");
    setCohorts(data);
  };

  const loadWindows = async (cohortId: number) => {
    const { data } = await api.get<ModuleWindow[]>(`/cohorts/${cohortId}/windows`);
    setWindows(data);
  };

  useEffect(() => {
    void loadCohorts();
  }, []);

  useEffect(() => {
    if (selectedCohort) void loadWindows(selectedCohort.id);
    else setWindows([]);
  }, [selectedCohort]);

  const create = async () => {
    await api.post("/cohorts", form);
    setForm({ name: "", start_date: "", end_date: "", locale: "es", max_students: 20 });
    await loadCohorts();
  };

  const patchWindow = async (
    w: ModuleWindow,
    patch: Partial<Pick<ModuleWindow, "opens_at" | "closes_at" | "live_session_at">>,
  ) => {
    await api.patch(`/cohorts/${w.cohort_id}/windows/${w.id}`, patch);
    await loadWindows(w.cohort_id);
  };

  const openNow = async (w: ModuleWindow) => {
    await api.post(`/cohorts/${w.cohort_id}/windows/${w.id}/open`);
    await loadWindows(w.cohort_id);
  };

  const closeNow = async (w: ModuleWindow) => {
    await api.post(`/cohorts/${w.cohort_id}/windows/${w.id}/close`);
    await loadWindows(w.cohort_id);
  };

  return (
    <div className="container-editorial py-16 space-y-14">
      <header>
        <p className="num-label">Admin</p>
        <h1 className="font-display text-display-md mt-3">{t("admin.cohorts")}</h1>
      </header>

      <section>
        <p className="num-label mb-6">Nueva cohorte</p>
        <div className="grid grid-cols-1 md:grid-cols-12 gap-6 items-end">
          <div className="md:col-span-4">
            <label className="num-label block mb-1">Nombre</label>
            <Input
              value={form.name}
              onChange={(e) => setForm({ ...form, name: e.target.value })}
              placeholder="SDR 001 — Mayo 2026"
            />
          </div>
          <div className="md:col-span-2">
            <label className="num-label block mb-1">Inicio</label>
            <Input
              type="date"
              value={form.start_date}
              onChange={(e) => setForm({ ...form, start_date: e.target.value })}
            />
          </div>
          <div className="md:col-span-2">
            <label className="num-label block mb-1">Fin</label>
            <Input
              type="date"
              value={form.end_date}
              onChange={(e) => setForm({ ...form, end_date: e.target.value })}
            />
          </div>
          <div className="md:col-span-2">
            <label className="num-label block mb-1">Idioma</label>
            <select
              className="w-full h-11 bg-transparent border-0 border-b border-bone-strong focus:border-ink focus:outline-none font-mono text-xs uppercase tracking-[0.2em]"
              value={form.locale}
              onChange={(e) => setForm({ ...form, locale: e.target.value })}
            >
              <option value="es">es</option>
              <option value="en">en</option>
              <option value="pt">pt</option>
            </select>
          </div>
          <div className="md:col-span-2">
            <Button onClick={create} className="w-full">
              {t("common.save")}
            </Button>
          </div>
        </div>
      </section>

      <section className="hairline pt-10">
        <p className="num-label mb-6">Cohortes ({cohorts.length})</p>
        <table className="w-full">
          <thead>
            <tr className="text-left border-b border-bone">
              {["№", "Nombre", "Idioma", "Inicio", "Fin", "Estado", ""].map((h, i) => (
                <th key={i} className="num-label py-3 font-medium">
                  {h}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {cohorts.map((c, idx) => (
              <tr
                key={c.id}
                className={`border-b border-bone/60 hover:bg-paper-tint/60 cursor-pointer ${
                  selectedCohort?.id === c.id ? "bg-paper-tint" : ""
                }`}
                onClick={() => setSelectedCohort(c)}
              >
                <td className="py-4 font-mono text-xs text-ink-faint tabular-nums">
                  {String(idx + 1).padStart(3, "0")}
                </td>
                <td className="py-4 font-display text-lg">{c.name}</td>
                <td className="py-4 font-mono text-xs uppercase tracking-[0.14em]">{c.locale}</td>
                <td className="py-4 text-sm">{c.start_date}</td>
                <td className="py-4 text-sm">{c.end_date}</td>
                <td className="py-4">
                  <span className="font-mono text-[10px] uppercase tracking-[0.18em] text-ink-muted">
                    {c.status}
                  </span>
                </td>
                <td className="py-4 text-right text-xs text-ember">ventanas ↓</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>

      {selectedCohort && (
        <section className="border-t-2 border-ink pt-10 space-y-6">
          <header className="flex items-baseline justify-between">
            <div>
              <p className="num-label">Ventanas de módulo</p>
              <h2 className="font-display text-display-md mt-2">{selectedCohort.name}</h2>
            </div>
            <button
              className="text-xs text-ink-muted hover:text-ink uppercase tracking-[0.14em]"
              onClick={() => setSelectedCohort(null)}
            >
              cerrar
            </button>
          </header>

          {windows.length === 0 ? (
            <p className="text-ink-muted text-sm">
              Esta cohorte aún no tiene ventanas de módulo. Crea módulos y añádelos aquí.
            </p>
          ) : (
            <ol className="border-y border-bone divide-y divide-bone">
              {windows.map((w) => {
                const now = new Date();
                const opens = new Date(w.opens_at);
                const closes = new Date(w.closes_at);
                const isOpen = now >= opens && now <= closes;
                return (
                  <li key={w.id} className="py-5 grid grid-cols-12 gap-4 items-center">
                    <span className="col-span-1 num-label tabular-nums">
                      m.{String(w.module_id).padStart(2, "0")}
                    </span>
                    <div className="col-span-4">
                      <label className="num-label block mb-1">Abre</label>
                      <Input
                        type="datetime-local"
                        value={w.opens_at.slice(0, 16)}
                        onChange={(e) =>
                          void patchWindow(w, { opens_at: new Date(e.target.value).toISOString() })
                        }
                      />
                    </div>
                    <div className="col-span-4">
                      <label className="num-label block mb-1">Cierra</label>
                      <Input
                        type="datetime-local"
                        value={w.closes_at.slice(0, 16)}
                        onChange={(e) =>
                          void patchWindow(w, { closes_at: new Date(e.target.value).toISOString() })
                        }
                      />
                    </div>
                    <div className="col-span-3 flex items-center gap-2 justify-end">
                      <span
                        className={`font-mono text-[10px] uppercase tracking-[0.16em] ${
                          isOpen ? "text-ember" : "text-ink-faint"
                        }`}
                      >
                        {isOpen ? "abierto" : "cerrado"}
                      </span>
                      {isOpen ? (
                        <Button size="sm" variant="outline" onClick={() => closeNow(w)}>
                          cerrar ahora
                        </Button>
                      ) : (
                        <Button size="sm" variant="outline" onClick={() => openNow(w)}>
                          abrir ahora
                        </Button>
                      )}
                    </div>
                    <div className="col-span-12 font-mono text-[10px] text-ink-muted">
                      Sesión en vivo:{" "}
                      {w.live_session_at
                        ? new Date(w.live_session_at).toLocaleString(i18n.language)
                        : "—"}
                    </div>
                  </li>
                );
              })}
            </ol>
          )}
        </section>
      )}
    </div>
  );
}
