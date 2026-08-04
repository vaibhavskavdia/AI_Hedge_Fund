import { Sparkles } from "lucide-react";

interface Props {
  onGenerate: () => void;
}

export default function PortfolioEmpty({
  onGenerate,
}: Props) {
  return (
    <div className="rounded-3xl border border-slate-800 bg-[#0F172A] p-20 text-center">
      <div className="mx-auto flex h-20 w-20 items-center justify-center rounded-full bg-blue-500/10">
        <Sparkles className="h-10 w-10 text-blue-400" />
      </div>

      <p className="mt-8 text-xs uppercase tracking-[0.35em] text-blue-400">
        AI PORTFOLIO PLATFORM
      </p>

      <h1 className="mt-4 text-5xl font-bold text-white">
        Build Your First
        <br />
        Institutional Portfolio
      </h1>

      <p className="mx-auto mt-6 max-w-2xl text-lg text-slate-400">
        Our AI investment committee analyzes earnings,
        financial statements, market signals, and risk
        to construct an institutional-grade portfolio.
      </p>

      <button
        onClick={onGenerate}
        className="mt-12 rounded-xl bg-blue-600 px-8 py-4 text-lg font-semibold text-white transition hover:bg-blue-500"
      >
        Generate AI Portfolio
      </button>
    </div>
  );
}