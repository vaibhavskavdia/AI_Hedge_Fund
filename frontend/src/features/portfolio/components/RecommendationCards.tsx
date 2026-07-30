"use client";

interface Recommendation {
  ticker: string;
  rating: string;
  conviction: string;
  horizon: string;
  bull_case: string;
  bear_case: string;
  recommendation: string;
}

interface RecommendationCardsProps {
  recommendations: Recommendation[];
}

const ratingColor = (rating: string) => {
  switch (rating.toUpperCase()) {
    case "BUY":
      return "bg-emerald-500/20 text-emerald-400 border border-emerald-500/30";

    case "SELL":
      return "bg-red-500/20 text-red-400 border border-red-500/30";

    default:
      return "bg-yellow-500/20 text-yellow-400 border border-yellow-500/30";
  }
};

export default function RecommendationCards({
  recommendations,
}: RecommendationCardsProps) {
  return (
    <section className="rounded-3xl border border-slate-800 bg-slate-900/70 p-8 backdrop-blur">
      <div className="mb-8">
        <p className="text-xs uppercase tracking-[0.35em] text-blue-400">
          AI Research
        </p>

        <h2 className="mt-2 text-3xl font-bold text-white">
          Stock Recommendations
        </h2>
      </div>

      <div className="space-y-6">
        {recommendations.map((stock) => (
          <div
            key={stock.ticker}
            className="rounded-2xl border border-slate-800 bg-slate-950/40 p-6 transition hover:border-blue-500"
          >
            <div className="flex flex-wrap items-center justify-between gap-4">
              <div>
                <h3 className="text-2xl font-bold text-white">
                  {stock.ticker}
                </h3>

                <p className="mt-2 text-slate-400">
                  Investment Horizon • {stock.horizon}
                </p>
              </div>

              <div className="flex gap-3">
                <span
                  className={`rounded-full px-4 py-2 text-sm font-semibold ${ratingColor(
                    stock.rating
                  )}`}
                >
                  {stock.rating}
                </span>

                <span className="rounded-full border border-blue-500/30 bg-blue-500/15 px-4 py-2 text-sm font-semibold text-blue-400">
                  {stock.conviction}
                </span>
              </div>
            </div>

            <div className="mt-8 grid gap-6 lg:grid-cols-3">
              <div className="rounded-xl border border-emerald-500/20 bg-emerald-500/5 p-5">
                <h4 className="mb-3 font-semibold text-emerald-400">
                  Bull Case
                </h4>

                <p className="text-sm leading-7 text-slate-300">
                  {stock.bull_case}
                </p>
              </div>

              <div className="rounded-xl border border-red-500/20 bg-red-500/5 p-5">
                <h4 className="mb-3 font-semibold text-red-400">
                  Bear Case
                </h4>

                <p className="text-sm leading-7 text-slate-300">
                  {stock.bear_case}
                </p>
              </div>

              <div className="rounded-xl border border-blue-500/20 bg-blue-500/5 p-5">
                <h4 className="mb-3 font-semibold text-blue-400">
                  AI Recommendation
                </h4>

                <p className="text-sm leading-7 text-slate-300">
                  {stock.recommendation}
                </p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}