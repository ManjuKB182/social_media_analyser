"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const topics = [
  { slug: "", label: "Overview", href: "/" },
  { slug: "travel", label: "Travel", href: "/travel" },
  { slug: "politics", label: "Politics", href: "/politics" },
  { slug: "sports", label: "Sports", href: "/sports" },
  { slug: "cinema", label: "Cinema", href: "/cinema" }
];

export default function HomePage() {
  const pathname = usePathname() || "/";

  return (
    <>
      <section className="page-header">
        <p className="page-subtitle">
          Choose a topic to explore live & mock social media trends across India.
        </p>
      </section>

      <nav className="card px-3 py-2 flex flex-wrap gap-2 items-center justify-between">
        <div className="flex flex-wrap gap-2">
          {topics.map((topic) => {
            const active =
              (topic.href === "/" && pathname === "/") || pathname === topic.href;
            return (
              <Link
                key={topic.href}
                href={topic.href}
                className={`tab-pill ${active ? "tab-pill-active" : ""}`}
              >
                {topic.label}
              </Link>
            );
          })}
        </div>
      </nav>

      <section className="grid gap-4 sm:grid-cols-2">
        <article className="card p-5 space-y-3">
          <h2 className="text-lg font-semibold text-slate-900">
            What is Social Trend Agent?
          </h2>
          <p className="text-sm text-slate-600 leading-relaxed">
            A modern web dashboard that mirrors your existing Streamlit app for analysing
            travel, politics, sports, and cinema trends using live or mock Twitter data.
            It will call a Python API for heavy analytics and LLM-powered insights, and
            later plug into MongoDB for persistence.
          </p>
        </article>

        <article className="card p-5 space-y-3">
          <h2 className="text-lg font-semibold text-slate-900">
            How migration works
          </h2>
          <p className="text-sm text-slate-600 leading-relaxed">
            This Next.js frontend uses the same underlying Python data pipelines and AI
            agent as the original Streamlit app, but exposes them via JSON APIs. That
            means you can deploy a fast, React-based experience today and later swap in a
            MongoDB-backed backend without breaking the UI.
          </p>
        </article>
      </section>
    </>
  );
}


