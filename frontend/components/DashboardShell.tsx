"use client";

import { useEffect, useMemo, useState } from "react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis
} from "recharts";
import { useRouter } from "next/navigation";
import { getDashboard } from "../lib/api";
import type {
  DashboardFilters,
  DashboardResponse,
  TopicKey
} from "../lib/types";

const DEFAULT_FILTERS = (topic: TopicKey): DashboardFilters => {
  const today = new Date();
  const iso = today.toISOString().slice(0, 10);
  return {
    topic,
    fromDate: iso,
    toDate: iso,
    startHour: 0,
    endHour: 23,
    mode: "historical"
  };
};

interface Props<T extends TopicKey> {
  topic: T;
  title: string;
  subtitle: string;
}

export function DashboardShell<T extends TopicKey>({
  topic,
  title,
  subtitle
}: Props<T>) {
  const router = useRouter();
  const [filters, setFilters] = useState<DashboardFilters>(() =>
    DEFAULT_FILTERS(topic)
  );
  const [draftFilters, setDraftFilters] = useState<DashboardFilters>(() =>
    DEFAULT_FILTERS(topic)
  );
  const [data, setData] = useState<DashboardResponse<T> | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setError(null);
    getDashboard({ ...(filters as any), topic })
      .then((res) => {
        if (!cancelled) {
          setData(res);
        }
      })
      .catch((err) => {
        if (!cancelled) {
          setError(err.message ?? "Failed to load dashboard data.");
        }
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });

    return () => {
      cancelled = true;
    };
  }, [topic, filters]);

  const handleApplyFilters = () => {
    setFilters(draftFilters);
  };

  const topStats = useMemo(() => {
    if (!data) return null;
    const rows: any[] = data.rows as any[];

    const rowsIndia = rows.filter((r) => r.State !== "Karnataka");
    const rowsKarnataka = rows.filter((r) => r.State === "Karnataka");

    const sumByKey = (rowsForKey: any[], key: string) => {
      const m = new Map<string, number>();
      for (const r of rowsForKey) {
        const k = r[key];
        if (!k || k === "Other" || k === "Unknown") continue;
        const engagement = typeof r.Engagement === "number" ? r.Engagement : 0;
        m.set(k, (m.get(k) ?? 0) + engagement);
      }
      const arr = [...m.entries()].sort((a, b) => b[1] - a[1]);
      return arr.map(([name, value]) => ({ name, value }));
    };

    const indiaStates = sumByKey(rowsIndia, "State").slice(0, 7);
    const indiaLocations = sumByKey(rowsIndia, "Location").slice(0, 10);

    if (topic === "travel") {
      // Travel-specific dashboards
      const allowedCategories = new Set([
        "Hill",
        "Mountains",
        "Beach",
        "Trekking",
        "Religious"
      ]);
      const travelRowsIndia = rowsIndia.map((r) => {
        const cat = r.Category;
        if (cat && allowedCategories.has(cat)) return r;
        return { ...r, Category: "Other" };
      });
      const travelCategories = sumByKey(travelRowsIndia, "Category");
      const karnatakaCities = sumByKey(rowsKarnataka, "Location").slice(0, 10);

      return {
        mode: "travel" as const,
        indiaStates,
        indiaLocations,
        travelCategories,
        karnatakaCities
      };
    }

    if (topic === "politics") {
      const indiaPoliticians = sumByKey(rowsIndia, "Politician").slice(0, 6);
      const karnatakaPoliticians = sumByKey(
        rowsKarnataka,
        "Politician"
      ).slice(0, 6);

      return {
        mode: "politics" as const,
        indiaStates,
        indiaLocations,
        indiaPoliticians,
        karnatakaPoliticians
      };
    }

    if (topic === "sports") {
      const indiaSports = sumByKey(rowsIndia, "Sport").slice(0, 6);
      const indiaStateSports = sumByKey(rowsIndia, "State").slice(0, 8);
      const indiaSportsPersons = sumByKey(
        rowsIndia,
        "SportsPerson"
      ).slice(0, 6);
      const karnatakaSports = sumByKey(rowsKarnataka, "Sport").slice(0, 6);

      return {
        mode: "sports" as const,
        indiaSports,
        indiaStateSports,
        indiaSportsPersons,
        karnatakaSports,
      };
    }

    // Default dashboards for cinema – keep previous behaviour
    let indiaDimKey: string;
    let indiaDimLabel: string;
    indiaDimKey = "Industry";
    indiaDimLabel = "Cinema Industries (India)";
    const indiaDim = sumByKey(rowsIndia, indiaDimKey).slice(0, 7);

    const hourMap = new Map<number, number>();
    for (const r of rowsKarnataka) {
      const hour = typeof r.Hour === "number" ? r.Hour : 0;
      const engagement = typeof r.Engagement === "number" ? r.Engagement : 0;
      hourMap.set(hour, (hourMap.get(hour) ?? 0) + engagement);
    }
    const karnatakaHourly = [...hourMap.entries()]
      .sort((a, b) => a[0] - b[0])
      .map(([hour, value]) => ({ hour, value }));

    return {
      mode: "default" as const,
      indiaStates,
      indiaLocations,
      indiaDim,
      indiaDimLabel,
      karnatakaHourly
    };
  }, [data, topic]);

  return (
    <section className="grid gap-4 lg:grid-cols-[260px,1fr] items-start">
      <aside className="card p-5 space-y-4">
        <div>
          <h3 className="text-sm font-semibold text-slate-900">Categories</h3>
          <div className="mt-2 flex flex-col gap-2 text-xs">
            {[
              { key: "travel", label: "Travel", href: "/travel" },
              { key: "politics", label: "Politics", href: "/politics" },
              { key: "sports", label: "Sports", href: "/sports" },
              { key: "cinema", label: "Cinema", href: "/cinema" }
            ].map((opt) => {
              const active = opt.key === topic;
              return (
                <button
                  key={opt.key}
                  type="button"
                  onClick={() => router.push(opt.href)}
                  className={`flex items-center justify-between rounded-lg border px-3 py-1.5 text-left transition-colors ${
                    active
                      ? "border-tealPrimary/70 bg-tealPrimary/5 text-tealPrimary font-semibold"
                      : "border-slate-200 hover:border-tealPrimary/40 hover:bg-slate-50"
                  }`}
                >
                  <span>{opt.label}</span>
                </button>
              );
            })}
          </div>
        </div>

        <div>
          <h3 className="text-sm font-semibold text-slate-900">Filters</h3>
          <form
            className="mt-2 space-y-3 text-xs text-slate-600"
            onSubmit={(e) => {
              e.preventDefault();
              handleApplyFilters();
            }}
          >
            <div className="grid grid-cols-2 gap-2">
              <label className="flex flex-col gap-1">
                <span className="font-semibold">From date</span>
                <input
                  type="date"
                  className="rounded-md border border-slate-200 px-2 py-1 text-xs"
                  value={draftFilters.fromDate}
                  onChange={(e) =>
                    setDraftFilters((prev) => ({
                      ...prev,
                      fromDate: e.target.value
                    }))
                  }
                />
              </label>
              <label className="flex flex-col gap-1">
                <span className="font-semibold">To date</span>
                <input
                  type="date"
                  className="rounded-md border border-slate-200 px-2 py-1 text-xs"
                  value={draftFilters.toDate}
                  onChange={(e) =>
                    setDraftFilters((prev) => ({
                      ...prev,
                      toDate: e.target.value
                    }))
                  }
                />
              </label>
            </div>

            <div className="grid grid-cols-2 gap-2">
              <label className="flex flex-col gap-1">
                <span className="font-semibold">Start hour</span>
                <input
                  type="number"
                  min={0}
                  max={23}
                  className="rounded-md border border-slate-200 px-2 py-1 text-xs"
                  value={draftFilters.startHour}
                  onChange={(e) =>
                    setDraftFilters((prev) => ({
                      ...prev,
                      startHour: Number(e.target.value)
                    }))
                  }
                />
              </label>
              <label className="flex flex-col gap-1">
                <span className="font-semibold">End hour</span>
                <input
                  type="number"
                  min={0}
                  max={23}
                  className="rounded-md border border-slate-200 px-2 py-1 text-xs"
                  value={draftFilters.endHour}
                  onChange={(e) =>
                    setDraftFilters((prev) => ({
                      ...prev,
                      endHour: Number(e.target.value)
                    }))
                  }
                />
              </label>
            </div>

            <div className="flex flex-col gap-1">
              <span className="font-semibold">Mode</span>
              <select
                className="rounded-md border border-slate-200 px-2 py-1 text-xs"
                value={draftFilters.mode ?? "historical"}
                onChange={(e) =>
                  setDraftFilters((prev) => ({
                    ...prev,
                    mode: e.target.value as DashboardFilters["mode"]
                  }))
                }
              >
                <option value="historical">Historical window</option>
                <option value="realtime">Realtime (last hour)</option>
              </select>
            </div>

            <button
              type="submit"
              className="mt-1 inline-flex w-full items-center justify-center rounded-lg bg-gradient-to-r from-tealPrimary to-warmAccent px-3 py-1.5 text-xs font-semibold text-white shadow-md hover:from-tealPrimary hover:to-warmAccent/80"
            >
              Apply filters
            </button>
          </form>
        </div>
      </aside>

      <article className="card p-5 space-y-3">
        <h2 className="text-xl font-semibold text-slate-900">{title}</h2>
        <p className="text-sm text-slate-600">{subtitle}</p>

        {loading && (
          <p className="text-xs text-slate-500 animate-pulse">
            Loading dashboard data from Python API…
          </p>
        )}
        {error && (
          <p className="text-xs text-red-600">
            {error} – check that the FastAPI server is running on
            <code className="ml-1 px-1 rounded bg-slate-100 text-[10px]">
              {process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000"}
            </code>
          </p>
        )}

        {data && !loading && !error && (
          <div className="mt-3 space-y-4">
            <div className="grid gap-3 sm:grid-cols-2">
              <div className="card p-3 space-y-1">
                <div className="text-xs uppercase tracking-wide text-slate-500">
                  Total records
                </div>
                <div className="text-2xl font-semibold text-tealPrimary">
                  {data.rows.length.toLocaleString()}
                </div>
                <p className="text-[11px] text-slate-500">
                  {data.summary.metricsHealth?.total_records ?? "–"}
                </p>
              </div>
              <div className="card p-3 space-y-1">
                <div className="text-xs uppercase tracking-wide text-slate-500">
                  Time range
                </div>
                <div className="text-sm font-semibold text-slate-900">
                  {filters.startHour}:00 – {filters.endHour}:00
                </div>
                <p className="text-[11px] text-slate-500">
                  {data.summary.metricsHealth?.timerange ?? "–"}
                </p>
              </div>
            </div>

            {topStats && (
              <div className="grid gap-3 lg:grid-cols-2">
                {/* DB1 – India overview */}
                <div className="card p-4 space-y-2">
                  <h3 className="text-sm font-semibold text-slate-900">
                    {topic === "sports"
                      ? "India – Sports vs Engagement"
                      : "India – State Trends"}
                  </h3>
                  <div className="h-56">
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart
                        data={
                          topic === "sports"
                            ? topStats.indiaSports
                            : topStats.indiaStates
                        }
                        margin={{ top: 10, right: 10, left: 0, bottom: 30 }}
                      >
                        <CartesianGrid strokeDasharray="3 3" vertical={false} />
                        <XAxis
                          dataKey="name"
                          tick={{ fontSize: 10 }}
                          interval={0}
                          angle={-30}
                          textAnchor="end"
                        />
                        <YAxis tick={{ fontSize: 10 }} />
                        <Tooltip
                          formatter={(value: number) =>
                            value.toLocaleString()
                          }
                        />
                        <Bar
                          dataKey="value"
                          fill="#00B7C2"
                          radius={[4, 4, 0, 0]}
                        />
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                </div>

                {/* DB2 – India secondary view */}
                <div className="card p-4 space-y-2">
                  <h3 className="text-sm font-semibold text-slate-900">
                    {topic === "sports"
                      ? "India – States vs Engagement (Sports)"
                      : "India – Top Cities"}
                  </h3>
                  <div className="h-56">
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart
                        data={
                          topic === "sports"
                            ? topStats.indiaStateSports
                            : topStats.indiaLocations
                        }
                        margin={{ top: 10, right: 10, left: 0, bottom: 40 }}
                      >
                        <CartesianGrid strokeDasharray="3 3" vertical={false} />
                        <XAxis
                          dataKey="name"
                          tick={{ fontSize: 9 }}
                          interval={0}
                          angle={-45}
                          textAnchor="end"
                        />
                        <YAxis tick={{ fontSize: 10 }} />
                        <Tooltip
                          formatter={(value: number) =>
                            value.toLocaleString()
                          }
                        />
                        <Bar
                          dataKey="value"
                          fill="#FFB15E"
                          radius={[4, 4, 0, 0]}
                        />
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                </div>

                {/* Topic-specific DB3 & DB4 */}
                {topic === "travel" && (
                  <>
                    {/* DB3 – India travel categories */}
                    <div className="card p-4 space-y-2">
                      <h3 className="text-sm font-semibold text-slate-900">
                        India – Travel / Holiday Preference Types
                      </h3>
                      <div className="h-56">
                        <ResponsiveContainer width="100%" height="100%">
                          <BarChart
                            data={topStats.travelCategories}
                            margin={{
                              top: 10,
                              right: 10,
                              left: 0,
                              bottom: 30
                            }}
                          >
                            <CartesianGrid
                              strokeDasharray="3 3"
                              vertical={false}
                            />
                            <XAxis
                              dataKey="name"
                              tick={{ fontSize: 10 }}
                              interval={0}
                              angle={-30}
                              textAnchor="end"
                            />
                            <YAxis tick={{ fontSize: 10 }} />
                            <Tooltip
                              formatter={(value: number) =>
                                value.toLocaleString()
                              }
                            />
                            <Bar
                              dataKey="value"
                              fill="#6366F1"
                              radius={[4, 4, 0, 0]}
                            />
                          </BarChart>
                        </ResponsiveContainer>
                      </div>
                    </div>

                    {/* DB4 – Karnataka top cities for travel */}
                    <div className="card p-4 space-y-2">
                      <h3 className="text-sm font-semibold text-slate-900">
                        Karnataka – Top Cities (Travel &amp; Holiday)
                      </h3>
                      <div className="h-56">
                        {topStats.karnatakaCities.length === 0 ? (
                          <p className="text-xs text-slate-500">
                            No Karnataka travel data available for the selected
                            filters.
                          </p>
                        ) : (
                          <ResponsiveContainer width="100%" height="100%">
                            <BarChart
                              data={topStats.karnatakaCities}
                              margin={{
                                top: 10,
                                right: 10,
                                left: 0,
                                bottom: 40
                              }}
                            >
                              <CartesianGrid
                                strokeDasharray="3 3"
                                vertical={false}
                              />
                              <XAxis
                                dataKey="name"
                                tick={{ fontSize: 9 }}
                                interval={0}
                                angle={-45}
                                textAnchor="end"
                              />
                              <YAxis tick={{ fontSize: 10 }} />
                              <Tooltip
                                formatter={(value: number) =>
                                  value.toLocaleString()
                                }
                              />
                              <Bar
                                dataKey="value"
                                fill="#22C55E"
                                radius={[4, 4, 0, 0]}
                              />
                            </BarChart>
                          </ResponsiveContainer>
                        )}
                      </div>
                    </div>
                  </>
                )}

                {topic === "politics" && (
                  <>
                    {/* DB3 – India politicians vs engagement */}
                    <div className="card p-4 space-y-2">
                      <h3 className="text-sm font-semibold text-slate-900">
                        India – Politicians vs Engagement
                      </h3>
                      <div className="h-56">
                        <ResponsiveContainer width="100%" height="100%">
                          <BarChart
                            data={topStats.indiaPoliticians}
                            margin={{
                              top: 10,
                              right: 10,
                              left: 0,
                              bottom: 40
                            }}
                          >
                            <CartesianGrid
                              strokeDasharray="3 3"
                              vertical={false}
                            />
                            <XAxis
                              dataKey="name"
                              tick={{ fontSize: 9 }}
                              interval={0}
                              angle={-30}
                              textAnchor="end"
                            />
                            <YAxis tick={{ fontSize: 10 }} />
                            <Tooltip
                              formatter={(value: number) =>
                                value.toLocaleString()
                              }
                            />
                            <Bar
                              dataKey="value"
                              fill="#6366F1"
                              radius={[4, 4, 0, 0]}
                            />
                          </BarChart>
                        </ResponsiveContainer>
                      </div>
                    </div>

                    {/* DB4 – Karnataka top politicians */}
                    <div className="card p-4 space-y-2">
                      <h3 className="text-sm font-semibold text-slate-900">
                        Karnataka – Top Politicians by Engagement
                      </h3>
                      <div className="h-56">
                        {topStats.karnatakaPoliticians.length === 0 ? (
                          <p className="text-xs text-slate-500">
                            No Karnataka political data available for the
                            selected filters.
                          </p>
                        ) : (
                          <ResponsiveContainer width="100%" height="100%">
                            <BarChart
                              data={topStats.karnatakaPoliticians}
                              margin={{
                                top: 10,
                                right: 10,
                                left: 0,
                                bottom: 40
                              }}
                            >
                              <CartesianGrid
                                strokeDasharray="3 3"
                                vertical={false}
                              />
                              <XAxis
                                dataKey="name"
                                tick={{ fontSize: 9 }}
                                interval={0}
                                angle={-30}
                                textAnchor="end"
                              />
                              <YAxis tick={{ fontSize: 10 }} />
                              <Tooltip
                                formatter={(value: number) =>
                                  value.toLocaleString()
                                }
                              />
                              <Bar
                                dataKey="value"
                                fill="#22C55E"
                                radius={[4, 4, 0, 0]}
                              />
                            </BarChart>
                          </ResponsiveContainer>
                        )}
                      </div>
                    </div>
                  </>
                )}

                {topic === "sports" && (
                  <>
                    {/* DB3 – India sports persons vs engagement */}
                    <div className="card p-4 space-y-2">
                      <h3 className="text-sm font-semibold text-slate-900">
                        India – Sports Persons vs Engagement
                      </h3>
                      <div className="h-56">
                        <ResponsiveContainer width="100%" height="100%">
                          <BarChart
                            data={topStats.indiaSportsPersons}
                            margin={{
                              top: 10,
                              right: 10,
                              left: 0,
                              bottom: 40,
                            }}
                          >
                            <CartesianGrid
                              strokeDasharray="3 3"
                              vertical={false}
                            />
                            <XAxis
                              dataKey="name"
                              tick={{ fontSize: 9 }}
                              interval={0}
                              angle={-30}
                              textAnchor="end"
                            />
                            <YAxis tick={{ fontSize: 10 }} />
                            <Tooltip
                              formatter={(value: number) =>
                                value.toLocaleString()
                              }
                            />
                            <Bar
                              dataKey="value"
                              fill="#6366F1"
                              radius={[4, 4, 0, 0]}
                            />
                          </BarChart>
                        </ResponsiveContainer>
                      </div>
                    </div>

                    {/* DB4 – Karnataka sports vs engagement */}
                    <div className="card p-4 space-y-2">
                      <h3 className="text-sm font-semibold text-slate-900">
                        Karnataka – Sports vs Engagement
                      </h3>
                      <div className="h-56">
                        {topStats.karnatakaSports.length === 0 ? (
                          <p className="text-xs text-slate-500">
                            No Karnataka sports data available for the selected
                            filters.
                          </p>
                        ) : (
                          <ResponsiveContainer width="100%" height="100%">
                            <BarChart
                              data={topStats.karnatakaSports}
                              margin={{
                                top: 10,
                                right: 10,
                                left: 0,
                                bottom: 40,
                              }}
                            >
                              <CartesianGrid
                                strokeDasharray="3 3"
                                vertical={false}
                              />
                              <XAxis
                                dataKey="name"
                                tick={{ fontSize: 9 }}
                                interval={0}
                                angle={-30}
                                textAnchor="end"
                              />
                              <YAxis tick={{ fontSize: 10 }} />
                              <Tooltip
                                formatter={(value: number) =>
                                  value.toLocaleString()
                                }
                              />
                              <Bar
                                dataKey="value"
                                fill="#22C55E"
                                radius={[4, 4, 0, 0]}
                              />
                            </BarChart>
                          </ResponsiveContainer>
                        )}
                      </div>
                    </div>
                  </>
                )}

                {topic !== "travel" && topic !== "politics" && topic !== "sports" && (
                  <>
                    <div className="card p-4 space-y-2">
                      <h3 className="text-sm font-semibold text-slate-900">
                        India – {topStats.indiaDimLabel}
                      </h3>
                      <div className="h-56">
                        <ResponsiveContainer width="100%" height="100%">
                          <BarChart
                            data={topStats.indiaDim}
                            margin={{
                              top: 10,
                              right: 10,
                              left: 0,
                              bottom: 40
                            }}
                          >
                            <CartesianGrid
                              strokeDasharray="3 3"
                              vertical={false}
                            />
                            <XAxis
                              dataKey="name"
                              tick={{ fontSize: 9 }}
                              interval={0}
                              angle={-30}
                              textAnchor="end"
                            />
                            <YAxis tick={{ fontSize: 10 }} />
                            <Tooltip
                              formatter={(value: number) =>
                                value.toLocaleString()
                              }
                            />
                            <Bar
                              dataKey="value"
                              fill="#6366F1"
                              radius={[4, 4, 0, 0]}
                            />
                          </BarChart>
                        </ResponsiveContainer>
                      </div>
                    </div>

                    <div className="card p-4 space-y-2">
                      <h3 className="text-sm font-semibold text-slate-900">
                        Karnataka – Hourly Engagement
                      </h3>
                      <div className="h-56">
                        {topStats.karnatakaHourly.length === 0 ? (
                          <p className="text-xs text-slate-500">
                            No Karnataka data available for the selected
                            filters.
                          </p>
                        ) : (
                          <ResponsiveContainer width="100%" height="100%">
                            <LineChart
                              data={topStats.karnatakaHourly}
                              margin={{
                                top: 10,
                                right: 10,
                                left: 0,
                                bottom: 20
                              }}
                            >
                              <CartesianGrid
                                strokeDasharray="3 3"
                                vertical={false}
                              />
                              <XAxis
                                dataKey="hour"
                                tick={{ fontSize: 10 }}
                                tickFormatter={(v: number) => `${v}:00`}
                              />
                              <YAxis tick={{ fontSize: 10 }} />
                              <Tooltip
                                formatter={(value: number) =>
                                  value.toLocaleString()
                                }
                                labelFormatter={(label: number) =>
                                  `Hour ${label}:00`
                                }
                              />
                              <Line
                                type="monotone"
                                dataKey="value"
                                stroke="#22C55E"
                                strokeWidth={2}
                                dot={false}
                                activeDot={{ r: 4 }}
                              />
                            </LineChart>
                          </ResponsiveContainer>
                        )}
                      </div>
                    </div>
                  </>
                )}
              </div>
            )}
          </div>
        )}
      </article>
    </section>
  );
}


