/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        paper: {
          DEFAULT: "#faf8f3",
          tint: "#f4f1e9",
          deep: "#ece8db",
        },
        ink: {
          DEFAULT: "#0f0f10",
          soft: "#2a2a2d",
          muted: "#5b5b61",
          faint: "#8a8a90",
        },
        bone: {
          DEFAULT: "#e6e2d6",
          strong: "#d8d3c2",
        },
        ember: {
          DEFAULT: "#b8461f",
          soft: "#e88664",
          ghost: "#f8e7dc",
        },
        moss: {
          DEFAULT: "#3d4d35",
          soft: "#6f805f",
        },
        brand: {
          50: "#f5f7ff",
          500: "#4f46e5",
          600: "#4338ca",
          700: "#3730a3",
          900: "#1e1b4b",
        },
      },
      fontFamily: {
        display: ['"Fraunces"', "Georgia", "serif"],
        sans: ['"Inter"', "system-ui", "sans-serif"],
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
