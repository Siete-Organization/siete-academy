import { Link, NavLink, useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { useAuth } from "@/lib/auth-context";
import { logout } from "@/lib/firebase";
import { cn } from "@/lib/utils";

export function Layout({ children }: { children: React.ReactNode }) {
  const { t, i18n } = useTranslation();
  const { isAuthenticated, me, logoutDev } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    logoutDev();
    await logout();
    navigate("/login");
  };

  return (
    <div className="min-h-full flex flex-col relative">
      <header className="sticky top-0 z-30 backdrop-blur-xl bg-paper/80 border-b border-bone">
        <div className="container-editorial h-16 flex items-center justify-between">
          <Link to="/" className="group flex items-baseline gap-2">
            <span className="font-display text-2xl tracking-editorial leading-none">Siete</span>
            <span className="font-mono text-[10px] uppercase tracking-[0.25em] text-ink-muted group-hover:text-ink transition-colors">
              /academy
            </span>
          </Link>
          <nav className="flex items-center gap-6 text-sm">
            {me?.role === "student" && (
              <>
                <NavLink to="/student" className={navCls} end>
                  {t("nav.dashboard")}
                </NavLink>
                <NavLink to="/student/feedback" className={navCls}>
                  {t("nav.feedback")}
                </NavLink>
                <NavLink to="/student/certificate" className={navCls}>
                  {t("nav.certificate")}
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
              <button
                onClick={handleLogout}
                className="text-xs uppercase tracking-[0.14em] text-ink-muted hover:text-ink transition-colors"
              >
                {t("nav.logout")}
              </button>
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
            <p className="font-display text-3xl leading-none">Siete</p>
            <p className="eyebrow mt-2">La agencia de prospección · desde Latinoamérica</p>
          </div>
          <div className="text-right">
            <p className="num-label">© {new Date().getFullYear()} — Est. 2023</p>
            <p className="text-xs text-ink-muted mt-1">Hecho para quien vende de verdad.</p>
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

function LocaleSwitch({ lang, onChange }: { lang: string; onChange: (l: string) => void }) {
  const items = ["es", "en", "pt"];
  return (
    <div className="flex items-center gap-2 font-mono text-[10px] uppercase tracking-[0.2em]">
      {items.map((l, i) => (
        <div key={l} className="flex items-center gap-2">
          <button
            onClick={() => onChange(l)}
            className={cn(
              "transition-colors",
              lang === l ? "text-ink" : "text-ink-faint hover:text-ink",
            )}
          >
            {l}
          </button>
          {i < items.length - 1 && <span className="text-ink-faint">·</span>}
        </div>
      ))}
    </div>
  );
}
