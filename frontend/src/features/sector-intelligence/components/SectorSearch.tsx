import { useState } from "react";
import { Search } from "lucide-react";

interface Props {
  loading: boolean;
  onSearch: (sector: string) => void;
}

export default function SectorSearch({
  loading,
  onSearch,
}: Props) {
  const [sector, setSector] =
    useState("");

  const submit = () => {
    if (!sector.trim()) return;

    onSearch(sector.trim());
  };

  return (
    <section className="rounded-3xl border border-slate-800 bg-[#0F172A] p-8">

      <p className="text-xs uppercase tracking-[0.35em] text-blue-400">
        Sector Intelligence
      </p>

      <h1 className="mt-3 text-5xl font-bold text-white">
        Market Sector Analysis
      </h1>

      <p className="mt-4 max-w-2xl text-slate-400">
        Analyze an entire market sector
        using AI-powered portfolio data.
      </p>

      <div className="mt-10 flex gap-4">

        <div className="relative flex-1">

          <Search
            size={18}
            className="absolute left-5 top-1/2 -translate-y-1/2 text-slate-500"
          />

          <input
            value={sector}
            onChange={(e) =>
              setSector(e.target.value)
            }
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                submit();
              }
            }}
            placeholder="Technology"
            className="h-16 w-full rounded-2xl border border-slate-700 bg-slate-950 pl-14 text-xl text-white outline-none focus:border-blue-500"
          />

        </div>

        <button
          disabled={loading}
          onClick={submit}
          className="rounded-2xl bg-blue-600 px-10 text-lg font-semibold text-white hover:bg-blue-500"
        >
          {loading
            ? "Analyzing..."
            : "Analyze"}
        </button>

      </div>

    </section>
  );
}