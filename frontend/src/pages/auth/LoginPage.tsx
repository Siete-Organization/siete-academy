import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { useNavigate } from "react-router-dom";
import { loginWithGoogle } from "@/lib/firebase";
import { useAuth } from "@/lib/auth-context";
import { Button } from "@/components/ui/button";

const IS_DEV = import.meta.env.MODE !== "production";

const DEV_USERS: Array<{
  email: string;
  label: string;
  hint: string;
  target: string;
}> = [
  { email: "admin@siete.com", label: "Admin", hint: "Gestión total", target: "/admin" },
  { email: "teacher@siete.com", label: "Profesor", hint: "Revisar entregas", target: "/teacher" },
  { email: "student@siete.com", label: "Alumno", hint: "Consumir contenido", target: "/student" },
  { email: "recruiter@siete.com", label: "Reclutador", hint: "Ver talento", target: "/recruiter" },
];

export function LoginPage() {
  const { t } = useTranslation();
  const { firebaseUser, me, loading, isAuthenticated, devLogin } = useAuth();
  const navigate = useNavigate();
  const [submitting, setSubmitting] = useState<string | null>(null);

  useEffect(() => {
    if (!loading && isAuthenticated && me) {
      if (me.role === "admin") navigate("/admin");
      else if (me.role === "teacher") navigate("/teacher");
      else if (me.role === "recruiter") navigate("/recruiter");
      else navigate("/student");
    }
  }, [firebaseUser, me, loading, isAuthenticated, navigate]);

  const onDevLogin = async (u: (typeof DEV_USERS)[number]) => {
    setSubmitting(u.email);
    try {
      await devLogin(u.email);
      navigate(u.target);
    } finally {
      setSubmitting(null);
    }
  };

  return (
    <div className="container-editorial py-24 md:py-32">
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-14 items-start">
        <div className="lg:col-span-7">
          <p className="num-label">Sesión</p>
          <h1 className="font-display text-display-lg mt-5 text-balance">
            De vuelta al <em className="italic font-light">trabajo.</em>
          </h1>
          <p className="text-ink-soft text-lg mt-6 leading-relaxed max-w-prose">
            Tu cuenta es la misma que te abrimos cuando fuiste aceptado. Si aún no has
            aplicado, empieza por el formulario de admisión.
          </p>
        </div>
        <div className="lg:col-span-5 lg:pl-8 lg:border-l lg:border-bone space-y-6">
          <Button size="lg" className="w-full justify-between" onClick={loginWithGoogle}>
            <span>Continuar con Google</span>
            <span aria-hidden className="font-mono text-xs opacity-60">⌘ ↵</span>
          </Button>
          <p className="text-xs text-ink-muted leading-relaxed">
            Firebase para producción. Usamos Google solo para verificar identidad.
          </p>

          {IS_DEV && (
            <div className="hairline pt-6">
              <p className="num-label text-ember mb-3">Modo demo local</p>
              <p className="text-xs text-ink-muted mb-4 leading-relaxed">
                Entra como cualquier rol para probar el flujo. Solo funciona en desarrollo.
              </p>
              <div className="grid grid-cols-2 gap-2">
                {DEV_USERS.map((u) => (
                  <button
                    key={u.email}
                    disabled={submitting !== null}
                    onClick={() => onDevLogin(u)}
                    className="text-left p-3 border border-bone hover:border-ink rounded-md transition-colors disabled:opacity-40"
                  >
                    <p className="font-display text-lg leading-tight">{u.label}</p>
                    <p className="text-xs text-ink-muted mt-0.5">{u.hint}</p>
                  </button>
                ))}
              </div>
            </div>
          )}
          <p className="num-label mt-8">{t("app.tagline")}</p>
        </div>
      </div>
    </div>
  );
}
