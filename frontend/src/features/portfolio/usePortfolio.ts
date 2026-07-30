import { useState } from "react";
import axios from "axios";

import {
  generatePortfolio,
  getJobStatus,
  getLatestPortfolio,
  
} from "../../services/portfolio";
import type { PortfolioRequest } from "../../services/portfolio";
export function usePortfolio() {
  const [loading, setLoading] = useState(false);

  const [portfolio, setPortfolio] = useState<any>(null);

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
      // Load Dashboard
      // ------------------------------------

      const latest =
        await getLatestPortfolio();

      setPortfolio(latest);
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

    error,

    progress,

    step,

    generatePortfolio: generate,
  };
}