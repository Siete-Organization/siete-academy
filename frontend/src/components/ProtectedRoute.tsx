import { Navigate } from "react-router-dom";
import { useAuth, type Role } from "@/lib/auth-context";

export function ProtectedRoute({
  children,
  roles,
}: {
  children: React.ReactNode;
  roles?: Role[];
}) {
  const { firebaseUser, me, loading } = useAuth();
  if (loading) return <div className="p-8 text-slate-500">Cargando...</div>;
  if (!firebaseUser) return <Navigate to="/login" replace />;
  if (roles && me && !roles.includes(me.role)) return <Navigate to="/" replace />;
  return <>{children}</>;
}
