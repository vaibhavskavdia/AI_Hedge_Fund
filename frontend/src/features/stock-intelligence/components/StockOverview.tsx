import {
  TrendingUp,
  Shield,
  Building2,
  Target,
} from "lucide-react";

interface Props {
  stock: {
    ticker: string;
    sector: string;
    prediction_score: number;
    expected_return_5d: number;
    risk_score: number;
    risk_level: string;
    recommendation: string;
  };
}

export default function StockOverview({
  stock,
}: Props) {
  return (
    <section className="space-y-8">

      {/* Hero */}

      <div className="rounded-3xl border border-slate-800 bg-[#0F172A] p-8">

        <p className="text-xs uppercase tracking-[0.35em] text-blue-400">
          Company Intelligence
        </p>

        <div className="mt-5 flex items-center justify-between">

          <div>

            <h1 className="text-6xl font-bold text-white">
              {stock.ticker}
            </h1>

            <p className="mt-3 text-xl text-slate-400">
              {stock.sector}
            </p>

          </div>

          <div
            className={`rounded-full px-6 py-3 text-lg font-semibold ${
              stock.recommendation === "BUY"
                ? "bg-green-500/20 text-green-400"
                : stock.recommendation === "SELL"
                ? "bg-red-500/20 text-red-400"
                : "bg-yellow-500/20 text-yellow-400"
            }`}
          >
            {stock.recommendation}
          </div>

        </div>

      </div>

      {/* Metrics */}

      <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-4">

        <MetricCard
          icon={<Target />}
          title="Prediction Score"
          value={`${(
            stock.prediction_score * 100
          ).toFixed(1)}%`}
          color="text-blue-400"
        />

        <MetricCard
          icon={<TrendingUp />}
          title="Expected Return"
          value={`${stock.expected_return_5d}%`}
          color="text-green-400"
        />

        <MetricCard
          icon={<Shield />}
          title="Risk Score"
          value={stock.risk_score.toString()}
          color="text-red-400"
        />

        <MetricCard
          icon={<Building2 />}
          title="Risk Level"
          value={stock.risk_level}
          color="text-orange-400"
        />

      </div>

    </section>
  );
}

interface MetricProps {
  icon: React.ReactNode;
  title: string;
  value: string;
  color: string;
}

function MetricCard({
  icon,
  title,
  value,
  color,
}: MetricProps) {
  return (
    <div className="rounded-2xl border border-slate-800 bg-[#0F172A] p-6">

      <div className={`${color} mb-5`}>
        {icon}
      </div>

      <p className="text-sm text-slate-400">
        {title}
      </p>

      <h3 className={`mt-3 text-3xl font-bold ${color}`}>
        {value}
      </h3>

    </div>
  );
}