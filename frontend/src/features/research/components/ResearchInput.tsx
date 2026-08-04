import { useState } from "react";
import { Search, Sparkles } from "lucide-react";

interface Props {
  loading: boolean;
  onSearch: (query: string) => void;
}

export default function ResearchInput({
  loading,
  onSearch,
}: Props) {
  const [query, setQuery] = useState("");

  const submit = () => {
    if (!query.trim()) return;

    onSearch(query.trim());
  };

  return (
    <div className="rounded-3xl border border-slate-800 bg-[#0F172A] p-8">

      <div className="mb-6">

        <p className="text-xs uppercase tracking-[0.35em] text-blue-400">
          Ask AI
        </p>

        <h2 className="mt-2 text-4xl font-bold text-white">
          AI Research Terminal
        </h2>

        <p className="mt-3 max-w-2xl text-slate-400">
          Search earnings calls, annual reports,
          SEC filings and institutional research
          using Retrieval-Augmented Generation.
        </p>

      </div>

      <div className="flex gap-4">

        <div className="relative flex-1">

          <Search
            size={18}
            className="absolute left-5 top-1/2 -translate-y-1/2 text-slate-500"
          />

          <input
            value={query}
            onChange={(e) =>
              setQuery(e.target.value)
            }
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                submit();
              }
            }}
            placeholder="What did Tesla management say about AI?"
            className="h-16 w-full rounded-2xl border border-slate-700 bg-slate-950 pl-14 pr-6 text-white outline-none transition focus:border-blue-500"
          />

        </div>

        <button
          onClick={submit}
          disabled={loading}
          className="flex items-center gap-3 rounded-2xl bg-blue-600 px-8 font-semibold text-white transition hover:bg-blue-500 disabled:opacity-50"
        >
          <Sparkles size={18} />

          {loading ? "Thinking..." : "Ask AI"}

        </button>

      </div>

    </div>
  );
}