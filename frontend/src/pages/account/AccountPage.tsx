import { useState } from "react";
import { useTranslation } from "react-i18next";
import { api } from "@/lib/api";
import { useAuth } from "@/lib/auth-context";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

export function AccountPage() {
  const { t } = useTranslation();
  const { me, refresh } = useAuth();
  const [displayName, setDisplayName] = useState(me?.display_name || "");
  const [photoUrl, setPhotoUrl] = useState(me?.photo_url || "");
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);
  const [error, setError] = useState<string | null>(null);

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
