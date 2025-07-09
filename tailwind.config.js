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
        primary: {
          DEFAULT: "#f43f5e", // Rose 600
          light: "#fecdd3", // Rose 300
          dark: "#dc2626", // Rose 700
        },
      },
    },
  },
  plugins: [],
};
