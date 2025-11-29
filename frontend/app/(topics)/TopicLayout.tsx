"use client";

export function TopicLayout({ children }: { children: React.ReactNode }) {
  // Layout responsibilities have moved into DashboardShell; this wrapper is now a no-op.
  return <>{children}</>;
}


