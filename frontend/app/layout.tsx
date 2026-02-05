import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'CineAI Pro | Film Türü Tahmin Sistemi',
  description: 'Yapay zeka destekli film türü tahmin uygulaması. Film konusunu girin, türünü öğrenin!',
  keywords: ['film', 'movie', 'genre', 'prediction', 'AI', 'machine learning'],
  authors: [{ name: 'CineAI Team' }],
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="tr">
      <body className={inter.className}>
        <div className="noise-overlay" />
        <div className="bg-grid min-h-screen">
          {children}
        </div>
      </body>
    </html>
  )
}
