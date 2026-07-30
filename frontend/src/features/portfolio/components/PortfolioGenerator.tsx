"use client";

import { useState } from "react";
import { Sparkles } from "lucide-react";

interface PortfolioGeneratorProps {
  onGenerate: (payload: {
    investment_amount: number;
    risk_profile: string;
    preferred_sectors: string[];
    max_holdings: number;
  }) => void;

  loading: boolean;
}

const RISK_OPTIONS = [
  "Conservative",
  "Balanced",
  "Aggressive",
];

const SECTORS = [
  "Technology",
  "Healthcare",
  "Finance",
  "Energy",
  "Industrials",
  "Consumer",
  "Communication",
  "Utilities",
];

export default function PortfolioGenerator({
  onGenerate,
  loading,
}: PortfolioGeneratorProps) {
  const [amount, setAmount] = useState(100000);

  const [risk, setRisk] =
    useState("Moderate");

  const [holdings, setHoldings] =
    useState(10);

  const [selectedSectors, setSelectedSectors] =
    useState<string[]>([
      "Technology",
      "Healthcare",
    ]);

  const toggleSector = (sector: string) => {
    if (selectedSectors.includes(sector)) {
      setSelectedSectors(
        selectedSectors.filter(
          (s) => s !== sector
        )
      );
    } else {
      setSelectedSectors([
        ...selectedSectors,
        sector,
      ]);
    }
  };

  return (
    <div className="mx-auto max-w-5xl rounded-3xl border border-slate-800 bg-slate-900/70 p-10 backdrop-blur">
      <div className="text-center">
        <p className="text-xs uppercase tracking-[0.35em] text-blue-400">
          AI Portfolio Generator
        </p>

        <h1 className="mt-4 text-5xl font-bold text-white">
          Build Your Institutional Portfolio
        </h1>

        <p className="mx-auto mt-5 max-w-2xl text-lg text-slate-400">
          Our AI committee analyzes market
          signals, earnings calls, financial
          fundamentals and risk to construct an
          optimized portfolio.
        </p>
      </div>

      <div className="mt-12 space-y-10">

        {/* Investment Amount */}

        <div>
          <label className="mb-3 block text-sm font-medium text-slate-300">
            Investment Amount
          </label>

          <input
            type="number"
            value={amount}
            onChange={(e) =>
              setAmount(Number(e.target.value))
            }
            className="w-full rounded-xl border border-slate-700 bg-slate-950 px-5 py-4 text-lg text-white outline-none focus:border-blue-500"
          />
        </div>

        {/* Risk */}

        <div>
          <label className="mb-4 block text-sm font-medium text-slate-300">
            Risk Profile
          </label>

          <div className="flex gap-4">
            {RISK_OPTIONS.map((item) => (
              <button
                key={item}
                onClick={() => setRisk(item)}
                className={`rounded-xl px-6 py-3 font-medium transition ${
                  risk === item
                    ? "bg-blue-600 text-white"
                    : "border border-slate-700 bg-slate-950 text-slate-300 hover:border-blue-500"
                }`}
              >
                {item}
              </button>
            ))}
          </div>
        </div>

        {/* Sectors */}

        <div>
          <label className="mb-4 block text-sm font-medium text-slate-300">
            Preferred Sectors
          </label>

          <div className="flex flex-wrap gap-3">
            {SECTORS.map((sector) => (
              <button
                key={sector}
                onClick={() =>
                  toggleSector(sector)
                }
                className={`rounded-full px-5 py-2 transition ${
                  selectedSectors.includes(
                    sector
                  )
                    ? "bg-blue-600 text-white"
                    : "border border-slate-700 bg-slate-950 text-slate-300"
                }`}
              >
                {sector}
              </button>
            ))}
          </div>
        </div>

        {/* Holdings */}

        <div>
          <label className="mb-3 block text-sm font-medium text-slate-300">
            Maximum Holdings
          </label>

          <input
            type="range"
            min={5}
            max={20}
            value={holdings}
            onChange={(e) =>
              setHoldings(
                Number(e.target.value)
              )
            }
            className="w-full"
          />

          <div className="mt-2 text-right text-blue-400">
            {holdings} Holdings
          </div>
        </div>

        <button
          disabled={loading}
          onClick={() =>
            onGenerate({
              investment_amount: amount,
              risk_profile: risk,
              preferred_sectors:
                selectedSectors,
              max_holdings: holdings,
            })
          }
          className="flex w-full items-center justify-center gap-3 rounded-2xl bg-blue-600 py-5 text-lg font-semibold text-white transition hover:bg-blue-500 disabled:opacity-50"
        >
          <Sparkles size={22} />

          {loading
            ? "Generating Portfolio..."
            : "Generate AI Portfolio"}
        </button>
      </div>
    </div>
  );
}