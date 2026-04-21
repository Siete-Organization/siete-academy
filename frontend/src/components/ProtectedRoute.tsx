import { Navigate } from "react-router-dom";
import { useAuth, type Role } from "@/lib/auth-context";

export function ProtectedRoute({
  children,
  roles,
}: {
  children: React.ReactNode;
  roles?: Role[];
}) {
  const { isAuthenticated, me, loading } = useAuth();
  if (loading) return <div className="p-8 text-ink-muted">Cargando...</div>;
  if (!isAuthenticated) return <Navigate to="/login" replace />;
  // If we know the user's role and it isn't allowed, send them home
  if (roles && me && !roles.includes(me.role)) return <Navigate to="/" replace />;
  return <>{children}</>;
}
