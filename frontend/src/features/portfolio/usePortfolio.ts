import { useState } from "react";
import axios from "axios";

import {
  generatePortfolio,
  getJobStatus,
  getLatestPortfolio,
} from "../../services/portfolio";

import { getLatestRisk } from "../../services/risk";

import type { PortfolioRequest } from "../../services/portfolio";

export function usePortfolio() {
  const [loading, setLoading] = useState(false);

  const [portfolio, setPortfolio] = useState<any>(null);

  const [risk, setRisk] = useState<any>(null);

  const [error, setError] = useState<string | null>(null);

  const [progress, setProgress] = useState(0);

  const [step, setStep] = useState("");

  const generate = async (
    payload: PortfolioRequest
  ) => {
    try {
      setLoading(true);

      setError(null);

      setProgress(0);

      setStep("Initializing...");

      // ------------------------------------
      // Start Portfolio Job
      // ------------------------------------

      const { job_id } =
        await generatePortfolio(payload);

      let completed = false;

      while (!completed) {
        await new Promise((resolve) =>
          setTimeout(resolve, 1500)
        );

        const job =
          await getJobStatus(job_id);

        setProgress(job.progress ?? 0);

        setStep(job.step ?? "");

        if (job.status === "completed") {
          completed = true;
        }

        if (job.status === "failed") {
          throw new Error(
            job.error ??
              "Portfolio generation failed."
          );
        }
      }

      // ------------------------------------
      // Load Dashboard Data
      // ------------------------------------

      const latestPortfolio =
        await getLatestPortfolio();

      setPortfolio(latestPortfolio);

      // ------------------------------------
      // Load Risk Snapshot
      // ------------------------------------

      try {
        const latestRisk =
          await getLatestRisk();

        setRisk(latestRisk);
      } catch (error) {
        console.warn(
          "Risk snapshot unavailable.",
          error
        );
      }
    } catch (err) {
      console.error(err);

      if (axios.isAxiosError(err)) {
        if (
          typeof err.response?.data?.detail ===
          "string"
        ) {
          setError(
            err.response.data.detail
          );
        } else {
          setError(
            err.message ??
              "Failed to generate portfolio."
          );
        }
      } else if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("Unexpected error.");
      }
    } finally {
      setLoading(false);
    }
  };

  return {
    loading,

    portfolio,

    risk,

    error,

    progress,

    step,

    generatePortfolio: generate,
  };
}