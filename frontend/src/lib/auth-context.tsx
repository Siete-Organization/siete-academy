import { createContext, useContext, useEffect, useState, type ReactNode } from "react";
import type { User } from "firebase/auth";
import { subscribeToAuth } from "./firebase";
import { api, DEV_USER_KEY } from "./api";

export type Role = "admin" | "teacher" | "student" | "recruiter";

export interface Me {
  id: number;
  email: string;
  display_name: string | null;
  photo_url: string | null;
  role: Role;
  locale: string;
}

interface AuthCtx {
  firebaseUser: User | null;
  me: Me | null;
  loading: boolean;
  refresh: () => Promise<void>;
  /** True when logged in via Firebase OR via dev bypass. */
  isAuthenticated: boolean;
  /** Dev-only: log in as a seeded user by email. */
  devLogin: (email: string) => Promise<void>;
  logoutDev: () => void;
}

const Ctx = createContext<AuthCtx>({
  firebaseUser: null,
  me: null,
  loading: true,
  refresh: async () => {},
  isAuthenticated: false,
  devLogin: async () => {},
  logoutDev: () => {},
});

export function AuthProvider({ children }: { children: ReactNode }) {
  const [firebaseUser, setFirebaseUser] = useState<User | null>(null);
  const [me, setMe] = useState<Me | null>(null);
  const [loading, setLoading] = useState(true);
  const [devEmail, setDevEmail] = useState<string | null>(
    typeof window !== "undefined" ? window.localStorage.getItem(DEV_USER_KEY) : null,
  );

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
      if (u || devEmail) {
        await fetchMe();
      } else {
        setMe(null);
      }
      setLoading(false);
    });
    return unsub;
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const devLogin = async (email: string) => {
    window.localStorage.setItem(DEV_USER_KEY, email);
    setDevEmail(email);
    setLoading(true);
    await fetchMe();
    setLoading(false);
  };

  const logoutDev = () => {
    window.localStorage.removeItem(DEV_USER_KEY);
    setDevEmail(null);
    setMe(null);
  };

  return (
    <Ctx.Provider
      value={{
        firebaseUser,
        me,
        loading,
        refresh: fetchMe,
        isAuthenticated: !!firebaseUser || !!devEmail,
        devLogin,
        logoutDev,
      }}
    >
      {children}
    </Ctx.Provider>
  );
}

export function useAuth() {
  return useContext(Ctx);
}
