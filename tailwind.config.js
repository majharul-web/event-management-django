/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./**/templates/**/*.html",
    "./events/templates/**/*.html",
    "./**/events/templates/**/*.html",
    "./users/templates/**/*.html",
    "./**/users/templates/**/*.html",
    "./events/forms.py",
  ],
  theme: {
    extend: {
      colors: {
        // ShadCN-style blue primary
        primary: {
          50: "#eff6ff",
          100: "#dbeafe",
          200: "#bfdbfe",
          300: "#93c5fd",
          400: "#60a5fa",
          500: "#3b82f6", // main blue
          600: "#2563eb",
          700: "#1d4ed8",
          800: "#1e40af",
          900: "#1e3a8a",
        },
        // Secondary lighter/cooler blue
        secondary: {
          50: "#f0f9ff",
          100: "#e0f2fe",
          200: "#bae6fd",
          300: "#7dd3fc",
          400: "#38bdf8",
          500: "#0ea5e9",
          600: "#0284c7",
          700: "#0369a1",
          800: "#075985",
          900: "#0c4a6e",
        },
        muted: {
          50: "#f9fafb",
          100: "#f3f4f6",
          200: "#e5e7eb",
          300: "#d1d5db",
          400: "#9ca3af",
          500: "#6b7280",
          600: "#4b5563",
          700: "#374151",
          800: "#1f2937",
          900: "#111827",
        },
        success: "#16a34a",
        warning: "#f59e0b",
        danger: "#dc2626",
      },
      ringColor: (theme) => ({
        primary: theme("colors.primary.500"),
        secondary: theme("colors.secondary.500"),
        success: theme("colors.success"),
        warning: theme("colors.warning"),
        danger: theme("colors.danger"),
      }),
    },
  },
  plugins: [],
};
