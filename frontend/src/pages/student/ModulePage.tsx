import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { api } from "@/lib/api";
import { Button } from "@/components/ui/button";

const RESOURCE_ICONS: Record<string, string> = {
  pdf: "📄",
  ppt: "📊",
  video: "🎞",
  doc: "📝",
  link: "🔗",
};

interface Lesson {
  id: number;
  order_index: number;
  kind: "video" | "reading";
  youtube_id: string | null;
  title: string;
  body: string | null;
}

interface Assessment {
  id: number;
  type: string;
  title: string;
  config: Record<string, unknown>;
  passing_score: number;
}

interface ModuleResource {
  id: number;
  module_id: number;
  kind: "pdf" | "ppt" | "video" | "doc" | "link";
  title: string;
  url: string;
  order_index: number;
}

export function ModulePage() {
  const { moduleId } = useParams();
  const { t, i18n } = useTranslation();
  const [lessons, setLessons] = useState<Lesson[]>([]);
  const [assessments, setAssessments] = useState<Assessment[]>([]);
  const [resources, setResources] = useState<ModuleResource[]>([]);
  const [selectedLesson, setSelectedLesson] = useState<Lesson | null>(null);

  useEffect(() => {
    if (!moduleId) return;
    const controller = new AbortController();
    void (async () => {
      try {
        const [l, a, r] = await Promise.all([
          api.get<Lesson[]>(`/courses/modules/${moduleId}/lessons`, {
            params: { locale: i18n.language.slice(0, 2) },
            signal: controller.signal,
          }),
          api.get<Assessment[]>(`/assessments/module/${moduleId}`, {
            signal: controller.signal,
          }),
          api.get<ModuleResource[]>(`/courses/modules/${moduleId}/resources`, {
            signal: controller.signal,
          }),
        ]);
        setLessons(l.data);
        setAssessments(a.data);
        setResources(r.data);
        // Solo fijar la primera lección en la carga inicial, no al cambiar idioma
        setSelectedLesson((prev) => {
          if (prev && l.data.some((lx) => lx.id === prev.id)) {
            // Preserva la selección + refresca sus traducciones
            return l.data.find((lx) => lx.id === prev.id) ?? l.data[0] ?? null;
          }
          return l.data[0] ?? null;
        });
      } catch (err) {
        if ((err as { code?: string })?.code !== "ERR_CANCELED") throw err;
      }
    })();
    return () => controller.abort();
  }, [moduleId, i18n.language]);

  return (
    <div className="container-editorial py-12 grid grid-cols-1 lg:grid-cols-[280px_1fr] gap-12">
      <aside className="lg:sticky lg:top-24 h-max space-y-8">
        <div>
          <p className="num-label mb-4">Lecciones</p>
          <ol className="space-y-0.5">
            {lessons.map((l, i) => (
              <li key={l.id}>
                <button
                  onClick={() => setSelectedLesson(l)}
                  className={`w-full text-left py-2.5 px-3 -mx-3 rounded grid grid-cols-[24px_1fr] gap-2 items-baseline transition-colors ${
                    selectedLesson?.id === l.id
                      ? "bg-ink text-paper"
                      : "hover:bg-paper-tint"
                  }`}
                >
                  <span
                    className={`font-mono text-[10px] tabular-nums ${
                      selectedLesson?.id === l.id ? "text-paper/60" : "text-ink-faint"
                    }`}
                  >
                    {l.kind === "reading" ? "📖" : String(i + 1).padStart(2, "0")}
                  </span>
                  <span className="text-sm leading-tight">{l.title}</span>
                </button>
              </li>
            ))}
          </ol>
        </div>

        {assessments.length > 0 && (
          <div className="hairline pt-6">
            <p className="num-label mb-4">{t("student.assessments")}</p>
            <ol className="space-y-3">
              {assessments.map((a, i) => (
                <li
                  key={a.id}
                  className="grid grid-cols-[24px_1fr] gap-2 items-baseline text-sm"
                >
                  <span className="font-mono text-[10px] text-ink-faint tabular-nums">
                    p.{String(i + 1).padStart(2, "0")}
                  </span>
                  <div>
                    <p className="leading-tight">{a.title}</p>
                    <p className="font-mono text-[10px] uppercase tracking-[0.14em] text-ink-faint mt-0.5">
                      {a.type.replace(/_/g, " ")}
                    </p>
                  </div>
                </li>
              ))}
            </ol>
          </div>
        )}

        {resources.length > 0 && (
          <div className="hairline pt-6">
            <p className="num-label mb-4">{t("student.resources")}</p>
            <ul className="space-y-2">
              {resources.map((r) => (
                <li key={r.id}>
                  <a
                    href={r.url}
                    target="_blank"
                    rel="noreferrer"
                    className="flex items-baseline gap-2 text-sm text-ink-soft hover:text-ember transition-colors"
                  >
                    <span>{RESOURCE_ICONS[r.kind] || "🔗"}</span>
                    <span className="leading-tight truncate">{r.title}</span>
                  </a>
                </li>
              ))}
            </ul>
          </div>
        )}
      </aside>

      <main>
        {selectedLesson ? (
          <article className="space-y-8">
            <header>
              <p className="num-label">
                {selectedLesson.kind === "reading"
                  ? t("student.reading")
                  : `${t("student.lesson")} ${String(selectedLesson.order_index + 1).padStart(2, "0")}`}
              </p>
              <h1 className="font-display text-display-md mt-3 text-balance">
                {selectedLesson.title}
              </h1>
            </header>

            {selectedLesson.kind === "video" && selectedLesson.youtube_id && (
              <div className="aspect-video border border-bone shadow-frame overflow-hidden rounded-md">
                <iframe
                  className="w-full h-full"
                  src={`https://www.youtube-nocookie.com/embed/${selectedLesson.youtube_id}?rel=0&modestbranding=1`}
                  title={selectedLesson.title}
                  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                  allowFullScreen
                />
              </div>
            )}

            {selectedLesson.kind === "reading" && selectedLesson.body ? (
              <ReadingBody body={selectedLesson.body} />
            ) : selectedLesson.body ? (
              <div className="prose prose-lg max-w-none text-ink-soft leading-relaxed">
                {selectedLesson.body}
              </div>
            ) : null}

            <div className="hairline pt-6">
              <Button variant="outline" onClick={() => markComplete(selectedLesson.id)}>
                {t("student.markComplete")} <span aria-hidden>✓</span>
              </Button>
            </div>
          </article>
        ) : (
          <p className="text-ink-muted">{t("common.loading")}</p>
        )}
      </main>
    </div>
  );
}

