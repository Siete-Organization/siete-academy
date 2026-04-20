/**
 * Lightweight frontend logger.
 *
 * Dev: pretty-prints to the console with context.
 * Prod: emits JSON so browser-log forwarders (Sentry breadcrumb, Datadog RUM,
 *       or a custom /api/academy/logs sink) can pick it up consistently.
 *
 * Every log carries a session id (persisted in sessionStorage) plus optional
 * request id so a frontend action can be correlated with a backend trace.
 */

type Level = "debug" | "info" | "warn" | "error";

const LEVEL_RANK: Record<Level, number> = { debug: 10, info: 20, warn: 30, error: 40 };

const isProd = import.meta.env.MODE === "production";
const MIN_LEVEL: Level = (import.meta.env.VITE_LOG_LEVEL as Level) || (isProd ? "info" : "debug");

function sessionId(): string {
  if (typeof window === "undefined") return "ssr";
  const KEY = "siete.academy.sid";
  let sid = window.sessionStorage.getItem(KEY);
  if (!sid) {
    sid = crypto.randomUUID().slice(0, 12);
    window.sessionStorage.setItem(KEY, sid);
  }
  return sid;
}

function emit(level: Level, event: string, data?: Record<string, unknown>) {
  if (LEVEL_RANK[level] < LEVEL_RANK[MIN_LEVEL]) return;

  const payload = {
    ts: new Date().toISOString(),
    level,
    event,
    sid: sessionId(),
    rid: data?.request_id ?? undefined,
    ...data,
  };

  if (isProd) {
    // One JSON line per event — trivially grepable
    const line = JSON.stringify(payload);
    // eslint-disable-next-line no-console
    (level === "error" ? console.error : console.log)(line);
    return;
  }

  const color =
    level === "error" ? "color:#b8461f;font-weight:600"
    : level === "warn" ? "color:#b8461f"
    : level === "info" ? "color:#3d4d35"
    : "color:#8a8a90";
  // eslint-disable-next-line no-console
  console.log(
    `%c[${level.toUpperCase()}] ${event}`,
    color,
    data ? data : "",
  );
}

export const logger = {
  debug: (event: string, data?: Record<string, unknown>) => emit("debug", event, data),
  info: (event: string, data?: Record<string, unknown>) => emit("info", event, data),
  warn: (event: string, data?: Record<string, unknown>) => emit("warn", event, data),
  error: (event: string, data?: Record<string, unknown>) => emit("error", event, data),
};

export function newRequestId(): string {
  return crypto.randomUUID().slice(0, 16);
}
