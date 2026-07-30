import {
  Brain,
  TrendingUp,
  AlertTriangle,
  Sparkles,
} from "lucide-react";

interface PortfolioIntelligenceData {
  overall_assessment: string;
  strengths: string[];
  weaknesses: string[];
  suggested_actions: string[];
  market_outlook: string;
}

interface Props {
  intelligence: PortfolioIntelligenceData;
}

export default function PortfolioIntelligence({
  intelligence,
}: Props) {
  return (
    <section className="rounded-3xl border border-slate-800 bg-slate-900/70 p-8 backdrop-blur">

      <div className="mb-8">
        <p className="text-xs uppercase tracking-[0.35em] text-blue-400">
          AI Intelligence
        </p>

        <h2 className="mt-2 text-3xl font-bold text-white">
          Portfolio Intelligence
        </h2>
      </div>

      {/* Overall Assessment */}

      <div className="rounded-2xl border border-blue-500/20 bg-blue-950/10 p-6">

        <div className="mb-5 flex items-center gap-3">
          <Brain
            size={22}
            className="text-blue-400"
          />

          <h3 className="text-xl font-semibold text-white">
            Overall Assessment
          </h3>
        </div>

        <p className="leading-8 text-slate-300">
          {intelligence.overall_assessment}
        </p>

      </div>

      <div className="mt-8 grid gap-6 lg:grid-cols-2">

        {/* Strengths */}

        <div className="rounded-2xl border border-emerald-500/20 bg-emerald-500/5 p-6">

          <div className="mb-5 flex items-center gap-3">
            <TrendingUp
              size={20}
              className="text-emerald-400"
            />

            <h3 className="text-lg font-semibold text-white">
              Strengths
            </h3>

          </div>

          <ul className="space-y-4">

            {intelligence.strengths.map((item) => (
              <li
                key={item}
                className="flex gap-3 text-slate-300"
              >
                <span className="mt-2 h-2 w-2 rounded-full bg-emerald-400" />

                <span>{item}</span>
              </li>
            ))}

          </ul>

        </div>

        {/* Weaknesses */}

        <div className="rounded-2xl border border-red-500/20 bg-red-500/5 p-6">

          <div className="mb-5 flex items-center gap-3">
            <AlertTriangle
              size={20}
              className="text-red-400"
            />

            <h3 className="text-lg font-semibold text-white">
              Weaknesses
            </h3>

          </div>

          <ul className="space-y-4">

            {intelligence.weaknesses.map((item) => (
              <li
                key={item}
                className="flex gap-3 text-slate-300"
              >
                <span className="mt-2 h-2 w-2 rounded-full bg-red-400" />

                <span>{item}</span>
              </li>
            ))}

          </ul>

        </div>

      </div>

      {/* Suggested Actions */}

      <div className="mt-8 rounded-2xl border border-yellow-500/20 bg-yellow-500/5 p-6">

        <div className="mb-5 flex items-center gap-3">
          <Sparkles
            size={20}
            className="text-yellow-400"
          />

          <h3 className="text-lg font-semibold text-white">
            Suggested Actions
          </h3>

        </div>

        <ul className="space-y-4">

          {intelligence.suggested_actions.map((item) => (
            <li
              key={item}
              className="flex gap-3 text-slate-300"
            >
              <span className="mt-2 h-2 w-2 rounded-full bg-yellow-400" />

              <span>{item}</span>
            </li>
          ))}

        </ul>

      </div>

      {/* Market Outlook */}

      <div className="mt-8 rounded-2xl border border-slate-700 bg-slate-950/40 p-6">

        <h3 className="text-lg font-semibold text-white">
          Market Outlook
        </h3>

        <p className="mt-4 leading-8 text-slate-300">
          {intelligence.market_outlook}
        </p>

      </div>

    </section>
  );
}