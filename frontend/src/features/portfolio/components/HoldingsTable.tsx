"use client";

interface Recommendation {
  ticker: string;
  rating: string;
  conviction: string;
  position_size: number;
  horizon: string;
}

interface HoldingsTableProps {
  portfolio: Record<string, number>;
  recommendations: Recommendation[];
}

const badgeColor = (rating: string) => {
  switch (rating.toUpperCase()) {
    case "BUY":
      return "bg-emerald-500/15 text-emerald-400 border border-emerald-500/30";

    case "SELL":
      return "bg-red-500/15 text-red-400 border border-red-500/30";

    default:
      return "bg-yellow-500/15 text-yellow-400 border border-yellow-500/30";
  }
};

const convictionColor = (conviction: string) => {
  switch (conviction.toUpperCase()) {
    case "HIGH":
      return "text-emerald-400";

    case "MEDIUM":
      return "text-yellow-400";

    default:
      return "text-slate-400";
  }
};

export default function HoldingsTable({
  portfolio,
  recommendations,
}: HoldingsTableProps) {
  return (
    <section className="rounded-3xl border border-slate-800 bg-slate-900/70 p-8 backdrop-blur">
      <div className="mb-8">
        <p className="text-xs uppercase tracking-[0.35em] text-blue-400">
          Holdings
        </p>

        <h2 className="mt-2 text-3xl font-bold text-white">
          Portfolio Positions
        </h2>
      </div>

      <div className="overflow-hidden rounded-2xl border border-slate-800">
        <table className="w-full">
          <thead className="bg-slate-950/60">
            <tr className="text-left text-sm uppercase tracking-wider text-slate-400">
              <th className="px-6 py-4">Ticker</th>
              <th className="px-6 py-4">Weight</th>
              <th className="px-6 py-4">Rating</th>
              <th className="px-6 py-4">Conviction</th>
              <th className="px-6 py-4">Horizon</th>
            </tr>
          </thead>

          <tbody>
            {recommendations.map((stock) => (
              <tr
                key={stock.ticker}
                className="border-t border-slate-800 transition hover:bg-slate-800/40"
              >
                <td className="px-6 py-5 font-semibold text-white">
                  {stock.ticker}
                </td>

                <td className="px-6 py-5 text-slate-300">
                  {portfolio[stock.ticker] ?? 0}%
                </td>

                <td className="px-6 py-5">
                  <span
                    className={`rounded-full px-3 py-1 text-xs font-semibold ${badgeColor(
                      stock.rating
                    )}`}
                  >
                    {stock.rating}
                  </span>
                </td>

                <td
                  className={`px-6 py-5 font-semibold ${convictionColor(
                    stock.conviction
                  )}`}
                >
                  {stock.conviction}
                </td>

                <td className="px-6 py-5 text-slate-400">
                  {stock.horizon}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}