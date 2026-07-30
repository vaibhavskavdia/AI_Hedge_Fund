import api from "./api";

export interface PortfolioRequest {
  investment_amount: number;
  risk_profile: string;
  preferred_sectors: string[];
  max_holdings: number;
}

export interface PortfolioJobResponse {
  job_id: string;
}

export interface JobStatusResponse {
  job_id: string;

  status:
    | "queued"
    | "running"
    | "completed"
    | "failed";

  progress?: number;

  step?: string;

  portfolio_id?: number;

  error?: string;
}

export const generatePortfolio = async (
  payload: PortfolioRequest
) => {
  const { data } =
    await api.post<PortfolioJobResponse>(
      "/portfolio/ai-portfolio",
      payload
    );

  return data;
};

export const getJobStatus = async (
  jobId: string
) => {
  const { data } =
    await api.get<JobStatusResponse>(
      `/portfolio/job/${jobId}`
    );

  return data;
};

export const getLatestPortfolio =
  async () => {
    const { data } = await api.get(
      "/portfolio/latest"
    );

    return data;
  };