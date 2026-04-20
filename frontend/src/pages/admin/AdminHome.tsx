import { Link } from "react-router-dom";
import { useTranslation } from "react-i18next";

export function AdminHome() {
  const { t } = useTranslation();
  const items = [
    { n: "01", to: "/admin/applications", label: t("admin.applications"), hint: "Revisar aplicantes, aprobar/rechazar." },
    { n: "02", to: "/admin/cohorts", label: t("admin.cohorts"), hint: "Crear cohortes, abrir/cerrar módulos." },
    { n: "03", to: "/admin/placement", label: t("admin.placement"), hint: "ATS Kanban del pipeline de colocación." },
    { n: "04", to: "/admin/analytics", label: t("admin.analytics"), hint: "Números clave del programa." },
  ];
  return (
    <div className="container-editorial py-16 md:py-24">
      <p className="num-label">Panel admin</p>
      <h1 className="font-display text-display-lg mt-4">Operación.</h1>

      <ol className="mt-16 border-y border-bone divide-y divide-bone">
        {items.map((it) => (
          <li key={it.to}>
            <Link
              to={it.to}
              className="grid grid-cols-12 gap-4 py-8 items-baseline group hover:bg-paper-tint/60 transition-colors -mx-6 md:-mx-10 px-6 md:px-10"
            >
              <span className="col-span-1 font-mono text-xs text-ink-faint tabular-nums">
                {it.n}
              </span>
              <div className="col-span-10 md:col-span-8">
                <h3 className="font-display text-3xl group-hover:text-ember transition-colors">
                  {it.label}
                </h3>
                <p className="text-ink-muted mt-2 text-sm">{it.hint}</p>
              </div>
              <span className="col-span-1 md:col-span-3 md:text-right text-ink-muted group-hover:text-ember group-hover:translate-x-1 transition-all">
                →
              </span>
            </Link>
          </li>
        ))}
      </ol>
    </div>
  );
}
