interface Props {
  progress: number;
  step: string;
}

export default function PortfolioLoading({
  progress,
  step,
}: Props) {
  return (
    <div className="rounded-3xl border border-slate-800 bg-[#0F172A] p-10">
      <div className="mb-8 text-center">
        <p className="text-xs uppercase tracking-[0.35em] text-blue-400">
          AI Portfolio Generator
        </p>

        <h2 className="mt-3 text-4xl font-bold text-white">
          Building Your Portfolio
        </h2>

        <p className="mt-4 text-slate-400">
          Our AI committee is analyzing thousands of
          financial signals.
        </p>
      </div>

      <div className="mb-5 h-3 w-full overflow-hidden rounded-full bg-slate-800">
        <div
          className="h-full rounded-full bg-blue-500 transition-all duration-500"
          style={{
            width: `${progress}%`,
          }}
        />
      </div>

      <div className="mb-2 flex justify-between text-sm">
        <span className="text-slate-400">
          {step || "Initializing..."}
        </span>

        <span className="font-semibold text-white">
          {progress}%
        </span>
      </div>

      <div className="mt-10 space-y-3 text-sm text-slate-400">
        <p>✓ Loading market data</p>
        <p>✓ Ranking stocks</p>
        <p>✓ Running AI committee</p>
        <p>✓ Optimizing allocation</p>
        <p>✓ Generating recommendations</p>
        <p>✓ Computing portfolio risk</p>
      </div>
    </div>
  );
}