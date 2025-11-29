import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Social Trend Agent",
  description: "AI-powered real-time analysis of social media trends"
};

export default function RootLayout({
  children
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="page-shell">
        <header className="border-b border-slate-200/70 bg-white/80 backdrop-blur">
          <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex items-center justify-between">
            <div>
              <h1 className="page-title text-2xl sm:text-3xl">Social Trend Agent</h1>
              <p className="page-subtitle text-xs sm:text-sm">
                AI-Powered Real-Time Analysis of Social Media Trends
              </p>
            </div>
          </div>
        </header>
        <main className="page-main">{children}</main>
        <footer className="border-t border-slate-200/70 bg-white/80 py-3">
          <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 text-center text-xs text-slate-500">
            Social media analytics dashboard
          </div>
        </footer>
      </body>
    </html>
  );
}


