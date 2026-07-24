import { useTranslation } from "react-i18next";
import { Button } from "@/components/ui/button";

/** Estado de error de carga con reintento — para que un fallo transitorio
 *  (p. ej. la API reiniciándose durante un deploy) no se muestre como
 *  "no hay datos". */
export function LoadError({ onRetry }: { onRetry: () => void }) {
  const { t } = useTranslation();
  return (
    <div className="py-12 max-w-xl">
      <p className="num-label">{t("common.error")}</p>
      <p className="mt-3 text-ink-soft leading-relaxed">{t("common.loadError")}</p>
      <Button className="mt-6" onClick={onRetry}>
        {t("common.retry")}
      </Button>
    </div>
  );
}
