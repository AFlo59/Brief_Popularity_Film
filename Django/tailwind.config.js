module.exports = {
  content: [
    './templates/*.html',
    './templates/**/*.html',
    './**/templates/**/*.html',
  ],
  theme: {
    extend: {
      colors: {
        // Bleu
        'custom-blue-light': '#66c6ff',
        'custom-blue': '#3399ff',
        'custom-blue-dark': '#005cb2',
        // Gris
        'custom-gray': '#999999',
        // Noir
        'custom-black': '#000000',
        // Rouge
        'custom-red': '#ff0000',
        // Blanc
        'custom-white': '#ffffff',
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
    require('@tailwindcss/aspect-ratio'),
  ],
}