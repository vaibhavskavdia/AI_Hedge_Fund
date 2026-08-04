"use client";

import PortfolioAllocation from "./components/PortfolioAllocation";
import PortfolioGenerator from "./components/PortfolioGenerator";
import HoldingsTable from "./components/HoldingsTable";
import PortfolioOverview from "./components/PortfolioOverview";
import RecommendationCards from "./components/RecommendationCards";
import CommitteeReview from "./components/CommitteeReview";
import PortfolioIntelligence from "./components/PortfolioIntelligence";
import RiskSnapshot from "./components/RiskSnapshot";
import PortfolioLoading from "./components/PortfolioLoading";
import PortfolioEmpty from "./components/PortfolioEmpty";
import { usePortfolio } from "./usePortfolio";

export default function PortfolioPage() {
  const {
    portfolio,
    loading,
    risk,
    error,
    progress,
    step,
    generatePortfolio,
  } = usePortfolio();

  // -----------------------------
  // Initial State
  // -----------------------------

  if (!portfolio && !loading) {
    return (
      <PortfolioGenerator
        loading={false}
        onGenerate={generatePortfolio}
      />
    );
  }

  // -----------------------------
  // Loading
  // -----------------------------

  if (loading) {
    return (
      <div className="mx-auto flex min-h-[70vh] max-w-3xl items-center justify-center">
        <div className="w-full rounded-3xl border border-slate-800 bg-slate-900/70 p-12 backdrop-blur">
          <p className="text-xs uppercase tracking-[0.35em] text-blue-400">
            AI Hedge Fund
          </p>

          <h1 className="mt-4 text-4xl font-bold text-white">
            Building Institutional Portfolio
          </h1>

          <p className="mt-4 text-slate-400">
            {step ?? "Initializing..."}
          </p>

          <div className="mt-10 h-3 overflow-hidden rounded-full bg-slate-800">
            <div
              className="h-full rounded-full bg-blue-500 transition-all duration-500"
              style={{
                width: `${progress ?? 0}%`,
              }}
            />
          </div>

          <div className="mt-3 flex justify-between text-sm text-slate-500">
            <span>Progress</span>

            <span>{progress ?? 0}%</span>
          </div>
        </div>
      </div>
    );
  }

  // -----------------------------
  // Error
  // -----------------------------

  if (error) {
    return (
      <div className="rounded-3xl border border-red-500/30 bg-red-500/10 p-8 text-red-300">
        {error}
      </div>
    );
  }
if (loading) {
  return (
    <div className="max-w-7xl mx-auto p-8">
      <PortfolioLoading
        progress={progress}
        step={step}
      />
    </div>
  );
}
if (!portfolio) {
  return (
    <div className="max-w-7xl mx-auto p-8">
      <PortfolioEmpty
        onGenerate={() =>
          generatePortfolio({
            investment_amount: 100000,
            risk_profile: "Balanced",
            preferred_sectors: [
              "Technology",
              "Healthcare",
            ],
            max_holdings: 10,
          })
        }
      />
    </div>
  );
}
  // -----------------------------
  // Dashboard
  // -----------------------------

  if (!portfolio) return null;

  return (
    <div className="space-y-8">
      <PortfolioOverview portfolio={portfolio} />

      <PortfolioAllocation
        portfolio={portfolio.portfolio}
      />

      <HoldingsTable
        portfolio={portfolio.portfolio}
        recommendations={
          portfolio.recommendations
        }/>

        <RecommendationCards
    recommendations={portfolio.recommendations}
/>
      <CommitteeReview
    review={portfolio.committee_review}
/>
{portfolio.portfolio_intelligence && (
    <PortfolioIntelligence
        intelligence={portfolio.portfolio_intelligence}
    />
)}
<RiskSnapshot risk={risk} />
      {/* Next Components */}

      {/* <RecommendationCards /> */}

      {/* <CommitteeReview /> */}

      {/* <PortfolioIntelligence /> */}

      {/* <RiskSnapshot /> */}
    </div>
  );
}