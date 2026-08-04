import api from "./api";

export interface ResearchRequest {
  question: string;
}

export interface ResearchResponse {
  question: string;
  answer: string;
}

export const askResearch = async (
  question: string
): Promise<ResearchResponse> => {
  const { data } =
    await api.post<ResearchResponse>(
      "/research/",
      {
        question,
      }
    );

  return data;
};

export const getResearchHistory = async () => {
  const { data } =
    await api.get("/research/history");

  return data;
};