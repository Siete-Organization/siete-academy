import { createContext, useContext, useEffect, useState, type ReactNode } from "react";
import type { User } from "firebase/auth";
import axios from "axios";
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
  /** Set when /auth/me returns 403 with code=not_invited. */
  notInvited: boolean;
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
  notInvited: false,
  devLogin: async () => {},
  logoutDev: () => {},
});

export function AuthProvider({ children }: { children: ReactNode }) {
  const [firebaseUser, setFirebaseUser] = useState<User | null>(null);
  const [me, setMe] = useState<Me | null>(null);
  const [loading, setLoading] = useState(true);
  const [notInvited, setNotInvited] = useState(false);
  const [devEmail, setDevEmail] = useState<string | null>(
    typeof window !== "undefined" ? window.localStorage.getItem(DEV_USER_KEY) : null,
  );

  const fetchMe = async () => {
    try {
      const { data } = await api.get<Me>("/auth/me");
      setMe(data);
      setNotInvited(false);
    } catch (err) {
      setMe(null);
      if (axios.isAxiosError(err) && err.response?.status === 403) {
        const detail = err.response.data?.detail;
        const code = typeof detail === "object" && detail ? detail.code : null;
        if (code === "not_invited") setNotInvited(true);
      }
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
        notInvited,
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
