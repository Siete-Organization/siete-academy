import { createContext, useContext, useEffect, useState, type ReactNode } from "react";
import type { User } from "firebase/auth";
import { subscribeToAuth } from "./firebase";
import { api } from "./api";

export type Role = "admin" | "teacher" | "student" | "recruiter";

interface Me {
  id: number;
  email: string;
  display_name: string | null;
  role: Role;
  locale: string;
}

interface AuthCtx {
  firebaseUser: User | null;
  me: Me | null;
  loading: boolean;
  refresh: () => Promise<void>;
}

const Ctx = createContext<AuthCtx>({
  firebaseUser: null,
  me: null,
  loading: true,
  refresh: async () => {},
});

export function AuthProvider({ children }: { children: ReactNode }) {
  const [firebaseUser, setFirebaseUser] = useState<User | null>(null);
  const [me, setMe] = useState<Me | null>(null);
  const [loading, setLoading] = useState(true);

  const fetchMe = async () => {
    try {
      const { data } = await api.get<Me>("/auth/me");
      setMe(data);
    } catch {
      setMe(null);
    }
  };

  useEffect(() => {
    const unsub = subscribeToAuth(async (u) => {
      setFirebaseUser(u);
      if (u) {
        await fetchMe();
      } else {
        setMe(null);
      }
      setLoading(false);
    });
    return unsub;
  }, []);

  return (
    <Ctx.Provider value={{ firebaseUser, me, loading, refresh: fetchMe }}>{children}</Ctx.Provider>
  );
}

export function useAuth() {
  return useContext(Ctx);
}
