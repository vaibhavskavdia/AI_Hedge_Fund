import {
  Newspaper,
  TrendingUp,
  TrendingDown,
  Minus,
} from "lucide-react";

interface Props {
  sentiment: {
    avg_sentiment_score: number;
    positive_count: number;
    neutral_count: number;
    negative_count: number;
  };
}

export default function NewsSentiment({
  sentiment,
}: Props) {
  const total =
    sentiment.positive_count +
    sentiment.neutral_count +
    sentiment.negative_count;

  const positive =
    total === 0
      ? 0
      : (sentiment.positive_count / total) * 100;

  const neutral =
    total === 0
      ? 0
      : (sentiment.neutral_count / total) * 100;

  const negative =
    total === 0
      ? 0
      : (sentiment.negative_count / total) * 100;

  return (
    <section className="rounded-3xl border border-slate-800 bg-[#0F172A] p-8">

      <div className="mb-8">

        <p className="text-xs uppercase tracking-[0.35em] text-blue-400">
          News Intelligence
        </p>

        <h2 className="mt-2 text-4xl font-bold text-white">
          Market Sentiment
        </h2>

      </div>

      {/* Overall Score */}

      <div className="rounded-2xl border border-slate-800 bg-slate-950/40 p-6">

        <div className="flex items-center gap-3">

          <Newspaper
            className="text-blue-400"
            size={22}
          />

          <p className="text-lg text-slate-300">
            Average Sentiment Score
          </p>

        </div>

        <h3 className="mt-6 text-6xl font-bold text-white">
          {sentiment.avg_sentiment_score.toFixed(2)}
        </h3>

      </div>

      {/* Distribution */}

      <div className="mt-8">

        <div className="mb-4 flex justify-between text-sm text-slate-400">
          <span>News Distribution</span>
          <span>{total} Articles</span>
        </div>

        <div className="flex h-5 overflow-hidden rounded-full">

          <div
            className="bg-green-500"
            style={{
              width: `${positive}%`,
            }}
          />

          <div
            className="bg-yellow-500"
            style={{
              width: `${neutral}%`,
            }}
          />

          <div
            className="bg-red-500"
            style={{
              width: `${negative}%`,
            }}
          />

        </div>

      </div>

      {/* Breakdown */}

      <div className="mt-10 grid gap-6 md:grid-cols-3">

        <StatCard
          icon={<TrendingUp />}
          title="Positive"
          value={sentiment.positive_count}
          color="text-green-400"
        />

        <StatCard
          icon={<Minus />}
          title="Neutral"
          value={sentiment.neutral_count}
          color="text-yellow-400"
        />

        <StatCard
          icon={<TrendingDown />}
          title="Negative"
          value={sentiment.negative_count}
          color="text-red-400"
        />

      </div>

    </section>
  );
}

interface StatProps {
  icon: React.ReactNode;
  title: string;
  value: number;
  color: string;
}

function StatCard({
  icon,
  title,
  value,
  color,
}: StatProps) {
  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-950/40 p-6">

      <div className={`mb-4 ${color}`}>
        {icon}
      </div>

      <p className="text-sm text-slate-400">
        {title}
      </p>

      <h3 className={`mt-3 text-4xl font-bold ${color}`}>
        {value}
      </h3>

    </div>
  );
}