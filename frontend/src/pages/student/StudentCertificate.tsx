import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { api } from "@/lib/api";

interface Certificate {
  id: number;
  verification_code: string;
  pdf_url: string | null;
  issued_at: string;
  cohort_id: number;
}

export function StudentCertificate() {
  const { t, i18n } = useTranslation();
  const [certs, setCerts] = useState<Certificate[] | null>(null);

  useEffect(() => {
    void (async () => {
      try {
        const { data } = await api.get<Certificate[]>("/certificates/me");
        setCerts(data);
      } catch {
        setCerts([]);
      }
    })();
  }, []);

  if (certs === null) {
    return <div className="container-editorial py-24 text-ink-muted">{t("common.loading")}</div>;
  }

  if (certs.length === 0) {
    return (
      <div className="container-editorial py-28 max-w-2xl">
        <p className="num-label">En construcción</p>
        <h1 className="font-display text-display-lg mt-4 text-balance">
          {t("certificate.title")}
        </h1>
        <p className="text-ink-soft mt-6 leading-relaxed">{t("certificate.empty")}</p>
      </div>
    );
  }

  return (
    <div className="container-editorial py-16 md:py-24 space-y-10">
      <header>
        <p className="num-label">Reconocimiento</p>
        <h1 className="font-display text-display-lg mt-4">{t("certificate.title")}</h1>
      </header>

      {certs.map((c) => (
        <article
          key={c.id}
          className="relative border border-bone bg-paper/90 shadow-lift rounded-md p-10 md:p-16 overflow-hidden"
        >
          <div className="absolute top-6 right-8 font-mono text-[10px] uppercase tracking-[0.2em] text-ink-faint">
            {t("certificate.verifyHint")}
          </div>
          <p className="eyebrow">Siete Academy · Programa SDR</p>
          <h2 className="font-display text-5xl md:text-6xl mt-6 tracking-editorial leading-none">
            Certificado <em className="italic font-light">de culminación</em>
          </h2>
          <div className="mt-12 grid grid-cols-2 gap-8 max-w-lg">
            <div>
              <p className="num-label">Cohorte</p>
              <p className="font-display text-2xl mt-1">#{c.cohort_id}</p>
            </div>
            <div>
              <p className="num-label">{t("certificate.issuedOn")}</p>
              <p className="font-display text-2xl mt-1">
                {new Date(c.issued_at).toLocaleDateString(i18n.language, {
                  day: "2-digit",
                  month: "long",
                  year: "numeric",
                })}
              </p>
            </div>
          </div>
          <div className="mt-14 flex flex-wrap items-center justify-between gap-4 hairline pt-6">
            <p className="font-mono text-xs tracking-[0.14em] text-ink-muted">
              {c.verification_code}
            </p>
            {c.pdf_url && (
              <a
                href={c.pdf_url}
                target="_blank"
                rel="noreferrer"
                className="text-ember hover:underline underline-offset-4 text-sm"
              >
                {t("certificate.downloadPdf")} ↗
              </a>
            )}
          </div>
        </article>
      ))}
    </div>
  );
}
