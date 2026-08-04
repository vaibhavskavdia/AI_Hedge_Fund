import { useState } from "react";
import axios from "axios";

import {
  askResearch,
} from "../../../services/research";

export function useResearch() {
  const [loading, setLoading] =
    useState(false);

  const [answer, setAnswer] =
    useState("");

  const [currentQuery, setCurrentQuery] =
    useState("");

  const [error, setError] =
    useState<string | null>(null);

  const ask = async (
    question: string
  ) => {
    try {
      setLoading(true);

      setError(null);

      setAnswer("");

      setCurrentQuery(question);

      const response =
        await askResearch(question);

      setAnswer(response.answer);
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
              "Unable to generate research."
          );
        }
      } else if (err instanceof Error) {
        setError(err.message);
      } else {
        setError(
          "Unexpected error."
        );
      }
    } finally {
      setLoading(false);
    }
  };

  return {
    loading,
    answer,
    error,
    currentQuery,
    askResearch: ask,
  };
}