/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        'urgent-important': '#dc2626', // red-600
        'urgent-not-important': '#ea580c', // orange-600
        'not-urgent-important': '#ca8a04', // yellow-600
        'not-urgent-not-important': '#64748b', // slate-500
      },
    },
  },
  plugins: [],
}