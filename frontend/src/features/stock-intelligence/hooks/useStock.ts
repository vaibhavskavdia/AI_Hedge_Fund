import { useState } from "react";
import axios from "axios";

import {
  getStockIntelligence,
} from "../../../services/stock";

export function useStock() {
  const [loading, setLoading] =
    useState(false);

  const [stock, setStock] =
    useState<any>(null);

  const [error, setError] =
    useState<string | null>(null);

  const searchStock = async (
    ticker: string
  ) => {
    try {
      setLoading(true);

      setError(null);

      const response =
        await getStockIntelligence(
          ticker
        );

      setStock(response);
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
            "Unable to fetch stock."
          );
        }
      } else if (
        err instanceof Error
      ) {
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

    stock,

    error,

    searchStock,
  };
}