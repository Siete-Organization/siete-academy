import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { api } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Input, Textarea } from "@/components/ui/input";

type Locale = "es" | "en" | "pt";
const LOCALES: Locale[] = ["es", "en", "pt"];

interface ModuleTranslation {
  locale: Locale;
  title: string;
  summary: string | null;
}

interface LessonTranslation {
  locale: Locale;
  title: string;
  body: string | null;
}

interface AdminLesson {
  id: number;
  module_id: number;
  order_index: number;
  kind: "video" | "reading";
  youtube_id: string | null;
  duration_seconds: number | null;
  translations: LessonTranslation[];
}

type ResourceKind = "pdf" | "ppt" | "video" | "doc" | "link";

interface ModuleResource {
  id: number;
  module_id: number;
  kind: ResourceKind;
  title: string;
  url: string;
  order_index: number;
}

type AssessmentType =
  | "mcq"
  | "written"
  | "prospection_db"
  | "cold_call_video"
  | "team_exercise";

interface Assessment {
  id: number;
  module_id: number;
  type: AssessmentType;
  title: string;
  config: Record<string, unknown>;
  passing_score: number;
}

interface AdminModule {
  id: number;
  course_id: number;
  slug: string;
  order_index: number;
  translations: ModuleTranslation[];
  lessons: AdminLesson[];
  resources: ModuleResource[];
}

interface Course {
  id: number;
  slug: string;
  title: string;
  description: string | null;
}

const DEFAULT_COURSE_SLUG = "sdr-fundamentals";

export function AdminCourse() {
  const { t } = useTranslation();
  const [course, setCourse] = useState<Course | null>(null);
  const [modules, setModules] = useState<AdminModule[]>([]);
  const [expanded, setExpanded] = useState<Record<number, boolean>>({});

  const load = async () => {
    const { data: courses } = await api.get<Course[]>("/courses");
    const c = courses.find((x) => x.slug === DEFAULT_COURSE_SLUG) || courses[0];
    if (!c) return;
    setCourse(c);
    const { data: mods } = await api.get<AdminModule[]>(`/courses/${c.id}/admin`);
    setModules(mods);
  };

  useEffect(() => {
    void load();
  }, []);

  if (!course) {
    return (
      <div className="container-editorial py-24 text-ink-muted">{t("common.loading")}</div>
    );
  }

  return (
    <div className="container-editorial py-16 md:py-20 space-y-10">
      <header className="flex items-end justify-between flex-wrap gap-4">
        <div>
          <p className="num-label">{t("adminCourse.eyebrow")}</p>
          <h1 className="font-display text-display-lg mt-4">{course.title}</h1>
          <p className="text-ink-soft mt-4 max-w-2xl">{t("adminCourse.subtitle")}</p>
        </div>
        <Link
          to="/admin/cohorts"
          className="text-xs uppercase tracking-[0.14em] font-mono text-ink-muted hover:text-ink transition-colors"
        >
          {t("adminCourse.goToCohorts")} →
        </Link>
      </header>

      <section className="space-y-4">
        {modules.map((m) => (
          <ModuleCard
            key={m.id}
            module={m}
            expanded={!!expanded[m.id]}
            onToggle={() =>
              setExpanded((prev) => ({ ...prev, [m.id]: !prev[m.id] }))
            }
            onReload={load}
          />
        ))}
        {modules.length === 0 && (
          <p className="text-ink-muted text-sm">{t("adminCourse.noModules")}</p>
        )}
      </section>
    </div>
  );
}

function getTitle(translations: { locale: Locale; title: string }[]): string {
  return (
    translations.find((t) => t.locale === "es")?.title ||
    translations[0]?.title ||
    "—"
  );
}

