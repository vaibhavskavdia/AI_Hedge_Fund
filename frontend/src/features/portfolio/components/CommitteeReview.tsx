"use client";

import {
  CheckCircle2,
  AlertTriangle,
  Star,
  ShieldCheck,
} from "lucide-react";

interface CommitteeReview {
  portfolio_rating: string;
  top_pick: string;
  biggest_risk: string;
  diversification: string;
  approved: boolean;
  committee_summary: string;
}

interface CommitteeReviewProps {
  review: CommitteeReview;
}

export default function CommitteeReview({
  review,
}: CommitteeReviewProps) {
  return (
    <section className="rounded-3xl border border-slate-800 bg-slate-900/70 p-8 backdrop-blur">
      {/* Header */}

      <div className="mb-8">
        <p className="text-xs uppercase tracking-[0.35em] text-blue-400">
          Investment Committee
        </p>

        <h2 className="mt-2 text-3xl font-bold text-white">
          Committee Review
        </h2>
      </div>

      {/* Metrics */}

      <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-4">
        <MetricCard
          icon={<Star size={20} />}
          label="Portfolio Rating"
          value={review.portfolio_rating}
          color="text-yellow-400"
        />

        <MetricCard
          icon={<CheckCircle2 size={20} />}
          label="Top Pick"
          value={review.top_pick}
          color="text-blue-400"
        />

        <MetricCard
          icon={<AlertTriangle size={20} />}
          label="Biggest Risk"
          value={review.biggest_risk}
          color="text-red-400"
        />

        <MetricCard
          icon={<ShieldCheck size={20} />}
          label="Diversification"
          value={review.diversification}
          color="text-emerald-400"
        />
      </div>

      {/* Approval */}

      <div className="mt-8 rounded-2xl border border-slate-800 bg-slate-950/40 p-6">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <p className="text-sm uppercase tracking-wider text-slate-400">
              Committee Decision
            </p>

            <h3 className="mt-2 text-3xl font-bold text-white">
              {review.approved
                ? "Approved"
                : "Pending Approval"}
            </h3>
          </div>

          <div
            className={`rounded-full px-6 py-3 text-sm font-semibold ${
              review.approved
                ? "border border-emerald-500/30 bg-emerald-500/15 text-emerald-400"
                : "border border-yellow-500/30 bg-yellow-500/15 text-yellow-400"
            }`}
          >
            {review.approved
              ? "APPROVED"
              : "PENDING"}
          </div>
        </div>
      </div>

      {/* Summary */}

      <div className="mt-8 rounded-2xl border border-blue-500/20 bg-blue-950/10 p-6">
        <h3 className="text-xl font-semibold text-white">
          Committee Summary
        </h3>

        <p className="mt-4 leading-8 text-slate-300">
          {review.committee_summary}
        </p>
      </div>
    </section>
  );
}

interface MetricCardProps {
  icon: React.ReactNode;
  label: string;
  value: string;
  color: string;
}

function MetricCard({
  icon,
  label,
  value,
  color,
}: MetricCardProps) {
  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-950/40 p-6 transition hover:border-blue-500">
      <div className={`mb-4 ${color}`}>
        {icon}
      </div>

      <p className="text-sm text-slate-400">
        {label}
      </p>

      <p className={`mt-2 text-xl font-bold ${color}`}>
        {value}
      </p>
    </div>
  );
}