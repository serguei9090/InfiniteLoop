/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          light: '#60a5fa', // Light Blue (Tailwind blue-400)
          DEFAULT: '#3b82f6', // Core Blue (Tailwind blue-500)
          dark: '#1e3a8a', // Cobalt/Navy (Tailwind blue-900)
        },
        accent: {
          DEFAULT: '#2563eb', // Cobalt Blue (Tailwind blue-600)
          dark: '#1d4ed8', // Dark Cobalt
        },
        surface: {
          50: '#f8fafc',
          100: '#f1f5f9',
          200: '#e2e8f0',
          300: '#cbd5e1',
          800: '#1e293b',
          900: '#0f172a',
        }
      },
      fontFamily: {
        sans: ['"Plus Jakarta Sans"', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'monospace'],
      }
    },
  },
  plugins: [],
}
