import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { api } from "@/lib/api";
import { useAuth } from "@/lib/auth-context";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

interface Enrollment {
  id: number;
  cohort_id: number;
  cohort_name: string | null;
  slack_invite_url: string | null;
  status: string;
}

export function AccountPage() {
  const { t } = useTranslation();
  const { me, refresh } = useAuth();
  const [displayName, setDisplayName] = useState(me?.display_name || "");
  const [photoUrl, setPhotoUrl] = useState(me?.photo_url || "");
  const [enrollments, setEnrollments] = useState<Enrollment[]>([]);
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (me?.role !== "student") return;
    void (async () => {
      try {
        const { data } = await api.get<Enrollment[]>("/enrollment/me");
        setEnrollments(data);
      } catch {
        // silencioso — admin/profesor/recruiter no tienen enrollments
      }
    })();
  }, [me?.role]);

  if (!me) return null;

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSaving(true);
    setSaved(false);
    try {
      await api.patch("/users/me", {
        display_name: displayName.trim() || null,
        photo_url: photoUrl.trim() || null,
      });
      await refresh();
      setSaved(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : t("common.error"));
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="container-editorial py-16 md:py-24 max-w-3xl space-y-12">
      <header>
        <p className="num-label">{t("account.eyebrow")}</p>
        <h1 className="font-display text-display-lg mt-4 text-balance">
          {t("account.title")}
        </h1>
        <p className="text-ink-soft mt-4">{t("account.subtitle")}</p>
      </header>

      <section className="flex items-center gap-6 hairline pt-8">
        <div className="w-20 h-20 rounded-full border border-bone overflow-hidden flex items-center justify-center bg-paper-tint">
          {photoUrl ? (
            <img src={photoUrl} alt="" className="w-full h-full object-cover" />
          ) : (
            <span className="font-display text-2xl text-ink-muted">
              {(me.display_name || me.email)[0]?.toUpperCase()}
            </span>
          )}
        </div>
        <div>
          <p className="font-display text-2xl">
            {me.display_name || me.email.split("@")[0]}
          </p>
          <p className="text-sm text-ink-muted">{me.email}</p>
          <p className="num-label mt-2">{t(`nav.${me.role}` as never)}</p>
        </div>
      </section>

      <form onSubmit={handleSave} className="space-y-8">
        <fieldset className="space-y-6">
          <legend className="num-label mb-2">{t("account.profile")}</legend>

          <label className="block">
            <span className="text-[13px] font-medium text-ink">{t("account.name")}</span>
            <Input
              value={displayName}
              onChange={(e) => setDisplayName(e.target.value)}
              placeholder={me.email.split("@")[0]}
            />
          </label>

          <label className="block">
            <span className="text-[13px] font-medium text-ink">{t("account.photo")}</span>
            <Input
              type="url"
              value={photoUrl}
              onChange={(e) => setPhotoUrl(e.target.value)}
              placeholder="https://..."
            />
            <p className="text-xs text-ink-muted mt-1.5">{t("account.photoHint")}</p>
          </label>

          <div className="block">
            <span className="text-[13px] font-medium text-ink">{t("account.email")}</span>
            <Input value={me.email} disabled />
            <p className="text-xs text-ink-muted mt-1.5">{t("account.emailHint")}</p>
          </div>
        </fieldset>

        <fieldset className="space-y-3 hairline pt-6">
          <legend className="num-label mb-2">{t("account.security")}</legend>
          <p className="text-sm text-ink-soft leading-relaxed">
            {t("account.passwordHint")}
          </p>
        </fieldset>

        {enrollments.filter((e) => e.slack_invite_url).length > 0 && (
          <fieldset className="space-y-3 hairline pt-6">
            <legend className="num-label mb-2">{t("account.communityTitle")}</legend>
            <p className="text-sm text-ink-soft leading-relaxed">
              {t("account.communityHint")}
            </p>
            <div className="space-y-2 pt-2">
              {enrollments
                .filter((e) => e.slack_invite_url)
                .map((e) => (
                  <a
                    key={e.id}
                    href={e.slack_invite_url!}
                    target="_blank"
                    rel="noreferrer"
                    className="inline-flex items-center gap-3 bg-ember text-paper hover:bg-ember-soft rounded-full pl-3 pr-5 h-11 text-sm font-semibold transition-colors"
                  >
                    <span className="w-7 h-7 rounded-full bg-paper/20 flex items-center justify-center font-display font-black">
                      #
                    </span>
                    {t("account.communityJoin")} — {e.cohort_name || `Cohorte ${e.cohort_id}`}
                    <span aria-hidden>→</span>
                  </a>
                ))}
            </div>
          </fieldset>
        )}

        {error && (
          <p className="text-ember border-l-2 border-ember pl-4 text-sm">{error}</p>
        )}
        {saved && (
          <p className="text-moss border-l-2 border-moss pl-4 text-sm">
            {t("account.saved")}
          </p>
        )}

        <div className="hairline pt-6">
          <Button type="submit" disabled={saving} variant="ember">
            {saving ? t("account.saving") : t("account.save")} <span aria-hidden>→</span>
          </Button>
        </div>
      </form>
    </div>
  );
}
