import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx}",
    "./components/**/*.{js,ts,jsx,tsx}"
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"]
      },
      colors: {
        tealPrimary: "#00B7C2",
        navyDeep: "#06324F",
        warmAccent: "#FFB15E",
        softBg: "#F5FBFF"
      },
      boxShadow: {
        "card-soft": "0 18px 45px -20px rgba(6,50,79,0.45)"
      }
    }
  },
  plugins: []
};

export default config;


