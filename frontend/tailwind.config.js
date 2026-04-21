/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        // Rebrand 2026 — paleta de wearesiete.com (System Blue + Glacial Sky).
        // Muestreado del stylesheet real del sitio (frecuencia descendente):
        //   #000 (1060x) · #007aff (509x) · #f5f5f7 (470x) · #fff (453x)
        //   #dbdbdb (113x) · #8fbdff (77x) · #1a1b1f · #bababa
        paper: {
          DEFAULT: "#F5F5F7",        // OFF WHITE (site bg)
          warm: "#FFFFFF",
          tint: "#FAFAFA",
          deep: "#EDEDF0",
        },
        ink: {
          DEFAULT: "#000000",        // BLACK (site text)
          soft: "#1a1b1f",
          muted: "#5D6C7B",
          faint: "#999FAE",
        },
        bone: {
          DEFAULT: "#DBDBDB",        // borders reales del site
          strong: "#BABABA",
        },
        // Accent principal — SYSTEM BLUE. CTAs, buttons, links, accents.
        ember: {
          DEFAULT: "#007AFF",        // System Blue (wearesiete.com)
          soft: "#3F9AFF",
          ghost: "#E5F2FF",
        },
        // Accent secundario — GLACIAL SKY (light blue).
        sky: {
          DEFAULT: "#8FBDFF",        // Glacial Sky (wearesiete.com)
          soft: "#C4DDFF",
          deep: "#5E9CE6",
        },
        // Semántico: success/warn ajustados para convivir con el azul.
        moss: {
          DEFAULT: "#2F5D45",
          soft: "#5E8873",
        },
        brand: {
          50: "#E5F2FF",
          500: "#007AFF",
          600: "#0062CC",
          700: "#004C99",
          900: "#002B56",
        },
      },
      fontFamily: {
        // wearesiete.com usa Montserrat para TODO. Seguimos el mismo camino.
        display: ['"Montserrat"', "Arial", "system-ui", "sans-serif"],
        sans: ['"Montserrat"', "Arial", "system-ui", "sans-serif"],
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
