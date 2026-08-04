import api from "./api";

export interface TopStock {
  ticker: string;

  prediction_score: number;

  expected_return_5d: number;

  risk_score: number;

  recommendation: string;
}

export interface SectorResponse {
  sector: string;

  stock_count: number;

  average_prediction_score: number;

  average_expected_return: number;

  average_risk_score: number;

  top_stocks: TopStock[];
}

export async function getSectorIntelligence(
  sector: string
): Promise<SectorResponse> {
  const { data } =
    await api.get<SectorResponse>(
      `/sector-intelligence/${sector}`
    );

  return data;
}