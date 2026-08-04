import api from "./api";

export interface RiskSnapshot {
  portfolio_id: number;
  portfolio: Record<string, number>;

  largest_holding: string;
  largest_weight: number;

  concentration_risk: string;

  risk_score: number;
}

export async function getLatestRisk() {
  const { data } = await api.get<RiskSnapshot>(
    "/risk/risk/latest"
  );

  return data;
}