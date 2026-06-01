import { Link } from "react-router-dom";
import { cn } from "@/lib/utils";

interface BackLinkProps {
  to: string;
  children: React.ReactNode;
  className?: string;
}

/**
 * Pequeño link "← Parent" para volver a la página home del rol o sección.
 * Estilo consistente con `library.back` que ya existía — text-xs, uppercase,
 * tracking expandido, color ink-muted con hover.
 */
export function BackLink({ to, children, className }: BackLinkProps) {
  return (
    <Link
      to={to}
      className={cn(
        "inline-flex items-center gap-2 text-xs uppercase tracking-[0.14em] text-ink-muted hover:text-ink transition-colors",
        className,
      )}
    >
      <span aria-hidden>←</span>
      <span>{children}</span>
    </Link>
  );
}
