import { useState } from "react";
import { Search } from "lucide-react";

interface Props {
  loading: boolean;
  onSearch: (ticker: string) => void;
}

export default function StockSearch({
  loading,
  onSearch,
}: Props) {
  const [ticker, setTicker] =
    useState("");

  const submit = () => {
    if (!ticker.trim()) return;

    onSearch(
      ticker.trim().toUpperCase()
    );
  };

  return (
    <section className="rounded-3xl border border-slate-800 bg-[#0F172A] p-8">

      <p className="text-xs uppercase tracking-[0.35em] text-blue-400">
        Stock Intelligence
      </p>

      <h1 className="mt-3 text-5xl font-bold text-white">
        Company Analysis
      </h1>

      <p className="mt-4 max-w-2xl text-slate-400">
        Generate institutional-grade AI
        analysis for any publicly traded
        company.
      </p>

      <div className="mt-10 flex gap-4">

        <div className="relative flex-1">

          <Search
            size={18}
            className="absolute left-5 top-1/2 -translate-y-1/2 text-slate-500"
          />

          <input
            value={ticker}
            onChange={(e) =>
              setTicker(e.target.value)
            }
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                submit();
              }
            }}
            placeholder="AAPL"
            className="h-16 w-full rounded-2xl border border-slate-700 bg-slate-950 pl-14 text-xl text-white outline-none focus:border-blue-500"
          />

        </div>

        <button
          disabled={loading}
          onClick={submit}
          className="rounded-2xl bg-blue-600 px-10 text-lg font-semibold text-white transition hover:bg-blue-500 disabled:opacity-50"
        >
          {loading
            ? "Analyzing..."
            : "Analyze"}
        </button>

      </div>

    </section>
  );
}