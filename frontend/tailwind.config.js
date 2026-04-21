/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        // Rebrand 2026 — paleta primaria (AZUL PROFUNDO / COOL STEEL)
        // Los tokens "paper/ink/bone/ember/moss" se mantienen por compatibilidad,
        // pero apuntan ahora a los valores oficiales del rebranding.
        paper: {
          DEFAULT: "#F5F5F7",        // OFF WHITE (rebrand)
          warm: "#FFFFFF",
          tint: "#EDEDF0",
          deep: "#E4E4E9",
        },
        ink: {
          DEFAULT: "#000000",        // BLACK (rebrand)
          soft: "#1a1a1c",
          muted: "#505058",
          faint: "#8c8c94",
        },
        bone: {
          DEFAULT: "#E4E4E9",
          strong: "#CECED4",
        },
        // Accent principal — COOL STEEL. Se usa para CTAs y highlights.
        ember: {
          DEFAULT: "#406E8E",        // COOL STEEL (rebrand)
          soft: "#6A94B0",
          ghost: "#E9F0F5",
        },
        // Accent secundario — FROZEN WATER. Para chips suaves y badges info.
        sky: {
          DEFAULT: "#B8DBD9",        // FROZEN WATER (rebrand)
          soft: "#D6EAE9",
          deep: "#86BAB7",
        },
        // Semántico: success/warn ajustados para convivir con el azul.
        moss: {
          DEFAULT: "#2F5D45",
          soft: "#5E8873",
        },
        brand: {
          50: "#E9F0F5",
          500: "#406E8E",
          600: "#345A75",
          700: "#274558",
          900: "#182C38",
        },
      },
      fontFamily: {
        // Brand: Montserrat para títulos + cuerpo largo.
        // Space Grotesk como stand-in del "Road Radio" del rebrand (display).
        display: ['"Space Grotesk"', '"Montserrat"', "system-ui", "sans-serif"],
        sans: ['"Montserrat"', "system-ui", "sans-serif"],
        mono: ['"JetBrains Mono"', "ui-monospace", "monospace"],
      },
      fontSize: {
        "display-xl": ["clamp(3.25rem, 8vw, 5.75rem)", { lineHeight: "0.95", letterSpacing: "-0.03em" }],
        "display-lg": ["clamp(2.25rem, 5vw, 3.75rem)", { lineHeight: "1", letterSpacing: "-0.025em" }],
        "display-md": ["2rem", { lineHeight: "1.1", letterSpacing: "-0.02em" }],
        eyebrow: ["0.72rem", { lineHeight: "1", letterSpacing: "0.18em" }],
        micro: ["0.68rem", { lineHeight: "1.1", letterSpacing: "0.12em" }],
      },
      letterSpacing: {
        editorial: "-0.02em",
      },
      borderRadius: {
        xs: "2px",
        DEFAULT: "4px",
        md: "6px",
        lg: "10px",
      },
      boxShadow: {
        frame: "0 0 0 1px rgb(15 15 16 / 0.06), 0 1px 2px rgb(15 15 16 / 0.04)",
        lift: "0 0 0 1px rgb(15 15 16 / 0.08), 0 12px 30px -12px rgb(15 15 16 / 0.22)",
        inset: "inset 0 0 0 1px rgb(15 15 16 / 0.08)",
      },
      keyframes: {
        "fade-up": {
          "0%": { opacity: "0", transform: "translateY(14px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
        "stroke-in": {
          "0%": { transform: "scaleX(0)" },
          "100%": { transform: "scaleX(1)" },
        },
      },
      animation: {
        "fade-up": "fade-up 0.7s cubic-bezier(0.2, 0.6, 0.2, 1) both",
        "stroke-in": "stroke-in 0.8s cubic-bezier(0.65, 0, 0.35, 1) both",
      },
    },
  },
  plugins: [],
};
