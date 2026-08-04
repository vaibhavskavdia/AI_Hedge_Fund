import {
  ShieldAlert,
  TriangleAlert,
  PieChart,
  Activity,
} from "lucide-react";

interface Props {
  risk: any;
}

export default function RiskSnapshot({
  risk,
}: Props) {
  if (!risk) return null;

  return (
    <section className="rounded-3xl border border-slate-800 bg-[#11182d] p-8">

      <p className="mb-2 text-xs uppercase tracking-[0.35em] text-blue-400">
        Risk Overview
      </p>

      <h2 className="mb-8 text-4xl font-bold">
        Portfolio Risk Snapshot
      </h2>

      <div className="grid gap-6 md:grid-cols-4">

        <div className="rounded-2xl border border-slate-800 bg-[#0d1324] p-6">
          <ShieldAlert className="mb-5 text-blue-400" />

          <p className="text-sm text-slate-400">
            Risk Score
          </p>

          <h3 className="mt-2 text-4xl font-bold">
            {risk.risk_score}
          </h3>
        </div>

        <div className="rounded-2xl border border-slate-800 bg-[#0d1324] p-6">
          <PieChart className="mb-5 text-green-400" />

          <p className="text-sm text-slate-400">
            Largest Holding
          </p>

          <h3 className="mt-2 text-3xl font-bold">
            {risk.largest_holding}
          </h3>

          <p className="mt-2 text-blue-400">
            {risk.largest_weight.toFixed(1)}%
          </p>
        </div>

        <div className="rounded-2xl border border-slate-800 bg-[#0d1324] p-6">
          <TriangleAlert className="mb-5 text-red-400" />

          <p className="text-sm text-slate-400">
            Concentration Risk
          </p>

          <h3 className="mt-2 text-xl font-semibold text-red-400">
            {risk.concentration_risk}
          </h3>
        </div>

        <div className="rounded-2xl border border-slate-800 bg-[#0d1324] p-6">
          <Activity className="mb-5 text-emerald-400" />

          <p className="text-sm text-slate-400">
            Holdings
          </p>

          <h3 className="mt-2 text-4xl font-bold">
            {Object.keys(risk.portfolio).length}
          </h3>
        </div>

      </div>

    </section>
  );
}