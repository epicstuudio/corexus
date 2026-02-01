export default async () => ({
  plugins: [
    (await import('tailwindcss')).default,
    (await import('autoprefixer')).default,
  ],
})