function ReadingBody({ body }: { body: string }) {
  const { t } = useTranslation();
  const html = renderMarkdown(body);
  const handleContextMenu = (e: React.MouseEvent) => e.preventDefault();
  return (
    <div className="space-y-3">
      <div className="flex items-center gap-2 text-xs font-mono uppercase tracking-[0.14em] text-ink-muted">
        <span>🔒</span>
        <span>{t("student.readingLock")}</span>
      </div>
      <div
        className="prose prose-lg max-w-none text-ink-soft leading-relaxed select-none reading-body"
        onContextMenu={handleContextMenu}
        dangerouslySetInnerHTML={{ __html: html }}
      />
    </div>
  );
}

function renderMarkdown(src: string): string {
  const esc = (s: string) =>
    s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  const lines = src.split("\n");
  const out: string[] = [];
  let inList = false;
  let inPara: string[] = [];
  const flushPara = () => {
    if (inPara.length) {
      out.push(`<p>${inPara.join(" ")}</p>`);
      inPara = [];
    }
  };
  const closeList = () => {
    if (inList) {
      out.push("</ul>");
      inList = false;
    }
  };
  for (const raw of lines) {
    const line = raw.trimEnd();
    if (!line.trim()) {
      flushPara();
      closeList();
      continue;
    }
    const h1 = /^# (.+)$/.exec(line);
    const h2 = /^## (.+)$/.exec(line);
    const h3 = /^### (.+)$/.exec(line);
    const li = /^[-*] (?:\[[ x]\] )?(.+)$/.exec(line);
    if (h1) {
      flushPara();
      closeList();
      out.push(`<h1>${esc(h1[1])}</h1>`);
    } else if (h2) {
      flushPara();
      closeList();
      out.push(`<h2>${esc(h2[1])}</h2>`);
    } else if (h3) {
      flushPara();
      closeList();
      out.push(`<h3>${esc(h3[1])}</h3>`);
    } else if (li) {
      flushPara();
      if (!inList) {
        out.push("<ul>");
        inList = true;
      }
      const item = esc(li[1]).replace(
        /\*\*(.+?)\*\*/g,
        "<strong>$1</strong>",
      );
      out.push(`<li>${item}</li>`);
    } else {
      closeList();
      const text = esc(line).replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
      inPara.push(text);
    }
  }
  flushPara();
  closeList();
  return out.join("\n");
}

async function markComplete(lessonId: number) {
  const { data: enrollments } = await api.get<{ id: number }[]>("/enrollment/me");
  const enrollment = enrollments[0];
  if (!enrollment) return;
  await api.post(`/enrollment/${enrollment.id}/progress`, {
    lesson_id: lessonId,
    watched_pct: 100,
    completed: true,
  });
}