function ModuleCard({
  module: mod,
  expanded,
  onToggle,
  onReload,
}: {
  module: AdminModule;
  expanded: boolean;
  onToggle: () => void;
  onReload: () => Promise<void>;
}) {
  const { t } = useTranslation();
  const [editing, setEditing] = useState(false);

  return (
    <article className="border border-bone rounded-xs overflow-hidden">
      <header
        className="flex items-center justify-between px-5 py-4 bg-paper-tint/40 cursor-pointer hover:bg-paper-tint transition-colors"
        onClick={onToggle}
      >
        <div className="flex items-baseline gap-4">
          <span className="font-mono text-xs text-ink-faint tabular-nums">
            {String(mod.order_index + 1).padStart(2, "0")}
          </span>
          <h2 className="font-display text-xl">{getTitle(mod.translations)}</h2>
          <span className="text-xs text-ink-muted font-mono">
            · {mod.lessons.length} {t("adminCourse.lessons")}
          </span>
        </div>
        <span
          className={`transition-transform text-ink-muted ${expanded ? "rotate-90" : ""}`}
        >
          →
        </span>
      </header>

      {expanded && (
        <div className="border-t border-bone px-5 py-6 space-y-8">
          <div className="flex items-center justify-between">
            <p className="num-label">{t("adminCourse.moduleSettings")}</p>
            <Button
              size="sm"
              variant={editing ? "outline" : "subtle"}
              onClick={() => setEditing((v) => !v)}
            >
              {editing ? t("common.cancel") : t("adminCourse.editModule")}
            </Button>
          </div>
          {editing && (
            <ModuleEditor
              module={mod}
              onSaved={async () => {
                setEditing(false);
                await onReload();
              }}
            />
          )}

          <div className="space-y-4 hairline pt-6">
            <p className="num-label">{t("adminCourse.lessons")}</p>
            {mod.lessons.map((le) => (
              <LessonRow key={le.id} lesson={le} onReload={onReload} />
            ))}
            <AddLessonForm
              moduleId={mod.id}
              nextIndex={
                mod.lessons.length
                  ? Math.max(...mod.lessons.map((l) => l.order_index)) + 1
                  : 0
              }
              onAdded={onReload}
            />
          </div>

          <ResourcesSection
            moduleId={mod.id}
            resources={mod.resources || []}
            onReload={onReload}
          />

          <AssessmentsSection moduleId={mod.id} />
        </div>
      )}
    </article>
  );
}

const RESOURCE_KINDS: {
  value: ResourceKind;
  icon: string;
  label: string;
}[] = [
  { value: "pdf", icon: "📄", label: "PDF" },
  { value: "ppt", icon: "📊", label: "PPT" },
  { value: "video", icon: "🎞", label: "Video" },
  { value: "doc", icon: "📝", label: "Doc" },
  { value: "link", icon: "🔗", label: "Link" },
];

