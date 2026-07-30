"use client";

import {
  PieChart,
  Pie,
    Cell,
  ResponsiveContainer,
  Tooltip,
} from "recharts";

interface PortfolioAllocationProps {
  portfolio: Record<string, number>;
}

const COLORS = [
  "#3B82F6",
  "#8B5CF6",
  "#06B6D4",
  "#10B981",
  "#F59E0B",
  "#EF4444",
  "#EC4899",
  "#6366F1",
];

export default function PortfolioAllocation({
  portfolio,
}: PortfolioAllocationProps) {
  const chartData = Object.entries(portfolio).map(
    ([ticker, weight]) => ({
      name: ticker,
      value: weight,
    })
  );

  const totalWeight = chartData.reduce(
    (sum, item) => sum + item.value,
    0
  );

  return (
    <section className="rounded-3xl border border-slate-800 bg-slate-900/70 p-8 backdrop-blur">
      <div className="mb-8">
        <p className="text-xs uppercase tracking-[0.35em] text-blue-400">
          Allocation
        </p>

        <h2 className="mt-2 text-3xl font-bold text-white">
          Portfolio Allocation
        </h2>
      </div>

      <div className="grid gap-10 lg:grid-cols-2">
        {/* Chart */}

        <div className="h-[360px]">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={chartData}
                dataKey="value"
                nameKey="name"
                innerRadius={75}
                outerRadius={120}
                paddingAngle={3}
              >
                {chartData.map((_, index) => (
                  <Cell
                    key={index}
                    fill={COLORS[index % COLORS.length]}
                  />
                ))}
              </Pie>

              <Tooltip
                formatter={(value: number) => `${value.toFixed(2)}%`}
              />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Legend */}

        <div className="flex flex-col justify-center gap-5">
          {chartData.map((item, index) => (
            <div
              key={item.name}
              className="flex items-center justify-between rounded-xl border border-slate-800 bg-slate-950/40 px-5 py-4 transition hover:border-blue-500"
            >
              <div className="flex items-center gap-4">
                <span
                  className="h-4 w-4 rounded-full"
                  style={{
                    backgroundColor:
                      COLORS[index % COLORS.length],
                  }}
                />

                <div>
                  <p className="font-semibold text-white">
                    {item.name}
                  </p>

                  <p className="text-sm text-slate-400">
                    Equity Position
                  </p>
                </div>
              </div>

              <div className="text-right">
                <p className="text-lg font-bold text-white">
                  {item.value.toFixed(2)}%
                </p>

                <p className="text-xs text-slate-500">
                  {(
                    (item.value / totalWeight) *
                    100
                  ).toFixed(1)}
                  % Allocation
                </p>
              </div>
            </div>
          ))}

          <div className="mt-4 rounded-xl border border-blue-900/50 bg-blue-950/20 p-5">
            <div className="flex items-center justify-between">
              <span className="text-slate-400">
                Holdings
              </span>

              <span className="font-bold text-white">
                {chartData.length}
              </span>
            </div>

            <div className="mt-3 flex items-center justify-between">
              <span className="text-slate-400">
                Total Weight
              </span>

              <span className="font-bold text-green-400">
                {totalWeight.toFixed(2)}%
              </span>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}