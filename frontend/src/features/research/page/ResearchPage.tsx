import ResearchInput from "../components/ResearchInput";
import SuggestedQueries from "../components/SuggestedQueries";
import ResearchLoading from "../components/ResearchLoading";
import ResearchResponse from "../components/ResearchResponse";

import { useResearch } from "../hooks/useResearch";

export default function ResearchPage() {
  const {
    loading,
    answer,
    currentQuery,
    askResearch,
  } = useResearch();

  return (
    <div className="mx-auto max-w-7xl space-y-10">

      {/* Header */}

      <section className="text-center">

        <p className="text-xs uppercase tracking-[0.35em] text-blue-400">
          AI Hedge Fund
        </p>

        <h1 className="mt-4 text-6xl font-bold text-white">
          AI Research Terminal
        </h1>

        <p className="mx-auto mt-5 max-w-3xl text-lg leading-8 text-slate-400">
          Search earnings calls, annual reports,
          SEC filings and institutional knowledge
          using Retrieval-Augmented Generation.
        </p>

      </section>

      {/* Search */}

      <ResearchInput
        loading={loading}
        onSearch={askResearch}
      />

      {/* Suggested Questions */}

      {!loading && !answer && (
        <SuggestedQueries
          onSelect={askResearch}
        />
      )}

      {/* Loading */}

      {loading && (
        <ResearchLoading
          query={currentQuery}
        />
      )}

      {/* AI Response */}

      {!loading && answer && (
        <ResearchResponse
          response={answer}
        />
      )}

    </div>
  );
}