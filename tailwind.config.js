/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter var', 'sans-serif'],
      },
      colors: {
        primary: {
          DEFAULT: '#3B82F6',
          hover: '#2563EB',
        },
        success: {
          DEFAULT: '#059669',
          hover: '#047857',
        },
        error: {
          DEFAULT: '#DC2626',
          hover: '#B91C1C',
        },
      },
    },
  },
  plugins: [],
};