function ResourcesSection({
  moduleId,
  resources,
  onReload,
}: {
  moduleId: number;
  resources: ModuleResource[];
  onReload: () => Promise<void>;
}) {
  const { t } = useTranslation();
  const [adding, setAdding] = useState(false);
  const [kind, setKind] = useState<ResourceKind>("pdf");
  const [title, setTitle] = useState("");
  const [url, setUrl] = useState("");
  const [saving, setSaving] = useState(false);

  const reset = () => {
    setAdding(false);
    setTitle("");
    setUrl("");
    setKind("pdf");
  };

  const handleAdd = async () => {
    if (!title.trim() || !url.trim()) return;
    setSaving(true);
    try {
      await api.post(`/courses/modules/${moduleId}/resources`, {
        kind,
        title,
        url,
        order_index: resources.length,
      });
      reset();
      await onReload();
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (!window.confirm(t("adminCourse.confirmDeleteResource"))) return;
    await api.delete(`/courses/resources/${id}`);
    await onReload();
  };

  return (
    <div className="space-y-4 hairline pt-6">
      <p className="num-label">{t("adminCourse.resources")}</p>
      {resources.length === 0 && !adding && (
        <p className="text-xs text-ink-muted">{t("adminCourse.resourcesEmpty")}</p>
      )}
      {resources.map((r) => (
        <div
          key={r.id}
          className="flex items-center justify-between border border-bone rounded-xs px-4 py-2.5 bg-paper"
        >
          <div className="flex items-baseline gap-3">
            <span className="text-base leading-none">
              {RESOURCE_KINDS.find((k) => k.value === r.kind)?.icon || "🔗"}
            </span>
            <div>
              <p className="text-sm font-medium text-ink">{r.title}</p>
              <p className="text-[11px] text-ink-muted truncate max-w-xl">{r.url}</p>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <a
              href={r.url}
              target="_blank"
              rel="noreferrer"
              className="text-xs font-mono uppercase tracking-[0.14em] text-ember hover:underline underline-offset-4"
            >
              {t("adminCourse.preview")} ↗
            </a>
            <button
              onClick={() => void handleDelete(r.id)}
              className="text-xs font-mono uppercase tracking-[0.14em] text-ink-faint hover:text-ember transition-colors"
            >
              {t("adminCourse.delete")}
            </button>
          </div>
        </div>
      ))}
      {adding ? (
        <div className="border border-bone bg-paper-warm/40 p-5 rounded-xs space-y-4">
          <div className="flex items-center gap-2 flex-wrap">
            {RESOURCE_KINDS.map((k) => (
              <button
                key={k.value}
                type="button"
                onClick={() => setKind(k.value)}
                className={`px-3 py-1.5 border text-xs uppercase tracking-[0.14em] font-mono transition-colors ${
                  kind === k.value
                    ? "border-ink bg-ink text-paper"
                    : "border-bone text-ink-muted hover:border-ink"
                }`}
              >
                {k.icon} {k.label}
              </button>
            ))}
          </div>
          <Input
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder={t("adminCourse.resourceTitlePlaceholder")}
          />
          <Input
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="https://drive.google.com/... · https://loom.com/..."
          />
          <p className="text-[11px] text-ink-muted">{t("adminCourse.resourceHint")}</p>
          <div className="flex items-center gap-3">
            <Button
              onClick={handleAdd}
              size="sm"
              variant="ember"
              disabled={saving || !title.trim() || !url.trim()}
            >
              {saving ? "…" : t("adminCourse.addResource")}
            </Button>
            <button
              type="button"
              onClick={reset}
              className="text-xs uppercase tracking-[0.14em] font-mono text-ink-muted hover:text-ink"
            >
              {t("common.cancel")}
            </button>
          </div>
        </div>
      ) : (
        <Button size="sm" variant="outline" onClick={() => setAdding(true)}>
          + {t("adminCourse.addResource")}
        </Button>
      )}
    </div>
  );
}

const ASSESSMENT_TYPES: AssessmentType[] = [
  "mcq",
  "written",
  "prospection_db",
  "cold_call_video",
  "team_exercise",
];

function AssessmentsSection({ moduleId }: { moduleId: number }) {
  const { t } = useTranslation();
  const [items, setItems] = useState<Assessment[]>([]);
  const [loaded, setLoaded] = useState(false);
  const [adding, setAdding] = useState(false);
  const [editingId, setEditingId] = useState<number | null>(null);

  const load = async () => {
    const { data } = await api.get<Assessment[]>(`/assessments/module/${moduleId}`);
    setItems(data);
    setLoaded(true);
  };

  useEffect(() => {
    void load();
  }, [moduleId]);

  const handleDelete = async (id: number) => {
    if (!window.confirm(t("adminCourse.confirmDeleteAssessment"))) return;
    await api.delete(`/assessments/${id}`);
    await load();
  };

  return (
    <div className="space-y-4 hairline pt-6">
      <p className="num-label">{t("adminCourse.assessments")}</p>
      {!loaded ? (
        <p className="text-xs text-ink-muted">{t("common.loading")}</p>
      ) : items.length === 0 && !adding ? (
        <p className="text-xs text-ink-muted">{t("adminCourse.assessmentsEmpty")}</p>
      ) : null}

      {items.map((a) =>
        editingId === a.id ? (
          <AssessmentEditor
            key={a.id}
            moduleId={moduleId}
            assessment={a}
            onDone={async () => {
              setEditingId(null);
              await load();
            }}
          />
        ) : (
          <div
            key={a.id}
            className="flex items-center justify-between border border-bone rounded-xs px-4 py-2.5 bg-paper"
          >
            <div className="flex items-baseline gap-3">
              <span className="font-mono text-[10px] uppercase tracking-[0.14em] text-ink-muted">
                {a.type.replace(/_/g, " ")}
              </span>
              <p className="text-sm font-medium text-ink">{a.title}</p>
              <span className="font-mono text-[10px] text-ink-faint">
                paso ≥ {a.passing_score}
              </span>
            </div>
            <div className="flex items-center gap-3">
              <button
                onClick={() => setEditingId(a.id)}
                className="text-xs font-mono uppercase tracking-[0.14em] text-ink-muted hover:text-ink"
              >
                {t("adminCourse.edit")}
              </button>
              <button
                onClick={() => void handleDelete(a.id)}
                className="text-xs font-mono uppercase tracking-[0.14em] text-ember hover:text-ink"
              >
                {t("adminCourse.delete")}
              </button>
            </div>
          </div>
        ),
      )}

      {adding ? (
        <AssessmentEditor
          moduleId={moduleId}
          assessment={null}
          onDone={async () => {
            setAdding(false);
            await load();
          }}
        />
      ) : (
        <Button size="sm" variant="outline" onClick={() => setAdding(true)}>
          + {t("adminCourse.addAssessment")}
        </Button>
      )}
    </div>
  );
}

function AssessmentEditor({
  moduleId,
  assessment,
  onDone,
}: {
  moduleId: number;
  assessment: Assessment | null;
  onDone: () => Promise<void>;
}) {
  const { t } = useTranslation();
  const [type, setType] = useState<AssessmentType>(assessment?.type || "mcq");
  const [title, setTitle] = useState(assessment?.title || "");
  const [passing, setPassing] = useState<number>(assessment?.passing_score ?? 70);
  const [configJson, setConfigJson] = useState(
    JSON.stringify(assessment?.config ?? {}, null, 2),
  );
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSave = async () => {
    setError(null);
    let config: unknown;
    try {
      config = JSON.parse(configJson || "{}");
    } catch (e) {
      setError(t("adminCourse.invalidJson"));
      return;
    }
    setSaving(true);
    try {
      if (assessment) {
        await api.patch(`/assessments/${assessment.id}`, {
          type,
          title,
          passing_score: passing,
          config,
        });
      } else {
        await api.post(`/assessments`, {
          module_id: moduleId,
          type,
          title,
          passing_score: passing,
          config,
        });
      }
      await onDone();
    } catch (err) {
      const detail =
        (err as { response?: { data?: { detail?: string } } }).response?.data?.detail ||
        (err instanceof Error ? err.message : t("common.error"));
      setError(String(detail));
    } finally {
      setSaving(false);
    }
  };

  const placeholderByType: Record<AssessmentType, string> = {
    mcq: JSON.stringify(
      {
        questions: [
          {
            id: "q1",
            prompt: "¿Pregunta aquí?",
            options: { a: "Opción A", b: "Opción B", c: "Opción C" },
          },
        ],
        correct_answers: { q1: "b" },
      },
      null,
      2,
    ),
    written: JSON.stringify({ prompt: "Enunciado de la entrega escrita (200-300 palabras)." }, null, 2),
    prospection_db: JSON.stringify(
      { instructions: "Sube un CSV con 50 prospects del ICP del módulo X. Columnas: ..." },
      null,
      2,
    ),
    cold_call_video: JSON.stringify(
      {
        instructions: "Graba un cold call de 2 min con el pitch que armaste.",
        rubric: ["apertura clara", "discovery", "manejo de objeciones", "cierre"],
      },
      null,
      2,
    ),
    team_exercise: JSON.stringify(
      { instructions: "En equipo de 3, diseñen una cadencia outbound para este ICP." },
      null,
      2,
    ),
  };

  return (
    <div className="border border-bone bg-paper-warm/40 p-5 rounded-xs space-y-4">
      <div className="flex items-center gap-2 flex-wrap">
        {ASSESSMENT_TYPES.map((ty) => (
          <button
            key={ty}
            type="button"
            onClick={() => setType(ty)}
            className={`px-3 py-1.5 border text-xs uppercase tracking-[0.14em] font-mono transition-colors ${
              type === ty
                ? "border-ink bg-ink text-paper"
                : "border-bone text-ink-muted hover:border-ink"
            }`}
          >
            {ty.replace(/_/g, " ")}
          </button>
        ))}
      </div>
      <Input
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        placeholder={t("adminCourse.assessmentTitlePlaceholder")}
      />
      <label className="block max-w-[160px]">
        <span className="num-label mb-1 block">{t("adminCourse.passing")}</span>
        <Input
          type="number"
          value={passing}
          min={0}
          max={100}
          onChange={(e) => setPassing(Number(e.target.value))}
        />
      </label>
      <div>
        <span className="num-label mb-1 block">{t("adminCourse.config")}</span>
        <Textarea
          value={configJson}
          onChange={(e) => setConfigJson(e.target.value)}
          rows={10}
          className="font-mono text-xs"
          placeholder={placeholderByType[type]}
        />
        <p className="text-[11px] text-ink-muted mt-1">{t("adminCourse.configHint")}</p>
      </div>
      {error && <p className="text-ember text-sm">{error}</p>}
      <div className="flex items-center gap-3">
        <Button
          onClick={handleSave}
          size="sm"
          variant="ember"
          disabled={saving || !title.trim()}
        >
          {saving ? "…" : t("common.save")}
        </Button>
        <button
          type="button"
          onClick={() => void onDone()}
          className="text-xs uppercase tracking-[0.14em] font-mono text-ink-muted hover:text-ink"
        >
          {t("common.cancel")}
        </button>
      </div>
    </div>
  );
}

function ModuleEditor({
  module: mod,
  onSaved,
}: {
  module: AdminModule;
  onSaved: () => Promise<void>;
}) {
  const { t } = useTranslation();
  const initial = useMemo(() => {
    const by = Object.fromEntries(
      mod.translations.map((t) => [t.locale, { title: t.title, summary: t.summary || "" }]),
    ) as Record<Locale, { title: string; summary: string }>;
    LOCALES.forEach((l) => {
      if (!by[l]) by[l] = { title: "", summary: "" };
    });
    return by;
  }, [mod]);
  const [trans, setTrans] = useState(initial);
  const [orderIndex, setOrderIndex] = useState(mod.order_index);
  const [saving, setSaving] = useState(false);

  const handleSave = async () => {
    setSaving(true);
    try {
      await api.patch(`/courses/modules/${mod.id}`, {
        order_index: orderIndex,
        translations: LOCALES.map((l) => ({
          locale: l,
          title: trans[l].title,
          summary: trans[l].summary || null,
        })),
      });
      await onSaved();
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="space-y-6 bg-paper-warm/40 p-5 rounded-xs border border-bone">
      <label className="block max-w-xs">
        <span className="num-label mb-1 block">{t("adminCourse.order")}</span>
        <Input
          type="number"
          value={orderIndex}
          onChange={(e) => setOrderIndex(Number(e.target.value))}
        />
      </label>
      {LOCALES.map((l) => (
        <div key={l} className="space-y-2">
          <p className="font-mono text-[10px] uppercase tracking-[0.14em] text-ink-muted">
            {l.toUpperCase()}
          </p>
          <Input
            value={trans[l].title}
            onChange={(e) =>
              setTrans({ ...trans, [l]: { ...trans[l], title: e.target.value } })
            }
            placeholder={t("adminCourse.moduleTitle")}
          />
          <Textarea
            value={trans[l].summary}
            onChange={(e) =>
              setTrans({ ...trans, [l]: { ...trans[l], summary: e.target.value } })
            }
            placeholder={t("adminCourse.moduleSummary")}
          />
        </div>
      ))}
      <Button onClick={handleSave} disabled={saving} variant="ember">
        {saving ? t("common.save") + "…" : t("common.save")}
      </Button>
    </div>
  );
}

function LessonRow({
  lesson,
  onReload,
}: {
  lesson: AdminLesson;
  onReload: () => Promise<void>;
}) {
  const { t } = useTranslation();
  const [editing, setEditing] = useState(false);
  const [deleting, setDeleting] = useState(false);

  const handleDelete = async () => {
    if (!window.confirm(t("adminCourse.confirmDelete"))) return;
    setDeleting(true);
    try {
      await api.delete(`/courses/lessons/${lesson.id}`);
      await onReload();
    } finally {
      setDeleting(false);
    }
  };

  return (
    <div className="border border-bone rounded-xs overflow-hidden">
      <div className="flex items-center justify-between px-4 py-3 bg-paper">
        <div className="flex items-baseline gap-3">
          <span className="font-mono text-[10px] text-ink-faint tabular-nums">
            {String(lesson.order_index + 1).padStart(2, "0")}
          </span>
          <span className="text-sm font-medium">
            {getTitle(lesson.translations)}
          </span>
          <span className="font-mono text-[10px] uppercase tracking-[0.14em] text-ink-muted">
            {lesson.kind === "reading" ? "📖 manual" : "▶ video"}
          </span>
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={() => setEditing((v) => !v)}
            className="text-xs uppercase tracking-[0.14em] font-mono text-ink-muted hover:text-ink transition-colors"
          >
            {editing ? t("common.cancel") : t("adminCourse.edit")}
          </button>
          <button
            onClick={handleDelete}
            disabled={deleting}
            className="text-xs uppercase tracking-[0.14em] font-mono text-ember hover:text-ink transition-colors disabled:opacity-50"
          >
            {deleting ? "…" : t("adminCourse.delete")}
          </button>
        </div>
      </div>
      {editing && (
        <div className="p-5 border-t border-bone bg-paper-warm/40">
          <LessonEditor
            lesson={lesson}
            onSaved={async () => {
              setEditing(false);
              await onReload();
            }}
          />
        </div>
      )}
    </div>
  );
}

function LessonEditor({
  lesson,
  onSaved,
}: {
  lesson: AdminLesson;
  onSaved: () => Promise<void>;
}) {
  const { t } = useTranslation();
  const initial = useMemo(() => {
    const by = Object.fromEntries(
      lesson.translations.map((t) => [t.locale, { title: t.title, body: t.body || "" }]),
    ) as Record<Locale, { title: string; body: string }>;
    LOCALES.forEach((l) => {
      if (!by[l]) by[l] = { title: "", body: "" };
    });
    return by;
  }, [lesson]);
  const [trans, setTrans] = useState(initial);
  const [kind, setKind] = useState<"video" | "reading">(lesson.kind);
  const [youtubeId, setYoutubeId] = useState(lesson.youtube_id || "");
  const [duration, setDuration] = useState(lesson.duration_seconds || 0);
  const [orderIndex, setOrderIndex] = useState(lesson.order_index);
  const [saving, setSaving] = useState(false);

  const handleSave = async () => {
    setSaving(true);
    try {
      await api.patch(`/courses/lessons/${lesson.id}`, {
        order_index: orderIndex,
        kind,
        youtube_id: kind === "video" ? youtubeId || null : null,
        duration_seconds: kind === "video" ? duration || null : null,
        translations: LOCALES.map((l) => ({
          locale: l,
          title: trans[l].title,
          body: trans[l].body || null,
        })),
      });
      await onSaved();
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4 flex-wrap">
        <label className="text-sm text-ink">
          <input
            type="radio"
            checked={kind === "video"}
            onChange={() => setKind("video")}
            className="mr-2"
          />
          {t("adminCourse.kindVideo")}
        </label>
        <label className="text-sm text-ink">
          <input
            type="radio"
            checked={kind === "reading"}
            onChange={() => setKind("reading")}
            className="mr-2"
          />
          {t("adminCourse.kindReading")}
        </label>
        <label className="block max-w-[120px]">
          <span className="num-label mb-1 block">{t("adminCourse.order")}</span>
          <Input
            type="number"
            value={orderIndex}
            onChange={(e) => setOrderIndex(Number(e.target.value))}
          />
        </label>
      </div>

      {kind === "video" && (
        <div className="grid grid-cols-1 md:grid-cols-[1fr_160px] gap-4">
          <label className="block">
            <span className="num-label mb-1 block">{t("adminCourse.youtubeId")}</span>
            <Input
              value={youtubeId}
              onChange={(e) => setYoutubeId(e.target.value)}
              placeholder="dQw4w9WgXcQ"
            />
            <p className="text-[11px] text-ink-muted mt-1">
              {t("adminCourse.youtubeHint")}
            </p>
          </label>
          <label className="block">
            <span className="num-label mb-1 block">{t("adminCourse.duration")}</span>
            <Input
              type="number"
              value={duration}
              onChange={(e) => setDuration(Number(e.target.value))}
              placeholder="600"
            />
          </label>
        </div>
      )}

      {LOCALES.map((l) => (
        <div key={l} className="space-y-2">
          <p className="font-mono text-[10px] uppercase tracking-[0.14em] text-ink-muted">
            {l.toUpperCase()}
          </p>
          <Input
            value={trans[l].title}
            onChange={(e) =>
              setTrans({ ...trans, [l]: { ...trans[l], title: e.target.value } })
            }
            placeholder={t("adminCourse.lessonTitle")}
          />
          <Textarea
            value={trans[l].body}
            onChange={(e) =>
              setTrans({ ...trans, [l]: { ...trans[l], body: e.target.value } })
            }
            placeholder={
              kind === "reading"
                ? t("adminCourse.readingPlaceholder")
                : t("adminCourse.lessonBody")
            }
            rows={kind === "reading" ? 10 : 4}
          />
        </div>
      ))}

      <Button onClick={handleSave} disabled={saving} variant="ember">
        {saving ? t("common.save") + "…" : t("common.save")}
      </Button>
    </div>
  );
}

function AddLessonForm({
  moduleId,
  nextIndex,
  onAdded,
}: {
  moduleId: number;
  nextIndex: number;
  onAdded: () => Promise<void>;
}) {
  const { t } = useTranslation();
  const [open, setOpen] = useState(false);
  const [kind, setKind] = useState<"video" | "reading">("video");
  const [titleEs, setTitleEs] = useState("");
  const [youtubeId, setYoutubeId] = useState("");
  const [saving, setSaving] = useState(false);

  if (!open) {
    return (
      <Button variant="outline" size="sm" onClick={() => setOpen(true)}>
        + {t("adminCourse.addLesson")}
      </Button>
    );
  }

  const handleAdd = async () => {
    if (!titleEs.trim()) return;
    setSaving(true);
    try {
      await api.post(`/courses/modules/${moduleId}/lessons`, {
        order_index: nextIndex,
        kind,
        youtube_id: kind === "video" ? youtubeId || null : null,
        translations: [
          { locale: "es", title: titleEs, body: null },
          { locale: "en", title: titleEs, body: null },
          { locale: "pt", title: titleEs, body: null },
        ],
      });
      setTitleEs("");
      setYoutubeId("");
      setOpen(false);
      await onAdded();
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="border border-bone bg-paper-warm/40 p-5 rounded-xs space-y-4">
      <div className="flex items-center gap-4">
        <label className="text-sm">
          <input
            type="radio"
            checked={kind === "video"}
            onChange={() => setKind("video")}
            className="mr-2"
          />
          {t("adminCourse.kindVideo")}
        </label>
        <label className="text-sm">
          <input
            type="radio"
            checked={kind === "reading"}
            onChange={() => setKind("reading")}
            className="mr-2"
          />
          {t("adminCourse.kindReading")}
        </label>
      </div>
      <Input
        value={titleEs}
        onChange={(e) => setTitleEs(e.target.value)}
        placeholder={t("adminCourse.lessonTitlePlaceholder")}
      />
      {kind === "video" && (
        <Input
          value={youtubeId}
          onChange={(e) => setYoutubeId(e.target.value)}
          placeholder="YouTube ID"
        />
      )}
      <div className="flex items-center gap-3">
        <Button
          onClick={handleAdd}
          disabled={saving || !titleEs.trim()}
          size="sm"
          variant="ember"
        >
          {saving ? "…" : t("adminCourse.addLesson")}
        </Button>
        <button
          type="button"
          onClick={() => setOpen(false)}
          className="text-xs uppercase tracking-[0.14em] font-mono text-ink-muted hover:text-ink"
        >
          {t("common.cancel")}
        </button>
      </div>
      <p className="text-[11px] text-ink-muted">{t("adminCourse.addLessonHint")}</p>
    </div>
  );
}
