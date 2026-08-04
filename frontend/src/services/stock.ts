import api from "./api";

export interface StockIntelligence {
  ticker: string;
  sector: string;

  prediction_score: number;

  expected_return_5d: number;

  risk_score: number;

  risk_level: string;

  recommendation: string;

  avg_sentiment_score: number;

  positive_count: number;

  neutral_count: number;

  negative_count: number;
}

export async function getStockIntelligence(
  ticker: string
): Promise<StockIntelligence> {
  const { data } =
    await api.get<StockIntelligence>(
      `/stock-intelligence/${ticker}`
    );

  return data;
}