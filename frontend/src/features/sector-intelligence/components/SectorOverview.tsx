import type { SectorResponse } from "../../../services/sector";

interface Props {
  sector: SectorResponse;
}

export default function SectorOverview({
  sector,
}: Props) {
  return (
    <section className="rounded-3xl border border-slate-800 bg-[#0F172A] p-8">

      <p className="text-xs uppercase tracking-[0.35em] text-blue-400">
        OVERVIEW
      </p>

      <h2 className="mt-3 text-4xl font-bold text-white">
        {sector.sector}
      </h2>

      <div className="mt-8 grid grid-cols-4 gap-6">

        <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
          <p className="text-slate-400 text-sm">
            Stocks Covered
          </p>

          <h3 className="mt-3 text-4xl font-bold text-white">
            {sector.stock_count}
          </h3>
        </div>

        <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
          <p className="text-slate-400 text-sm">
            Avg Prediction
          </p>

          <h3 className="mt-3 text-4xl font-bold text-emerald-400">
            {(sector.average_prediction_score * 100).toFixed(1)}%
          </h3>
        </div>

        <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
          <p className="text-slate-400 text-sm">
            Expected Return
          </p>

          <h3 className="mt-3 text-4xl font-bold text-blue-400">
            {sector.average_expected_return.toFixed(2)}%
          </h3>
        </div>

        <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
          <p className="text-slate-400 text-sm">
            Average Risk
          </p>

          <h3 className="mt-3 text-4xl font-bold text-red-400">
            {sector.average_risk_score.toFixed(2)}
          </h3>
        </div>

      </div>

    </section>
  );
}