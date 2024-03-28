/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    '/templates/**/*.html',
    '/../templates/**/*.html',
    '/**/templates/**/*.html',
  ],
  theme: {
    extend: {
      colors: {
        midnight: '#0D2951',
        light_blue: '#52C5F2',
        gray: '#2b2d42',
        red: '#F25041',
        ghost_white: '#F8F8FF',
      },
    },
  },
  plugins: [
    /**
         * '@tailwindcss/forms' is the forms plugin that provides a minimal styling
         * for forms. If you don't like it or have own styling for forms,
         * comment the line below to disable '@tailwindcss/forms'.
         */
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
    require('@tailwindcss/aspect-ratio'),
  ],
}

