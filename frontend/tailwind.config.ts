import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        'cine-dark': '#0e1117',
        'cine-darker': '#090b10',
        'cine-card': '#161b22',
        'cine-border': '#30363d',
        'cine-red': '#FF4B2B',
        'cine-pink': '#FF416C',
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'cine-gradient': 'linear-gradient(135deg, #FF4B2B 0%, #FF416C 100%)',
        'cine-gradient-reverse': 'linear-gradient(135deg, #FF416C 0%, #FF4B2B 100%)',
      },
      boxShadow: {
        'cine-glow': '0 0 40px rgba(255, 75, 43, 0.3)',
        'cine-glow-sm': '0 0 20px rgba(255, 75, 43, 0.2)',
        'card': '0 8px 32px rgba(0, 0, 0, 0.4)',
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'glow': 'glow 2s ease-in-out infinite alternate',
      },
      keyframes: {
        glow: {
          '0%': { boxShadow: '0 0 20px rgba(255, 75, 43, 0.2)' },
          '100%': { boxShadow: '0 0 40px rgba(255, 75, 43, 0.4)' },
        },
      },
    },
  },
  plugins: [],
}
export default config
