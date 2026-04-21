import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { api } from "@/lib/api";

interface Enrollment {
  id: number;
  cohort_id: number;
  status: string;
  progress_pct: number;
}

interface ModuleWindow {
  id: number;
  cohort_id: number;
  module_id: number;
  opens_at: string;
  closes_at: string;
  live_session_at: string | null;
}

interface LiveSession {
  id: number;
  module_window_id: number;
  title: string;
  zoom_url: string;
  recording_url: string | null;
}

interface CalendarEntry {
  window: ModuleWindow;
  session: LiveSession | null;
  moduleNumber: number;
}

export function StudentCalendar() {
  const { t, i18n } = useTranslation();
  const [entries, setEntries] = useState<CalendarEntry[] | null>(null);

  useEffect(() => {
    const controller = new AbortController();
    void (async () => {
      try {
        const { data: enrollments } = await api.get<Enrollment[]>("/enrollment/me", {
          signal: controller.signal,
        });
        const windowsLists = await Promise.all(
          enrollments.map((e) =>
            api
              .get<ModuleWindow[]>(`/cohorts/${e.cohort_id}/windows`, {
                signal: controller.signal,
              })
              .then((r) => r.data),
          ),
        );
        const flat: CalendarEntry[] = [];
        windowsLists.forEach((windows) => {
          windows
            .slice()
            .sort(
              (a, b) => new Date(a.opens_at).getTime() - new Date(b.opens_at).getTime(),
            )
            .forEach((w, idx) => {
              flat.push({ window: w, session: null, moduleNumber: idx + 1 });
            });
        });

        const withSessions = await Promise.all(
          flat.map(async (entry) => {
            try {
              const { data } = await api.get<LiveSession>(
                `/live-sessions/window/${entry.window.id}`,
                { signal: controller.signal },
              );
              return { ...entry, session: data };
            } catch {
              return entry;
            }
          }),
        );

        setEntries(
          withSessions.sort((a, b) => {
            const ta = new Date(a.window.live_session_at || a.window.opens_at).getTime();
            const tb = new Date(b.window.live_session_at || b.window.opens_at).getTime();
            return ta - tb;
          }),
        );
      } catch (err) {
        if ((err as { code?: string })?.code !== "ERR_CANCELED") throw err;
      }
    })();
    return () => controller.abort();
  }, []);

  if (entries === null) {
    return <div className="container-editorial py-24 text-ink-muted">{t("common.loading")}</div>;
  }

  if (entries.length === 0) {
    return (
      <div className="container-editorial py-28 max-w-2xl">
        <p className="num-label">{t("calendar.eyebrow")}</p>
        <h1 className="font-display text-display-lg mt-4 text-balance">
          {t("calendar.title")}
        </h1>
        <p className="text-ink-soft mt-6 leading-relaxed">{t("calendar.empty")}</p>
      </div>
    );
  }

  const now = new Date();

  return (
    <div className="container-editorial py-16 md:py-24 space-y-10">
      <header>
        <p className="num-label">{t("calendar.eyebrow")}</p>
        <h1 className="font-display text-display-lg mt-4 text-balance">
          {t("calendar.title")}
        </h1>
        <p className="text-ink-soft mt-4 max-w-2xl">{t("calendar.subtitle")}</p>
      </header>

      <ol className="divide-y divide-bone border-y border-bone">
        {entries.map((entry) => {
          const { window: w, session, moduleNumber } = entry;
          const opens = new Date(w.opens_at);
          const closes = new Date(w.closes_at);
          const live = w.live_session_at ? new Date(w.live_session_at) : null;
          const isOpen = now >= opens && now <= closes;
          const isPast = now > closes;
          const canJoin =
            session &&
            live &&
            Math.abs(now.getTime() - live.getTime()) < 1000 * 60 * 60 * 2;

          return (
            <li key={w.id} className="py-6 grid grid-cols-12 gap-4 items-start">
              <div className="col-span-3 md:col-span-2">
                {live ? (
                  <>
                    <p className="font-display text-3xl tabular-nums">
                      {live.toLocaleDateString(i18n.language, { day: "2-digit" })}
                    </p>
                    <p className="num-label">
                      {live.toLocaleDateString(i18n.language, { month: "short" })}
                    </p>
                    <p className="font-mono text-[11px] text-ink-muted mt-1 tabular-nums">
                      {live.toLocaleTimeString(i18n.language, {
                        hour: "2-digit",
                        minute: "2-digit",
                      })}
                    </p>
                  </>
                ) : (
                  <>
                    <p className="font-display text-3xl tabular-nums text-ink-faint">
                      {opens.toLocaleDateString(i18n.language, { day: "2-digit" })}
                    </p>
                    <p className="num-label text-ink-faint">
                      {opens.toLocaleDateString(i18n.language, { month: "short" })}
                    </p>
                  </>
                )}
              </div>

              <div className="col-span-9 md:col-span-7">
                <p className="num-label">
                  {t("student.module")} {String(moduleNumber).padStart(2, "0")}
                </p>
                <h2 className="font-display text-xl mt-1">
                  {session?.title || t("calendar.moduleWindow")}
                </h2>
                <p className="font-mono text-[11px] text-ink-muted mt-2">
                  {opens.toLocaleDateString(i18n.language, { day: "2-digit", month: "short" })}
                  {" → "}
                  {closes.toLocaleDateString(i18n.language, { day: "2-digit", month: "short" })}
                </p>
                {!live && (
                  <p className="text-xs text-ink-faint mt-1">{t("calendar.noLive")}</p>
                )}
              </div>

              <div className="col-span-12 md:col-span-3 md:text-right space-y-2">
                <StateChip isOpen={isOpen} isPast={isPast} />
                {session && (
                  <div className="space-y-1">
                    {canJoin ? (
                      <a
                        href={session.zoom_url}
                        target="_blank"
                        rel="noreferrer"
                        className="inline-block px-3 py-1.5 bg-ember text-paper text-xs uppercase tracking-[0.14em] font-mono hover:bg-ink transition-colors"
                      >
                        {t("student.watchLive")} →
                      </a>
                    ) : live && !isPast ? (
                      <p className="text-xs text-ink-muted font-mono">
                        {t("calendar.inDays", {
                          days: Math.max(
                            0,
                            Math.ceil((live.getTime() - now.getTime()) / 86_400_000),
                          ),
                        })}
                      </p>
                    ) : null}
                    {session.recording_url && (
                      <a
                        href={session.recording_url}
                        target="_blank"
                        rel="noreferrer"
                        className="block text-xs text-ember hover:underline underline-offset-4"
                      >
                        {t("calendar.recording")} ↗
                      </a>
                    )}
                  </div>
                )}
              </div>
            </li>
          );
        })}
      </ol>
    </div>
  );
}

function StateChip({ isOpen, isPast }: { isOpen: boolean; isPast: boolean }) {
  const { t } = useTranslation();
  const { label, cls } = isOpen
    ? { label: t("calendar.statusOpen"), cls: "border-ember text-ember bg-ember-ghost" }
    : isPast
      ? { label: t("calendar.statusPast"), cls: "border-bone text-ink-faint" }
      : { label: t("calendar.statusUpcoming"), cls: "border-bone text-ink-muted" };
  return (
    <span
      className={`inline-flex items-center px-2.5 py-1 border rounded-xs font-mono text-[10px] uppercase tracking-[0.18em] ${cls}`}
    >
      {label}
    </span>
  );
}
