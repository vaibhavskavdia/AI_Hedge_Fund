import SectorSearch from "../components/SectorSearch";
import SectorOverview from "../components/SectorOverview";
import TopStocksTable from "../components/TopStocksTable";

import { useSector } from "../hooks/useSector";

export default function SectorPage() {
  const {
    loading,
    error,
    sector,
    searchSector,
  } = useSector();

  return (
    <div className="space-y-8">

      <SectorSearch
        loading={loading}
        onSearch={searchSector}
      />

      {error && (
        <div className="rounded-2xl border border-red-500/30 bg-red-500/10 p-6 text-red-300">
          {error}
        </div>
      )}

      {sector && (
        <>
          <SectorOverview sector={sector} />

          <TopStocksTable
            stocks={sector.top_stocks}
          />
        </>
      )}

    </div>
  );
}