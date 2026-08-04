import type { TopStock } from "../../../services/sector";

interface Props {
  stocks: TopStock[];
}

export default function TopStocksTable({
  stocks,
}: Props) {
  return (
    <section className="rounded-3xl border border-slate-800 bg-[#0F172A] p-8">

      <p className="text-xs uppercase tracking-[0.35em] text-blue-400">
        LEADERS
      </p>

      <h2 className="mt-3 text-4xl font-bold text-white">
        Top Stocks
      </h2>

      <div className="mt-8 overflow-hidden rounded-2xl border border-slate-800">

        <table className="w-full">

          <thead className="bg-slate-950 text-left">

            <tr className="text-slate-400">

              <th className="px-6 py-5">Ticker</th>

              <th>Prediction</th>

              <th>Return</th>

              <th>Risk</th>

              <th>Recommendation</th>

            </tr>

          </thead>

          <tbody>

            {stocks.map((stock) => (

              <tr
                key={stock.ticker}
                className="border-t border-slate-800"
              >
                <td className="px-6 py-5 font-semibold text-white">
                  {stock.ticker}
                </td>

                <td className="text-emerald-400">
                  {(stock.prediction_score * 100).toFixed(1)}%
                </td>

                <td className="text-blue-400">
                  {stock.expected_return_5d.toFixed(2)}%
                </td>

                <td className="text-red-400">
                  {stock.risk_score.toFixed(2)}
                </td>

                <td>

                  <span className="rounded-full bg-emerald-500/20 px-3 py-1 text-xs font-semibold text-emerald-400">
                    {stock.recommendation}
                  </span>

                </td>

              </tr>

            ))}

          </tbody>

        </table>

      </div>

    </section>
  );
}