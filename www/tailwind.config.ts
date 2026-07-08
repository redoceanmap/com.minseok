import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // === pixel (ragwatson) ===
        canvas: "#0B1E3F",
        night: {
          DEFAULT: "#0B1E3F",
          deep: "#050E22",
          mid: "#152D55",
        },
        ocean: {
          DEFAULT: "#1B3A5C",
          deep: "#0A2540",
          light: "#2D5A8A",
          foam: "#7AA8C7",
        },
        ink: "#F0EFE7",
        accent: {
          DEFAULT: "#FFC857",
          hover: "#E5A82C",
          soft: "#3D2C0F",
        },
        glow: {
          DEFAULT: "#FF8C42",
          warm: "#FFB36B",
        },
        star: "#FFE873",
        iceberg: {
          DEFAULT: "#B8D4E3",
          shadow: "#6FA0BC",
        },
        hull: "#0A0E1A",
        muted: "#8AA0C0",
        border: "#000000",
        // === glass (portfolio) ===
        glass: {
          surface: "rgba(255, 255, 255, 0.08)",
          border: "rgba(255, 255, 255, 0.18)",
          highlight: "rgba(255, 255, 255, 0.35)",
        },
      },
      fontFamily: {
        sans: ["var(--font-sans)", "var(--font-noto)", "system-ui", "sans-serif"],
        display: ["var(--font-display)", "var(--font-sans)", "sans-serif"],
        pixel: ["var(--font-press-start)", "Galmuri11", "Galmuri14", "var(--font-noto)", "monospace"],
        "pixel-kr": ["Galmuri11", "Galmuri14", "var(--font-noto)", "monospace"],
      },
      backdropBlur: {
        xs: "2px",
      },
      boxShadow: {
        // pixel
        pixel: "4px 4px 0 0 #000000",
        "pixel-sm": "2px 2px 0 0 #000000",
        "pixel-lg": "6px 6px 0 0 #000000",
        glow: "0 0 0 4px #000, 0 0 24px rgba(255,200,87,0.6)",
        porthole: "inset 0 0 0 4px #000, 0 0 16px rgba(255,140,66,0.4)",
        // glass
        glass:
          "inset 0 1px 0 0 rgba(255,255,255,0.25), inset 0 -1px 0 0 rgba(255,255,255,0.05), 0 10px 40px -10px rgba(0,0,0,0.45)",
        "glass-sm":
          "inset 0 1px 0 0 rgba(255,255,255,0.22), 0 4px 16px -4px rgba(0,0,0,0.35)",
      },
      keyframes: {
        // pixel
        twinkle: {
          "0%, 100%": { opacity: "1" },
          "50%": { opacity: "0.3" },
        },
        flicker: {
          "0%, 100%": { opacity: "1" },
          "45%": { opacity: "0.7" },
          "50%": { opacity: "0.95" },
          "55%": { opacity: "0.6" },
        },
        wave: {
          "0%, 100%": { transform: "translateX(0)" },
          "50%": { transform: "translateX(-16px)" },
        },
        // glass
        "float-slow": {
          "0%, 100%": { transform: "translate3d(0,0,0) scale(1)" },
          "50%": { transform: "translate3d(20px,-30px,0) scale(1.05)" },
        },
        "float-slower": {
          "0%, 100%": { transform: "translate3d(0,0,0) scale(1)" },
          "50%": { transform: "translate3d(-30px,20px,0) scale(1.08)" },
        },
      },
      animation: {
        // pixel
        twinkle: "twinkle 2s ease-in-out infinite",
        "twinkle-slow": "twinkle 3.5s ease-in-out infinite",
        flicker: "flicker 4s ease-in-out infinite",
        wave: "wave 6s ease-in-out infinite",
        "sail-sink": "sail-and-sink 22s ease-in-out infinite",
        "iceberg-shake": "iceberg-shake 22s ease-in-out infinite",
        explosion: "explosion 22s ease-in-out infinite",
        "explosion-aftershock": "explosion-aftershock 22s ease-in-out infinite",
        // glass
        "float-slow": "float-slow 14s ease-in-out infinite",
        "float-slower": "float-slower 18s ease-in-out infinite",
      },
    },
  },
  plugins: [],
};

export default config;
