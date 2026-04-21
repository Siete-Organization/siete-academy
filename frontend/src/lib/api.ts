import axios, { AxiosError, type AxiosInstance } from "axios";
import { getIdToken } from "./firebase";
import { logger, newRequestId } from "./logger";

const baseURL = import.meta.env.VITE_API_BASE_URL || "/api/academy";

/** LocalStorage key used by the dev-mode auth bypass (demo only). */
export const DEV_USER_KEY = "siete.dev.user";

export const api: AxiosInstance = axios.create({
  baseURL,
  headers: { "Content-Type": "application/json" },
});

api.interceptors.request.use(async (config) => {
  // Firebase bearer (prod / real users)
  const token = await getIdToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  // Dev-mode bypass header — only set when user picked a role on /login
  const devUser =
    typeof window !== "undefined" ? window.localStorage.getItem(DEV_USER_KEY) : null;
  if (devUser) {
    config.headers["X-Dev-User"] = devUser;
  }

  // Correlate frontend & backend logs via a request id
  const rid = newRequestId();
  config.headers["X-Request-ID"] = rid;
  (config as typeof config & { metadata?: Record<string, unknown> }).metadata = {
    rid,
    startedAt: performance.now(),
  };
  logger.debug("api.request", {
    method: config.method?.toUpperCase(),
    url: config.url,
    request_id: rid,
  });
  return config;
});

api.interceptors.response.use(
  (response) => {
    const meta = (response.config as typeof response.config & {
      metadata?: { rid: string; startedAt: number };
    }).metadata;
    const durationMs = meta ? Math.round(performance.now() - meta.startedAt) : undefined;
    logger.debug("api.response", {
      method: response.config.method?.toUpperCase(),
      url: response.config.url,
      status: response.status,
      duration_ms: durationMs,
      request_id: meta?.rid,
      server_rid: response.headers["x-request-id"],
    });
    return response;
  },
  (error: AxiosError) => {
    const meta = (error.config as typeof error.config & {
      metadata?: { rid: string; startedAt: number };
    })?.metadata;
    logger.warn("api.error", {
      method: error.config?.method?.toUpperCase(),
      url: error.config?.url,
      status: error.response?.status,
      code: error.code,
      message: error.message,
      request_id: meta?.rid,
      server_rid: error.response?.headers?.["x-request-id"],
    });
    return Promise.reject(error);
  },
);
