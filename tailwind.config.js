/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [

    "./templates/**/*.html", // template level
    "./**/templates/**/*.html", // tempates inside the apps like task
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}

