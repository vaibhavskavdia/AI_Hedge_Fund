import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

import AppLayout from "./components/layout/AppLayout";

import PortfolioPage from "./features/portfolio/PortfolioPage";
import ResearchPage from "./features/research/page/ResearchPage";
import StockPage from "./features/stock-intelligence/pages/StockPage";
import SectorPage from "./features/sector-intelligence/pages/SectorPage";
function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<AppLayout />}>
          <Route path="/" element={<PortfolioPage />} />

          <Route path="/research" element={<ResearchPage />} />

          <Route path="/stocks" element={<StockPage />} />

          <Route path="/sectors" element={<SectorPage />} />

          

          <Route path="*" element={<Navigate to="/" replace />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;