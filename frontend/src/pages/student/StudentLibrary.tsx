import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { Link, useParams } from "react-router-dom";
import { api } from "@/lib/api";

interface IndustrySummary {
  slug: string;
  order_index: number;
  name: string;
  what_is: string | null;
  examples: string[] | null;
  tags: string[] | null;
}

interface IndustryDetail extends IndustrySummary {
  how_makes_money: string | null;
  what_sells: string | null;
  sells_to: string | null;
  buys_to_operate: string | null;
  dynamics: string | null;
  deepen_in: string | null;
}

export function StudentLibrary() {
  const { t, i18n } = useTranslation();
  const [industries, setIndustries] = useState<IndustrySummary[]>([]);
  const [loading, setLoading] = useState(true);
  const locale = i18n.language.slice(0, 2);

  useEffect(() => {
    void (async () => {
      setLoading(true);
      try {
        const r = await api.get<IndustrySummary[]>("/library/industries", {
          params: { locale },
        });
        setIndustries(r.data);
      } finally {
        setLoading(false);
      }
    })();
  }, [locale]);

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
        <p className="num-label">{t("library.eyebrow")}</p>
        <h1 className="font-display text-display-lg mt-4 text-balance">
          {t("library.title")}
        </h1>
        <p className="text-ink-soft mt-6 max-w-2xl leading-relaxed">
          {t("library.intro")}
        </p>
      </header>

      <section className="space-y-6">
        <p className="num-label">{t("library.industries")}</p>
        <ul className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {industries.map((card) => (
            <IndustryListItem key={card.slug} card={card} t={t} />
          ))}
        </ul>
      </section>
    </div>
  );
}

function IndustryListItem({
  card,
  t,
}: {
  card: IndustrySummary;
  t: (k: string) => string;
}) {
  return (
    <li className="border border-bone rounded-md p-5 bg-paper hover:border-ink/30 transition-colors">
      <div className="flex items-baseline gap-3">
        <span className="font-mono text-[10px] tabular-nums text-ink-faint">
          {String(card.order_index).padStart(2, "0")}
        </span>
        <h3 className="font-display text-2xl text-balance">{card.name}</h3>
      </div>
      {card.what_is && (
        <p className="text-sm text-ink-soft leading-relaxed mt-3 line-clamp-3">
          {card.what_is}
        </p>
      )}
      {card.tags && card.tags.length > 0 && (
        <div className="flex flex-wrap gap-1.5 mt-3">
          {card.tags.map((tag) => (
            <span
              key={tag}
              className="font-mono text-[10px] uppercase tracking-[0.1em] text-ink-muted bg-paper-tint border border-bone rounded-xs px-1.5 py-0.5"
            >
              {tag}
            </span>
          ))}
        </div>
      )}
      <Link
        to={`/student/library/industries/${card.slug}`}
        className="inline-block mt-4 text-xs uppercase tracking-[0.14em] text-ink hover:text-ember transition-colors"
      >
        {t("library.openCard")} →
      </Link>
    </li>
  );
}

export function StudentLibraryIndustryDetail() {
  const { t, i18n } = useTranslation();
  const { slug } = useParams<{ slug: string }>();
  const [card, setCard] = useState<IndustryDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [notFound, setNotFound] = useState(false);
  const locale = i18n.language.slice(0, 2);

  useEffect(() => {
    if (!slug) return;
    setLoading(true);
    setNotFound(false);
    void (async () => {
      try {
        const r = await api.get<IndustryDetail>(
          `/library/industries/${slug}`,
          { params: { locale } },
        );
        setCard(r.data);
      } catch (err: unknown) {
        const status =
          typeof err === "object" && err !== null && "response" in err
            ? (err as { response?: { status?: number } }).response?.status
            : undefined;
        if (status === 404) setNotFound(true);
      } finally {
        setLoading(false);
      }
    })();
  }, [slug, locale]);

  if (loading) {
    return (
      <div className="container-editorial py-24 text-ink-muted">
        {t("common.loading")}
      </div>
    );
  }

  if (notFound || !card) {
    return (
      <div className="container-editorial py-16 space-y-6">
        <Link
          to="/student/library"
          className="text-xs uppercase tracking-[0.14em] text-ink-muted hover:text-ink"
        >
          ← {t("library.back")}
        </Link>
        <p className="text-ink-soft">{t("library.notFound")}</p>
      </div>
    );
  }

  return (
    <div className="container-editorial py-16 md:py-20 space-y-10">
      <Link
        to="/student/library"
        className="text-xs uppercase tracking-[0.14em] text-ink-muted hover:text-ink"
      >
        ← {t("library.back")}
      </Link>

      <header>
        <p className="num-label">
          {String(card.order_index).padStart(2, "0")} · {t("library.eyebrow")}
        </p>
        <h1 className="font-display text-display-lg mt-4 text-balance">
          {card.name}
        </h1>
        {card.tags && card.tags.length > 0 && (
          <div className="flex flex-wrap gap-1.5 mt-4">
            {card.tags.map((tag) => (
              <span
                key={tag}
                className="font-mono text-[10px] uppercase tracking-[0.1em] text-ink-muted bg-paper-tint border border-bone rounded-xs px-1.5 py-0.5"
              >
                {tag}
              </span>
            ))}
          </div>
        )}
      </header>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-x-12 gap-y-8">
        <Field label={t("library.fields.whatIs")} body={card.what_is} />
        <Field
          label={t("library.fields.howMakesMoney")}
          body={card.how_makes_money}
        />
        <Field label={t("library.fields.whatSells")} body={card.what_sells} />
        <Field label={t("library.fields.sellsTo")} body={card.sells_to} />
        <FieldFull
          label={t("library.fields.buysToOperate")}
          body={card.buys_to_operate}
        />
        <FieldFull label={t("library.fields.dynamics")} body={card.dynamics} />
        {card.examples && card.examples.length > 0 && (
          <FieldFull
            label={t("library.fields.examples")}
            body={card.examples.map((e) => `• ${e}`).join("\n")}
          />
        )}
        <FieldFull
          label={t("library.fields.deepenIn")}
          body={card.deepen_in}
        />
      </div>
    </div>
  );
}

function Field({ label, body }: { label: string; body: string | null }) {
  if (!body) return null;
  return (
    <section>
      <p className="num-label mb-2">{label}</p>
      <p className="text-sm text-ink-soft leading-relaxed whitespace-pre-line">
        {body}
      </p>
    </section>
  );
}

function FieldFull({ label, body }: { label: string; body: string | null }) {
  if (!body) return null;
  return (
    <section className="md:col-span-2">
      <p className="num-label mb-2">{label}</p>
      <p className="text-sm text-ink-soft leading-relaxed whitespace-pre-line">
        {body}
      </p>
    </section>
  );
}
