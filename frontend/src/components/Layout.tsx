import { useEffect, useRef, useState } from "react";
import { Link, NavLink, useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { useAuth } from "@/lib/auth-context";
import { logout } from "@/lib/firebase";
import { cn } from "@/lib/utils";

const HOME_BY_ROLE: Record<string, string> = {
  student: "/student",
  teacher: "/teacher",
  admin: "/admin",
  recruiter: "/recruiter",
};

export function Layout({ children }: { children: React.ReactNode }) {
  const { t, i18n } = useTranslation();
  const { isAuthenticated, me, logoutDev } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    logoutDev();
    await logout();
    navigate("/login");
  };

  const logoHref = (me?.role && HOME_BY_ROLE[me.role]) || "/";

  return (
    <div className="min-h-full flex flex-col relative">
      <header className="sticky top-0 z-30 backdrop-blur-xl bg-paper/80 border-b border-bone">
        <div className="container-editorial h-16 flex items-center justify-between">
          <Link to={logoHref} className="group flex items-baseline gap-2">
            <span className="font-display text-2xl tracking-editorial leading-none">Siete</span>
            <span className="font-mono text-[10px] uppercase tracking-[0.25em] text-ink-muted group-hover:text-ink transition-colors">
              /academy
            </span>
          </Link>
          <nav className="flex items-center gap-6 text-sm">
            {me?.role === "student" && (
              <>
                <NavLink to="/student" className={navCls} end>
                  {t("nav.myProgress")}
                </NavLink>
                <NavLink to="/student/feedback" className={navCls}>
                  {t("nav.teacherFeedback")}
                </NavLink>
                <NavLink to="/student/calendar" className={navCls}>
                  {t("nav.calendar")}
                </NavLink>
              </>
            )}
            {me?.role === "teacher" && (
              <NavLink to="/teacher" className={navCls}>
                {t("nav.teacher")}
              </NavLink>
            )}
            {me?.role === "admin" && (
              <NavLink to="/admin" className={navCls}>
                {t("nav.admin")}
              </NavLink>
            )}
            {me?.role === "recruiter" && (
              <NavLink to="/recruiter" className={navCls}>
                {t("nav.recruiter")}
              </NavLink>
            )}

            <LocaleSwitch
              lang={i18n.language.slice(0, 2)}
              onChange={(l) => i18n.changeLanguage(l)}
            />

            {isAuthenticated ? (
              <AccountMenu onLogout={handleLogout} />
            ) : (
              <Link
                to="/login"
                className="text-xs uppercase tracking-[0.14em] text-ink hover:text-ember transition-colors"
              >
                {t("nav.login")}
              </Link>
            )}
          </nav>
        </div>
      </header>

      <main className="flex-1 relative z-[2]">{children}</main>

      <footer className="border-t border-bone mt-24">
        <div className="container-editorial py-10 flex flex-col md:flex-row items-start md:items-end justify-between gap-6">
          <div>
            <p className="font-display text-3xl leading-none font-black">Siete</p>
            <p className="eyebrow mt-2">{t("footer.tagline")}</p>
          </div>
          <div className="text-right">
            <p className="num-label">© {new Date().getFullYear()} — Est. 2023</p>
            <p className="text-xs text-ink-muted mt-1">{t("footer.motto")}</p>
          </div>
        </div>
      </footer>
    </div>
  );
}

const navCls = ({ isActive }: { isActive: boolean }) =>
  cn(
    "text-xs uppercase tracking-[0.14em] transition-colors relative py-1",
    isActive ? "text-ink" : "text-ink-muted hover:text-ink",
    isActive && "after:absolute after:left-0 after:-bottom-0.5 after:h-px after:w-full after:bg-ink",
  );

const LOCALE_FLAGS: { code: string; flag: string; label: string }[] = [
  { code: "es", flag: "🇪🇸", label: "Español" },
  { code: "en", flag: "🇺🇸", label: "English" },
  { code: "pt", flag: "🇧🇷", label: "Português" },
];

function LocaleSwitch({ lang, onChange }: { lang: string; onChange: (l: string) => void }) {
  return (
    <div className="flex items-center gap-1">
      {LOCALE_FLAGS.map(({ code, flag, label }) => (
        <button
          key={code}
          onClick={() => onChange(code)}
          aria-label={label}
          title={label}
          className={cn(
            "text-lg leading-none px-1.5 py-1 rounded-xs transition-all",
            lang === code
              ? "opacity-100 scale-110"
              : "opacity-50 hover:opacity-100 grayscale hover:grayscale-0",
          )}
        >
          {flag}
        </button>
      ))}
    </div>
  );
}

function initials(name: string | null | undefined, email: string | null | undefined): string {
  if (name && name.trim()) {
    const parts = name.trim().split(/\s+/);
    const first = parts[0]?.[0] ?? "";
    const last = parts.length > 1 ? parts[parts.length - 1][0] : "";
    return (first + last).toUpperCase();
  }
  if (email) return email[0]?.toUpperCase() || "?";
  return "?";
}

function AccountMenu({ onLogout }: { onLogout: () => void | Promise<void> }) {
  const { t } = useTranslation();
  const { me } = useAuth();
  const [open, setOpen] = useState(false);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!open) return;
    const onDocClick = (e: MouseEvent) => {
      if (ref.current && !ref.current.contains(e.target as Node)) setOpen(false);
    };
    const onEsc = (e: KeyboardEvent) => {
      if (e.key === "Escape") setOpen(false);
    };
    document.addEventListener("mousedown", onDocClick);
    document.addEventListener("keydown", onEsc);
    return () => {
      document.removeEventListener("mousedown", onDocClick);
      document.removeEventListener("keydown", onEsc);
    };
  }, [open]);

  return (
    <div ref={ref} className="relative">
      <button
        onClick={() => setOpen((v) => !v)}
        aria-label={t("nav.account")}
        title={me?.display_name || me?.email || ""}
        className={cn(
          "w-9 h-9 rounded-full border border-bone overflow-hidden flex items-center justify-center transition-all",
          open ? "ring-2 ring-ink" : "hover:ring-1 hover:ring-ink",
        )}
      >
        {me?.photo_url ? (
          <img src={me.photo_url} alt="" className="w-full h-full object-cover" />
        ) : (
          <span className="font-mono text-[11px] tracking-[0.08em] text-ink">
            {initials(me?.display_name, me?.email)}
          </span>
        )}
      </button>
      {open && (
        <div className="absolute right-0 top-full mt-2 w-56 border border-bone bg-paper shadow-frame py-2 z-40">
          <div className="px-4 py-2 border-b border-bone">
            <p className="text-sm font-medium text-ink truncate">
              {me?.display_name || me?.email?.split("@")[0]}
            </p>
            <p className="text-xs text-ink-muted truncate">{me?.email}</p>
            <p className="num-label mt-1">{t(`nav.${me?.role}` as never)}</p>
          </div>
          <Link
            to="/account"
            onClick={() => setOpen(false)}
            className="block px-4 py-2 text-xs uppercase tracking-[0.14em] text-ink-muted hover:text-ink hover:bg-paper-tint transition-colors"
          >
            {t("nav.account")}
          </Link>
          <button
            onClick={() => {
              setOpen(false);
              void onLogout();
            }}
            className="block w-full text-left px-4 py-2 text-xs uppercase tracking-[0.14em] text-ink-muted hover:text-ink hover:bg-paper-tint transition-colors"
          >
            {t("nav.logout")}
          </button>
        </div>
      )}
    </div>
  );
}
