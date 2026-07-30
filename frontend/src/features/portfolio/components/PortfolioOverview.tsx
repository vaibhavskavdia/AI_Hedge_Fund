interface PortfolioOverviewProps {
  portfolio: any;
}

export default function PortfolioOverview({
  portfolio,
}: PortfolioOverviewProps) {
  const committee = portfolio?.committee_review;

  const overview = [
    {
      label: "Portfolio ID",
      value: `#${portfolio?.portfolio_id ?? "--"}`,
    },
    {
      label: "Holdings",
      value: Object.keys(portfolio?.portfolio ?? {}).length,
    },
    {
      label: "Top Pick",
      value: committee?.top_pick ?? "--",
    },
    {
      label: "Approval",
      value: committee?.approved ? "Approved" : "Pending",
    },
  ];

  return (
    <section className="space-y-6">
      <div>
        <p className="text-sm uppercase tracking-[0.3em] text-blue-500">
          Overview
        </p>

        <h2 className="mt-2 text-3xl font-bold text-white">
          Portfolio Summary
        </h2>
      </div>

      <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-4">
        {overview.map((item) => (
          <div
            key={item.label}
            className="rounded-3xl border border-slate-800 bg-slate-900/70 p-6 backdrop-blur"
          >
            <p className="text-sm text-slate-400">
              {item.label}
            </p>

            <h3 className="mt-4 text-3xl font-bold text-white">
              {item.value}
            </h3>
          </div>
        ))}
      </div>
    </section>
  );
}