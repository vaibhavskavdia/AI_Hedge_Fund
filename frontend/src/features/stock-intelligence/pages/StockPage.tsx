import StockSearch from "../components/StockSearch";
import StockOverview from "../components/StockOverview";
import NewsSentiment from "../components/NewsSentiment";

import { useStock } from "../hooks/useStock";

export default function StockPage() {
  const {
    loading,
    stock,
    error,
    searchStock,
  } = useStock();

  return (
    <div className="mx-auto max-w-7xl space-y-10">

      <StockSearch
        loading={loading}
        onSearch={searchStock}
      />

      {error && (
        <div className="rounded-2xl border border-red-900 bg-red-500/10 p-6 text-red-300">
          {error}
        </div>
      )}

      {stock && (
        <>
          <StockOverview
            stock={stock}
          />

          <NewsSentiment
            sentiment={stock}
          />
        </>
      )}

    </div>
  );
}